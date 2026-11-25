# Selección de estrategia agresiva

La política congelada fue **momentum con exposición objetivo del 100 %, compra directa, revisión cada 16 ticks y umbral de 8**. En el tramo reservado terminó con $9.265, por debajo de comprar y mantener. Los máximos observados del tramo reservado se registran como evidencia posterior a la selección.

## Datos y protocolo

Se usaron 12.000 ticks de entrenamiento, 4.000 de validación y los últimos 4.000 de prueba. Cada tramo empieza con caja de $10.000, cero acciones y estado vacío. La corrida completa empieza una sola vez y conserva su estado en los cortes. Todas las políticas usan la contabilidad del simulador del proyecto. El byte decidido al cerrar un tick se ejecuta al precio del siguiente. La maestra ajusta las compras al saldo disponible después de la comisión. Una orden ejecutada cuesta $5.

Antes de leer resultados del tramo reservado se probaron 384 configuraciones en entrenamiento. La grilla combina cuatro familias, cuatro exposiciones, dos tamaños de entrada, cuatro cadencias y tres umbrales. Se conservaron 32 finalistas, una por familia, exposición y modo de entrada. El techo de drawdown fue $5.000 por tramo. El presupuesto de comisiones fue $1.000 en entrenamiento y $400 en validación. El drawdown y las comisiones se usan como filtros. El ranking prioriza la diferencia de patrimonio frente a comprar y mantener y rompe empates con el resultado de entrenamiento.

La selección se congeló con `--fase seleccionar` y el tramo reservado se evaluó en una segunda ejecución. El simulador usa solo precios observados. Se comprobó que la ejecución de los prefijos de 12.000 y 16.000 ticks produce las mismas decisiones que la corrida completa hasta cada corte. [Selección congelada](resultados/seleccion.json) · [Grilla de entrenamiento](resultados/grilla_entrenamiento.csv) · [Pruebas del backtest](resultados/verificacion_backtest.log)

## Señales, cantidad y exposición

| Familia | Entrada | Salida |
|---|---|---|
| Momentum | Cambio al alza entre precios de dos revisiones | Cambio a la baja de magnitud suficiente en una revisión |
| Breakout | Superación del máximo de cuatro revisiones previas | Ruptura del mínimo de las mismas revisiones |
| Tendencia y trailing | Momentum en revisión | Caída de momentum en revisión o descenso suficiente desde el pico con confirmación SMA10, comprobada cada tick |
| Híbrida | Momentum con confirmación SMA10 en revisión | Momentum bajista confirmado por SMA10 o stop del pico confirmado cada tick |

La cadencia toma 16, 32, 64 o 128 ticks. El umbral toma 2, 4 u 8 puntos de precio y el stop se activa a una distancia de `8 + 2*umbral` del pico, con `10*p - SUM10 <= 0`. El inventario se mantiene entre señales. Una salida activa el envío de una orden de hasta 63 acciones por tick hasta vaciar la posición.

El objetivo se calcula marcando la posición a precio actual. Para `k = exposición/25`, la cantidad objetivo es `floor(k*(caja+acciones*precio)/(4*precio))`. La compra solicita el mínimo entre el faltante, las acciones pagables al precio observado tras reservar $5 y el límite 63. La ejecución al precio siguiente puede recortar cantidades. En modo directo se entra desde una posición plana. El progresivo permite añadir sobre una posición abierta. Limita la orden moderada a 16, permite hasta 63 con una señal fuerte e ignora incrementos menores a 4 acciones cuando ya hay posición. La exposición realizada puede diferir del objetivo por el tope, el precio de ejecución o el escalonamiento. Un escenario sintético ejercitó 111 acciones acumuladas y su liquidación mediante órdenes de 63 y 48 en dos ticks consecutivos.

## Resultado de la política congelada

| Tramo | Agresiva | No operar | Comprar y mantener ejecutable | Diferencia frente a ejecutable | Referencia teórica del profesor |
|---|---:|---:|---:|---:|---:|
| Entrenamiento, 12.000 | $15.965 | $10.000 | $13.055 | +$2.910 | $13.055 |
| Validación, 4.000 | $10.000 | $10.000 | $6.177 | +$3.823 | $6.177 |
| Prueba reservada, 4.000 | $9.265 | $10.000 | $11.633 | −$2.368 | $11.919 |
| Completa, 20.000 | $15.232 | $10.000 | $9.695 | +$5.537 | $9.695 |

La referencia teórica del profesor permite usar toda la caja en su compra inicial. Con el reinicio en el tick 16.000, el precio inicial de 134 permite 74 acciones en esa referencia y solo 63 en la ejecutable. Frente a la referencia teórica, la pérdida relativa de la candidata en ese tramo fue de $2.654.

| Tramo | Compras | Ventas | Comisiones | Drawdown | Acciones finales |
|---|---:|---:|---:|---:|---:|
| Entrenamiento | 2 | 2 | $20 | $1.459 | 0 |
| Validación | 0 | 0 | $0 | $0 | 0 |
| Prueba reservada | 4 | 4 | $40 | $1.865 | 0 |
| Completa | 6 | 6 | $60 | $3.558 | 0 |

En la corrida completa las 12 órdenes ejecutaron 63 acciones cada una. La primera compra llegó a MISO en el tick 3.249 y la primera venta en el 3.953, contando desde cero. La segunda posición se mantuvo desde el tick 4.737 hasta el 11.361 durante 6.624 ticks.

## Resultado reservado de las exposiciones alternativas

Máximo patrimonio observado entre las finalistas congeladas de cada exposición y modo. Las celdas se computaron después de congelar. La selección permaneció en momentum directo de 100 %.

| Exposición objetivo | Mejor directa | Mejor progresiva |
|---|---:|---:|
| 25 % | $10.198 | $10.198 |
| 50 % | $10.422 | $10.831 |
| 75 % | $10.630 | $10.470 |
| 100 % | $10.854 | $10.620 |

Ninguna de las 32 finalistas superó comprar y mantener en el tramo reservado. La mejor de ese tramo fue breakout directa con exposición objetivo de 100 %, que terminó $779 por debajo de la referencia ejecutable y $1.065 por debajo de la teórica. La corrida completa muestra capacidad de aprovechar tendencias con comisiones bajas. La ventaja fuera de muestra sigue sin demostrarse. [Comparación con referencias](resultados/comparacion.csv) · [Todas las familias, tamaños y exposiciones](resultados/finalistas_todas_exposiciones.csv) · [Decisiones por tick](resultados/decisiones_tick.csv)

## Reproducir

La selección existente se abre en modo exclusivo. Para repetir ajustes desde cero, elegir una carpeta de salida nueva. Para repetir la evaluación desde el JSON congelado, ejecutar:

```powershell
python -X utf8 -B proyecto4/alternativas/agresiva/backtest_agresiva.py --fase evaluar
```

