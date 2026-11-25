# Proyecto 4 — inicio rápido y estado de cierre

## Variante que se debe tratar como entrega de referencia

La arquitectura documentada como versión final de competencia es **MMIO SMA10 base**:

- Top: `proyecto4/alternativas/mmio_sma10/trade_top.v`.
- SoC y periférico: `proyecto4/alternativas/mmio_sma10/rtl/`.
- Firmware RV32E: `proyecto4/alternativas/mmio_sma10/sw/trade.s`.
- Imagen: `proyecto4/alternativas/mmio_sma10/sw/trade.hex`.
- PCF de la Go Board: `goboard.pcf`.
- Build físico reproducible: `proyecto4/programacion_fisica/generar_bitstream.py`.

No usar como imagen de competencia el `spi_smoke.hex`, el `game.hex` del Proyecto 2 ni el wrapper genérico `proyecto4/rtl/trade_top.v`: son pruebas o imágenes de otras etapas. El top de MMIO base activa `EnableSpi=1` y apunta al HEX de su propia carpeta.

## Comandos principales (PowerShell, desde la raíz)

### 1. Ensamblar el firmware final

```powershell
python -B proyecto4/sw/assembler.py proyecto4/alternativas/mmio_sma10/sw/trade.s -o proyecto4/alternativas/mmio_sma10/sw/trade.hex
```

El programa usa RV32E, x0–x15, y no necesita MUL, DIV ni instrucciones de shift.

### 2. Ejecutar la suite Python del Proyecto 4

```powershell
python -B -m unittest discover -s proyecto4/python -v
```

La suite actual registra **36/36 pruebas aprobadas** para el Proyecto 4 en GitHub Actions (25/11/2026). La misma ejecución aprobó también 11/11 pruebas Python del Proyecto 2, los cuatro bancos RTL heredados y el ensamblado final de 71 instrucciones. [Ver regresión aprobada](https://github.com/eaponce1/Proyecto_4_Arquitectura/actions/runs/45665702222). La generación del PDF también terminó correctamente: [ver render](https://github.com/eaponce1/Proyecto_4_Arquitectura/actions/runs/45665702176).

Para la prueba del assembler custom-0:

```powershell
python -B -m unittest proyecto4.alternativas.custom0.tb.test_assembler_custom0 -v
```

### 3. Repetir la validación oficial de las tres rondas

El testbench oficial se conserva en `proyecto4/resultados/validacion_oficial/`. Cada ejecución completa procesa 20.000 ticks. Ronda 1 = 10 ms; ronda 2 = 1 ms; ronda 3 = 0,1 ms.

```powershell
python -B proyecto4/resultados/validacion_oficial/ejecutar_validacion.py --variant mmio --round 3
python -B proyecto4/resultados/validacion_oficial/ejecutar_validacion.py --variant software --round 3
python -B proyecto4/resultados/validacion_oficial/ejecutar_validacion.py --variant mmio --round 2 --fast-idle
python -B proyecto4/resultados/validacion_oficial/ejecutar_validacion.py --variant software --round 2 --fast-idle
python -B proyecto4/resultados/validacion_oficial/ejecutar_validacion.py --variant mmio --round 1 --fast-idle
python -B proyecto4/resultados/validacion_oficial/ejecutar_validacion.py --variant software --round 1 --fast-idle
python -B proyecto4/resultados/validacion_oficial/resumir_corridas.py --tres-rondas
```

La espera acelerada solo se usa cuando el ejecutor verifica que el estado del SoC se mantiene entre transacciones; las tramas SPI y los cuatro criterios siguen simulándose en Icarus de cuatro estados. Las seis corridas históricas están resumidas en `resultados/validacion_oficial/comparacion_tres_rondas.csv`.

### 4. Medir co-diseño

```powershell
python -B proyecto4/alternativas/mmio_sma10/medir_mmio_sma10.py --ticks 20000
python -B proyecto4/alternativas/custom0/medir_custom0.py --ticks 20000
```

Estas mediciones usan una cadencia de prueba de 30 µs por tick por defecto. No confundirlas con la validación oficial por rondas.

### 5. Sintetizar, enrutar y generar el bitstream

```powershell
python -B proyecto4/programacion_fisica/generar_bitstream.py
```

El script ejecuta Yosys, nextpnr-ice40 e icepack. **No programa la Go Board.** Para programar manualmente, con la placa conectada por USB y la FPGA maestra desconectada:

```powershell
iceprog proyecto4/programacion_fisica/trade_mmio_base.bin
iceprog -c proyecto4/programacion_fisica/trade_mmio_base.bin
```

La construcción registrada para MMIO base usa HX1K/VQ100 y objetivo de 25 MHz: 1.055 LUT4, 1.279/1.280 LC, 13/16 BRAM y Fmax post-route de 40,50 MHz. Queda solo una LC libre; no agregar lógica a esta variante sin repetir síntesis y P&R.

## Resultados que deben comunicarse con precisión

### Funcionalidad y tiempo

- En las tres rondas de práctica, MMIO SMA10 base y software original procesaron 20.000 ticks por ronda y aprobaron 4/4 criterios del testbench.
- Las decisiones transmitidas coincidieron con Python en los 20.000 ticks.
- En ronda 3, MMIO midió 60 ciclos promedio (entero truncado) y 255 de peor caso; software midió 218 y 413 ciclos. El presupuesto efectivo reportado es 2.262 ciclos.
- El co-diseño MMIO redujo los ciclos medios aproximadamente 3,606× frente al software original.

### Resultado financiero de la estrategia SMA10

La estrategia de referencia **no fue rentable en la serie de práctica**. En 20.000 ticks terminó con $4.577, frente a $10.000 de no operar y $9.695 de comprar y mantener; ejecutó 931 órdenes, pagó $4.655 en comisiones y registró drawdown máximo de $5.476. El acelerador MMIO mejora el tiempo de ejecución, no la rentabilidad ni las decisiones.

La carpeta `proyecto4/alternativas/agresiva/` contiene una investigación adicional. No se eligió para la imagen final: aunque la corrida completa termina en $15.232, la prueba reservada termina en $9.265 frente a $11.633 de comprar y mantener ejecutable. No presentar su resultado completo como evidencia fuera de muestra.

### Evidencia física y límites

- Hay una demo autónoma de 16 ticks que obtuvo PASS físico en Go Board, pero utilizó una imagen de autotest distinta de la imagen de competencia MMIO base.
- Se registró una práctica con la FPGA maestra (Tesla, Fila 2) con patrimonio visible de $5.329. No se dispone del cotejo MISO tick a tick ni del hash del BIN de esa sesión; no se puede atribuir ese resultado de forma concluyente al BIN auditado.
- La integración física final con la FPGA maestra, el registro de la competencia oficial y la defensa presencial siguen pendientes.
- El testbench heredado `tests/periph_tb.v` fue corregido para respetar la polaridad activa-baja. El cambio quedó en el commit `a4825d8`; falta ejecutar `python -B tests/run_tests.py` en un entorno con Icarus para confirmar la regresión completa.

## Conexión física SPI

| Señal | Go Board | Pin FPGA |
|---|---|---:|
| CS_n | PMOD PS1 | 65 |
| MOSI | PMOD PS2 | 64 |
| MISO | PMOD PS3 | 63 |
| SCLK | PMOD PS4 | 62 |

Usar SPI modo 0, byte de 8 bits, MSB primero, SCLK ≤ 1 MHz, señales de 3,3 V y GND común. La Go Board se alimenta por USB; no usar el pin VCC del PMOD como señal.

## Documentos para entrega y defensa

- [Informe final PDF](entrega_final/informe_final_proyecto4.pdf)
- [Informe técnico editable](documentacion/informe_final_proyecto4.md)
- [Matriz de cierre por requisito](documentacion/matriz_cierre_pochoco.md)
- [Auditoría final](documentacion/auditoria_final_cierre.md)
- [Guía de defensa](documentacion/guia_defensa.md)
- [Guion de presentación](documentacion/guion_presentacion.md)
- [Manifiesto de entrega](entrega_final/MANIFIESTO.md)

> Nota: el `Makefile` de la raíz y `make all` construyen el top heredado `game_top` del Proyecto 2. Para el trader del Proyecto 4, usar los comandos de esta guía.
