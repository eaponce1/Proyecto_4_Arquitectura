# Pochoco Trader — auditoría y candidata RV32E

Fecha de trabajo: 25 de noviembre de 2026. La candidata conserva Espino, el SPI Slave, SMA10 y el mapa MMIO. Usa el arranque, la ROM de instrucciones y el reloj de 12,5 MHz del top SPI externo probado en RTL. Las imágenes de entrega anteriores quedan identificadas en el respaldo de referencias. La candidata busca una mejora de rentabilidad comprobable en la serie de práctica y la validación fuera de muestra determina el alcance de esa mejora.

## Qué explica los cero trades

En Conservar, Espino atiende STATUS/PRICE/SUM10/READY y siempre escribe `sw x0, 8(x1)`. Esa instrucción deja DECISION en `0x00`. Por diseño, la maestra mantiene $10.000, cero acciones y cero órdenes aunque reciba correctamente todos los bytes. Es la última imagen cuya programación y verificación de flash constan en la conversación: SHA-256 `5F3C32E0AC266614B4B8FE825672255D7D29BF924CE51D3BB3E249516E052FC1`. En esta misión se reconstruyó el BIN desde su ASC y se simuló el circuito recuperado directamente del BIN. [Evidencia del binario y diagnósticos A–F](../../resultados/mision_final_diagnostico/)

| Sesión física | Resultado registrado | Atribución |
|---|---|---|
| Apple, F7 | $10.000, cero órdenes, precio final 124 | La práctica fue distinta de la serie local, que termina en 160. |
| Tesla ene 2022, Fila 2 | $5.329, 8.ª de 8, −46,7 % frente a mantener ($9.995) | La maestra contabilizó operaciones. Faltan el detalle y el BIN de la sesión. |
| Fila 5, JC arriba | 20.000 ticks a 10 ms y fuente PLACAS. $10.000, 0 acciones, 0 órdenes, última respuesta `0x00`. | Reporte del usuario. Conservar reproduce exactamente ese comportamiento. El usuario desconoce si se cargó otra imagen antes de la sesión. |

La causa de los ceros queda demostrada para **Conservar**. La atribución histórica exacta a **Fila 5** sigue abierta porque la pantalla agrega resultados del canal y el reporte carece de una huella de flash de esa sesión. La prueba física de la candidata necesita su propio registro de MISO, la referencia de precios y la verificación de la imagen.

## Protocolo y contabilidad

El enunciado oficial especifica 25 MHz en la placa, SPI modo 0, MSB primero, un byte, SCLK hasta 1 MHz, precios 1…255, caja inicial $10.000, inventario inicial 0 y comisión $5 por orden ejecutada. Los bits 7:6 del byte codifican mantener, comprar, vender y reservado. Los bits 5:0 codifican 0…63 acciones. El banco del profesor trata reservado y cantidad cero como mantener.

Durante el tick `n`, la maestra lee el byte retenido desde el tick `n-1` y lo ejecuta al precio que transmite en `n`. El hardware sincroniza CS/SCLK/MOSI, compone el byte, emite `byte_done`, enclava PRICE y eleva el bit de precio nuevo. El Espino consulta STATUS, lee PRICE para limpiar ese bit, reconstruye el fill de la orden anterior en su cartera local y consulta SUM10 y READY. El Espino escribe DECISION para el siguiente tick. La maestra ejecuta una compra parcial si la caja es insuficiente, recorta la venta al inventario y ejecuta una venta baja solo si la caja resultante cubre la comisión. El algoritmo usa únicamente datos recibidos por SPI hasta el tick de cálculo.

| Dirección | Registro | Evidencia de uso |
|---|---|---|
| `0x80010000` | STATUS | Sondeo de bit 0 y lectura sincronizada. |
| `0x80010004` | PRICE | Una lectura consume cada precio completo. |
| `0x80010008` | DECISION | Escritura única del byte decidido para el siguiente precio. |
| `0x8001000C` | SUM10 | Suma de las últimas 10 muestras con ventana inclusiva. |
| `0x80010010` | READY | Se activa al llenar la ventana. |

El banco separado A–F cotejó 3.492 ticks en 18 pruebas RTL para el SMA10 base, Activo anterior y Conservar. Comprueba el precio y los registros de estrategia, caja/inventario, escritura y desfase MISO. Conservar se mantiene en los seis escenarios. Base y Activo anterior compran en descenso, caída y recuperación y venden en el escenario de recuperación. El banco de la nueva candidata cubre arranque, reset, lectura MMIO, límites contables, cargas mantenidas, evento STATUS/byte_done simultáneo y timeout negativo. [Escenarios de diagnóstico](../../resultados/mision_final_diagnostico/resumen_escenarios.csv) · [Banco integrado](tb/README.md)

## Candidata

Cada 128 ticks se toma una decisión de exposición. La tendencia es el precio actual menos el de la revisión previa. La confirmación reciente usa `10*p - SUM10`. Con posición cero, se entra si la tendencia es al menos 8 y la confirmación es no negativa. Se apunta a 32 acciones con señal moderada o 63 si la tendencia llega a 16. Se ordena como máximo `floor((caja - 510)/255)` acciones para reservar $500 y las dos comisiones incluso con ejecución al peor precio de compra permitido. Con posición abierta, se mantiene hasta que la tendencia cae por lo menos 8 o cuando la tendencia es negativa y la confirmación es no positiva. En ese caso se vende la posición. El firmware espera la revisión siguiente sin repetir compras al alcanzar su posición.

La contabilidad de Assembly resuelve cantidades con descomposición en 32, 16, 8, 4, 2 y 1, doblando el precio con ADD y descontando costos en orden decreciente para hallar la máxima cantidad financiable. La venta usa la misma rutina con presupuesto temporal suficiente y limita cantidad al inventario. Para cotizar una compra futura usa precio 255. En ticks sin señal el camino corto escribe mantener. Los registros persistentes son x1 MMIO, x4 orden, x5 acciones, x6 fase, x7 precio de revisión y x15 caja. Todos los datos son enteros RV32E. Las instrucciones usadas pertenecen a ADD, SUB, ADDI, ANDI, LW, SW, LUI, BEQ, BNE, BLT, BGE y JAL. El acelerador calcula la suma y Espino decide.

La escala de precio máxima de la rutina es 8.160 y el coste máximo de una orden es 16.065. Incluso al acotar la caja por $10.000 más 20.000 ingresos brutos de $16.065, el límite de $321.310.000 cabe en un entero con signo de 32 bits.

El piso de caja de $500 exige precios válidos y que cada orden se ejecute a lo sumo una vez con el desfase especificado. Una prueba extrema fuerza compra de 37 a 255 y liquidación a 1. Cierra con $592, dos órdenes y pérdida de $9.408. Esa prueba ilustra la protección de la reserva y el riesgo del tamaño de posición bajo movimientos extremos. El ensayo sintético se conserva aparte de la medición financiera de la serie oficial.

## Datos, optimización y evaluación fuera de muestra

El CSV oficial de 20.000 precios se dividió por tiempo en 12.000 desarrollo, 4.000 validación y los 4.000 finales de prueba. Los tramos parciales parten de cartera e historial vacíos. Se evaluaron 480 configuraciones y 154 cumplieron los filtros de desarrollo y validación, que contemplan patrimonio, drawdown, actividad mínima y estabilidad por bloques. Se exploraron ventanas/horizontes, cadencia, umbrales, confirmación, volumen de 1…63, reserva y protección de ganancias. La candidata se congeló antes de evaluar el tramo final. El walk-forward usa cinco cortes del primer 80 % para medir sensibilidad sin consumir el tramo reservado.

| Estrategia, serie completa | Patrimonio | Rentabilidad | Diferencia vs mantener | Compras | Ventas | Órdenes | Comisiones | Drawdown | Acciones finales | Caja |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| No operar | $10.000 | 0,00 % | +$305 | 0 | 0 | 0 | $0 | $0 | 0 | $10.000 |
| Comprar y mantener | $9.695 | −3,05 % | $0 | 1 | 0 | 1 | $5 | $9.300 | 60 | $95 |
| SMA10 base | $4.577 | −54,23 % | −$5.118 | 466 | 465 | 931 | $4.655 | $5.476 | 16 | $2.017 |
| Adaptativa RV32E | $10.198 | +1,98 % | +$503 | 8 | 8 | 16 | $80 | $1.983 | 0 | $10.198 |

| Tramo | Adaptativa | Comprar y mantener | Diferencia |
|---|---:|---:|---:|
| Desarrollo, 0…11.999 | $11.792 | $13.055 | −$1.263 |
| Validación, 12.000…15.999 | $10.000 | $6.177 | +$3.823 |
| Prueba reservada, 16.000…19.999 | $10.000 | $11.633 | −$1.633 |

En la validación y en la prueba reservada la candidata quedó plana. De las estrategias evaluadas, la reversión filtrada obtuvo el mayor patrimonio activo en el tramo reservado, $11.238. Comprar y mantener terminó en $11.633. La búsqueda adaptativa superó esa referencia en tres de cinco segmentos walk-forward y quedó detrás en dos. La evidencia justifica una candidata de menor rotación y mejor resultado en la práctica completa que el SMA10 base. El criterio de superar a comprar y mantener fuera de muestra queda incumplido.

[Comparación de todas las estrategias](resultados/comparacion.csv) · [Búsqueda 60/20/20](resultados/busqueda_desarrollo_validacion.csv) · [Validación walk-forward](resultados/walk_forward.csv) · [Decisiones y señales por tick](resultados/decisiones_tick.csv)

[Precio](resultados/precio.svg) · [Patrimonio](resultados/patrimonio.svg) · [Diferencia vs mantener](resultados/vs_mantener.svg) · [Señales](resultados/senales.svg) · [Inventario](resultados/inventario.svg) · [Caja](resultados/caja.svg) · [Comisiones](resultados/comisiones.svg)

## Protección de las referencias

El árbol descargado carece de `.git`. El checkout separado publicado estaba limpio en main, SHA `5229fdbd3d9d674fc9fec207d3e68f4370294017`. Se registraron las diferencias previas y se archivaron BIN y firmware de referencia antes de generar el nuevo HEX. El ASM y HEX históricos de MMIO SMA10, PCF, CSV oficial y los BIN base se cotejan por hash. El trabajo de esta misión vive en una variante independiente. [Estado Git inicial](auditoria_git.log) · [Hashes de referencia](SHA256_referencia.txt) · [Respaldo](firmware_referencia.zip)

El análisis previo de co-diseño conserva las comparativas de software, custom-0 y MMIO base. Esta candidata reutiliza el MMIO SMA10 y cambia la política de decisión y el cálculo acotado de cantidades. [Informe previo de co-diseño](../../documentacion/informe_final_proyecto4.md)

## Validación de la candidata y rendimiento

Se cotejaron **20.000/20.000 ticks en RTL** a 30 µs entre tramas y SCLK de 1 MHz. El monitor verificó STATUS/PRICE/SUM10/READY, una escritura DECISION por precio, MISO del tick anterior y caja/acciones de Espino frente a la cartera de la maestra emulada. Se registraron 769 coincidencias de STATUS con `byte_done` y 80.769 cargas mantenidas en la LSU, sin una solicitud de bus repetida. Un cotejo independiente de los dos CSV comprobó cada precio, DECISION, MISO, caja, inventario, comisiones y patrimonio. El intérprete de las palabras RV32E también coincidió en los 20.000 ticks.

| Ensayo | Ticks | Período | IC promedio / máximo | Ciclos promedio / peor | CPI global | Tiempo promedio / peor |
|---|---:|---:|---:|---:|---:|---:|
| Práctica RTL | 20.000 | 30 µs | 12,006 / 73 | 30,382 / 161 | 2,531 | 2,431 / 12,88 µs |
| Reserva extrema RTL | 386 | 100 µs | 12,723 / 73 | 31,790 / 160 | 2,499 | 2,543 / 12,80 µs |

La ventana medida va de `byte_done` a DECISION. Excluye tiempo de sondeo anterior al precio. El CPI global es la suma de ciclos dividida entre la suma de commits. El mayor CPI por tick de práctica fue 2,636 y el CPI del tick de mayor latencia fue 161/73 = 2,205. Una operación útil es un precio procesado con una DECISION publicada. El promedio de práctica equivale a cerca de 411.422 operaciones útiles por segundo de **cómputo**, separado del ritmo de la maestra y de la transferencia SPI. La ruta de cartera y cotización por pasos binarios requiere más IC en los ticks con orden; el peor medido ocurrió en el tick 3.328, una revisión de posición.

| Ronda | Período | Ciclos a 12,5 MHz descontando trama de 9,5 µs | Margen con 161 ciclos |
|---|---:|---:|---:|
| 1 | 10 ms | 124.881 | 124.720 |
| 2 | 1 ms | 12.381 | 12.220 |
| 3 | 100 µs | 1.131 | 970 |

El ensayo completo de 30 µs es más exigente en intervalo disponible que la ronda 3 y aprobó con holgura de 95 ciclos. Se ejecutaron además 4 tramas a 10 ms y 8 tramas a 1 ms y el ensayo de 386 ticks a 100 µs. Estos tamaños identifican el alcance de cada prueba. El netlist sintetizado pasó 386 transacciones en cada una de las fases 0 y 41 ns, incluidas una compra, una venta y el bloqueo por reserva. En netlist se observa la respuesta MISO y la cartera; la observación directa de la última escritura corresponde al RTL.

La candidata también pasó A–F en RTL con 386 ticks por escenario. Compra en creciente y subida brusca, queda plana en descendente y lateral y completa un ciclo de compra y venta en caída y recuperación. Los CSV muestran el precio, SUM10, MISO y DECISION observados y señales de tendencia/momentum cotejadas con la referencia. El intérprete pasó 11 casos de fills forzados, incluidas compra de 1 y 63, caja insuficiente, venta parcial y descartar venta por comisión o falta de inventario. El timeout negativo de la prueba del banco salió con error, como se esperaba.

Las 36 pruebas Python y las 3 del ensamblador custom-0 aprobaron. La regresión heredada pasó los 11 tests Python y el core, y se detuvo en `periph_tb` por la expectativa histórica `debounced buttons`. SPI y decoder se ejecutaron por separado y aprobaron. `game_top` compiló.

El banco original de Windows completó **2.000/2.000 ticks** con el firmware MMIO base. Registró **4/4**, cero pérdidas, cero errores MISO y cero diferencias frente a Python. Quedó en $9.839, 109 órdenes y drawdown de $396. La peor latencia fue 253 de 2.262 ciclos y VVP tardó 583,62 s. Se conservó el aviso de carga de 71 palabras en un rango de 512. [Repetición original](../../resultados/mision_final_diagnostico/windows_2000_repeticion/)

[Métricas crudas por tick](build/rtl_practica_20000.csv) · [Log de 20.000 ticks](build/rtl_practica_20000.log) · [Pruebas de fills](build/equivalencia_hex.log) · [Resumen A–F y rondas largas](build/escenarios/resumen.csv) · [Regresiones](tb/pruebas_banco/regresion_general/)

## Implementación y firmas

Se ensamblaron 124 palabras RV32E y el verificador comprobó 44 transferencias directas de control, alineadas dentro del rango de ROM. La placa recibe 25 MHz en el pin 15 y el divisor entrega 12,5 MHz al SoC. Yosys y nextpnr cerraron la implementación HX1K/VQ100, semilla 1, con restricción de 25 MHz. La red del SoC obtuvo **50,85 MHz de Fmax**, **1.174/1.280 Logic Cells**, **1.060 LUT4** y **7/16 BRAM**. Deja 106 celdas libres y conserva la asignación SPI del PCF. [Yosys](build/yosys.log) · [nextpnr](build/nextpnr.log) · [Resumen](build/resultados.json)

| Artefacto | SHA-256 |
|---|---|
| `trade.s` | `B3E881DADF44BAF95D9A5ED524D2336B8FEAAD48D4066C6131EFEBDE176AD1A0` |
| `trade.hex` | `C9F3E12D2ACCAA15569F7FE4DE211B13F3F5A9DE4DD3E11DF1777D6C25A68114` |
| `build/competition.bin` | `F4008142A370D5ACD63506FB098FE7A6114A248753A1F862BB15204826AC175A` |

El BIN se generó después de aprobar RTL y netlist. Su tamaño es de 32.220 bytes. Se volvió a desempaquetar y empaquetar y coincidió byte por byte. Las copias `trade.s` y `trade.hex` tienen exactamente los bytes de las fuentes candidatas ensambladas. Los BIN, el firmware, el PCF y los datos previos coinciden con las huellas capturadas antes de empezar. [Comandos y prueba física manual](README.md)

El primer preflight directo en PowerShell perdió las comillas del parámetro de ruta de ROM y Yosys rechazó el valor. El ejecutor Python conserva ese argumento y completó el build.

## Estado de cierre

La candidata cuenta con equivalencia, validación RTL completa de práctica, pruebas de límites, síntesis y timing. La superioridad fuera de muestra frente a comprar y mantener quedó incumplida. La causa del resultado histórico de Fila 5 requiere trazabilidad de aquella sesión. La prueba física del nuevo BIN queda pendiente. El nombre `competition.bin` identifica el archivo preparado para ensayo de competencia en esta variante independiente.


