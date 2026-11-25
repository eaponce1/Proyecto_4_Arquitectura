# Diagnóstico y trazado de progreso – demo autónoma

## Conclusión del diagnóstico

Se volvió a ejecutar la variante `demo_autonoma_handshake` original en Icarus.
El fallo físico de D1 solamente **no se reproduce**: la simulación pasa los 16
precios, 16 decisiones y 16 respuestas MISO. Por eso no hay evidencia para
atribuir el bloqueo físico a `WAIT_ACK`, al reset, a la fase SPI o al acceso
MMIO.

La causa confirmada de la ambigüedad es la instrumentación de la variante
anterior: D1 significaba que se vio un fetch y D2/D4 eran bits del código de
error. “Solo D1” significaba `error_code=00`, no indicaba si el maestro arrancó,
si el slave recibió precio o si el ACK llegó. El evento físico donde se detiene
la ejecución sigue siendo desconocido hasta programar manualmente esta variante
de trazas y leer su código LED. No se modifica el firmware ni se presupone una
causa que los LEDs actuales no permiten observar.

## Secuencia baseline observada

El testbench `tb_baseline_trace.sv` instrumenta el handshake ya existente, sin
alterar sus RTL. Ciclos contados desde la simulación a 25 MHz:

| Evento | Ciclo | Observación |
|---|---:|---|
| Reset liberado y primer fetch Espino | 16 | `instr_req` tras `rst_ni` |
| Maestro inicia primera trama | 18 | CS_n baja; maestro pasa a estado de transmisión |
| Primer STATUS del firmware | 28 | Antes de precio; polling esperado |
| SPI Slave completa PRICE | 500 | `price_valid`/`byte_done`, precio 200 |
| STATUS tras recibir precio | 508 | El firmware observa el estado nuevo |
| PRICE leído | 515 | Inicia el ACK de consumo |
| SUM10 leído | 529 | Lectura MMIO real del Espino |
| ACK visible/aceptado en WAIT_ACK | 531 | El maestro abandona la espera |
| READY leído | 532 | Completa las dos lecturas SMA10 |
| DECISION escrita | 542 | Byte `00` en este primer tick |
| Primera respuesta MISO del flujo calculada tras tick 1 | 7046 | Capturada en trama 2; respuesta `00` |

El primer STATUS ocurre antes del primer precio porque `trade.hex` sondea
STATUS desde el inicio. Por tanto, ver STATUS antes de `byte_done` es correcto;
la lectura importante para el primer precio es la de ciclo 508.

En la simulación baseline terminaron 16 ticks, 16 PRICE, 16 DECISION, 16 MISO,
12162 lecturas STATUS, 16 SUM10, 16 READY y cero pérdidas. El testbench
instrumentado también comparó los 16 precios, decisiones y respuestas MISO con
los vectores generados por Python.

## Instrumentación de la variante nueva

El top nuevo expone el último hito como un código binario monotónico en los
cuatro LEDs. Cada código solo se asigna tras confirmar el evento, en este orden:

1. Fetch de Espino después de reset.
2. Inicio de trama: flanco de bajada de CS_n del master.
3. Recepción del primer precio: `byte_done` del SPI Slave.
4. Lectura STATUS después de `byte_done`.
5. Lectura PRICE.
6. ACK aceptado por el master estando en WAIT_ACK.
7. Lecturas de SUM10 y READY completadas.
8. Primera escritura DECISION.
9. MISO del primer tick capturado en la segunda trama.

El primer STATUS de polling se omite del avance de hitos. El master de
diagnóstico emite pulsos separados `frame_start_o` y `ack_accepted_o`; el ACK se
considera recibido cuando WAIT_ACK lo consume, no cuando solo se genera en el
top. En Icarus los códigos avanzaron `1,2,3,4,5,6,7,8,9`, con patrones finales
`0001,0010,0011,0100,0101,0110,0111,1000,1001` (bits en orden D4..D1).

## Síntesis y bitstream

Yosys 0.70+176 y nextpnr-ice40 0.11.1-68-g1daf1f5c; HX1K/VQ100, seed 1,
objetivo de 25 MHz.

| Medida | Resultado |
|---|---:|
| LUT4 | 1003 |
| Logic Cells | 1183/1280 (92%) |
| BRAM | 9/16 |
| Fmax final | 41,15 MHz |
| Timing a 25 MHz | PASS |
| Place and route | Completado normalmente |

Se generó `build/demo_autonoma_trace.bin` (32220 bytes), solo después de pasar
simulación, síntesis y P&R.

SHA-256: `6398D0D433CAAB4925357C63FC9E25D342A8C7B3377E79BB1CCD5707ED299613`.

No se programó la Go Board. La corrección mínima aplicada es de diagnóstico:
mostrar el último hito real en vez de inferir el punto de bloqueo a partir del
LED de actividad y el código de error agregado. La próxima observación física
con este binario señalará directamente el último evento alcanzado.
