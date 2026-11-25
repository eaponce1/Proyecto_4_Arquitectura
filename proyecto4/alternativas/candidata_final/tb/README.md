> **Referencia de investigacion y validacion.** La imagen activa para programar se encuentra en la raiz del repositorio: [guia actual](../../../../README.md). Este directorio conserva fuentes que necesitan los comparadores y bancos; sus builds y documentos completos anteriores estan en el [historial previo](https://github.com/eaponce1/Proyecto_4_Arquitectura/tree/66eede4c46e211c02dc5ef22de18f86e22e775c5/proyecto4/alternativas/candidata_final/tb). Los comandos y resultados historicos de abajo no identifican el BIN vigente.

# Banco integral de la candidata

`tb_candidata.sv` instancia el top `trade_spi_externo`. El banco de RTL observa el Espino, el esclavo SPI, el acelerador SMA10 y la cartera emulada por la maestra. La opción `NETLIST` instancia el mismo top mapeado y verifica las salidas observables.

| Parámetro | Uso |
|---|---|
| `TICKS` | Número de precios del vector. |
| `FASE_NS` | Tiempo añadido a la espera inicial para variar la fase respecto del reloj de placa. |
| `PERIODO_NS` | Separación entre inicios de tramas. Por defecto 30.000 ns de estrés. |
| `PALABRAS_FIRMWARE`, `ARCHIVO_FIRMWARE` | Tamaño y ruta de la ROM. Se aplican al RTL. El netlist ya contiene la ROM elegida. |
| `REG_CAJA`, `REG_ACCIONES` | Registros RV32E de cartera, 0 a 15. Con −1 se desactiva el cotejo de ese registro. |

`+vectores=<directorio>` requiere tres archivos con una palabra hexadecimal de 8 bits por línea. `precios.hex` contiene los precios SPI de 1 a 255. `miso.hex` contiene la orden que ejecuta la maestra en cada tick. `escrituras.hex` contiene la decisión publicada por Espino para el tick siguiente.

`+cartera=<archivo>` habilita el cotejo de hasta tres magnitudes de la maestra por tick. El archivo usa 16 dígitos hexadecimales por línea. Los bits 63:32 son caja, 31:8 son patrimonio y 7:0 son acciones. El banco detecta valores que exceden ese formato.

`+metricas=<csv>` guarda MISO y DECISION observados en RTL, cantidad ejecutada, caja, acciones, comisiones acumuladas, patrimonio, drawdown, SUM10, lecturas de STATUS, IC, ciclos y CPI por tick. `+progreso=<n>` informa el avance cada `n` ticks. El valor 0 desactiva el avance. En modo netlist, la columna DECISION corresponde a la referencia y su transmisión se comprueba en el MISO del tick siguiente. El banco de netlist compara MISO y la cartera de todos los ticks probados.

## Relojes y medición

SPI se emula en modo 0, MSB primero y SCLK de 1 MHz. CS está bajo durante una trama de 9.500 ns. El primer MISO es 0x00 tras reset. La orden publicada tras analizar el precio de un tick se ejecuta al precio del tick siguiente.

El reloj de entrada de Go Board es 25 MHz. El divisor del top entrega 12,5 MHz al SoC, con 80 ns por ciclo. El análisis de síntesis exige 25 MHz de restricción en nextpnr. El presupuesto operativo del firmware corresponde a los 12,5 MHz.

| Ronda o ensayo | Período | Ciclos de SoC tras descontar la trama |
|---|---:|---:|
| Ronda 1 | 10 ms | 124.881 |
| Ronda 2 | 1 ms | 12.381 |
| Ronda 3 | 0,1 ms | 1.131 |
| Estrés acelerado | 0,03 ms | 256 |
| Estrés acelerado | 0,04 ms | 381 |

El intervalo medido va de `byte_done` a la escritura de DECISION. La cuenta de IC suma commits del Espino en ese intervalo y deja fuera el polling antes de llegar el byte. El CPI global usa la suma de ciclos dividida por la suma de instrucciones. Como la maestra envía precios desde otro reloj, el período y la fase del banco forman parte de cada resultado.

El monitor de RTL exige observar reset y arranque, una recepción, lectura PRICE, lectura SUM10, lectura READY y escritura por tick. Verifica las direcciones, el dato retornado por MMIO, la puesta y limpieza de `new_price` y el byte pendiente. Cuenta también coincidencias de STATUS y recepción, y verifica que la LSU retenga la carga sin duplicar el pulso de solicitud. Opcionalmente coteja el contenido de los registros de caja y acciones en el momento de DECISION.

## Prueba del banco

`probar_banco.py` usa los primeros 64 precios de práctica y el firmware MMIO SMA10 base. Comprueba las operaciones de 1 y 63 acciones, el llenado parcial por falta de caja, la venta parcial y la liquidación, un intento de venta sin inventario, la comisión, la acción reservada y el caso sin recursos para pagar comisión. La prueba de timeout impone deliberadamente un período insuficiente y exige que Icarus termine con error.

Desde la raíz de `pochoco_soc-main` con Icarus y OSS CAD Suite en el PATH:

```powershell
python -X utf8 -B proyecto4/alternativas/candidata_final/tb/probar_banco.py `
  --salida proyecto4/alternativas/candidata_final/tb/pruebas_banco `
  --netlist proyecto4/pruebas_fisicas/spi_externo_robusto/build/trade_netlist.v
```

La prueba de referencia pasó 64 ticks RTL al período de 100.000 ns, con 6 coincidencias de STATUS y `byte_done` y 262 cargas internas mantenidas. Pasaron el modelo de contabilidad y el ensayo negativo de timeout. La simulación con el netlist base pasó los 64 ticks con período de estrés de 30.000 ns y fase inicial de 41 ns.

