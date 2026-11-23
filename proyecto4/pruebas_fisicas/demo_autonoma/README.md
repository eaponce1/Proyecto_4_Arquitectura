# Demo autónoma del Pochoco Trader

Variante independiente para la Go Board HX1K/VQ100. El maestro SPI interno envía
16 precios deterministas (10×200, 3×90, 3×220) al SPI Slave original. El Pochoco
SoC reducido conserva el Espino original, RAM con `trade.hex`, SPI Slave y
acelerador SMA10 de la alternativa MMIO base. Se quitaron del wrapper solamente
los displays, switches y periférico del juego, que `trade.hex` no usa.

El generador solo transmite bytes de precio y captura MISO. No escribe
DECISION, no calcula la media móvil ni genera señales. El firmware real es el
único que accede a STATUS/PRICE/SUM10/READY y escribe DECISION. El testbench
genera las decisiones esperadas mediante `proyecto4/python/enfoques_finales.py`
y `simulador.py`, y contrasta las escrituras del core y cada byte MISO.

## Indicadores

| LED | Significado |
|---|---|
| LED0 | El Espino inició fetch |
| LED1 | El firmware leyó SUM10 o READY |
| LED2 | Error: tick sin consumir o DECISION fuera de secuencia |
| LED3 | Secuencia de 16 precios y 16 decisiones terminada |

Los pines se derivan del `goboard.pcf` del Proyecto 2: reloj 25 MHz en FPGA pin
15 y LED0–LED3 en 56, 57, 59 y 60. El PCF independiente no asigna pines SPI,
porque maestro y slave se conectan internamente. La polaridad LED debe
confirmarse visualmente en la placa al programar manualmente.

## Simulación

Desde la raíz `pochoco_soc-main`:

```powershell
powershell -ExecutionPolicy Bypass -File proyecto4/pruebas_fisicas/demo_autonoma/ejecutar_pruebas.ps1
```

La simulación comprueba fetch/commit, lecturas STATUS, PRICE, SUM10 y READY,
16 escrituras DECISION, 16 respuestas MISO, orden temporal SPI y ausencia de
ticks no consumidos. `python/generar_vectores.py` regenera precios y respuestas
esperadas antes de compilar.

## Síntesis y prueba física

```powershell
powershell -ExecutionPolicy Bypass -File proyecto4/pruebas_fisicas/demo_autonoma/sintetizar.ps1
```

El script sintetiza HX1K/VQ100, intenta place and route a 25 MHz y genera un
`.bin` dentro de `build/` solo cuando nextpnr termina correctamente y reporta
como máximo 1280 LC. Nunca programa la placa. Si no cabe o falla timing, no
produce el binario.

Validación del 22-11-2026: simulación integrada **PASS** (16/16 ticks y MISO,
16 escrituras DECISION, equivalencia con Python, 0 ticks perdidos). Síntesis:
991 LUT4, 1174/1280 LC, 9/16 BRAM; nextpnr estimó 41,53 MHz y pasó a 25 MHz.
Se generó `build/demo_autonoma.bin`; la placa no fue programada. Los logs de
Yosys y nextpnr y el detalle de resultados están en `build/` y
`informe_validacion.md`.

El firmware y los RTL reutilizados están referenciados en su ubicación base;
esta carpeta no los copia ni modifica. Para una prueba física manual, verificar
primero que LED0 enciende durante ejecución, LED1 tras lecturas SMA10, LED2
permanece apagado y LED3 enciende al concluir.
