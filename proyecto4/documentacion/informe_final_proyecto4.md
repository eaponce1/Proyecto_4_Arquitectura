# Informe final del Proyecto 4 — Arquitectura de Computadores

## Alcance y criterio de evidencia

Este documento reúne la implementación, validación y límites del trabajo de Proyecto 4 contenido en este repositorio. Las cifras se contrastaron con los CSV y reportes citados en cada sección. «Medido» significa que existe una ejecución de simulación/síntesis registrada; no significa que se midió sobre la Go Board. No se atribuye una comprobación física sin registro de esa comprobación.

La versión usada como referencia de co-diseño es MMIO SMA10 base. Las variantes custom-0 y MMIO optimizada permanecen aisladas. La verificación del modo interno SPI es un fixture de prueba independiente y no reemplaza el diseño comercial/de inversión.

## 1. Estructura y componentes principales

| Ruta | Contenido / función |
|---|---|
| `proyecto4/python/` | Estrategias de referencia, simulador contable, pruebas, comparador, medición y síntesis. |
| `proyecto4/data/practica_meta.csv` | Serie de 20.000 precios. |
| `proyecto4/sw/` | `trade.s`, imagen `trade.hex` y herramientas de software del Proyecto 4. |
| `proyecto4/rtl/`, `tb/` | Wrapper/testbench integrador del Proyecto 4. |
| `proyecto4/alternativas/custom0/` | Opcode custom-0, assembler, firmware, bancos y medición aislados. No cabe en HX1K. |
| `proyecto4/alternativas/mmio_sma10/` | Periférico SMA10 base y wrapper con SPI habilitado; referencia seleccionada para hardware. |
| `proyecto4/alternativas/mmio_sma10_opt/` | Optimización experimental, funcionalmente equivalente, con pequeña reducción de LC. |
| `proyecto4/referencia/` | Snapshot/hashes del RTL original y referencias de medición. |
| `proyecto4/pruebas_fisicas/spi_slave/` | Prueba SPI independiente; `internal/` conecta maestro y slave dentro del FPGA. |
| `proyecto4/pruebas_fisicas/agente_completo/` | Integración diagnóstica con generador SPI y verificador internos; simulada, no implementable en HX1K por exceso de LC. |
| `proyecto4/programacion_fisica/` | PCF, scripts, logs y bitstream de MMIO base. El script genera; no programa. |
| `proyecto4/resultados/` | CSV tick a tick, comparaciones, gráficas e informes de estrategia, rendimiento y síntesis. |

El software de la variante se debe ensamblar con el assembler ubicado junto a esa variante cuando corresponda. El wrapper genérico `proyecto4/rtl/trade_top.v` y el wrapper `alternativas/mmio_sma10/trade_top.v` no apuntan a la misma imagen; para generar el bitstream base se usa el último.

## 2. Estrategia Python, contabilidad y causalidad

La investigación evaluó no operar, comprar y mantener y estrategias activas. La estrategia SMA10 de referencia espera diez observaciones, mantiene una suma de los últimos diez precios y evita dividir: calcula `10*p` como `8*p + 2*p`. Sin posición compra una orden solicitada de 16 acciones cuando `10*p <= suma10-10`; con posición vende hasta 16 cuando `10*p >= suma10+10`; en otro caso mantiene. La cantidad real se limita por caja, acciones disponibles y codificación de seis bits (máximo 63). Caja inicial: $10.000; comisión: $5 por orden ejecutada; no hay deuda ni corto.

El modelo SPI conserva el orden causal: en tick n se ejecuta al precio actual la decisión recibida, calculada anteriormente; luego se incorpora el precio y se calcula la decisión para el tick siguiente. La comparación no aplica una señal al mismo precio que la generó. Las pruebas de contabilidad verifican caja/acciones no negativas, comisiones por fills, patrimonio `caja + acciones*precio` y desfase.

En la auditoría previa, el drawdown absoluto de $10.152 se reprodujo desde un peak de $10.254 hasta un valle de $102. El drawdown en dólares puede exceder el capital inicial porque su referencia es el máximo histórico, sin que exista deuda. Ese número pertenece a la estrategia SMA5/10+momentum original de la etapa Python y no a la estrategia SMA10 ensamblada.

La investigación final concluyó que ninguna estrategia activa probada era apropiada para recomendar por rentabilidad robusta en esta serie; no operar es la referencia prudente. El firmware SMA10 se eligió para estudiar equivalencia y aceleración, no como promesa de retorno. Ver `resultados/investigacion_final.md`, `resultados/comparacion_final.csv` y `resultados/analisis_estrategias.md`.

## 3. Firmware Assembly y protocolo SPI

`proyecto4/sw/trade.s` reproduce la función `estrategia_reversion_media` documentada en `resultados/etapa3_assembly.md`. Usa diez palabras de RAM como anillo de precios, espera `STATUS`, lee `PRICE`, actualiza cartera local y la suma, forma la señal SMA10 con sumas/restas y escribe `DECISION`. La zona de historial empieza en palabra RAM 500, fuera de la imagen de 89 palabras. El ensamblador genera `proyecto4/sw/trade.hex`.

Direcciones comprobadas en el RTL (no inferidas): SPI base `0x80010000`; STATUS `+0`, PRICE `+4`, DECISION `+8`. En la variante MMIO, SUM10 es `+0xC` y READY `+0x10`. El decode SoC habilita SPI cuando corresponden los bits altos de la dirección y el wrapper MMIO configura `EnableSpi=1`.

La decisión se escribe después de leer y consumir el precio del tick; el slave captura `tx_hold` al comienzo de la próxima transacción, por lo que MISO devuelve la decisión pendiente anterior. En el modo de prueba física interna se probaron cinco transacciones, incluidos STATUS, PRICE, DECISION y MISO con ese desfase.

El Espino es RV32E, con x0–x15. La implementación usa el subset admitido: `lui`, `addi`, `lw`, `sw`, `andi`, `add`, `sub`, branches (`beq`, `bne`, `bge`) y `jal`. No usa shifts, MUL/DIV ni instrucciones de sistema. El decoder no admite actualmente las instrucciones de shift aun cuando existan códigos internos relacionados; no hay extensión M. Consultar `proyecto4/sw/trade.s` y `proyecto4/alternativas/mmio_sma10/rtl/` para el RTL empleado.

## 4. Rendimiento de software original

La medición RTL original procesa 20.000 ticks a 30 μs entre transacciones, con reloj de simulación de 25 MHz. IC se contó externamente en el commit (`instr_valid_id && !stall`), sin añadir contador al core. La ventana de cálculo va de `byte_done` a la escritura de DECISION; el polling/espera posterior se presenta aparte. Es una medición de simulación RTL, no una lectura de osciloscopio ni una corrida física.

| Medida por tick | Promedio | Mediana | P95 | Peor caso |
|---|---:|---:|---:|---:|
| IC | 91,917 | 88 | 91 | 174 |
| Ciclos respuesta precio→DECISION | 218,664 | 210 | 217 | 412 |
| CPI | 2,379 | 2,382 | 2,402 | 2,409 |
| Tiempo respuesta | 8,75 μs | 8,40 μs | 8,68 μs | 16,48 μs |

El cálculo posterior a PRICE promedia 206 ciclos; la suma SMA10 domina con 163,9 ciclos. La cartera varía y llega a 208 ciclos en el peor evento observado. A 30 μs se procesaron 20.000 ticks sin discrepancias ni pérdidas. Aunque el reporte compara sus peores respuestas con los presupuestos de las tres rondas, solo ejecutó una cadencia personalizada de 30 μs; las rondas oficiales no se corrieron individualmente en ese experimento.

Fuente: `resultados/rendimiento_software.md`, `resultados/mediciones_software.csv`, `resultados/rendimiento_software.svg`.

## 5. Co-diseño y cifras comparativas

Una operación útil se define como un tick procesado: consumir el precio recibido y dejar escrita a tiempo la decisión para el tick posterior. Speedup medido = ciclos medios software original / ciclos medios variante. No se mezcla con speedup de frecuencia o predicción Amdahl.

| Variante | IC media | Ciclos media | CPI | Peor ciclos | Speedup ciclos | LUT4 | LC / 1280 | BRAM / 16 | Fmax routeada | Estado HX1K |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| Software original | 91,917 | 218,664 | 2,379 | 412 | 1,000× | 980 | 1200 | 12 | 42,6 MHz | PASS |
| custom-0 | 30,945 | 70,734 | 2,286 | 266 | 3,091× | 1133 | 1350 | 14 | No routeada | FAIL: excede 70 LC |
| MMIO SMA10 base | 26,848 | 60,640 | 2,259 | 255 | 3,606× | 1055 | 1279 | 13 | 40,50 MHz | PASS @25 MHz |
| MMIO SMA10 optimizada | 26,848 | 60,640 | 2,259 | 255 | 3,606× | 1051 | 1274 | 13 | 42,33 MHz | PASS @25 MHz |

Las primeras tres filas provienen de `resultados/co_disenio/comparacion_codisenio.csv`; la fila optimizada, de `resultados/mmio_optimizacion/comparacion_mmio_sma10.csv`. Las mediciones de actividad cubren 20.000 ticks; perfil de kernel/Amdahl de algunas variantes usa 100 ticks. MMIO base reduce ciclos 3,606× y sí enruta, aunque queda una LC libre. MMIO optimizada libera cinco LC adicionales respecto de base y sube Fmax; no alcanza el objetivo de 1.150–1.200 LC y deja solo seis LC libres. No se deben tratar esos seis como margen cómodo.

La alternativa custom-0 agrega una instrucción `rd <- rd - outgoing + incoming`, pero el netlist consume 1350/1280 LC y no completa P&R. El periférico MMIO mantiene el anillo/SMA; Espino sigue decidiendo. Es la única alternativa acelerada de la tabla que completó P&R HX1K con el rendimiento y equivalencia reportados.

### Amdahl y roofline

El análisis Amdahl usa `P=0,8535`: el kernel de actualización de historial, SMA y señal ocupa 186,62/218,66 ciclos en baseline. `S = 1 / ((1-P)+P/S_local)`. Predicción: custom-0 3,076×; MMIO base 3,692×. Son predicciones calculadas con perfil de 100 ticks, distintas de speedup medido de 3,091× y 3,606×. No se inventa predicción para MMIO optimizada: su reporte demuestra ciclos globales iguales a base, pero no publica una medición independiente del perfil/Amdahl.

El roofline es un modelo, no una medida de ancho de banda: una operación útil se cuenta como suma/resta entera del kernel; supone un byte SPI por tick, un puerto BRAM iCE40 de 16 bits a 25 MHz (50 MB/s) y pico del core de una operación por ciclo a 25 MHz (25 Mops/s). Excluye ramas, polling y control. Intensidad estimada: software 0,341 ops/B; custom-0 1,2; MMIO 0,545. Bajo esos supuestos, el original cae bajo el techo de memoria del modelo y las variantes aceleradas se aproximan/limitan por cómputo. No es un roofline de memoria externa ni instrumentación de tráfico real.

## 6. Optimización MMIO

La variante optimizada sustituye el contador saturante de cuatro bits por `ready_q`, activado al aceptar el décimo precio cuando el puntero llega a slot 9. Conserva el anillo BRAM, la suma, el instante de captura, el mapa MMIO, protocolo SPI, contabilidad y Espino. Test autónomo e integrado compararon 20.000 precios/decisiones.

Resultado: 5 LC menos (1279→1274, reducción aproximada 0,39%), LUT4 1055→1051, BRAM sin cambio (13), ciclos iguales, Fmax 40,50→42,33 MHz. El objetivo de área 1.150–1.200 LC no se alcanzó. La versión base sigue intacta como referencia; la optimizada es experimental.

## 7. Programación física y prueba independiente

El build registrado para MMIO base usa `trade_top` bajo `alternativas/mmio_sma10`, `EnableSpi=1`, la imagen de esa misma variante y HX1K/VQ100, PCF `goboard.pcf`, objetivo de 25 MHz. El resultado empaquetado es `programacion_fisica/trade_mmio_base.bin` (32.220 bytes). Logs Yosys/nextpnr registran 1055 LUT4, 1279/1280 LC, 13/16 BRAM y Fmax 40,50 MHz. Se trata de síntesis, place-and-route e icepack.

El registro de build acredita el bitstream SPI externo. El usuario informó la programación de esa imagen. La ejecución de competencia junto a la FPGA maestra sigue pendiente. La confirmación física de la demo con maestro interno consta en la sección de cierre.

El fixture `pruebas_fisicas/spi_slave/internal/` conecta internamente maestro y slave, sin jumpers. Su TB simulado aprobó cinco tramas; el build HX1K/VQ100 reporta 161 LUT4, 220 LC, cero BRAM, Fmax 146,43 MHz y binario independiente de 32.220 bytes. Sus LEDs PASS/DONE se verificaron en simulación. No se ha programado ni ejecutado este fixture físicamente; además valida el SPI slave aislado, no el SoC completo con Espino y el agente de inversión.

### Integración RTL del agente completo

Se creó una variante de diagnóstico independiente en `proyecto4/pruebas_fisicas/agente_completo/`. Conecta un maestro SPI interno de **solo precios** al SPI Slave de la arquitectura MMIO SMA10 base. `trade.hex` es cargado por la RAM y ejecutado por el Espino Core original en el SoC RTL; el generador no escribe DECISION ni calcula operaciones. El testbench observa fetch y commit del core y los accesos al bus MMIO.

La secuencia contiene 16 ticks (`200` diez veces, `90` tres veces y `220` tres veces), suficiente para llenar SMA10 y provocar una compra y una venta. La simulación verificó reset, 94.156 fetches, 70.652 commits, 23.410 lecturas STATUS, 16 lecturas PRICE, 16 lecturas SUM10, 16 lecturas READY y **16 escrituras DECISION**. Los bytes escritos desde el bus del Espino coincidieron tick a tick con las salidas Python. El verificador recibió **16/16 respuestas MISO correctas** frente al vector Python, preservando el desfase: una decisión escrita tras un precio se devuelve en la transacción siguiente. El test también comprueba que no quede un precio anterior sin consumir.

Estos datos son evidencia de **simulación RTL**, no de ejecución/programación física. El test usa el SoC completo y el firmware real `trade.hex` en RTL; no usa la FPGA maestra del curso.

La **síntesis** de esta variante de diagnóstico se ejecutó para HX1K/VQ100 con Yosys y nextpnr. Yosys informó 1.295 LUT4; nextpnr estimó **1.550/1.280 LC (121%)** y 13/16 BRAM, y falló al ubicar las celdas. No se obtuvo Fmax ni se generó un bitstream de esta variante. El exceso corresponde a la lógica añadida de prueba —generador SPI, tabla de precios, verificador, tabla de respuestas y control/indicadores—, no al diseño MMIO SMA10 base. Los taps de observación son salidas de señales que ya existen en el SoC; los bloques MMIO base se compilaron desde su RTL original. La referencia MMIO base conserva sus métricas registradas: 1.055 LUT4, 1.279/1.280 LC, 13/16 BRAM y Fmax de 40,50 MHz.

La **prueba física** del agente completo no se ejecutó: no hay bitstream de diagnóstico que pueda programarse, y no se programó la placa durante esta validación. El bitstream de referencia MMIO SMA10 base no se sobrescribió. Por tanto, se mantiene **MMIO SMA10 base** como arquitectura final; el fixture de agente completo es solo evidencia de integración RTL y queda pendiente una solución de área antes de cualquier demostración física.

Pines de interfaz de la configuración MMIO base, extraídos del PCF/reportes locales: reloj onboard 25 MHz pin 15; SPI SCLK pin 62/PMOD PS4; MOSI pin 64/PS2; MISO pin 63/PS3; CS_n pin 65/PS1. La prueba interna no necesita jumpers; sus señales opcionales de sonda se exponen en PS7–PS10. Alimentación PMOD es 3,3 V/GND y no es GPIO. Consultar los PCF e informes antes de cablear hardware externo.

Comandos manuales de referencia desde la raíz `pochoco_soc-main`:

```powershell
python proyecto4/programacion_fisica/generar_bitstream.py
iceprog proyecto4/programacion_fisica/trade_mmio_base.bin
```

El segundo comando programa la placa y no se ejecutó durante la documentación. Para la prueba interna, consulte `pruebas_fisicas/spi_slave/internal/README.md`; su script produce un archivo distinto y tampoco programa.

## 8. Pruebas y estado de regresión

Ejecutadas al cerrar esta documentación: `python -B -m unittest discover -s proyecto4/python -v` — **32 pruebas, todas aprobadas**, incluyendo auditoría contable, causalidad, reglas, equivalencia de HEX en 20.000 precios, caso de fills parciales e integración RTL SPI. La integración RTL completa de rendimiento de las variantes base/MMIO/custom está además respaldada por los CSV/reportes de co-diseño.

La suite heredada de Proyecto 2 no queda verde completa: los reportes previos documentan `periph_tb` fallando en `debounced buttons` por expectativa antigua de polaridad, mientras `core_tb`, `spi_tb` y `decoder_tb` pasan por separado y game_top compila. Esta condición es ajena a los cambios documentados de Proyecto 4; no se corrigió aquí. Para volver a comprobar:

```powershell
python -B -m unittest discover -s proyecto4/python -v
python -B -m unittest proyecto4.alternativas.custom0.tb.test_assembler_custom0 -v
python -B tests/run_tests.py
```

El estado del segundo comando se registró aprobado (3 pruebas) en el informe de co-diseño. El tercero conserva el fallo conocido de `periph_tb`.

## 9. Validación oficial del profesor - ronda 3

Se ejecutó el testbench oficial sin cambiar su contabilidad ni sus cuatro condiciones. Se conserva su copia original y el CSV de 20.000 ticks en `resultados/validacion_oficial/`. Para cada arquitectura se generó una copia de ejecución que solo configura las rutas, habilita SPI y usa la ronda/longitud solicitadas. Ambas arquitecturas aprobaron **4/4 criterios**.

| Métrica oficial, 20.000 ticks | MMIO SMA10 base | Software original |
|---|---:|---:|
| Criterios aprobados | 4/4 | 4/4 |
| Patrimonio final | $4.577 | $4.577 |
| Órdenes ejecutadas | 931 | 931 |
| Compras / ventas | 466 / 465 | 466 / 465 |
| Comisiones | $4.655 | $4.655 |
| Drawdown máximo | $5.476 | $5.476 |
| Ciclos promedio, entero truncado por el TB | 60 | 218 |
| Peor caso medido | 255 ciclos | 413 ciclos |
| Decisiones diferentes entre arquitecturas | 0/20.000 | 0/20.000 |

Los promedios son los enteros truncados que produjo la instrumentación de esa corrida, no valores decimales exactos. MMIO reduce el costo computacional; **no altera la estrategia, la secuencia de decisiones ni el resultado financiero**. La referencia del mismo testbench fue no operar = $10.000 y comprar y mantener = $9.695, por lo que este resultado activo no implica rentabilidad positiva.

La versión publicada del testbench comprueba MISO sin X, que existan escrituras DECISION, que no queden precios sin consumir y que la respuesta llegue dentro del presupuesto. Ambas arquitecturas aprobaron los cuatro checks. Sus decisiones transmitidas coinciden exactamente tick a tick en los 20.000 ticks. Los artefactos y logs están en `resultados/validacion_oficial/informe_validacion_oficial.md`, `comparacion_oficial.csv` y `decisiones.csv`.

### Validación de las tres rondas con la serie de práctica

Se completaron 20.000 ticks y 4/4 criterios en cada arquitectura y cada ronda. Para los periodos de 10 ms y 1 ms se usó Icarus de cuatro estados con espera verificada. El ejecutor comprueba que el SoC repita su estado entre tramas, conserva el tiempo entre precios y simula las transacciones SPI y los cuatro criterios.

| Ronda | MMIO promedio / peor (ciclos) | Software promedio / peor (ciclos) | Presupuesto efectivo (ciclos) |
|---|---:|---:|---:|
| 1 | 60,66 / 254 | 218,67 / 413 | 249.762 |
| 2 | 60,66 / 254 | 218,67 / 413 | 24.762 |
| 3 | 60 / 255 | 218 / 413 | 2.262 |

Los promedios de ronda 3 conservan el truncamiento de la corrida histórica. Las seis corridas conservaron el patrimonio de $4.577, las 931 órdenes, las comisiones de $4.655 y el drawdown de $5.476. Cotejamos las 20.000 decisiones de cada corrida con la referencia. Los logs, resultados completos y tiempos de Icarus están en `resultados/validacion_oficial/`. La integración física con la FPGA maestra sigue pendiente.

## 10. Pendientes y conclusión técnica

1. Probar las conexiones SPI externas y la ejecución física del diseño de competencia con la FPGA maestra.
2. Revisar el margen de implementación si cambia la configuración. MMIO base tiene una LC libre y la variante optimizada mejora cinco LC.
3. Medir el resultado de la competencia. En la serie histórica, no operar obtuvo mayor patrimonio final que la estrategia activa.

**MMIO SMA10 base es la arquitectura final de competencia.** Conserva la decisión final en Espino, pasó P&R y cuenta con comparación oficial de 20.000 ticks. La demo autónoma independiente completó en placa su secuencia de 16 ticks con maestro SPI interno.

## Estado de entrega verificado el 23 de noviembre de 2026

Se verificó que el testbench y el CSV adjuntos coinciden byte a byte con sus copias oficiales del repositorio. SHA-256 del testbench F83486755FE2B3DE385A2BDC39C2F275B9DD690342FB4FC0391401706876F8F3. SHA-256 del CSV FED122E0A9861276D76B1396B264FD34077C280C80FE6B356B6971D55242DA3F. Se revisaron las cinco páginas del enunciado.

La imagen SPI externa MMIO SMA10 base es trade_mmio_base.bin, SHA-256 0150BF6FCE608FD463B15EB945F84354B151E581C71A36B47629E889EC0B6DFD. Ocupa 1.279 LC, 1.055 LUT4 y 13 BRAM. Fmax post-route de 40,50 MHz. La imagen solo se acredita con simulación e implementación y no hay una corrida física con FPGA maestra.

La demostración autónoma mantiene el generador SPI de 16 precios, el Espino ejecutando el firmware y el verificador de DECISION y MISO. En Icarus aprobó los 16 ticks y 15 ACK. En placa, el capturador del primer commit dio 0101. El diagnóstico posterior registró WAIT_ACK en el primer tick y una instrucción nula en PC 0x1C, cuya palabra esperada en `trade.hex` es 0xFE010CE3. Tras verificarse manualmente la flash, las imágenes integrales con habilitación RE y con entradas de BRAM registradas volvieron a mostrar 1111, correspondiente al watchdog.

La imagen independiente `selftest_fetch_rom.bin` implementa la memoria de instrucciones de la demo en LUTs. Usa las 71 palabras de `trade.hex` y un PC de siete bits de dirección de palabra, con 22 transferencias de control verificadas dentro del firmware. En Icarus aprobó 36.914 pares PC/instrucción y los 16 ticks frente a Python. La simulación del netlist alcanzó 1010. El enrutado utiliza 1.234/1.280 LC, 1.096 LUT4 y 7 BRAM con Fmax de 43,94 MHz. En placa se observó 1111 con la flash verificada mediante `iceprog -c`. La arquitectura de competencia es MMIO SMA10 base con SPI externo.

La revisión autónoma `selftest_fetch_rom_lento.bin` usa la misma ROM, reset registrado y un reloj de 12,5 MHz nominal para el SoC. El oscilador de placa de 25 MHz mantiene la UART de confirmación. Las simulaciones RTL y del netlist completaron los 16 ticks. El enrutado ocupa 1.270/1.280 LC, 1.122 LUT4 y 7 BRAM, con Fmax de 44,29 MHz para la red del SoC bajo la restricción de 25 MHz.

**La demo autónoma obtuvo PASS físico en la Go Board.** Se observaron D2 y D4 encendidos y D1 y D3 apagados, código 1010. La verificación de solo lectura de la flash devolvió `VERIFY OK`. Tres arranques devolvieron `AUTOTEST LED=1010 UART=0xAA RESULT=PASS` por COM10. El código confirma que se completó la comprobación integral de los 16 ticks con maestro interno. El BIN validado tiene SHA-256 `0CCD156590DAECF3F9C3E6031E7E987B0CE6A0795BB801A9672C88CCC91FB9CC`. El ZIP conserva los registros de flash y UART.

El ZIP incluye las seis corridas de práctica completas, el código de la espera verificada, los contrastes con Icarus directo y `comparacion_tres_rondas.csv`. Las pruebas de práctica usan la serie publicada. El resultado de las series ocultas corresponde a la competencia en vivo.

La entrega incluye las dos alternativas de co-diseño, código y bancos de prueba, tablas de IC, CPI, ciclos, tiempo, recursos y roofline, el PDF y la guía de defensa. La matriz de cierre identifica la evidencia por requisito. La demostración física con la maestra y la defensa presencial siguen pendientes.

## 11. Investigación posterior al plazo (25 de noviembre de 2026)

Esta sección incorpora evidencia publicada después del plazo de entrega del 24 de noviembre. Las variantes se mantienen como investigación posterior y no reemplazan la arquitectura MMIO SMA10 base seleccionada para la entrega original.

### Candidata adaptativa RV32E

La candidata utiliza una revisión cada 128 ticks, tendencia y confirmación SMA10, con posiciones objetivo de 32 o 63 acciones. Completó 20.000 ticks RTL a 30 μs y un ensayo de estrés de 386 ticks a 100 μs. El monitor cotejó MMIO, DECISION, MISO y cartera con Python. Registró 12,006 IC medios, 30,382 ciclos medios, CPI 2,531 y 161 ciclos de peor caso, equivalentes a 12,88 μs a 12,5 MHz. La síntesis reportó 1.174 Logic Cells, 1.060 LUT4, 7 BRAM y Fmax post-route de 50,85 MHz bajo restricción de 25 MHz.

En la serie completa terminó con $10.198, $503 sobre comprar y mantener ($9.695). En el tramo temporal reservado de 4.000 ticks terminó con $10.000, frente a $11.633 de comprar y mantener. Por tanto, la mejora de la serie completa no se sostuvo en la prueba reservada. La nueva imagen no tiene validación física con la FPGA maestra.

### Variante momentum agresiva

La variante seleccionada usa momentum directo, exposición objetivo de 100 %, revisión cada 16 ticks y umbral de 8. El intérprete RV32E coincidió con Python en los 20.000 ticks. La cobertura RTL publicada incluye 2.000 ticks de práctica a 100 μs, pruebas de 4.000 ticks a 32 μs, ensayos de estrés y pruebas de netlist en dos fases SPI; no corresponde describirla como una corrida RTL continua de 20.000 ticks.

En la prueba RTL de 2.000 ticks registró 20,227 IC medios, 47,644 ciclos medios, CPI 2,355 y 54 ciclos de peor caso. La síntesis reportó 1.193 Logic Cells, 1.079 LUT4, 7 BRAM y Fmax post-route de 50,70 MHz bajo restricción de 25 MHz.

La variante terminó la serie completa con $15.232, pero en la prueba temporal reservada obtuvo $9.265 frente a $11.633 de comprar y mantener, una diferencia de −$2.368. En una serie de estrés adicional terminó con $84. Su nueva imagen no tiene prueba física con la FPGA maestra y no sustituye la arquitectura MMIO SMA10 base.

### Registro de práctica con FPGA maestra

El registro publicado para Tesla enero de 2022, Fila 2, indica un patrimonio de $5.329 y octavo lugar de ocho, aproximadamente 46,7 % por debajo de comprar y mantener ($9.995). No se conservaron la serie exacta, el MISO por tick ni el hash del BIN de esa sesión; el resultado no puede atribuirse de forma concluyente a una imagen concreta ni reproducirse exactamente. Otros registros reportan Apple F7 con $10.000 y cero órdenes, y Fila 5 con $10.000, cero acciones, cero órdenes y última respuesta `0x00`, también sin huella de flash verificable.

### Separación respecto de la entrega original

La primera publicación del PDF y del manifiesto figura el 23 de noviembre de 2026 a las 09:21, hora de Chile, antes del plazo del 24 de noviembre a las 10:00. La actualización de este informe incorpora experimentos del 25 de noviembre y no debe confundirse con el artefacto disponible antes del cierre. El documento reúne exclusivamente el desarrollo técnico y la evidencia de validación del proyecto.
