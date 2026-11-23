# Auditoría final de entrega — Proyecto 4

**Fecha de revisión:** 22 de noviembre de 2026  
**Fecha límite del enunciado:** 24 de noviembre, 10:00  
**Fuente oficial revisada:** `C:\Users\Edu Ponce\Downloads\Proyecto_4_arq.pdf` (5 páginas).  
**Alcance:** revisión documental y de artefactos. En el cierre posterior se generaron PDF/manifiesto y se actualizaron README/guion; no se modificaron RTL, Assembly, assembler, firmware ni bitstreams.

## Resumen ejecutivo

El proyecto tiene evidencia sólida de implementación y simulación RTL, incluida una reconstrucción aislada del bitstream MMIO base idéntica byte a byte al artefacto entregado. El PDF técnico ya se generó y el manifiesto de entrega apunta a fuentes/evidencia canónicas. **No está listo para afirmar que completó todo el Proyecto 4**: faltan las rondas oficiales 1 y 2, la integración/prueba con la FPGA maestra y resultados de competencia. Tampoco existe metadata Git en el árbol de trabajo revisado, por lo que no se pudo auditar el conjunto rastreado ni probar un `git clone` limpio.

La versión final de competencia es **MMIO SMA10 base**. En la simulación del testbench oficial de ronda 3, software original y MMIO aprobaron 4/4 criterios en 20.000 ticks y produjeron decisiones idénticas. En la Go Board, la demo autónoma de 16 ticks aprobó a 12,5 MHz con flash verificada, LEDs 1010 y 0xAA en tres arranques por COM10.

### Estados

- **Completo:** hay fuente y evidencia reproducible suficiente para el requisito en el alcance indicado.
- **Parcial:** hay implementación/evidencia, pero falta una parte exigida o su validación.
- **Pendiente:** no se encontró evidencia de cumplimiento.

## Checklist contra el enunciado

| # | Requisito del enunciado oficial | Estado | Evidencia / brecha concreta |
|---:|---|---|---|
| 1 | Agente sobre Pochoco SoC y Espino, precio por SPI y decisión compra/venta/mantener | **Completo en RTL y en demo autónoma** | El testbench oficial aprobó en ronda 3. La Go Board aprobó 16 ticks con maestro SPI interno. Queda pendiente la FPGA maestra externa. |
| 2 | Modo SPI 0, byte MSB-first, SCLK ≤1 MHz y niveles 3,3 V/GND común | **Parcial** | RTL/testbench y PCF identifican SPI y las señales. No hay captura de osciloscopio, medición eléctrica ni ensayo con la FPGA maestra. |
| 3 | Desfase: MISO en tick n devuelve la decisión previa, ejecutada al precio n | **Completo en simulación** | `informe_final_proyecto4.md`, `guia_defensa.md`, prueba de equivalencia y validación oficial ronda 3. No se verificó eléctricamente con el maestro real. |
| 4 | Codificación de decisión: acción [7:6], cantidad [5:0], 0–63; reservado se trata como mantener | **Completo en RTL/modelo y pruebas** | Decoder SPI, `trade.s`, documentación del protocolo y testbench. Cantidad del firmware elegido no excede 63. |
| 5 | Caja inicial $10.000, comisión $5, máximo comprable/vendible, sin deuda ni corto | **Completo en simulación de práctica** | Contabilidad oficial conservada en `tb_proyecto_4_profesor.sv`; auditorías Python y resultados. La FPGA maestra real no está disponible para cotejo. |
| 6 | Presupuestos de rondas: 250.000, 25.000 y 2.500 ciclos antes de descontar SPI/sincronización | **Parcial** | Ronda 3 oficial completa: 20.000 ticks, 4/4 para ambas arquitecturas; software peor 413 ciclos y MMIO peor 255, dentro del presupuesto efectivo de la copia TB (2.262 ciclos tras SPI). Rondas 1 y 2 tienen corridas parciales. |
| 7 | Diseñar/explicar algoritmo, validarlo con serie práctica y explicar cantidad q | **Completo para serie práctica** | Código en `proyecto4/python/`, análisis en `resultados/investigacion_final.md` y `documentacion/informe_final_proyecto4.md`. SMA10 usa enteros, ventana de diez precios y q solicitada de 16. |
| 8 | Comparar contra no operar y comprar al inicio/mantener: patrimonio, órdenes, comisiones y drawdown | **Completo para la práctica; resultado activo desfavorable** | Tablas de estrategia y ronda 3 oficial. Oficial ronda 3: no operar $10.000, buy-and-hold $9.695, MMIO/software $4.577; 931 órdenes, $4.655 de comisión, drawdown $5.476. |
| 9 | Implementar `trade.s` para RV32E y describir bucle, registros, memoria y operaciones no soportadas | **Completo** | `proyecto4/alternativas/mmio_sma10/sw/trade.s`, `trade.hex` y `resultados/etapa3_assembly.md`. Se describe historial de diez precios, subset de instrucciones y ausencia de shifts/MUL/DIV. |
| 10 | Igualdad de decisiones Python/Assembly en los 20.000 precios | **Completo según test del intérprete HEX; integración RTL full en ronda 3 comparada entre variantes** | Suite Python incluye `test_hex_igual_a_python_tick_a_tick_en_los_20000_precios`. En la validación oficial de ronda 3 las decisiones software/MMIO coincidieron 20.000/20.000. No debe describirse la prueba del intérprete como una ejecución RTL de 20.000 ticks. |
| 11 | IC, ciclos, CPI y tiempo por tick: promedio/peor; comparar con T | **Parcial** | `rendimiento_software.md`, `mediciones_software.csv` y reporte de co-diseño contienen estadísticas RTL a 30 μs; oficial ronda 3 contiene promedio truncado y peor caso. R1/R2 y sus tiempos oficiales no tienen medición. La tabla final de informe no consolida todas las métricas por variante/ronda. |
| 12 | Perfilar parte costosa, aplicar Amdahl y comparar ≥2 alternativas hardware con LUT/BRAM/Fmax/ciclos/CPI/Ops/s/speedup/roofline | **Completo documentalmente** | Custom-0 y MMIO SMA10 están separados, tienen pruebas y `resultados/co_disenio/informe_codisenio.md`/CSV incluye Ops/s, Amdahl, roofline y métricas. Custom-0 excede HX1K (1350 LC) y no routea; MMIO base routea. El informe PDF incluye estos apartados. |
| 13 | Elegir variante final y justificar balance entre rendimiento, recursos y estrategia | **Completo con riesgo explícito** | Informe final selecciona MMIO SMA10 base como referencia de hardware, no por rentabilidad. Es 1279/1280 LC: queda una sola celda libre. |
| 14 | Competencia en vivo en tres rondas, registro de patrimonio y comparación con buy-and-hold/otros grupos | **Pendiente** | No se dispone de FPGA maestra; no hay resultados de competencia. No se deben usar los resultados de la serie práctica como si fueran puntajes de competencia. |
| 15 | Decisión final calculada por Espino; hardware adicional solo acelera | **Completo en diseño y demo autónoma** | MMIO mantiene la suma/READY; Espino lee y decide con `trade.hex`. El monitor de la Go Board aprobó los 16 ticks con decisiones y MISO verificados. |
| 16 | No usar datos externos ni almacenar otra serie de precios en el diseño | **Completo por inspección del diseño** | Firmware recibe precios SPI y conserva diez muestras de ventana. CSV se utiliza en pruebas, no está precargado en la lógica del bitstream. |
| 17 | Cada hardware agregado en repo con testbench | **Completo en árbol local** | Testbenches de MMIO SMA10, custom-0 y fixture SPI independiente están presentes. En ausencia de Git no se pudo confirmar qué quedaría incluido en el remoto. |
| 18 | README con síntesis/programación, ensamblado, testbenches, referencia Python y versiones de herramientas | **Completo con caveat** | `proyecto4/README.md` cubre comandos y versiones exactas observables. `icepack` no reporta versión por CLI; se documentó su SHA-256 en lugar de inventar una. El README raíz enlaza al específico. `iceprog` está documentado, no ejecutado. |
| 19 | Defensa presencial, todos los integrantes pueden explicar informe/algoritmo/Assembly/RTL | **Parcial** | `guia_defensa.md` y `guion_presentacion.md` incluyen ahora la ronda oficial 3, 20.000 ticks, patrimonio, 931 órdenes, speedup y pendientes. La preparación individual y la defensa presencial no se pueden verificar documentalmente. |
| 20 | Entregables de algoritmo, Assembly, co-diseño como código + PDF | **Completo documentalmente** | Código y documentación Markdown existen; `entrega_final/informe_final_proyecto4.pdf` se genera desde el informe técnico. Falta que cada integrante lo revise y que el PDF/código queden en el checkout GitHub correcto. |

## Validación oficial reportada

Ronda 3 (0,1 ms), testbench oficial y serie de 20.000 ticks:

| Resultado | MMIO SMA10 base | Software original |
|---|---:|---:|
| Criterios oficiales | 4/4 PASS | 4/4 PASS |
| Patrimonio final | $4.577 | $4.577 |
| Órdenes (compras / ventas) | 931 (466 / 465) | 931 (466 / 465) |
| Comisiones | $4.655 | $4.655 |
| Drawdown | $5.476 | $5.476 |
| Ciclos promedio truncado | 60 | 218 |
| Peor caso | 255 | 413 |
| Decisiones diferentes entre variantes | 0/20.000 | 0/20.000 |

La ronda 3 y su 4/4 aparecen en `proyecto4/README.md`, `documentacion/informe_final_proyecto4.md`, `documentacion/guia_defensa.md`, `documentacion/guion_presentacion.md`, `resultados/validacion_oficial/informe_validacion_oficial.md` y `comparacion_oficial.csv`. `informe_comparativo_tres_rondas.md` registra que las corridas de rondas 1 y 2 están incompletas. El guion conserva la distinción entre perfil a 30 μs y validación oficial.

## Firmware y bitstream: trazabilidad comprobada

- El top de programación es `proyecto4/alternativas/mmio_sma10/trade_top.v`; instancia `EnableSpi=1` y carga `proyecto4/alternativas/mmio_sma10/sw/trade.hex`.
- El periférico base está en `alternativas/mmio_sma10/rtl/pochoco_sma10.v` y el wrapper usa su SoC/RTL base; el PCF seleccionado es `goboard.pcf` y el target es HX1K/VQ100 a 25 MHz.
- Regeneré el HEX en `%TEMP%` con `sw/assembler.py` desde `alternativas/mmio_sma10/sw/trade.s`: 71 palabras y SHA-256 idéntico al HEX seleccionado: `B7611ED78166A6E503EB09E4082FDD0C5811118CF08E68DEF32CE1ECD9C77706`.
- Regeneré en una copia temporal aislada Yosys → nextpnr → icepack. Resultado: 1055 LUT4, 1279/1280 LC, 13/16 BRAM, Fmax 40,50 MHz, binario 32.220 bytes. SHA-256 del binario generado y del entregado coincide: `0150BF6FCE608FD463B15EB945F84354B151E581C71A36B47629E889EC0B6DFD`.
- Por tanto, el bitstream **sí corresponde al RTL MMIO SMA10 base y al firmware HEX citado por ese top**, según el flujo reproducible actual. No programé la placa.
- Hay dos imágenes con nombre `trade.hex`: `proyecto4/sw/trade.hex` (software original, 89 palabras) y `alternativas/mmio_sma10/sw/trade.hex` (firmware MMIO, 71 palabras). El bitstream usa la segunda. En comandos/entrega se debe nombrar siempre la ruta completa para evitar cargar la imagen equivocada.

La reconstrucción se efectuó sobre una copia temporal del árbol completo, no sobre un `git clone`: el directorio auditado y su padre no contienen `.git`; `git rev-parse`/`git status` fallan con “not a git repository”. La suite Python en esa copia pasó **32/32**; el HEX recompilado y el bitstream fueron idénticos por hash. Esto comprueba reproducibilidad de los pasos descritos con las fuentes disponibles, pero no verifica que el remoto de GitHub contenga esas fuentes.

Versiones detectadas durante esta auditoría: Python 3.13; Yosys 0.70+176 (`365bb887b`); nextpnr-ice40 0.11.1-68 (`g1daf1f5c`); Icarus 14.0 de desarrollo. Añadir estas versiones concretas o el paquete OSS CAD Suite y versión/build al README, pues el enunciado lo solicita.

## Archivos recomendados para GitHub

No hay `.git` en el árbol de trabajo; esta lista es una recomendación de preparación, no una auditoría de archivos rastreados ni de lo que ya existe en GitHub.

**Incluir como fuente y evidencia de entrega:**

- `README.md`, `proyecto4/README.md`, `proyecto4/documentacion/*.md` y `proyecto4/entrega_final/informe_final_proyecto4.pdf`.
- RTL original de Proyecto 2 y las variantes del Proyecto 4 con sus testbenches y scripts de prueba.
- `proyecto4/python/`, `proyecto4/data/practica_meta.csv`, fuentes `trade.s`, assembler original requerido, y el HEX de la variante seleccionada (`alternativas/mmio_sma10/sw/trade.hex`).
- PCF, `trade_top.v`, script de build y `programacion_fisica/trade_mmio_base.bin` final si el curso espera el binario. Conservar también el HEX porque el script de Yosys usa `$readmemh`.
- Resumen comparativo, métricas y CSV necesarios para respaldar los resultados, especialmente validación oficial de ronda 3 y decisiones por tick.
- Información de toolchain/versiones y comandos reproducibles.

**Excluir de un commit normal o limitar a artefactos de evidencia seleccionados:**

- Ejecutables de simulación (`*.vvp`), configuraciones derivadas temporales del testbench y CSV duplicados en carpetas de corrida.
- Intermedios grandes de P&R (`*.json`, `*.asc`, timing JSON) y logs voluminosos si el repositorio prioriza tamaño. Conservar los logs compactos de síntesis/P&R si se usan como evidencia; en cualquier caso el informe y el comando reproducible deben quedar.
- Resultados exploratorios, curvas/CSV históricos redundantes y binarios de alternativas no seleccionadas, salvo que se etiqueten explícitamente como comparación/experimento.

El `.gitignore` específico de `proyecto4/` solo ignora `/tb_proyecto_4.vvp` y `/decisiones.csv`; **no** cubre de forma general los `*.vvp`, `decisiones.csv` dentro de `resultados/validacion_oficial/corridas/` ni los intermedios `.asc/.json`. Revisar reglas antes de `git add .`. No eliminar artefactos ni resultados históricos en esta auditoría.

## Riesgos para entrega y competencia

1. **Crítico — rondas 1 y 2 pendientes.** No presentar proyecciones como pruebas. La pauta requiere las tres rondas en la competencia; la validación oficial solo cubre la ronda 3 de práctica.
2. **Crítico — integración física con FPGA maestra pendiente.** Sin verificar niveles, frecuencia SPI, tierra común, timing y retorno MISO, el sistema no está listo para una competición conectada.
3. **Crítico — rendimiento financiero de práctica débil.** En ronda 3 el agente activo cerró en $4.577 frente a $9.695 de comprar y mantener y $10.000 de no operar. La serie de práctica no predice la serie oculta, pero tampoco respalda una expectativa de ganar.
4. **Alto — margen HX1K mínimo.** 1279/1280 LC para MMIO base deja solo una celda libre. No agregar lógica ni cambiar constraints sin repetir P&R.
5. **Alto — procedencia GitHub no verificable.** No existe `.git` local y hay copias anidadas del Proyecto 2 en el directorio de descarga. Solo el directorio canónico `pochoco_soc-main` contiene esta versión; no subir por error la carpeta duplicada/archivo de descarga como fuente competidora.
6. **Medio — icepack no publica versión.** El README deja constancia y fija el ejecutable por hash; si se usa otro entorno, registrar su hash o paquete de distribución.
7. **Medio — regresión heredada no completamente verde.** `tests/run_tests.py` mantiene el fallo documentado `periph_tb` de expectativa de polaridad de botones. Reportarlo como issue de base, no ocultarlo ni atribuirlo a los cambios de P4.

## Correcciones recomendadas por prioridad

1. Confirmar que se usará el checkout Git correcto, verificar `git status`, rama/remoto y que los artefactos requeridos están versionados; revisar el diff antes de cualquier commit.
2. Verificar PDF y fuentes desde el checkout Git correcto y confirmar que ambos están dentro de la entrega.
3. Completar rondas oficiales 1 y 2 cuando el entorno de simulación lo permita con 20.000 ticks y los mismos cuatro checks; después hacer integración física con la FPGA maestra y conservar evidencia.
4. Preparar la defensa con la comparación honesta contra las referencias: MMIO mejora cómputo, no rentabilidad; no afirmar ganancia esperada en la serie oculta.
5. Revisar el conjunto de subida según la lista anterior y las reglas de `.gitignore` antes de staging, sin borrar evidencia que se decida conservar.

**Conclusión.** Reproducibilidad local de firmware y bitstream confirmada con la suite 32/32 y hashes idénticos en copia temporal. Ronda oficial 3 completa y demo autónoma física aprobada. El informe PDF, la guía y el ZIP contienen la evidencia. Restan las rondas 1 y 2 completas y la integración con la FPGA maestra para competencia.
