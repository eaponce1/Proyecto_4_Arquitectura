# Informe de corrección por handshake PRICE

## Implementación

Se creó la variante `demo_autonoma_handshake`, sin modificar las carpetas
`demo_autonoma`, `demo_autonoma_debug`, MMIO SMA10 base, Espino ni firmware.
El único cambio funcional frente al master de diagnóstico es el control de
flujo entre transacciones:

1. El master envía el precio actual en SPI modo 0 y desactiva CS_n al terminar.
2. Entra en `WAIT_ACK`; no selecciona ni transmite otro precio.
3. `pochoco_spi_slave` expone su lectura MMIO PRICE como `dbg_price_read`.
4. El top enclava ese evento en `price_ack` hasta el siguiente byte recibido.
5. El master observa el ACK y luego conserva el gap mínimo de 6000 ciclos antes
   de comenzar la siguiente transacción.

De esta manera el gap fijo es un margen de bus, no una suposición de cuánto
tarda el software. La condición 1 de diagnóstico permanece activa como detector
de error: si aparece un `spi_byte_done` antes de que PRICE se lea, guarda el
código 1. La respuesta MISO sigue siendo la decisión previamente escrita; el
generador solo envía precios y recoge MISO.

## Medición de latencia en simulación

La testbench integrada contó ciclos desde el `spi_byte_done` del SPI Slave hasta
el acceso MMIO PRICE del Espino:

| Medida | Resultado |
|---|---:|
| Lecturas PRICE medidas | 16/16 |
| Latencia máxima | 15 ciclos = 0,60 µs a 25 MHz |
| Latencia media | 13,19 ciclos = 0,528 µs a 25 MHz |
| Mínimo desde lectura PRICE al siguiente `spi_byte_done` | 6500 ciclos = 260 µs |

Estas latencias son mediciones del RTL simulado. No se hizo una captura con
analizador lógico de la placa; el handshake evita depender de esa estimación en
la ejecución real.

## Pruebas ejecutadas

Comandos desde `pochoco_soc-main`:

```powershell
powershell -ExecutionPolicy Bypass -File proyecto4/pruebas_fisicas/demo_autonoma_handshake/ejecutar_pruebas.ps1
powershell -ExecutionPolicy Bypass -File proyecto4/pruebas_fisicas/demo_autonoma_handshake/sintetizar.ps1
```

| Prueba | Resultado |
|---|---|
| Monitor de primer error, códigos 1/2/3 | PASS |
| Secuencia Python de 16 precios | PASS |
| PRICE recibido | 16/16 correctos |
| Decisiones del Espino contra Python | 16/16 correctas |
| Respuestas MISO contra Python | 16/16 correctas |
| STATUS / PRICE / SUM10 / READY | 12160 / 16 / 16 / 16 lecturas |
| Escrituras DECISION | 16, exactamente una por precio |
| Ticks perdidos | 0 |
| Código de error al completar | 00 |
| Fetch/commit Espino | 49163 / 36908 |

## Síntesis y place-and-route

Herramientas observadas: Yosys 0.70+176 y nextpnr-ice40 0.11.1-68-g1daf1f5c.
Destino HX1K/VQ100, seed 1, restricción 25 MHz.

| Métrica | Resultado |
|---|---:|
| LUT4 (Yosys) | 985 |
| Logic Cells | 1161/1280 (90%) |
| BRAM | 9/16 |
| Fmax final de nextpnr | 41,65 MHz |
| Timing a 25 MHz | PASS |
| Place-and-route | Completado normalmente |

Se generó el bitstream independiente:
`build/demo_autonoma_handshake.bin` (32220 bytes).

SHA-256: `5D5957236545D9DCC2CB7C3C8A3A7CBEA5C79B48A8F6E65F960F38AB4A9A65BC`.

No se programó la Go Board. Para atribuir el resultado físico al nuevo
handshake se debe programar manualmente este binario exacto y comprobar D1/D2/D3/D4.
