# Demo autónoma con trazado de progreso

Variante independiente para localizar el último evento confirmado por el RTL
en la Go Board. Los cuatro LEDs muestran el valor binario del último hito; D1
es el bit menos significativo y D4 el más significativo. En esta variante D1
no significa por sí solo “Espino activo” ni D3 “error”.

| Código | LEDs D4..D1 | Último hito alcanzado |
|---:|---|---|
| 0000 | apagados | Reset / aún sin fetch |
| 0001 | D1 | El Espino hizo fetch después de reset |
| 0010 | D2 | El maestro bajó CS_n para la primera trama |
| 0011 | D1+D2 | SPI Slave produjo el primer `byte_done`/precio |
| 0100 | D3 | STATUS leído después de recibir el primer precio |
| 0101 | D1+D3 | El Espino leyó PRICE |
| 0110 | D2+D3 | El maestro aceptó el ACK de lectura PRICE |
| 0111 | D1+D2+D3 | El Espino leyó tanto SUM10 como READY |
| 1000 | D4 | El Espino escribió la primera DECISION |
| 1001 | D1+D4 | Primera decisión volvió por MISO en la segunda trama |

El primer STATUS anterior al precio se omite del avance de etapa: es el sondeo
normal de `trade.hex`. La señal ACK se cuenta cuando el maestro está en
`WAIT_ACK` y acepta el nivel enclavado `price_ack`, no cuando el top lo genera.
El evento 9 representa el retorno de MISO en la siguiente transacción, por el
desfase de una decisión.

## Reproducción

Desde `pochoco_soc-main`:

```powershell
powershell -ExecutionPolicy Bypass -File proyecto4/pruebas_fisicas/demo_autonoma_trace/ejecutar_pruebas.ps1
powershell -ExecutionPolicy Bypass -File proyecto4/pruebas_fisicas/demo_autonoma_trace/sintetizar.ps1
```

El primer testbench traza la variante handshake existente; el segundo corre el
top instrumentado y compara los 16 precios, decisiones y bytes MISO contra
Python. Síntesis y P&R: HX1K/VQ100, 25 MHz. No programa la placa.

La simulación llega a etapa 9, pasa los 16 ticks y no pierde precios. El informe
con ciclos de cada evento, recursos, timing y hash del bitstream está en
`informe_trace.md`.
