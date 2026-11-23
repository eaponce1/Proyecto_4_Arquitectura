# Matriz de cierre del Proyecto 4

Fuente: Proyecto_4_arq.pdf, cinco páginas, secciones 2 a 6. La entrega es el 24/11 a las 10:00 y la competencia y defensa a las 10:30.

| Requisito | Estado y evidencia | Pendiente o riesgo |
|---|---|---|
| Algoritmo entero, causal y dos referencias (§3.1) | Python, 32 pruebas aprobadas. comparacion_final.csv: no operar $10.000, 0 órdenes, $0 comisiones y $0 drawdown. Comprar y mantener $9.695, 1 orden, $5 y $9.300. SMA10 $4.577, 931 órdenes, $4.655 y $5.476. | SMA10 rinde menos que las dos referencias en la práctica. |
| Assembly RV32E y equivalencia (§3.2) | trade.s y trade.hex conservados. comparar_python.py coteja 20.000 respuestas oficiales contra Python en cada arquitectura, con cero diferencias. test_trade_equivalencia.py prueba el HEX original y compara un caso corto en RTL. | Las series ocultas siguen sin medirse. |
| Métricas IC, CPI, ciclos y tiempo (§3.2) | CSV por tick de la instrumentación de rendimiento y comparacion_codisenio.csv. En ronda 3 oficial, promedio truncado y máximo de MMIO 60/255 ciclos, software 218/413. | El promedio entero oficial difiere del promedio decimal de la prueba de perfil. |
| Dos alternativas, Amdahl y roofline (§3.3) | comparacion_codisenio.csv e informe final. Custom-0 y MMIO base se comparan contra software. MMIO elegido por ciclos y porque enruta. | Custom-0 requiere 1.350 LC y carece de Fmax post-route. |
| SPI externo y decisión en Espino (§2, §4) | trade_top de MMIO base. competition.py solo lee las fuentes de esa alternativa. MISO de ronda 3 coincide con la referencia desplazada un tick. | Validación eléctrica y competencia con la FPGA maestra pendientes. |
| Tres rondas (§2.5, §3.4) | Ronda 3 completa 20.000 ticks y 4/4 en software y MMIO. Rondas 1/2 lanzadas con el emulador oficial y 20.000 ticks por corrida. | Rondas 1/2 sin resultado completo al cierre de esta revisión. No se acredita ningún PASS. |
| Hardware y testbenches (§4) | Tests y logs de co-diseño, arranque y autotest. Yosys y nextpnr aprobados para competition y selftest. | Selftest anterior mostró 1111 en placa. El nuevo monitor registra el primer fallo para la siguiente prueba física. |
| Informe, README y defensa (§4–6) | Informe Markdown/PDF, guía de defensa y comandos de compilación en los README. | Prueba física integral, publicación y defensa oral pendientes. |

## Presupuestos y mediciones

El testbench oficial reserva 9.500 ns por trama SPI, equivalentes a 237,5 ciclos. Su fórmula con división entera deja 249.762, 24.762 y 2.262 ciclos en rondas 1, 2 y 3. El contador oficial mide desde la llegada del precio hasta DECISION, por lo que recoge el tiempo que Espino tarda en detectar y atender el acceso MMIO. La espera entre ticks es el período impuesto por la maestra. En ronda 3 se midieron 2,40 us de media truncada y 10,20 us de máximo para MMIO, y 8,72 us y 16,52 us para software. Los presupuestos de las rondas largas son cálculos, no resultados de sus corridas.

| Arquitectura | IC medio | Ciclos medios / máximo de perfil | CPI | ticks/s de cómputo a 25 MHz | LUT4 / LC / BRAM | Fmax | Speedup medido / Amdahl |
|---|---:|---:|---:|---:|---:|---:|---:|
| Software | 91,917 | 218,664 / 412 | 2,379 | 114.331 | 980 / 1.200 / 12 | 42,60 MHz | 1 / 1 |
| Custom-0 | 30,945 | 70,734 / 266 | 2,286 | 353.435 | 1.133 / 1.350 / 14 | Sin ruta | 3,091 / 3,076 |
| MMIO base | 26,848 | 60,640 / 255 | 2,259 | 412.270 | 1.055 / 1.279 / 13 | 40,50 MHz | 3,606 / 3,692 |

Los ticks/s cuentan un precio consumido con su decisión escrita. No son el caudal SPI efectivo. El roofline del informe usa sumas/restas como operación elemental y sus hipótesis de ancho de banda son modeladas.

### Evidencia física actualizada el 23 de noviembre

El diagnóstico anterior dio D1 solo según el usuario. El byte llegó y no se observó PRICE antes del timeout de WAIT_ACK. La revisión separa el acceso a STATUS de la respuesta STATUS con new_price=1. Pasó Icarus y place-and-route, con 1.279 LC y Fmax de 40,25 MHz. Su prueba física y la competencia SPI externa siguen pendientes. Los hashes de los insumos adjuntos coinciden con las copias oficiales. Las corridas Icarus de rondas 1 y 2 aún no tienen salida completa.
