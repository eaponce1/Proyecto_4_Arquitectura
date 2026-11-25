# Proyecto 4 — Pochoco Trader

Este directorio reúne la investigación, firmware, alternativas de co-diseño, testbenches, resultados y documentación del Proyecto 4.

**Punto de entrada recomendado:** [INICIO_RAPIDO.md](INICIO_RAPIDO.md). Allí están la variante que se debe usar, los comandos de ensamblado, las pruebas por ronda, la síntesis, los pines SPI y los límites de la evidencia física.

La arquitectura de referencia de competencia documentada es **MMIO SMA10 base**, en `alternativas/mmio_sma10/`. El firmware de humo `sw/spi_smoke.s` de la etapa inicial solo comprobó STATUS/PRICE/DECISION; no es el agente final. Las variantes `custom0`, `mmio_sma10_opt`, `candidata_final` y `agresiva` se conservan como experimentos o comparaciones y no sustituyen automáticamente a la imagen final.

La carpeta contiene también documentación histórica de las etapas de desarrollo. Para conocer el estado real de cierre y las tareas que todavía requieren la FPGA maestra, consulta primero la guía de inicio rápido y la [matriz de cierre](documentacion/matriz_cierre_pochoco.md).

## Preparación y pruebas

Ejecutar desde la carpeta `pochoco_soc-main` en PowerShell:

```powershell
python sw/assembler.py proyecto4/sw/spi_smoke.s -o proyecto4/sw/spi_smoke.hex
python -B tests/run_tests.py
$rtl = (Get-ChildItem rtl -Recurse -Filter *.v).FullName
iverilog -g2012 -s tb_proyecto_4 -o proyecto4/tb_proyecto_4.vvp $rtl tests/ram_model.v proyecto4/tb/tb_proyecto_4.sv
vvp proyecto4/tb_proyecto_4.vvp +ROUND=3 +TICKS=100
```

`ROUND` selecciona el período entre transacciones: 1 = 10 ms, 2 = 1 ms,
3 = 0,1 ms. `TICKS` limita los ticks simulados para pruebas rápidas; si se omite,
el testbench procesa los 20 000 ticks. En todos los casos carga y valida la serie
completa antes de iniciar la simulación. Para ejecutar cada ronda completa:

```powershell
vvp proyecto4/tb_proyecto_4.vvp +ROUND=1
vvp proyecto4/tb_proyecto_4.vvp +ROUND=2
vvp proyecto4/tb_proyecto_4.vvp +ROUND=3
```

El modelo `tests/ram_model.v` es funcional, no el modelo temporal del fabricante.
Las simulaciones no programan la Go Board.

## Estado de validación de esta etapa

- Compilación del testbench Proyecto 4 con Icarus: aprobada.
- Simulación de humo: 9/9 chequeos aprobados en las tres rondas. Se ejecutaron
  100 ticks en ronda 3 y 2 ticks en cada una de las rondas 1 y 2; en cada ejecución
  se cargó y validó el CSV completo de 20 000 filas.
- Regresión Python del Proyecto 2: 11/11 pruebas aprobadas.
- Banco `core_tb`: aprobado.
- Banco `periph_tb`: se identificó que el estímulo final usaba `btn=3` aunque
  las entradas físicas son activas en bajo. Se corrigió a `btn=4'b1100` para que,
  tras la inversión del RTL, el valor lógico observado sea `0011`. El cambio está
  en el commit `a4825d8`. Falta volver a ejecutar `python -B tests/run_tests.py`
  con Icarus en el equipo local; no se declara una regresión completa aprobada
  hasta repetirla.
- Bancos `spi_tb` y `decoder_tb`, ejecutados por separado tras el fallo anterior:
  aprobados; compilación completa de `game_top`: aprobada.
- Icarus advierte que `spi_smoke.hex` contiene menos de 512 palabras. La imagen de
  prueba sí se carga y simula; la advertencia no detuvo la ejecución.

En esta etapa se comprobaron las transacciones de humo con `spi_smoke.s`.
Las seis corridas completas con el agente se documentan en la
[validación de las tres rondas](resultados/validacion_oficial/informe_comparativo_tres_rondas.md).

## Etapa 2: estrategia de referencia en Python

Desde `pochoco_soc-main`, ejecutar:

```powershell
python -B -m unittest discover -s proyecto4/python -v
python -B proyecto4/python/simulador.py
```

El simulador lee exactamente 20 000 filas con ticks secuenciales desde
`proyecto4/data/practica_meta.csv`. Escribe `decisiones_trading.csv`,
`comparacion_estrategias.csv`, `precio_serie.svg` y
`patrimonio_estrategias.svg` en `proyecto4/resultados/`. El cálculo y los gráficos
usan solo la biblioteca estándar de Python.

La estrategia propia espera diez observaciones. Compara SMA 5 y SMA 10 con la
comparación entera `2 * suma_5` contra `suma_10`, evitando divisiones. El momentum
es `precio_actual - precio_de_hace_tres_ticks`. Compra una acción si ambas señales
son alcistas; vende una si ambas son bajistas y hay acciones; en los demás casos
mantiene. No se ajustaron parámetros a la rentabilidad. La referencia comprar y
mantener coloca antes del primer tick una orden de 63 acciones; el simulador aplica
el máximo asequible y conserva el resto de la caja. Así la orden inicial respeta
el byte SPI de seis bits sin consultar precios futuros.

Ejemplo con los cinco primeros precios reales:

| Tick | Precio | Decisión recibida y ejecutada | Decisión calculada para el tick siguiente |
|---:|---:|---|---|
| 0 | 165 | Mantener (inicial) | Mantener (1 observación) |
| 1 | 165 | Mantener | Mantener (2 observaciones) |
| 2 | 165 | Mantener | Mantener (3 observaciones) |
| 3 | 165 | Mantener | Mantener (4 observaciones) |
| 4 | 166 | Mantener | Mantener (5 observaciones) |

No hay señal hasta contar con diez precios. Cada decisión de la última columna
queda pendiente para el siguiente tick, nunca se ejecuta contra el precio que la
generó.

### Resultados medidos sobre la serie completa

| Estrategia | Patrimonio final | Caja final | Acciones | Rentabilidad | Órdenes | Comisiones | Pérdida máxima | Drawdown máximo |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| No operar | $10 000 | $10 000 | 0 | 0,00% | 0 | $0 | $0 | 0,00% |
| Comprar y mantener | $9 695 | $95 | 60 | -3,05% | 1 | $5 | $9 300 | 60,41% |
| Trading SMA 5/10 + momentum | $102 | $102 | 0 | -98,98% | 2 022 | $10 110 | $10 152 | 99,01% |

Estos valores son la salida observada de `simulador.py`, no una expectativa de
rentabilidad futura. El trading de referencia pierde casi todo el capital por la
frecuencia de órdenes y las comisiones; se conserva como baseline transparente,
sin afinar ventanas ni señales con la serie de práctica.

Al traducirlo a Assembly, lo más costoso será mantener el historial de diez precios
y actualizar las ventanas móviles: almacenamiento/lectura de los precios que salen
de las ventanas, sumas/restas y control de un índice circular. También se necesitan
comparaciones con branches y la resta de momentum. El criterio de SMA evita dividir
y no requiere multiplicador: duplicar la suma corta equivale a una suma consigo
mismo. La cantidad fija de una acción evita multiplicación para formar órdenes.

En la validación inicial de etapa 2 pasaron sus 13 pruebas de estrategia y las
11 pruebas Python heredadas. La suite ampliada de etapa 3 se describe a continuación.

## Auditoría y sensibilidad de estrategias v2

Para repetir la auditoría contable y generar la grilla v2:

```powershell
python -B -m unittest discover -s proyecto4/python -v
python -B proyecto4/python/investigacion.py
```

La investigación ejecuta 24 escenarios: las dos referencias, la estrategia
original y las variantes A/B/C con cantidades 1, 2, 4, 8, 16, 32 y 63. La grilla
es descriptiva; no se escoge una cantidad maximizando esta serie.

El drawdown de $10.152 se reproduce: peak $10.254 en tick 535 y valle $102 en
tick 17.106. Caja y acciones son no negativas. El drawdown absoluto se mide desde
el peak histórico, por eso puede superar el capital inicial sin que exista deuda.
El informe FIFO incorpora comisiones al costo de compra y resta la comisión de
venta al cerrar.

Salidas: `resultados/comparacion_estrategias_v2.csv`,
`resultados/operaciones_v2.csv`, `resultados/analisis_estrategias.md` y
`resultados/patrimonio_estrategias_v2.svg`. Las 23 pruebas Python del Proyecto 4
verifican contabilidad, FIFO, desfase, causalidad, variantes y cantidades. En la
etapa v2 se ejecutaron 23 pruebas; la investigación final amplía el total a 29.
La regresión Python heredada del Proyecto 2 conserva sus 11 pruebas.

## Investigación final de estrategias

```powershell
python -B -m unittest discover -s proyecto4/python -v
python -B proyecto4/python/investigacion_final.py
```

La corrida final evalúa 20.000 ticks y cuatro corridas independientes de 5.000
ticks. Cada segmento comienza con $10.000, cero acciones e historial vacío. Los
parámetros q=16 y las señales se fijan antes de comparar. El costo de decisión
RV32E es una estimación de kernel a CPI 2,35, no una medición de `trade.s`.
Entregables: `resultados/investigacion_final.md`,
`resultados/comparacion_final.csv` y `resultados/patrimonio_final.svg`.

## Etapa 3: firmware RV32E SMA10

Generar y probar `trade.hex` desde la raíz `pochoco_soc-main`:

```powershell
python sw/assembler.py proyecto4/sw/trade.s -o proyecto4/sw/trade.hex
python -B -m unittest discover -s proyecto4/python -v
```

`test_trade_equivalencia.py` interpreta las instrucciones reales del HEX y las compara tick por tick con `estrategia_reversion_media` sobre los 20.000 precios. Además compila el SoC RTL y `tb_trade_equivalencia.sv` con Icarus para verificar la decisión transmitida por SPI en una serie sintética. Esta segunda prueba es corta y de integración; no equivale a ejecutar el RTL durante los 20.000 ticks. La distribución de registros, las direcciones MMIO, el buffer, la estimación de ciclos, resultados y limitaciones están en `resultados/etapa3_assembly.md`.

La regresión heredada se ejecuta con `python -B tests/run_tests.py`. Actualmente se detiene en `periph_tb` por su expectativa antigua de polaridad de botones; esto es independiente de `trade.s`. Las pruebas Python de Proyecto 2 se pueden ejecutar aparte con `python -B -m unittest discover -s tests`.

## Etapa 3: medicion de rendimiento

Desde `pochoco_soc-main`, ejecutar la medicion completa (20.000 ticks):

```powershell
python -B proyecto4/python/medir_rendimiento_trade.py
```


Por defecto el banco usa una cadencia custom de 30 us para reducir el largo periodo de polling en la simulacion. Compara MISO tick por tick con Python, cuenta IC con `instr_valid_id && !stall`, separa STATUS, PRICE y las secciones del algoritmo, y falla ante ticks perdidos. Los resultados medidos estan en `resultados/rendimiento_software.md`, `resultados/mediciones_software.csv` y `resultados/rendimiento_software.svg`. `--round 3` ejecuta a 100 us oficiales; `--round 1/2` corre a 10 ms/1 ms.

## Cierre, co-diseño y preparación física

La documentación de cierre, guía de preguntas y guion de presentación están en:

- `documentacion/informe_final_proyecto4.md`: auditoría de arquitectura, estrategia/contabilidad, Assembly, SPI/MMIO, métricas de software/co-diseño, síntesis y límites de evidencia.
- `documentacion/guia_defensa.md`: preguntas técnicas y respuestas breves.
- `documentacion/guion_presentacion.md`: exposición de aproximadamente nueve minutos.

La versión acelerada MMIO SMA10 base es la referencia de hardware. A 20.000 ticks mide 60,64 ciclos promedio y acelera 3,606× por ciclos frente al software original. La síntesis/P&R para HX1K informa 1055 LUT4, 1279/1280 LC, 13/16 BRAM y 40,50 MHz. La variante optimizada es independiente y baja a 1274 LC con los mismos ciclos; no alcanza la meta de área. custom-0 no cabe en HX1K (1350 LC).

La imagen base está en `programacion_fisica/trade_mmio_base.bin`; `python proyecto4/programacion_fisica/generar_bitstream.py` regenera el build. El informe de programación indica que `iceprog` no se ejecutó. La placa programada con MMIO base es un estado comunicado por el usuario; el repositorio no incluye transcripción de `VERIFY OK`. La fixture `pruebas_fisicas/spi_slave/internal/` es una prueba separada: su testbench y P&R pasaron, pero no se programó la placa para ella. No se debe describir ninguno de esos resultados como ejecución física verificada.

### Validación oficial de ronda 3

Con el testbench publicado y 20.000 ticks, MMIO SMA10 base y software original aprobaron **4/4 criterios**. Las 20.000 decisiones coinciden exactamente entre ambas arquitecturas. Ambas terminaron con patrimonio de **$4.577**, 931 órdenes (466 compras y 465 ventas), $4.655 en comisiones y drawdown de $5.476. Los promedios enteros truncados que imprimió el testbench fueron 60 ciclos para MMIO y 218 para software; los peores casos fueron 255 y 413 ciclos, respectivamente. MMIO reduce el costo computacional sin cambiar la estrategia ni el resultado financiero.

Las rondas 1 y 2 también completaron 20.000 ticks y 4/4 criterios por arquitectura con Icarus y espera verificada. Todas las decisiones coincidieron. [Comparación de las tres rondas](resultados/validacion_oficial/comparacion_tres_rondas.csv)

### Repetir la validación de 2.000 ticks en Windows

Extrae `Pochoco_Trader_cierre_auditado.zip` en un directorio vacío o usa el árbol local auditado. La raíz es el directorio que contiene `goboard.pcf` y `tb/ejecutar_tb_proyecto4.ps1`. El ZIP de la publicación anterior carece del ejecutor nuevo.

Se usó Windows PowerShell 5.1, Python 3.13.3 e Icarus Verilog 14.0 de desarrollo. Agrega al `PATH` Python y el directorio `bin` de OSS CAD Suite que contiene `iverilog.exe` y `vvp.exe`. El modelo de RAM para simular está en `tests/ram_model.v`.

```powershell
Get-Command python, iverilog, vvp
powershell -NoProfile -ExecutionPolicy Bypass -File .\tb\ejecutar_tb_proyecto4.ps1
if ($LASTEXITCODE -ne 0) { throw 'Fallo la validacion del banco' }
python -B -m unittest discover -s proyecto4/python -v
if ($LASTEXITCODE -ne 0) { throw 'Fallo la suite Python' }
```

El ejecutor compila el SoC de `proyecto4/alternativas/mmio_sma10/rtl/` y carga `proyecto4/alternativas/mmio_sma10/sw/trade.hex`. Valida las 20.000 filas de `proyecto4/resultados/validacion_oficial/practica_meta.csv` y simula sus primeras 2.000 a 100.000 ns por tick. Guarda `tb/build/icarus.log`, `tb/build/decisiones.csv` y el ejecutable `.vvp`. El CSV registra MISO, DECISION, ciclos y contabilidad por tick. Espera `PASS integral`, patrimonio 9.839, 109 órdenes, drawdown 396 y un máximo de 253 ciclos.

El aviso de `$readmemh` indica que el HEX ocupa 71 de las 512 palabras de RAM. La corrida completa y el cotejo con Python constan en la [auditoría final](documentacion/auditoria_final_cierre.md).

### Comprobaciones al cierre

Desde `pochoco_soc-main`:

```powershell
python -B -m unittest discover -s proyecto4/python -v
python -B -m unittest proyecto4.alternativas.custom0.tb.test_assembler_custom0 -v
python -B tests/run_tests.py
```

La suite Proyecto 4 se ejecutó al preparar el informe: 32/32 aprobadas. El test del assembler custom-0 está reportado con 3 pruebas aprobadas. La regresión heredada `tests/run_tests.py` tiene un fallo conocido en `periph_tb` (`debounced buttons`, expectativa de polaridad); los bancos `core_tb`, `spi_tb` y `decoder_tb` pasan por separado según los registros previos. No se modificaron fuentes funcionales en esta etapa de documentación.

## Informe PDF y versiones de herramientas

El informe técnico de entrega se genera desde `documentacion/informe_final_proyecto4.md` con ReportLab:

```powershell
python -B proyecto4/documentacion/generar_pdf.py
```

El PDF resultante queda en `proyecto4/entrega_final/informe_final_proyecto4.pdf`. La carpeta incluye un manifiesto; los fuentes, firmware y evidencias se conservan en sus ubicaciones canónicas para evitar duplicarlos.

Versiones observadas al preparar y validar este árbol en Windows (no representan una garantía para otro equipo):

| Herramienta | Versión detectada | Nota |
|---|---|---|
| Python | 3.13.3 | Intérprete usado para pruebas y scripts. |
| Icarus Verilog (`iverilog`) | 14.0 devel, `s20260301-626-g7e3d0c6bd-dirty` | Compilador HDL de las simulaciones. |
| Icarus runtime (`vvp`) | 14.0 devel, `s20260301-626-g7e3d0c6bd-dirty` | Ejecuta los `.vvp`. |
| Yosys | 0.70+176, Git `365bb887b` | Síntesis observada. |
| nextpnr-ice40 | 0.11.1-68, Git `g1daf1f5c` | Place and route observado. |
| icepack | El ejecutable no informa versión por CLI | SHA-256 de `icepack.exe`: `A5BEEC407C1A0AE8D22547DB91F9818A182CF3D2BB5BE552ACBF97A77227CB7F`. No se infiere una versión a partir de Yosys. |
| ReportLab | 5.0.1 | Renderizador PDF desde Markdown, mediante `documentacion/generar_pdf.py`. |
| Assembler RV32E del repositorio | No tiene release independiente | `sw/assembler.py`; SHA-256: `1541359E87F59FEEDCE169EC58573EFA063316A7121A9EE27C37AEED8795184D`. |
| Verilator | 5.053 devel `v5.052-507-g01770671e` | Evaluado para traducir RTL; no sustituye el check MISO de cuatro estados. |

Los hashes fijan los ejecutables cuando la herramienta carece de una versión utilizable. El árbol descargado carece de metadata Git. La auditoría lo comparó con el checkout publicado en `5229fdbd3d9d674fc9fec207d3e68f4370294017`.

## Carpeta compacta de entrega

`proyecto4/entrega_final/` contiene el PDF, el ZIP y `MANIFIESTO.md`. La imagen final de competencia es MMIO SMA10 base. Las seis corridas de práctica aprobaron 4/4 criterios y la demo autónoma pasó en Go Board. Queda pendiente la integración física con la FPGA maestra.

## Objetivos finales de Go Board

La imagen elegida para el curso es `programacion_fisica/trade_mmio_base.bin`, con MMIO SMA10 base y SPI externo. Las tres rondas de práctica completaron 20.000 ticks y 4/4 criterios para ambas arquitecturas, con equivalencia exacta de decisiones.

La demo autónoma verificó físicamente los 16 precios, decisiones y MISO con la imagen `selftest_fetch_rom_lento.bin` a 12,5 MHz. La flash dio `VERIFY OK`, los LEDs mostraron `1010` y COM10 registró `0xAA` en tres arranques.

En la práctica con la FPGA maestra **Tesla ene 2022**, el grupo fue **Fila 2** y terminó con **$5.329**. La maestra reflejó operaciones en esa fila. Quedan pendientes el cotejo de MISO tick a tick y la verificación del BIN de esa sesión. [Registro de la práctica física](pruebas_fisicas/spi_externo_robusto/README.md#práctica-física-en-fila-2)

La [matriz de cierre](documentacion/matriz_cierre_pochoco.md) registra el alcance por requisito y el [manifiesto](entrega_final/MANIFIESTO.md) describe el ZIP.
