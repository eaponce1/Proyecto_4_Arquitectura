# Informe final — Pochoco Trader competitiva_definitiva



**Estado digital:** imagen generada con las puertas digitales aprobadas.

**Prueba física:** PENDIENTE. No se programó ninguna placa ni se ejecutó iceprog.



## Resultado y límites financieros



Política elegida: exposición inicial alcista del 100%, momentum de 32 ticks, revisión cada 8; salir con delta <= -16 o retroceso de 20 puntos desde el pico de la posición; reentrar con delta >= +6. Entre umbrales conservar régimen. Reconciliar cada fill al precio siguiente, completar compras y liquidaciones con órdenes <=63. El pico se reinicia al quedar plano. Stop y momentum solo se revisan cada 8 ticks; un salto brusco puede causar una pérdida grande antes de vender.



6/8 ventajas; mediana 24.90%; media 33.08%; peor -6.14%. 6/8 terminan sobre $10.000.

Peor patrimonio: $8615. Mayor drawdown absoluto: $15881. Mayor drawdown porcentual: 61.11%.



| serie | patrimonio | mantener_oficial | ventaja | ordenes | comisiones | drawdown |
|---|---|---|---|---|---|---|
| practica_amd_2022_ene | 19312 | 8315 | 10997 | 63 | 315 | 5341 |
| practica_amd_2022_may | 11490 | 9647 | 1843 | 45 | 225 | 7730 |
| practica_apple_2022 | 12528 | 11063 | 1465 | 64 | 320 | 8668 |
| practica_apple_2023 | 13555 | 10371 | 3184 | 62 | 310 | 15881 |
| practica_meta_2022 | 13700 | 9695 | 4005 | 56 | 280 | 8955 |
| practica_netflix_2022 | 8615 | 9179 | -564 | 59 | 295 | 8352 |
| practica_netflix_2023 | 8929 | 9170 | -241 | 41 | 205 | 7691 |
| practica_tesla_2022 | 13671 | 9995 | 3676 | 43 | 215 | 4469 |


La política pierde frente a mantener en Netflix 2022 y Netflix 2023. Las salidas y reentradas pueden vender bajo, perder recuperaciones y pagar comisiones. En oscilaciones violentas la diferencia es mucho peor: ver los escenarios sintéticos. No existe garantía de superar a mantener en series ocultas.



## Preservación y procedencia



Trabajo aislado en una extracción nueva de Proyecto_4_Arquitectura-main.zip; sin modificar las variantes históricas. El ZIP no trae .git: no se inventó un commit para esta extracción. La copia local _p4_pub_20261125 sí tiene Git: referencia 66eede4c46e211c02dc5ef22de18f86e22e775c5, status y diff iniciales vacíos; consulta git_referencia.json. Se comprobaron sin cambios los 244 BIN/HEX/Assembly/PCF históricos contra SHA256_previos.txt. El workspace original también se conservó.

Los scripts estrategia_tendencia_32_prototipo.py y resultados_tendencia_32_prototipo.csv no aparecieron en la búsqueda del espacio local y Downloads. Momentum32 se reconstruyó desde la solicitud y reproduce exactamente los ocho resultados documentados: reproduccion_momentum32.csv. La CSV Meta adjunta es igual en precios a la Meta del ZIP; el TB adjunto es idéntico byte por byte al profesor del ZIP.

Se distinguió la solicitud pegada del contenido de documentos históricos. Las afirmaciones de pruebas físicas previas son antecedentes, no evidencia física nueva. La sesión de $10.000/0 órdenes y la de $5.329 se mantienen separadas; no se atribuye una causa común ni se demuestra qué BIN estaba cargado.



## Datos y estudio estadístico



8 CSV, 20.000 filas secuenciales cada uno, 160.000 precios en 100..255. estadisticas_series.csv contiene precios extremos, variaciones, repetición, volatilidad poblacional de diferencias, drawdown de precio y duración bajo el máximo histórico. estadisticas_horizontes.csv cubre 4/8/16/32/64/128/256 ticks. Para las duraciones, los bloques no solapados se clasifican alcistas/bajistas con delta >=2 / <=-2, y laterales dentro de ese intervalo; los cambios de régimen son transiciones entre clases. Las magnitudes de retroceso son la mayor caída sobre el horizonte. Son medidas descriptivas retrospectivas y nunca se entregan como información futura al algoritmo.

Gráficos comparables: patrimonios.png y estudio_series.png. La normalización de estas muestras no equivale al retorno anual de sus acciones.



## Comparación y selección



comparacion_existentes.csv reproduce Conservar, SMA10, candidata_final, agresiva, Momentum32 y mantener ejecutable SPI. Todas las carteras usan el mismo fill independiente. Las reglas de las variantes antiguas se importan de sus fuentes conservadas, sin reoptimizar. El benchmark oficial compra en tick 0 con una sola comisión y sin límite 63; se presenta aparte del benchmark físicamente ejecutable, que empieza con MISO=0 y compra desde tick 1 hasta completar exposición.

Momentum32 sin stop supera las ocho series completas conocidas, con patrimonios exactamente 11659, 10458, 11427, 18150, 13521, 11122, 9794, 10702. Ese éxito es desarrollo sobre datos ya vistos; falla en la caída gradual sintética y tiene drawdowns altos.

Grilla declarada: momentum simple y doble, breakout, trailing fijo/adaptativo, híbrida, promedio lento, máximos decrecientes y persistencia negativa; exposiciones 0/25/50/75/100 y pisos neutrales 25/50/75. Se conserva la grilla y toda medición, incluidos perdedores. Los parámetros slow=128 y gradual=12 de la configuración final son campos comunes de la grilla: NO participan en la decisión trailing. El delta lento se calcula solo para telemetría; no se atribuye mejora a un filtro inactivo.

V1, elegida en los primeros 12.000 ticks, fue breakout y fracasó en caída gradual. V2 añadió un filtro de admisibilidad de desarrollo: DD <=3025 (mitad de la pérdida de mantener en ese escenario sintético). No se ocultó la revisión: revision_v1_descartada conserva sus resultados. Después se seleccionó por ventaja y riesgo únicamente sobre los primeros 12.000 ticks. Los últimos 8.000 siguen siendo validación interna conocida. Este proceso es adaptación de desarrollo, NO descubrimiento de una prueba externa independiente.

Ranking lexicográfico: proporción de ventajas; mediana + 0,25*media + 0,5*peor ventaja porcentual - 0,05*mayor DD porcentual; patrimonio mínimo; comisiones. La rentabilidad manda dentro del filtro de riesgo. No se favorece la cantidad de operaciones.



## Validación y sobreajuste



Leave-one-company-out: 5/8 ventajas; mediana 10.55%; media 13.18%; peor -6.14%.

Leave-one-series-out: 6/8 ventajas; mediana 9.03%; media 10.66%; peor -16.66%.

Walk-forward: 14/24 ventajas; mediana 3.37%; media 4.50%; peor -14.75%. Ajuste en prefijos 0..8000/12000/16000 de cada serie y evaluación en sus siguientes 4000 ticks; cartera e indicadores reinician en cada ventana de prueba. Es cronología por serie, no alineación de fechas entre empresas.

Cada fold elige configuración usando exclusivamente sus empresas/series/prefijos de entrenamiento, con el mismo escenario de desarrollo sintético. Los resultados excluidos no intervienen en esa elección. El espacio de familias y el filtro adverso sí son decisiones de desarrollo conocidas: no existe una muestra verdaderamente inédita. Los folds estiman el procedimiento de selección, no son ocho pruebas independientes de la única configuración final.



Sensibilidad de componentes activos (±2 puntos):



| parametro | cambio | resultado |
|---|---|---|
| entry | -2 | 6/8 ventajas; mediana 22.15%; media 21.74%; peor -10.94% |
| entry | 0 | 6/8 ventajas; mediana 24.90%; media 33.08%; peor -6.14% |
| entry | 2 | 5/8 ventajas; mediana 10.68%; media 25.66%; peor -15.72% |
| exit | -2 | 6/8 ventajas; mediana 26.78%; media 31.63%; peor -16.83% |
| exit | 0 | 6/8 ventajas; mediana 24.90%; media 33.08%; peor -6.14% |
| exit | 2 | 6/8 ventajas; mediana 18.94%; media 30.61%; peor -7.33% |
| stop | -2 | 8/8 ventajas; mediana 16.09%; media 23.87%; peor 0.13% |
| stop | 0 | 6/8 ventajas; mediana 24.90%; media 33.08%; peor -6.14% |
| stop | 2 | 6/8 ventajas; mediana 19.52%; media 22.59%; peor -22.30% |


La variación entre umbrales confirma fragilidad; no se afirma estabilidad perfecta ni superioridad consistente fuera de muestra.



## Escenarios adversos



| escenario | patrimonio | mantener_oficial | ventaja | drawdown | comisiones |
|---|---|---|---|---|---|
| subida | 25335 | 25340 | -5 | 10 | 10 |
| caida_gradual | 9210 | 3950 | 5260 | 790 | 10 |
| caida_brusca | 4590 | 4595 | -5 | 5410 | 10 |
| lateral | 9937 | 9937 | 0 | 116 | 5 |
| recuperacion | 9331 | 9995 | -664 | 5415 | 15 |
| limites_inventario | 9975 | 25340 | -15365 | 15360 | 25 |
| alternancia | 9990 | 25340 | -15350 | 6050 | 10 |
| integracion_cadencias | 9980 | 9995 | -15 | 11890 | 20 |


La caída gradual vende y queda en caja; una caída brusca ya recibida no se puede evitar con una orden ejecutada en el tick posterior. La subida sostenida mantiene exposición alta y paga una comisión adicional por el límite 63. La lateralidad puede perder por comisiones. La recuperación puede llegar tarde; la alternancia 100/255 demuestra que el desfase SPI es un riesgo económico severo. No se promete un piso de capital.

Comisiones por serie: $315, $225, $320, $310, $280, $295, $205, $215. Son el débito contabilizado; no equivalen a comparar con una estrategia de cero comisión, pues esa comparación cambiaría cantidades futuras. Tiempo en caja y exposición >=75% están en ticks_caja y ticks_exposicion_alta de comparacion_final.csv; dividir por 20.000 para obtener proporciones.



## Implementación y equivalencia



trade.s usa x0..x15 y únicamente LUI/ADDI/ANDI/ADD/SUB/LW/SW/BEQ/BNE/BLT/BGE/JAL. Sin MUL, DIV ni shifts. 150 instrucciones, ROM separada y RAM de 512 palabras. Historial en palabras 256..511, pico en dirección 1000 (palabra 250); código en 0..149. Se evita leer historial antes de su inicialización. No hay acceso fuera de 0..2047; el código y los datos no se solapan. La división por precio usa un greedy binario acotado por 63; los fills se reconstruyen al precio recibido.

Cada traza contiene tick, precio, decisión nueva, MISO recibido, tendencias, régimen, objetivo, cantidad solicitada por el MISO actual, fill, caja, inventario, patrimonio, comisión y pendiente. La orden calculada en el último tick queda pendiente y no se ejecuta. No se cobra comisión a una orden sin fill. Python valida cada invariante de caja e inventario. test_invariantes.py cubre límites de caja, comisión, inventario, cantidad cero, acción reservada, conservación de patrimonio por operación, causalidad y reinicio.

El intérprete ejecuta el HEX ensamblado, no una versión reescrita de la política. Se compararon 160.000 ticks y los escenarios sintéticos, incluidos MISO/DECISION/caja/inventario y régimen. La cartera determina patrimonio, fills y comisiones; las trazas RTL cotejan también esos campos de forma explícita.

Verilator completó 8*20.000 ticks del RTL a 100 µs con aserciones de instrucciones, PRICE/SUM10/READY, DECISION, una escritura por precio, cartera y MISO. Es un simulador de dos estados: los chequeos de X se apoyan en Icarus. Icarus completa los escenarios adversos y los bancos oficiales; las dos corridas largas iniciales de Icarus fueron INTERRUMPIDAS, no PASS. Sus CSV parciales se conservan como diagnóstico.



## Bancos oficiales y protocolo



El TB adjunto y tb_proyecto_4_profesor.sv son idénticos. tb/tb_proyecto_4.sv añade EnableSpi=1, rutas, chequeos de CSV y carga MMIO mantenida; diferencias_bancos.diff registra el contraste. El original literal apunta a un SoC distinto, sw/trade.hex inexistente y no habilita SPI: para verificar el top final se generaron copias de ambos bancos. Los diffs explícitos están en build/oficial: tipos de string compatibles con Icarus, rutas, cableado del top, jerarquía de observación, espera de POR y medición del reloj real. Las tareas financieras y constantes se preservan literalmente; los cuatro chequeos siguen activos. Se cotejaron también sus CSV de 2000 ticks con Python. Es PASS del banco adaptado al top; no se presenta como ejecución literal sin cambios.

SPI: modo 0, 8 bits, MSB primero, 1 MHz en simulación; sincronizadores de tres registros; MISO carga tx_hold al activar CS. Espino decide y escribe MMIO 0x80010008; STATUS 0x80010000, PRICE 0x80010004, SUM10 +12 y READY +16. No hay decisión reemplazada por hardware. El top robusto conecta SPI incondicionalmente; el parámetro EnableSpi=0 del antiguo game SoC NO participa en esta imagen.

Cadena crítica sintética (48 ticks): Espino calcula 0x7F en tick 0, el periférico almacena el byte y MISO lo devuelve en tick 1; calcula venta 0xBF en tick 32 y MISO la devuelve en tick 33. Los siguientes ticks liquidan posiciones mayores que 63. Ambas direcciones se verifican también en el netlist sintetizado antes de icepack.

PCF conservado: entrada 25 MHz pin 15; CS_n pin 65 (PS1), MOSI 64 (PS2), MISO 63 (PS3), SCLK 62 (PS4); LEDs 56/57/59/60. Se coteja cada asignación con goboard.pcf y no se cambian pines. Las etiquetas PMOD provienen de la documentación histórica del proyecto; el cableado físico sigue pendiente de verificar. Señales 3,3 V y tierra común; no conectar el VCC entre placas.



## Tiempo de respuesta



Reloj de entrada 25 MHz, Espino 12,5 MHz (80 ns/ciclo), con división por dos y SB_GB. SPI ocupa 9,5 µs por transacción. Se mide desde byte_done hasta la escritura efectiva de DECISION. El presupuesto conservador descuenta la trama completa; además se informa reserva de 3 ciclos de sincronización. IC corresponde a commits observados en ese intervalo y CPI=ciclos/commits. Los CSV contienen media, máximo y valores por tick.

Peor caso en series completas y escenarios medidos: 321 ciclos; 25.68 µs. Es máximo observado, no una prueba formal de todas las secuencias posibles.



| ronda | MHz | periodo_us | disponibles | consumidos_max | margen_ciclos | margen_us | margen_us_con_sync |
|---|---|---|---|---|---|---|---|
| 1 | 12.5 | 10000.0 | 124881 | 321 | 124560 | 9964.82 | 9964.58 |
| 2 | 12.5 | 1000.0 | 12381 | 321 | 12060 | 964.82 | 964.58 |
| 3 | 12.5 | 100.0 | 1131 | 321 | 810 | 64.82 | 64.58 |


| serie | ciclos_max | ciclos_media | ic_max | ic_media | cpi |
|---|---|---|---|---|---|
| practica_amd_2022_ene | 312 | 159.56785 | 142 | 71.01225 | 2.2470468123457574 |
| practica_amd_2022_may | 304 | 160.73775 | 138 | 71.5403 | 2.2468140334888167 |
| practica_apple_2022 | 312 | 158.48365 | 143 | 70.52125 | 2.247317652480635 |
| practica_apple_2023 | 321 | 166.8928 | 147 | 74.31835 | 2.24564727284715 |
| practica_meta_2022 | 311 | 163.9519 | 142 | 72.99015 | 2.2462195241412712 |
| practica_netflix_2022 | 306 | 160.55395 | 140 | 71.4576 | 2.246842183336692 |
| practica_netflix_2023 | 283 | 157.445 | 128 | 70.05475 | 2.247456453702283 |
| practica_tesla_2022 | 303 | 165.55185 | 138 | 73.71495 | 2.2458381915744363 |




## Síntesis e imagen



Yosys + nextpnr HX1K/VQ100: 1257/1280 Logic Cells; 9/16 BRAM. Timing impuesto a 25 MHz, incluso al reloj dividido; consulta timing.json y nextpnr.log. Se verificaron dos fases del netlist y después icepack produjo 32.220 bytes.

SHA-256 BIN: `44e48b3701159a79148990e6610254d573985049dd4a0c4a0ab690461c838366`.

SHA-256 HEX: `27d895e1747120d5c4d1b3cc17a91e82ed87d772aeebae4fc5bdcda7d9e04058`.

El manifiesto build/fuentes_validadas.json liga las fuentes, el HEX y PCF al ensamblado. SHA256_entrega.txt incluye BIN, HEX, Assembly, JSON, ASC y netlist. La programación manual debe comprobar ese hash; ningún BIN histórico se reemplaza.



## Matriz de aceptación



| Validación | Resultado | Evidencia |
|---|---|---|
| Datos de práctica | PASS | estadisticas_series.csv: 8*20000 |
| Ocho backtests | PASS | comparacion_final.csv y trazas |
| Buy & Hold | 6/8 ventajas | mediana +24,90%; peor -6,14% |
| Robustez fuera de muestra | NO DEMOSTRADA independientemente | LOCO 5/8; LOSO 6/8; WF 14/24; datos conocidos |
| Control de inventario | PASS | invariantes.log; equivalencia_rv32e.json |
| Compras y ventas digitales | PASS | integracion_compra_venta.json; RTL y netlist |
| Python vs RV32E | PASS | 160000 ticks + sintéticos |
| RV32E vs RTL | PASS | equivalencia_verilator.json, 160000 ticks |
| SPI y MISO | PASS | Icarus cuatro estados y Verilator |
| Testbench oficial | PASS adaptado | 2 bancos 4/4, 2000 ticks; diffs explícitos |
| Timing ronda 1 | PASS | timing_rondas.csv + pruebas a cadencia real |
| Timing ronda 2 | PASS | timing_rondas.csv + pruebas a cadencia real |
| Timing ronda 3 | PASS | timing_rondas.csv + pruebas a cadencia real |
| Síntesis HX1K | PASS | build/resultados.json y logs |
| SHA-256 final | Verificado | SHA256_entrega.txt |
| Prueba física Go Board | PENDIENTE | no se programó la placa |
| Prueba FPGA maestra | PENDIENTE | requiere conexión y sesión física |


Compilar, simular, sintetizar, programar, funcionar físicamente y obtener ventaja económica son resultados distintos. Esta entrega demuestra lo digital descrito y no afirma los demás resultados.