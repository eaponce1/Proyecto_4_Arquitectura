# Proyecto 4 — Pochoco Trader

[![Pruebas Proyecto 4](https://github.com/eaponce1/Proyecto_4_Arquitectura/actions/workflows/test-project4.yml/badge.svg)](https://github.com/eaponce1/Proyecto_4_Arquitectura/actions/workflows/test-project4.yml)
[![Informe LaTeX](https://github.com/eaponce1/Proyecto_4_Arquitectura/actions/workflows/render-project4-report.yml/badge.svg)](https://github.com/eaponce1/Proyecto_4_Arquitectura/actions/workflows/render-project4-report.yml)

Agente de negociación para **Go Board Lattice iCE40 HX1K/VQ100**, con decisiones calculadas por **Espino RV32E**. Recibe precios por SPI y responde con compras, ventas o mantener.

**[Informe final PDF](docs/INFORME_FINAL.pdf)** · **[Fuente LaTeX](docs/informe/informe_final.tex)** · **[Ocho gráficos y resultados](resultados_simulacion/informe_tendencia_lenta/INFORME_COMPARATIVO.md)** · **[Guía de simulación](COMO_SIMULAR.md)**

## Programar la FPGA

El archivo vigente es **[`competition.bin`](competition.bin)**, en la raíz de este repositorio. No necesitas volver a compilar para programarlo. Desde esta carpeta, con la Go Board conectada por USB y OSS CAD Suite disponible:

```powershell
iceprog competition.bin
iceprog -c competition.bin
```

También puedes ejecutar el script que verifica fuentes y hashes antes de escribir y comparar la flash:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\programar.ps1
```

Agrega `-SoloVerificar` para comprobar los archivos sin acceder a la placa.

Después de programar, reinicia la Go Board, espera D1 e inicia una serie nueva
desde la maestra. Los LED quedan encendidos como registro: D1 CPU arrancó,
D2 precio recibido, D3 precio leído y D4 orden distinta de cero.

Esta versión corrige un bloqueo del receptor con CS poco antes del primer SCLK:
se perdía el primer bit y no se recibía ningún precio. La prueba corta se repite con
`python -B tools/trader.py spi`. La evidencia y el diagnóstico están en
[Corrección de ausencia de órdenes](docs/CORRECCION_SIN_ORDENES.md).

BIN SHA-256:

```text
1f514301f1a7300351f4d3d8f48b77c2c85dcd2a274f44910d11d00df406db45
```

El top activo es `rtl/trade_spi_externo.v`, el firmware está en `sw/trade.s` / `sw/trade.hex` y las restricciones están en `goboard_trader.pcf`. El Makefile compila Trader. No ejecuta el juego de versiones anteriores.

## Simular y observar

Instala la dependencia gráfica una vez (Tkinter viene con el instalador habitual de Python para Windows):

```powershell
python -m pip install -r requirements.txt
```

```powershell
python simular_competencia.py
```

El visor permite elegir AMD, Apple, Meta, Netflix o Tesla, pausar, avanzar un tick y exportar informes. Para generar las ocho series sin ventana:

```powershell
python simular_competencia.py --todas --sin-ventana
```

Cada ejecución guarda PNG/SVG, CSV de ticks, operaciones y resumen con hashes. La animación reproduce una traza precalculada del modelo; **no es telemetría de la placa**. Las trazas RTL anteriores, cuando están disponibles, se cotejan con el modelo antes de exportar.

## Validación y límites

| Validación | Evidencia |
|---|---|
| Ocho series conocidas | 160.000 ticks Python/RV32E/RTL, sin diferencias |
| SPI y contabilidad | Escenarios Icarus, límites de inventario y comisiones |
| Bancos oficiales | Dos bancos adaptados al top final, 4/4 y 2.000 ticks cada uno; diffs conservados |
| Integración activa | Recuperación de 768 ticks; compra/venta de 396; netlist y BIN en tres separaciones de CS |
| Corrección SPI | CS de 20/40 ns y distintas fases; compras y ventas en RTL, netlist y BIN reconstruido |
| HX1K/VQ100 | 1.219/1.280 Logic Cells, 9/16 BRAM |
| Relojes | Entrada 25 MHz; Espino 12,5 MHz; timing de enrutado 50,67 MHz |
| Plazo más rápido | Peor caso observado de 21,04 µs incluyendo estrés; margen conservador 69,22 µs |
| Go Board y maestra reales | Pendiente para esta imagen. Los dos `VERIFY OK` y compras/ventas previos corresponden al respaldo Momentum32 |

La política activa es **tendencia lenta: SUM10, revisión cada 128 ticks y umbral de ±5%**. Empieza en caja; actualiza el ancla en cada revisión. Compra hasta 63 acciones; las compras adicionales requieren al menos ocho. Vende en régimen bajista. La primera compra posible se ejecuta en el **tick 257**, contando desde cero. Puede permanecer sin operar si no hay señal; D1/D2/D3 encendidos y D4 apagado puede ser correcto.

Supera a mantener en **5/8 series conocidas**, con patrimonio medio **$10.971,13**, peor resultado **$8.540** y drawdown máximo **50,55%**. Momentum32 anterior obtenía 6/8 y media $12.725. Mejora Netflix y empeora otros casos: **no se demuestra superioridad general ni se garantiza ganar la competencia**. [Comparación y reglas](proyecto4/alternativas/tendencia_lenta/README.md).

Las ocho series RTL completas se probaron a 100 µs; a 1 ms y 10 ms se probó integración de 396 ticks por cadencia. La evidencia física anterior no se atribuye a este BIN nuevo.

## Compilar y comprobar

Con Python 3, Icarus/VVP y OSS CAD Suite en PATH:

```powershell
python -B tools/trader.py verify
make test
make
```

`make` ensambla, simula, sintetiza y publica `competition.bin` solo tras pasar las comprobaciones. `make prog` programa manualmente y compara la flash. Los logs y las firmas quedan en `build/trader/`.

La referencia Python activa es `proyecto4/alternativas/tendencia_lenta/modelo_lento.py`. Para repetir sus comprobaciones:

```powershell
python -B proyecto4/alternativas/tendencia_lenta/test_invariantes.py
python -B proyecto4/alternativas/tendencia_lenta/validar_equivalencia.py
python -B tools/validar_oficial.py
wsl.exe -d Ubuntu -- bash tools/validar_activo_wsl.sh
```

Para reconstruir desde cero, repetir equivalencia y RTL antes de `make`; la publicación exige evidencia de las ocho series y bancos oficiales ligada a las fuentes. Windows usa OSS CAD Suite y Ubuntu WSL con Python, g++ y make para las simulaciones de puertas. La síntesis requiere Yosys, nextpnr, icepack e icebox_vlog. El build no programa la placa.

El HEX se compara por palabras tras reensamblar en un archivo temporal; se conservan los bytes originales LF. No sobrescribir `sw/trade.hex` con una copia CRLF sin reconstruir y validar su manifiesto.

La [auditoría de entrega](docs/AUDITORIA_ENTREGA.pdf) distingue comprobaciones digitales y pendientes reales. El [registro físico anterior](docs/evidencia_fisica/registro_20261125.md) solo aplica a Momentum32. El respaldo local completo está en `respaldos/momentum32_fisico_5e1579ca/`; puede recuperarse la versión publicada anterior desde el commit `07d0dd95d491f7b7f08a6f1b813d998e53a8c123`.

## Conectar la maestra

| Señal | PMOD según documentación del proyecto | Pin FPGA |
|---|---|---:|
| CS_n | PS1 | 65 |
| MOSI desde maestra | PS2 | 64 |
| MISO hacia maestra | PS3 | 63 |
| SCLK | PS4 | 62 |

Confirmar físicamente el conector con el PCF. SPI modo 0, ocho bits MSB primero, hasta 1 MHz, señales de 3,3 V y GND común. La Go Board se alimenta por USB y el VCC del PMOD queda libre. Reiniciar antes de cada serie y esperar D1 antes de iniciar la maestra. Los LED indican actividad; el patrimonio lo calcula la maestra a partir de precios y MISO.

## Organización

| Ruta | Contenido |
|---|---|
| `competition.bin`, `competition.sha256` | Imagen activa y hash |
| `rtl/`, `sw/` | Hardware y firmware activos |
| `tools/`, `Makefile`, `programar.ps1` | Compilación y programación |
| `tb/`, `tests/` | Banco oficial y modelo auxiliar de RAM |
| `build/trader/` | Evidencia de la integración activa |
| `docs/INFORME_FINAL.pdf` | Informe principal, compilado desde LaTeX |
| `docs/informe/` | Fuentes, tablas y figuras del informe |
| `resultados_simulacion/informe_tendencia_lenta/` | Ocho gráficos e informes de la política activa |
| `proyecto4/alternativas/tendencia_lenta/` | Modelo activo, Assembly, procedencia y equivalencia |
| `proyecto4/alternativas/competitiva_definitiva/` | Momentum32 anterior, datos compartidos y evidencia histórica |
| `proyecto4/` | Dependencias de investigación y estrategias de referencia |

Los builds y documentos anteriores se conservan en el **historial Git**; el árbol principal muestra la versión ordenada. Los logs históricos conservan sus rutas originales como evidencia. Los archivos temporales, ejecutables de simulación y auxiliares LaTeX no se publican.

Los workflows de Actions comprueban la imagen actual y recompilan el informe desde LaTeX. Guardan los logs y el PDF generado como artefactos; no programan hardware ni escriben automáticamente en `main`.

El [informe de desarrollo anterior](docs/INFORME_DESARROLLO.md) conserva los recursos de su build de 1.257 LC; para la versión actual usar el PDF principal y `build/trader/validacion.json`.
