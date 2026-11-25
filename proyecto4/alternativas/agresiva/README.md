# Experimento agresivo de Pochoco Trader

Se evaluaron momentum, breakout, tendencia con trailing stop e híbrida, con exposiciones objetivo de 25 %, 50 %, 75 % y 100 %. Cada familia se probó con entrada directa y compras progresivas. La grilla tiene 384 configuraciones. Con los parámetros congelados se evaluaron 32 finalistas en los últimos 4.000 ticks.

**Selección previa al tramo reservado:** momentum directo, exposición objetivo 100 %, revisión cada 16 ticks, umbral 8. El firmware reutiliza el SPI externo y el SoC Espino a 12,5 MHz. La candidata queda en investigación porque no superó a comprar y mantener en el tramo reservado. [Informe cuantitativo y política de selección](INFORME_CUANTITATIVO.md)

| Tramo | Momentum 100 % | No operar | Buy & Hold ejecutable | Diferencia |
|---|---:|---:|---:|---:|
| Entrenamiento, 12.000 ticks | $15.965 | $10.000 | $13.055 | +$2.910 |
| Validación, 4.000 ticks | $10.000 | $10.000 | $6.177 | +$3.823 |
| Prueba reservada, 4.000 ticks | $9.265 | $10.000 | $11.633 | −$2.368 |
| Serie completa, 20.000 ticks | $15.232 | $10.000 | $9.695 | +$5.537 |

La posición se mantuvo hasta 6.624 ticks consecutivos. El detector de salida revisa el momentum cada 16 ticks y activa la liquidación si la caída respecto de la revisión anterior alcanza 8 puntos. La maestra ejecuta la próxima orden con un tick de desfase. El detector trailing de las alternativas evaluadas revisa caídas desde el pico en cada tick.

Una exposición objetivo de 100 % describe la intención al precio observado. La política directa solicita un máximo de 63 acciones en la entrada. El saldo remanente, el desfase y el límite por orden pueden reducir la exposición realizada. El límite de drawdown y los límites de comisiones fueron filtros de selección en entrenamiento y validación. La política agresiva puede sufrir una pérdida mayor en una serie nueva o en una caída entre dos ticks.

## Assembly RV32E

`trade.s` usa el mapa MMIO del Proyecto 4. Lee STATUS, PRICE, SUM10 y READY y emite DECISION una vez por precio. Durante cada tick aplica localmente la orden transmitida en esa trama al precio actual. Las compras usan un algoritmo voraz por bloques de 32, 16, 8, 4, 2 y 1 para hallar la cantidad financiable. Las ventas se recortan al inventario y requieren caja suficiente para la comisión. Si una venta se rechaza al precio de ejecución, persiste el estado de liquidación.

Los registros persistentes son x1 para la base MMIO, x4 para la orden pendiente, x5 para el inventario, x6 para la fase y la bandera de liquidación, x7 para el precio de revisión anterior y x15 para la caja. La compra directa solo abre una posición si el inventario es cero, por lo que en esta política el inventario nunca excede 63. Cada orden se mantiene entre cero y 63, y el producto máximo de una orden por el precio es 16.065. El programa tiene 128 palabras, usa aritmética entera y carece de MUL, DIV y desplazamientos. Reutiliza el top SPI externo y su ROM de instrucciones.

## Validación medida

El intérprete de RV32E ejecutó el HEX contra Python en los 20.000 ticks, también con reinicio independiente en cada tramo. Coincidieron MISO, DECISION, caja e inventario. Pasaron las 36 pruebas de regresión Python. [Equivalencia](equivalencia_local.log) · [Regresión Python](regresion_python.log)

| Prueba RTL previa a síntesis | Precios | Período | Peor latencia / presupuesto |
|---|---:|---:|---:|
| Prefijo de práctica | 2.000 | 100 µs | 54 / 1.131 ciclos |
| Estrés de compra parcial y liquidación | 34 | 100 µs | 169 / 1.131 ciclos |
| Prefijo ampliado, incluida una compra y una venta ejecutadas | 4.000 | 32 µs | 178 / 281 ciclos |
| Estrés de brecha de precio y reintento de venta | 85 | 32 µs | 164 / 281 ciclos |

Las cuatro corridas RTL cotejaron precios, DECISION, MISO y cartera con Python. La latencia se mide desde la llegada del precio hasta la escritura de DECISION. El núcleo opera a 12,5 MHz, así que los 178 ciclos del prefijo ampliado equivalen a 14,24 µs. En el netlist se simularon 34 precios de estrés a 30 µs en cada una de dos fases SPI, 0 y 41 ns. Las 34 respuestas MISO y la cartera de cada corrida coincidieron con Python. [Métricas del flujo](build/resultados.json) · [Cobertura ampliada](build_cobertura/resultados.json) · [Traza de 4.000 ticks](build_cobertura/rtl_practica.csv) · [Traza del reintento](build_cobertura/rtl_estres.csv)

Yosys y nextpnr aprobaron para **iCE40 HX1K/VQ100** con la restricción de **25 MHz**. Se ocuparon **1.193/1.280 celdas lógicas**, **1.079 LUT4** y **7/16 BRAM**. La Fmax informada para `clk_soc` después de ruteo fue **50,70 MHz**. [Yosys](build/yosys.log) · [Place and route](build/nextpnr.log) · [Timing](build/timing.json)

La imagen experimental de 32.220 bytes es [competition.bin](build/competition.bin). Su SHA-256 es `240898F3A860546B3CB694F4F7102E9566D50427E26FAB1A06F92D78708A84A9`. Se conservaron el BIN anterior, sus fuentes y la serie oficial con los hashes registrados. La FPGA sigue con su última programación verificada. La prueba física de esta candidata está pendiente. [Hashes anteriores](SHA256_previo.txt) · [Hashes de la entrega](SHA256_entrega.txt)

## Reproducir en Windows

Ejecutar desde la raíz del repositorio con Python 3.13.3, Icarus/VVP 14.0 devel (`s20260301-626-g7e3d0c6bd-dirty`), Yosys 0.70+176 (`365bb887b`) y nextpnr-ice40 `0.11.1-68-g1daf1f5c` en PATH. El binario `icepack.exe` usado tiene SHA-256 `A5BEEC407C1A0AE8D22547DB91F9818A182CF3D2BB5BE552ACBF97A77227CB7F`. El flujo usa `share/yosys/ice40/cells_sim.v` de la distribución de Yosys para simular las primitivas de la FPGA.

```powershell
$p = 'proyecto4/alternativas/agresiva'
# Repetir la evaluación con los parámetros congelados
python -X utf8 -B "$p/backtest_agresiva.py" --fase evaluar
# Ensamblar y cotejar las decisiones y cartera de 20.000 ticks
python -X utf8 -B "$p/validar_agresiva.py" --solo-hex --salida "$p/verify_hex"
# Comprobar compras y ventas sobre 4.000 precios reales y 85 ticks de estrés
python -X utf8 -B "$p/validar_agresiva.py" --solo-rtl --estres-reintento --ticks-rtl 4000 --periodo-rtl-ns 32000 --salida "$p/verify_4000"
# Ejecutar la regresión Python
python -X utf8 -B -m unittest discover -s proyecto4/python -v
# Construir en una carpeta aparte
python -X utf8 -B "$p/validar_agresiva.py" --salida "$p/verify_fpga"
```

El ejecutor sólo lanza síntesis tras aprobar la equivalencia del intérprete y las corridas RTL requeridas por el build. Cada ejecución de síntesis se valida con nextpnr HX1K/VQ100 y pruebas del netlist en dos fases de SPI. El PCF y el BIN programado de la candidata anterior tienen huellas en `SHA256_previo.txt`.

