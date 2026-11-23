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

El informe de build dice explícitamente que `iceprog` no se ejecutó. El usuario informó que la Go Board ya estaba programada con MMIO SMA10 base; el repositorio no contiene un log de programación ni una captura de VERIFY OK. Por tanto, se registra como estado reportado por el usuario, no como verificación independiente de bitstream. No se afirma que la estrategia haya sido probada físicamente ni que haya participado en competencia.

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

**Alcance pendiente:** solo se ejecutó la ronda 3 (0,1 ms). Las rondas 1 (10 ms) y 2 (1 ms) siguen pendientes. La integración física del diseño con la FPGA maestra también sigue pendiente; estos resultados son de simulación RTL, no una prueba física.

## 10. Pendientes y conclusión técnica

1. Añadir/archivar evidencia del programador (`iceprog`/VERIFY OK) si se requiere afirmar programación física verificada.
2. Completar las rondas oficiales 1 y 2 (20.000 ticks por ronda) para MMIO base y software original.
3. Probar la integración física con la FPGA maestra; la prueba SPI interna aislada no reemplaza esta integración. La simulación no sustituye cableado/timing eléctrico.
4. MMIO base queda al límite (1 LC libre); optimizada solo mejora 5 LC. Debe verificarse margen ante cualquier cambio de configuración.
5. No se reporta participación en competencia ni resultado de rentabilidad real. La serie histórica no respalda recomendar una estrategia activa frente a no operar.
Conclusión: existe equivalencia funcional demostrada para firmware/estrategia en el alcance de pruebas indicado. **MMIO SMA10 base se mantiene como arquitectura final seleccionada**: conserva la decisión final en Espino, pasó P&R y cuenta con comparación oficial de 20.000 ticks. La variante agente completo es solo una simulación RTL de diagnóstico; su implementación física excede el dispositivo por la lógica interna de prueba. El margen de LC de la arquitectura base es mínimo. Las rondas oficiales 1 y 2, y las pruebas físicas del agente con FPGA maestra siguen pendientes. El estado físico y la decisión de inversión deben describirse con esas limitaciones.

## Imágenes finales y prueba física pendiente

El autotest local de 16 precios y la imagen SPI externa tienen objetivos separados. La prueba física anterior del capturador dio 0101. La versión integral anterior dio 1111, un error genérico que no identifica la causa. La nueva imagen de autotest preserva el primer código de fallo. La causa física concreta se resolverá con ese código. En Icarus se reprodujo un fallo MISO inyectado en el flanco 531 y se obtuvo 1101.

El autotest instrumentado verificó 16 precios, decisiones y respuestas MISO contra Python, y 15 ACK. Con mapeo Yosys -dff ocupa 1.089 LUT4, 1.279 LC y 9 BRAM, con Fmax 38,80 MHz. El top de competencia trade_top ocupa 1.055 LUT4, 1.279 LC y 13 BRAM, con Fmax 40,50 MHz. Ambos cerraron 25 MHz. El autotest local y la conexión a la maestra siguen pendientes en placa.

La matriz requisito por requisito está en documentacion/matriz_cierre_pochoco.md. La ronda 3 mantiene sus 20.000 ticks y 4/4 PASS en cada arquitectura. Se relanzaron las rondas 1 y 2 con Icarus y no se dispone aún de resultados completos.

## Estado de entrega verificado el 23 de noviembre de 2026

Se verificó que el testbench y el CSV adjuntos coinciden byte a byte con sus copias oficiales del repositorio. SHA-256 del testbench F83486755FE2B3DE385A2BDC39C2F275B9DD690342FB4FC0391401706876F8F3. SHA-256 del CSV FED122E0A9861276D76B1396B264FD34077C280C80FE6B356B6971D55242DA3F. Se revisaron las cinco páginas del enunciado.

La imagen SPI externa MMIO SMA10 base es trade_mmio_base.bin, SHA-256 0150BF6FCE608FD463B15EB945F84354B151E581C71A36B47629E889EC0B6DFD. Ocupa 1.279 LC, 1.055 LUT4 y 13 BRAM. Fmax post-route de 40,50 MHz. La imagen solo se acredita con simulación e implementación y no hay una corrida física con FPGA maestra.

El usuario observó D1 solamente en la imagen diagnóstica anterior. El código identifica WAIT_ACK después de recibir un byte, sin lectura PRICE observada. La revisión de diagnóstico distingue ausencia de consulta STATUS, consulta sin respuesta new_price=1 y respuesta new_price=1 sin lectura PRICE. Los tres casos se ejercitaron en Icarus, junto a DONE, MISO y el caso nominal de 16 ticks. La imagen temporal ocupa 1.279 LC y cerró a 25 MHz con Fmax de 40,25 MHz. Falta observar los códigos nuevos en placa para identificar el punto exacto de detención de Espino.

La evidencia oficial completa sigue siendo la ronda 3 con 20.000 ticks y 4/4 para software y MMIO. Rondas 1 y 2 se están simulando con Icarus. Su avance parcial no acredita PASS. Verilator pudo traducir el banco y MSVC 2019 está instalado, pero el entorno carece de los encabezados del SDK/UCRT necesarios para compilarlo. Una corrida alternativa de dos estados tampoco acreditaría el criterio MISO sin X.

La entrega incluye las dos alternativas de co-diseño, código y bancos de prueba, tablas de IC, CPI, ciclos, tiempo, recursos y roofline, el PDF y la guía de defensa. La demostración física con la maestra y la defensa presencial siguen pendientes.
