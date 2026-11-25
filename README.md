# Proyecto 4 — Pochoco Trader

[![Pruebas Proyecto 4](https://github.com/eaponce1/Proyecto_4_Arquitectura/actions/workflows/test-project4.yml/badge.svg)](https://github.com/eaponce1/Proyecto_4_Arquitectura/actions/workflows/test-project4.yml)
[![Informe LaTeX](https://github.com/eaponce1/Proyecto_4_Arquitectura/actions/workflows/render-project4-report.yml/badge.svg)](https://github.com/eaponce1/Proyecto_4_Arquitectura/actions/workflows/render-project4-report.yml)

Agente de negociación para **Go Board Lattice iCE40 HX1K/VQ100**, con decisiones calculadas por **Espino RV32E**. Recibe precios por SPI y responde con compras, ventas o mantener.

**[Informe final PDF](docs/INFORME_FINAL.pdf)** · **[Fuente LaTeX](docs/informe/informe_final.tex)** · **[Ocho gráficos y resultados](resultados_simulacion/informe_ocho_series/INFORME_COMPARATIVO.md)** · **[Guía de simulación](COMO_SIMULAR.md)**

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
5e1579caef1f8de2813b6cf50bb17c505e77b3a534787447d27660eaad63a606
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
| Integración activa | Recuperación de 768 ticks, compra/venta de 48 y netlist en dos fases |
| Corrección SPI | CS de 20/40 ns y distintas fases; compras y ventas en RTL, netlist y BIN reconstruido |
| HX1K/VQ100 | 1.260/1.280 Logic Cells, 9/16 BRAM |
| Relojes | Entrada 25 MHz; Espino 12,5 MHz; timing de enrutado 50,19 MHz |
| Plazo más rápido | Peor caso observado de 25,68 µs; margen conservador 64,58 µs |
| Go Board y maestra reales | Dos `VERIFY OK` y compras/ventas confirmados por el grupo; faltan resultados por ronda |

La política es Momentum32 con trailing stop de 20 puntos, revisión cada ocho ticks, salida con delta <= -16 y reentrada con delta >= +6. Supera a mantener en **6/8 muestras conocidas**; las dos de Netflix pierden frente al benchmark. Peor patrimonio: **$8.615**; máximo drawdown porcentual: **61,11%**. La validación por empresa obtiene ventaja en 5/8 y walk-forward en 14/24 ventanas. **No se demuestra superioridad consistente en series secretas.**

## Compilar y comprobar

Con Python 3, Icarus/VVP y OSS CAD Suite en PATH:

```powershell
python -B tools/trader.py verify
make test
make
```

`make` ensambla, simula, sintetiza y publica `competition.bin` solo tras pasar las comprobaciones. `make prog` programa manualmente y compara la flash. Los logs y las firmas quedan en `build/trader/`.

Para ensamblar explícitamente: `python -B sw/assembler.py sw/trade.s -o sw/trade.hex`.
La referencia Python es `proyecto4/alternativas/competitiva_definitiva/estrategia.py`;
`python -B proyecto4/alternativas/competitiva_definitiva/validar_equivalencia.py`
la compara con RV32E. La configuración congelada está en `resultados/seleccion.json`
dentro de esa alternativa. Herramientas usadas: Python 3.13.3, Icarus 14 de desarrollo,
Verilator 5.020, Yosys 0.70+176 y nextpnr 0.11.1-68; el PDF se compila con
pdfLaTeX de TeX Live 2023.

La [auditoría de entrega](docs/AUDITORIA_ENTREGA.pdf) revisa el PDF contra el
enunciado oficial. El [registro físico](docs/evidencia_fisica/registro_20261125.md)
conserva lo aportado por el grupo. El estudio histórico de hardware está incorporado
en el informe, con procedencia en `docs/evidencia_codisenio/`.

Para repetir la equivalencia completa y las tres cadencias, consultar `proyecto4/alternativas/competitiva_definitiva/ejecutar_pruebas.ps1`. Verilator utiliza Ubuntu WSL, Python, g++ y make. La auditoría de artefactos históricos requiere el historial Git completo o el respaldo local original.

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
| `resultados_simulacion/informe_ocho_series/` | Gráficos, CSV e informes por serie |
| `proyecto4/alternativas/competitiva_definitiva/` | Modelo congelado, datos y validación completa |
| `proyecto4/` | Dependencias de investigación y estrategias de referencia |

Los builds y documentos anteriores se conservan en el **historial Git**; el árbol principal muestra la versión ordenada. Los logs históricos conservan sus rutas originales como evidencia. Los archivos temporales, ejecutables de simulación y auxiliares LaTeX no se publican.

Los workflows de Actions comprueban la imagen actual y recompilan el informe desde LaTeX. Guardan los logs y el PDF generado como artefactos; no programan hardware ni escriben automáticamente en `main`.

El [informe de desarrollo anterior](docs/INFORME_DESARROLLO.md) conserva los recursos de su build de 1.257 LC; para la versión actual usar el PDF principal y `build/trader/validacion.json`.
