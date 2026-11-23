# Medicion de rendimiento de `trade.hex`

Se ejecutaron 20,000 ticks con el SoC RTL original y `EnableSpi=1`, a una cadencia personalizada de 30 us (750 ciclos por intervalo a 25 MHz). El periodo es menor que el de la ronda 3 (100 us) para reducir el tiempo de sondeo y verificar el caso de mayor demanda. No son tres corridas con los periodos oficiales.

## Instrumentacion y validez

IC se cuenta externamente con `dut.u_core.instr_valid_id && !dut.u_core.stall`, la condicion `commit` del Espino. No se agrego logica ni contador al core. Por tick, IC/ciclos/tiempo cubren `byte_done` hasta escritura de DECISION; CPI=ciclos/IC. Los contadores separan el polling STATUS previo a leer PRICE, el acceso PRICE, cartera, historial, SMA10 y comparaciones/DECISION. El tiempo postdecision hasta el siguiente `byte_done` se deriva del periodo menos la respuesta; en ese intervalo el core continua sondeando STATUS y sus IC no estan incluidos en la ventana de respuesta.

El banco comprobo 20,000 bytes MISO contra `decision_recibida` de Python, 20,000 lecturas PRICE y escrituras DECISION, cero ticks perdidos y cero discrepancias. El criterio de tick perdido verifica que `new_price_q` ya se haya limpiado antes del siguiente `byte_done`. El tiempo medido usa el `$time` de RTL y coincide con 40 ns por ciclo.

## Estadisticas por tick

Promedio, mediana, P95 (interpolacion lineal) y maximo sobre los 20.000 ticks.

| Medicion | Promedio | Mediana | P95 | Peor caso |
|---|---:|---:|---:|---:|
| IC comprometidas, byte_done a DECISION | 91.9 | 88.0 | 91.0 | 174.0 |
| Ciclos precio a DECISION | 219 | 210 | 217 | 412 |
| CPI total de respuesta | 2.380 | 2.382 | 2.402 | 2.409 |
| CPI posterior a PRICE | 2.377 | 2.373 | 2.386 | 2.393 |
| Tiempo de respuesta (us) | 8.75 | 8.40 | 8.68 | 16.48 |
| Ciclos de calculo posteriores a PRICE | 206 | 198 | 201 | 398 |
| Tiempo de calculo (us) | 8.25 | 7.92 | 8.04 | 15.92 |
| STATUS hasta lectura de PRICE (us) | 0.35 | 0.36 | 0.48 | 0.48 |
| Lectura MMIO PRICE (us) | 0.15 | 0.16 | 0.16 | 0.16 |
| Espera derivada hasta siguiente byte_done (us) | 21.25 | 21.60 | 21.76 | 28.36 |
| Actualizacion de cartera (ciclos) | 20 | 11 | 11 | 208 |
| Actualizacion historial (ciclos) | 12 | 12 | 13 | 21 |
| Suma SMA10 (ciclos) | 164 | 164 | 164 | 164 |
| Comparaciones y escritura DECISION (ciclos) | 11 | 11 | 11 | 14 |

## Presupuestos oficiales

La tabla compara la latencia respuesta precio a DECISION observada en la corrida de 30 us con los ciclos disponibles por ronda. Solo se ejecutaron los 20.000 ticks en la cadencia personalizada indicada; las rondas 1 y 2 no se simularon por separado. La cadencia de 30 us (750 ciclos) es mas estricta que el intervalo de ronda 3, y ninguna respuesta lo excedio.

| Ronda | Periodo | Presupuesto | Respuestas dentro del presupuesto | Margen minimo medido |
|---:|---:|---:|---:|---:|
| 1 | 10000 us | 250,000 ciclos | 20,000/20,000 | 249,588 ciclos |
| 2 | 1000 us | 25,000 ciclos | 20,000/20,000 | 24,588 ciclos |
| 3 | 100 us | 2,500 ciclos | 20,000/20,000 | 2,088 ciclos |

## Perfil de costo

SMA10 es la etapa dominante: 163.9 ciclos medios de 206.2 ciclos de calculo post-PRICE (79.5%). La suma de diez palabras requiere diez lecturas y acumulaciones; `10*precio` se arma con sumas. La actualizacion de cartera cuesta hasta 208 ciclos en tick 17, precio 166, debido a sus bucles de cantidad/efectivo. El peor precio a DECISION fue 412 ciclos, tick 9909, equivalente a 16.48 us. La lectura SPI completa (transaccion maestra) dura 9,5 us y ocurre antes de `byte_done`; CPU/status y calculo observados despues suman la latencia reportada.

El grafico `rendimiento_software.svg` muestra ciclos medios por seccion. El CSV contiene las mediciones por tick.

## Errores pendientes y limites

Icarus mostro el aviso esperado de `$readmemh`: `trade.hex` tiene 89 palabras frente a 512 palabras de RAM; las palabras restantes no se cargan desde el archivo. La medicion es RTL con reloj ideal y no mide temporizacion post-sintesis ni la Go Board. IC/ciclos no incluyen el sondeo STATUS despu?s de escribir DECISION; su duraci?n restante se reporta derivada del periodo. No se modificaron estrategia, assembler, ALU ni RTL.

## Reproduccion

Desde `pochoco_soc-main`:

```powershell
python -B proyecto4/python/medir_rendimiento_trade.py
python -B proyecto4/python/medir_rendimiento_trade.py --round 3
python -B -m unittest discover -s proyecto4/python -v
```

Sin `--round`, el script procesa 20.000 ticks a 30 us. `--round 1/2/3` solicita el periodo oficial y ejecuta la serie completa a esa cadencia; esas simulaciones tienen un costo alto en Icarus. `--ticks` permite depurar con una muestra corta.
