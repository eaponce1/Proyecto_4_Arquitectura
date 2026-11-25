> **Referencia de investigacion y validacion.** La imagen activa para programar se encuentra en la raiz del repositorio: [guia actual](../../../README.md). Este directorio conserva fuentes que necesitan los comparadores y bancos; sus builds y documentos completos anteriores estan en el [historial previo](https://github.com/eaponce1/Proyecto_4_Arquitectura/tree/66eede4c46e211c02dc5ef22de18f86e22e775c5/proyecto4/pruebas_fisicas/spi_externo_robusto). Los comandos y resultados historicos de abajo no identifican el BIN vigente.

# Reprueba de SPI externo en Go Board

## Práctica física en Fila 2

En la práctica **Tesla ene 2022**, el grupo ocupó la **Fila 2**. La captura en curso muestra $6.321. La pantalla de resultados muestra **$5.329**, **8.º de 8**, y **−46,7 %** frente a comprar al inicio y mantener ($9.995). La diferencia fue de $4.666.

Con caja inicial de $10.000 y cero acciones, el patrimonio de $5.329 indica que la maestra contabilizó órdenes en esa fila. Para cotejar la ejecución con Python quedan por obtener la serie exacta de Tesla, el registro de MISO por tick y el hash del BIN cargado. El conteo de órdenes y las comisiones de esa sesión también quedan por confirmar.

La observación previa de **Apple, F7 (`JD arriba`)** corresponde a otro ensayo. Allí se registraron $10.000 y cero órdenes. Su precio final visible fue 124. El CSV de práctica del repositorio termina en 160 y produjo 931 órdenes en la validación RTL de 20.000 ticks.

## Candidato para la prueba en placa

`trade_spi_externo` usa el SPI Slave y SMA10 de MMIO base, el mismo `trade.hex` de 71 palabras y el camino de ejecución de la demo autónoma aprobada. Reutiliza su ROM de instrucciones en lógica, fetch acotado, reloj del SoC a 12,5 MHz y reset registrado tras 1.024 ciclos. Conecta directamente el SPI externo y usa los cuatro LEDs para observar hitos. Las salidas de displays y el maestro interno de la demo quedan fuera de este top. El firmware sigue generando la decisión.

La guía de Lattice especifica las entradas de reloj y habilitación de los bloques BRAM. La ROM en lógica retira los BRAM del fetch de instrucciones de este diseño, mientras el banco de registros y el historial SMA10 siguen usando BRAM. [Guía de memoria iCE40](https://www.latticesemi.com/~/media/LatticeSemi/Documents/ApplicationNotes/MP2/FPGA-TN-02002-1-7-Memory-Usage-Guide-for-iCE40-Devices.ashx?document_id=47775)

| Indicador | Se queda encendido después de |
|---|---|
| D1 | Primer commit de Espino. |
| D2 | Primer byte completo recibido por SPI. |
| D3 | Primera lectura PRICE del Espino. |
| D4 | Primera escritura DECISION con un byte distinto de cero. |

Con los primeros 51 precios del CSV de práctica, la maestra debe leer `0x50` en el tick 17 y `0x90` en el 50, contando desde cero. Si D4 se enciende pero la maestra lee cero en esos ticks, medir PS3 en la Go Board y la entrada de la maestra. Si hay D2 y falta D3, comprobar el arranque del Espino y la lectura PRICE. Si solo hay D1, comprobar MOSI, SCLK, CS_n y GND. Con una serie sin señales válidas, D1, D2 y D3 encendidos con D4 apagado es un resultado posible.

| PMOD de la Go Board | Señal | Pin FPGA |
|---|---|---:|
| PS1 | CS_n | 65 |
| PS2 | MOSI | 64 |
| PS3 | MISO hacia la entrada del grupo | 63 |
| PS4 | SCLK | 62 |

Usar GND común, señales de 3,3 V y alimentación de la Go Board por USB. Confirmar con Chen el canal MISO antes de conectar. El banco prueba SPI modo 0, 8 bits MSB primero, 1 MHz y período de 100.000 ns.

## Resultados y reproducción

| Métrica | MMIO base | Candidato SPI externo |
|---|---:|---:|
| Reloj del SoC | 25 MHz | 12,5 MHz |
| Logic Cells | 1.279 / 1.280 | 1.062 / 1.280 |
| LUT4 | 1.055 | 949 |
| BRAM | 13 / 16 | 7 / 16 |
| Fmax post-route del SoC | 40,50 MHz | 54,30 MHz |
| Peor latencia en los primeros 2.000 ticks | 253 ciclos, 10,12 µs | 254 ciclos, 20,32 µs |
| Presupuesto efectivo a 0,1 ms | 2.262 ciclos | 1.131 ciclos |

La simulación RTL cotejó 2.000 precios, accesos PRICE/SUM10/READY, escrituras DECISION y bytes MISO con Python. La reducción de reloj incrementa la latencia absoluta y deja 877 ciclos de holgura en el peor caso medido. El flujo aplica una restricción de 25 MHz a las redes en nextpnr. Los resultados de área, tiempo y validación de netlist se guardan en `build/`. La simulación de netlist usa primitivas lógicas y varias fases de SPI. Para atribuir el ensayo físico de Fila 2 a este BIN se requiere verificar su hash en la placa.

Los cuatro ensayos del netlist pasaron 64 transferencias cada uno con desplazamientos de fase de 0, 19, 41 y 63 ns. En RTL, los primeros 16 ticks también pasaron en fase 27 ns con LEDs `0111`, el patrón que corresponde a una secuencia que todavía no produce una orden. Los ensayos cortos registran avisos de `$readmemh` porque toman un prefijo de los vectores de 2.000 ticks. La suite Python del Proyecto 4 aprobó 32/32 pruebas.

El BIN resultante tiene SHA-256 `745D4437FA71A3CF0D3933E17F2670EC97F7134D7629C78570469CE15DBD9200`. [Resumen de medidas y hash](build/resultados.json)

Desde la raíz, con Python y OSS CAD Suite en PATH:

```powershell
python -X utf8 -B proyecto4/pruebas_fisicas/spi_externo_robusto/validar.py
```

Si existe un BIN en `build/`, indicar otro directorio con `--salida`. Se puede pasar la serie real de 20.000 filas de Chen con `--serie` para probar su prefijo. El BIN se empaqueta después de aprobar RTL, netlist y enrutado. Para programarlo manualmente una vez validado, con la maestra desconectada:

```powershell
$p = 'proyecto4/pruebas_fisicas/spi_externo_robusto/build'
Get-FileHash -Algorithm SHA256 "$p/trade_spi_externo.bin"
iceprog "$p/trade_spi_externo.bin"
iceprog -c "$p/trade_spi_externo.bin"
```

## Experimento de menor rotación

El SMA10 base pagó 4.655 en comisiones sobre 931 órdenes en la práctica publicada. Se evaluaron reglas fijas con menos señales. Todas conservan el desfase de un tick y usan el mismo simulador contable. Cada bloque de 5.000 ticks parte de caja e historial iniciales. Los bloques pertenecen a la misma serie de práctica.

| Estrategia | Patrimonio final, 20.000 ticks | Órdenes | Comisiones | Drawdown |
|---|---:|---:|---:|---:|
| No operar | 10.000 | 0 | 0 | 0 |
| Comprar y mantener | 9.695 | 1 | 5 | 9.300 |
| SMA10 base | 4.577 | 931 | 4.655 | 5.476 |
| SMA10 con umbral de 4 | 9.843 | 41 | 205 | 1.832 |
| SMA10 evaluada cada 64 ticks | 9.960 | 40 | 200 | 1.356 |
| Tendencia de 256 ticks evaluada cada 64 | 8.454 | 50 | 250 | 1.936 |

Las dos SMA10 de menor rotación superaron a la base en los cuatro bloques. El umbral 4 superó el capital inicial en tres de ellos. La evaluación cada 64 ticks tuvo el menor drawdown entre las estrategias activas de la serie completa. Ambas terminaron por debajo de 10.000 en la trayectoria completa. Son candidatas de investigación para medir con datos nuevos. La imagen de SPI externo ejecuta el SMA10 base para permitir comparaciones de extremo a extremo.

```powershell
python -B proyecto4/python/investigacion_baja_frecuencia.py
```

[CSV de las seis evaluaciones cronológicas](../../resultados/ensayo_baja_frecuencia.csv)

## Firmware de conservación y de riesgo acotado

Hay dos programas RV32E para el mismo top de SPI externo. Cada uno lee PRICE, SUM10 y READY y escribe una DECISION por tick. Ambos usan el desfase SPI original y se construyen en carpetas independientes.

| Modo | Programa | Regla |
|---|---|---|
| Conservar | `sw/conservar.s` | Emite `0x00` en cada tick. Desde una cartera plana conserva $10.000 y paga $0 en comisiones. |
| Activo | `sw/activo.s` | Reversión SMA10 cada 64 ticks con margen de 4 unidades. Compra y vende un lote fijo de 3. Solo compra con caja de al menos $9.775. |

Con la contabilidad de la maestra, la primera compra reduce el patrimonio en $5 de comisión porque las acciones se valoran al mismo precio de ejecución. El verde estricto frente a $10.000 exige permanecer plano. Las posiciones de otros grupos y la referencia de comprar y mantener pueden subir.

El modo activo reserva $9.000 más el coste máximo de 3 acciones a $255 y dos comisiones de $5. Tras comprar quedan por lo menos $9.005 en caja, y tras vender quedan al menos $9.000. Mientras haya posición, esta tiene valor no negativo. El piso se aplica respecto del capital inicial para precios de 1 a 255 y ejecución sincronizada, con cada orden ejecutada como máximo una vez según el calendario SPI. El máximo drawdown desde un pico puede superar la distancia entre el capital inicial y el piso.

| Modo | Patrimonio final de práctica | Mínimo observado | Órdenes | Comisiones | Drawdown |
|---|---:|---:|---:|---:|---:|
| SMA10 base | $4.577 | $4.577 | 931 | $4.655 | $5.476 |
| Conservar | $10.000 | $10.000 | 0 | $0 | $0 |
| Activo | $10.224 | $9.947 | 2 | $10 | $96 |

Los cuatro bloques independientes de 5.000 ticks del activo cerraron en $10.000, $10.000, $9.923 y $10.000. El beneficio de la serie completa corresponde a una compra y una venta. Para evaluar la generalización hace falta otra serie. La foto de Fila 2 de Tesla carece de los precios por tick necesarios para repetirla. [Comparación medible de práctica](../../resultados/capital_protegido.csv)

En la referencia de Python se verificó la reserva con las 65.025 combinaciones de precios de compra y venta. El intérprete cotejó las decisiones y MISO de los dos HEX durante los 20.000 ticks de práctica. También cotejó caja y acciones del activo. El vector sintético de reserva fuerza compra de tres a 255, venta de tres a 1 y bloqueo de una segunda compra. Su caja final esperada es $9.228. Este vector comprueba el firmware y el protocolo bajo un caso límite.

| Modo | Icarus RTL | Netlist a 0 y 41 ns de fase | Logic Cells | LUT4 | BRAM | Fmax | Peor latencia RTL |
|---|---|---|---:|---:|---:|---:|---:|
| Conservar | 2.000 precios de práctica | 16 precios de práctica por fase | 749 | 632 | 7 | 52,42 MHz | 24 ciclos, 1,92 µs |
| Activo | 2.000 precios de práctica y 194 ticks de reserva | 194 ticks de reserva por fase | 966 | 854 | 7 | 51,78 MHz | 52 ciclos, 4,16 µs |

Los dos RTL pasaron a 100 µs por tick con presupuesto de 1.131 ciclos de SoC. El netlist Conservar usó 100 µs por tick. El netlist Activo usó 24 µs por tick y SPI a 1 MHz para cubrir la compra y la venta sintéticas en ambas fases. Yosys, nextpnr con restricción de 25 MHz e icepack aprobaron para HX1K/VQ100. La suite Python pasó 36/36. La validación física de estas dos imágenes queda pendiente.

Para reproducir en Windows con Python, Icarus y OSS CAD Suite:

```powershell
$p = 'proyecto4/pruebas_fisicas/spi_externo_robusto'
python -B proyecto4/python/capital_protegido.py
python -B -m unittest discover -s proyecto4/python -v
python -X utf8 -B "$p/validar.py" --modo conservar
python -X utf8 -B "$p/validar.py" --modo activo
```

Para una compilación adicional usa otro directorio con `--salida`. Cada directorio `build_conservar` o `build_activo` contiene el HEX ensamblado, los logs de RTL/netlist, síntesis, enrutado y empaquetado, el resumen `resultados.json` y el BIN del modo.

Los LEDs conservan la tabla de este top. En Conservar, D4 queda apagado porque cada decisión es cero. D1–D3 permiten verificar arranque, recepción de un byte y lectura PRICE. En Activo, D4 se enciende al aparecer la primera orden. El retorno MISO debe cotejarse en la maestra.

| BIN | SHA-256 |
|---|---|
| [trade_conservar.bin](build_conservar/trade_conservar.bin) | `5F3C32E0AC266614B4B8FE825672255D7D29BF924CE51D3BB3E249516E052FC1` |
| [trade_activo.bin](build_activo/trade_activo.bin) | `5871E56055BB12359373F22A750B41E7037B91B44180668157AA7A6E9B7CB89F` |

Para instalar Conservar, ejecutar con la Go Board conectada por USB y la maestra desconectada. Usar el segundo BIN únicamente si se quiere habilitar trading con el piso de $9.000.

```powershell
$bin = 'proyecto4/pruebas_fisicas/spi_externo_robusto/build_conservar/trade_conservar.bin'
Get-FileHash -Algorithm SHA256 $bin
iceprog $bin
iceprog -c $bin
```


