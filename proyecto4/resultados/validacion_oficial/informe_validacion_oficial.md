# Validación oficial final — Proyecto 4

## Alcance y archivos de entrada

Se usó el `tb_proyecto_4.sv` adjunto en esta conversación y el CSV `practica_meta.csv` adjunto. Se guardaron copias inalteradas como `tb_proyecto_4_profesor.sv` y `practica_meta.csv`. SHA-256 del testbench (adjunto y copia): `f83486755fe2b3de385a2bdc39c2f275b9dd690342fb4fc0391401706876f8f3`. SHA-256 del CSV (adjunto, copia de validación y `proyecto4/data/practica_meta.csv`): `fed122e0a9861276d76b1396b264fd34077c280c80fe6b356b6971d55242da3f`.

El CSV tiene encabezado `tick,price` y 20.000 filas consecutivas; los ticks son 0–19.999 y todos los precios caben en un byte. Se verificó que el adjunto es idéntico a la serie ya versionada del proyecto.

## Conservación del testbench oficial

El testbench del profesor se conserva byte a byte. Su configuración original era de 2.000 ticks, apuntaba a `sw/trade.hex` y `tb/practica.csv`, y omitía el parámetro SPI. El SoC original tiene `EnableSpi=0` por omisión, así que esa configuración no valida el SPI.

Para correrlo sin editar el original, `ejecutar_validacion.py` genera una copia de ejecución en cada carpeta de corrida. Solo adapta las rutas, fija `NTICKS=20000`, fija el período de ronda, apunta al HEX correcto y pasa `.EnableSpi(1)`. Añade un acumulador observacional de ciclos de respuesta. El bloque contable `ejecutar` se comprobó idéntico entre original y copia; también se comprobó que las cuatro expresiones oficiales aparecen una vez y sin cambios:

1. `bits_x == 0` — MISO no contiene X.
2. `respuestas > 0` — se observa que el firmware escribe DECISION.
3. `precios_perdidos == 0` — no queda un precio anterior sin consumir al llegar el siguiente.
4. `peor_caso < presupuesto` — la respuesta precede el siguiente tick según el presupuesto que calcula el propio TB.

El testbench publicado no compara el valor de cada DECISION contra Python ni imprime compras/ventas o comisiones. Las decisiones por tick y la contabilidad se obtienen de su `decisiones.csv`; compras, ventas y comisión se derivan y se cotejan contra el contador oficial de órdenes.

## Resultados completos: ronda 3

Periodo de tick: 100.000 ns (0,1 ms). El TB descuenta 9.500 ns para SPI y calcula `presupuesto = (100000-9500)/40 = 2262` ciclos. Cada variante ejecutó 20.000 transacciones con el mismo CSV, testbench, reloj de 25 MHz y contabilidad inicial.

| Métrica | MMIO SMA10 base | Software original |
|---|---:|---:|
| Ticks/fila de `decisiones.csv` | 20.000 | 20.000 |
| Criterios oficiales | **4/4 PASS** | **4/4 PASS** |
| Patrimonio final | $4.577 | $4.577 |
| Caja final | $2.017 | $2.017 |
| Acciones finales | 16 | 16 |
| Órdenes ejecutadas | 931 | 931 |
| Compras ejecutadas | 466 | 466 |
| Ventas ejecutadas | 465 | 465 |
| Comisiones ($5/orden) | $4.655 | $4.655 |
| Drawdown máximo | $5.476 | $5.476 |
| Ciclos promedio, TB de ejecución | 60 ciclos* | 218 ciclos* |
| Peor caso precio→DECISION | 255 ciclos | 413 ciclos |
| Presupuesto oficial | 2.262 ciclos | 2.262 ciclos |
| Decisiones distintas entre variantes | 0/20.000 | 0/20.000 |

`*` El testbench del profesor solo informa el peor caso. La copia de ejecución acumula ciclos, pero la primera corrida registrada imprimió el promedio mediante división entera (`longint/respuestas`): 60 y 218 son promedios truncados hacia abajo; solo se puede afirmar `60 ≤ promedio < 61` y `218 ≤ promedio < 219` para las corridas oficiales. Los CSV de rendimiento anteriores registran 60,6398 y 218,6635 ciclos/tick a intervalo custom de 30 μs; se citan únicamente como referencia separada, no como promedio exacto de esta corrida oficial. El peor caso software anterior difiere en un ciclo (412 vs. los 413 oficiales), así que no se mezcla esa precisión con el resultado oficial. La contabilidad y secuencia de decisiones de las dos corridas oficiales sí coinciden tick a tick.

El patrimonio por tick, caja, acciones, compras/ventas y drawdown se deriva de la contabilidad oficial del testbench. Se verificó `466+465=931` órdenes y `931×$5=$4.655`; la caja y las acciones permanecen según los límites de esa misma contabilidad. Las dos referencias de cartera que imprime el TB son: no operar `$10.000`; comprar y mantener `$9.695`.

### Cuatro comprobaciones por implementación

| Check oficial | MMIO base | Software original |
|---|---|---|
| MISO sin valores X | PASS | PASS |
| Se observó escritura DECISION | PASS | PASS |
| No se perdieron precios | PASS | PASS |
| DECISION antes del próximo tick | PASS, 255 < 2262 | PASS, 413 < 2262 |

El aviso `$readmemh: Not enough words` es esperado: el HEX contiene menos de 512 palabras de RAM; la carga termina correctamente y los cuatro checks pasan.

## Rondas 1 y 2

**Pendientes; no se ejecutaron.** La instrucción condicional de ejecutarlas quedó activada porque ronda 3 pasó. En esta máquina, los archivos de corrida registran aproximadamente 7 h 38 min para MMIO ronda 3 y 2 h 30 min para software ronda 3. Icarus evalúa continuamente el reloj RTL durante el sondeo STATUS. Una extrapolación lineal por ciclos (no medida) lleva ronda 2 a aproximadamente 10× esos tiempos y ronda 1 a 100×: del orden de 25–76 horas para ronda 2 y 10–32 días para ronda 1, por variante. No es razonable presentar como terminadas corridas que no se han ejecutado ni sustituirlas por una estimación o una serie parcial. No reporto PASS para ninguna de las dos rondas.

Los comandos para continuarlas con el runner reproducible están abajo. Cuando se ejecuten, se deben correr las dos variantes para que la comparación mantenga iguales condiciones.

## Comparación y diagnóstico

En ronda 3, software original y MMIO SMA10 base tuvieron resultados de inversión idénticos tick a tick: el acelerador no cambió la señal, el desfase ni el comportamiento contable observado. MMIO reduce el promedio reportado en aproximadamente 158 ciclos y el peor caso en 158 ciclos (`413-255`), manteniendo 1.849 ciclos de margen respecto del presupuesto oficial. La cartera acabó en pérdida frente a no operar; el resultado no es una recomendación financiera.

El banco oficial valida solo sus cuatro condiciones enumeradas. No incluye una comparación Python tick a tick, no cuenta STATUS/PRICE/DECISION individualmente y no detecta un valor DECISION erróneo si sigue siendo una señal MISO válida. La comparación de las dos implementaciones no presentó diferencias; las pruebas previas de equivalencia Python se documentan por separado. La prueba se ejecutó en RTL, no en la Go Board física.

## Comandos reproducibles

Desde la raíz `pochoco_soc-main`:

```powershell
python -B proyecto4/resultados/validacion_oficial/ejecutar_validacion.py --variant mmio --round 3
python -B proyecto4/resultados/validacion_oficial/ejecutar_validacion.py --variant software --round 3
python -B proyecto4/resultados/validacion_oficial/resumir_corridas.py
```

Para ronda 2 y ronda 1, repetir con `--round 2` y `--round 1` en ambas variantes. El runner falla si no se imprimen los cuatro checks aprobados o no se genera el CSV esperado. `iverilog` y `vvp` deben estar en PATH.

## Artefactos

- `tb_proyecto_4_profesor.sv`: original sin cambios.
- `practica_meta.csv`: serie oficial, copia idéntica al original.
- `decisiones.csv`: salida principal seleccionada (MMIO base, ronda 3).
- `corridas/mmio_sma10_base/ronda_3/`: fuente adaptada, log de compilación, log de simulación, ejecutable y 20.000 decisiones.
- `corridas/software_original/ronda_3/`: mismos artefactos para la comparación software.
- `comparacion_oficial.csv`: resumen de ambas corridas completas.
- `ejecutar_validacion.py` y `resumir_corridas.py`: comandos automatizados y cálculo de métricas derivadas.

No se modificaron RTL, Assembly, HEX, assembler ni los resultados históricos de otras etapas. No se creó commit ni push.
