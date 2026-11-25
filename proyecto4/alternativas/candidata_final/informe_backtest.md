# Evaluación cuantitativa de la candidata RV32E

La candidata adaptativa terminó con **$10.198** en la serie de práctica completa y superó comprar y mantener por **$503**. En la prueba temporal reservada obtuvo **$10.000 con cero órdenes**, frente a **$11.633** de comprar y mantener. La imagen es una candidata de ingeniería. Estos datos no acreditan una ventaja fuera de muestra sobre la referencia.

## Datos y contabilidad

Se usaron las 20.000 filas consecutivas de `proyecto4/resultados/validacion_oficial/practica_meta.csv`. La caja inicial es $10.000, el inventario inicial es cero, la comisión es $5 por orden ejecutada y el máximo codificable es 63. Se valora `W = caja + inventario × precio`; el drawdown es la mayor diferencia desde el máximo previo, incluyendo el capital inicial. La referencia de comprar al inicio y mantener emite una compra inicial de hasta 63, limitada por caja.

En el tick `t` se ejecuta al precio actual la orden calculada con precios hasta `t−1`. Después se incorpora el precio `t`, se actualiza el estado y se calcula la orden que viajará por MISO al tick siguiente. El backtest conserva los límites y los fills parciales a través del simulador del repositorio.

## Selección y alcance temporal

- **Desarrollo (60 %)**: ticks 0 a 11.999. Se cribaron 480 combinaciones de período 32/64/128/256/512, entrada y salida, confirmación corta, dos tamaños de inventario y reserva de caja. La confirmación usa SMA10, el acelerador de hardware presente.
- **Validación (20 %)**: ticks 12.000 a 15.999, con caja, historial e inventario reinicializados. Se exigió desarrollo ≥$10.000, al menos cuatro órdenes, drawdown de desarrollo ≤$1.700, cada tercio de desarrollo ≥$9.600 y validación ≥$9.700. Resultaron 154 configuraciones admisibles. El puntaje fue `(V−10000) + 0,35(D−10000) + 0,20(mediana_dev−10000) − 0,20(peor_DD)`. La candidata obtuvo 466,80 puntos. El horizonte 128, la banda ±8 y los tamaños 32/63 quedaron congelados antes de evaluar el segmento final.
- **Prueba (20 %)**: ticks 16.000 a 19.999 con arranque independiente. Aquí se evalúa la selección congelada. Los 20.000 ticks completos también se simulan en una pasada encadenada para reproducir el comportamiento de placa.
- **Walk-forward**: cinco períodos futuros de 2.000 ticks entre 6.000 y 15.999. Cada período recibe parámetros ajustados en el pasado expansivo y una validación inmediatamente anterior de 2.000 ticks. El modelo volvió a empezar en cada período de prueba. Las diferencias frente a comprar y mantener fueron −1.696, −653, +425, +971 y +2.072. La familia superó la referencia en tres de cinco y preservó capital en dos. 
- **Sensibilidades de desarrollo**: se midieron límites fuertes de 1 a 63 acciones. También se probaron salidas por caída de 12, 24 y 36 unidades desde el máximo mientras se mantiene posición. Umbral 12 redujo el drawdown de desarrollo de 1.006 a 830 y dejó el patrimonio de desarrollo en 10.731, frente a 11.792. Se conserva la salida por tendencia del candidato.

El histórico disponible pertenece a una sola trayectoria. La prueba reservada quedó excluida de este selector. El repositorio ya contiene análisis anteriores de la serie completa. Se necesita otra serie íntegra para evaluar generalización. Las fotos de resultados de Tesla y Apple carecen de las series por tick que permitirían repetirlas.

## Política desplegable

Cada 128 ticks, se compara el precio con el precio guardado en la revisión anterior. El primer precio solo inicializa el ancla. La confirmación de momentum se calcula como `10×precio − SUM10`, con ventana que incluye el precio actual. Se evalúa siempre sobre una cartera local que aplica la orden pendiente a precio actual antes de decidir la siguiente.

- **Compra** estando plano si la tendencia es al menos +8 y el momentum es no negativo. La posición objetivo es 32 ante una subida de 8 a 15 y 63 a partir de 16. La cantidad solicitada es el mínimo entre objetivo y `max(0, floor((caja−510)/255))`.
- **Salida total** si la tendencia es −8 o inferior, o si es negativa y el momentum también es no positivo.
- **Mantener** fuera de las revisiones y entre las bandas. Una sola compra abre posición y la salida vende lo que se posee. Las señales repetidas estando largo solo conservan el inventario.

La compra reserva $500, el peor precio posible y dos comisiones. Con ejecución sincronizada y precios válidos de 1 a 255, deja caja de al menos $505 mientras exista posición y de al menos $500 tras liquidar, incluso si la venta neta consume caja por la comisión. El máximo objetivo de 63 acota el byte y la estrategia se mantiene exclusivamente larga o plana. El firmware opera con sumas, restas y comparaciones sobre las magnitudes enteras.

## Resultados

| Estrategia | Patrimonio, 20.000 ticks | Retorno | Frente a mantener | Compras / ventas | Órdenes | Comisiones | Drawdown | Acciones | Caja |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| No operar | $10.000 | 0,00 % | +$305 | 0 / 0 | 0 | $0 | $0 | 0 | $10.000 |
| Comprar y mantener | $9.695 | −3,05 % | $0 | 1 / 0 | 1 | $5 | $9.300 | 60 | $95 |
| SMA10 base | $4.577 | −54,23 % | −$5.118 | 466 / 465 | 931 | $4.655 | $5.476 | 16 | $2.017 |
| Protección anterior | $10.224 | 2,24 % | +$529 | 1 / 1 | 2 | $10 | $96 | 0 | $10.224 |
| Cruce medias 10/40 | $9.898 | −1,02 % | +$203 | 15 / 15 | 30 | $150 | $1.346 | 0 | $9.898 |
| Momentum 128 | $8.772 | −12,28 % | −$923 | 30 / 30 | 60 | $300 | $1.914 | 0 | $8.772 |
| Ruptura 64 | $9.036 | −9,64 % | −$659 | 2 / 2 | 4 | $20 | $1.722 | 0 | $9.036 |
| Reversión filtrada | $11.238 | 12,38 % | +$1.543 | 1 / 1 | 2 | $10 | $512 | 0 | $11.238 |
| Híbrida fija 16 | $10.224 | 2,24 % | +$529 | 8 / 8 | 16 | $80 | $783 | 0 | $10.224 |
| **Adaptativa RV32E** | **$10.198** | **1,98 %** | **+$503** | **8 / 8** | **16** | **$80** | **$1.983** | **0** | **$10.198** |

| Segmento | Candidata | Comprar y mantener | Diferencia | Órdenes candidata | Drawdown candidata |
|---|---:|---:|---:|---:|---:|
| Desarrollo | $11.792 | $13.055 | −$1.263 | 14 | $1.006 |
| Validación | $10.000 | $6.177 | +$3.823 | 0 | $0 |
| Prueba | $10.000 | $11.633 | −$1.633 | 0 | $0 |

En el último 20 %, ninguna política activa de la tabla superó comprar y mantener. La reversión filtrada obtuvo el mayor patrimonio entre las activas en la prueba ($11.238), con una compra y una venta y $395 de desventaja. Cambiar la ROM a ese enfoque sobre la base de estos mismos resultados convertiría la prueba reservada en datos de ajuste. La evidencia actual justifica probar la candidata en otra serie y conservar el firmware anterior en paralelo.

## Reproducción y artefactos

```powershell
python -X utf8 -B proyecto4/alternativas/candidata_final/backtest.py
python -X utf8 -B -m unittest discover -s proyecto4/alternativas/candidata_final -p test_referencia.py -v
```

Para aplicar la política congelada a otra serie de 20.000 filas, añade `--solo-evaluar --serie <CSV> --salida <carpeta>`.

- [Comparación de estrategias y segmentos](resultados/comparacion.csv)
- [Decisión y contabilidad por tick](resultados/decisiones_tick.csv)
- [Grilla de desarrollo y validación](resultados/busqueda_desarrollo_validacion.csv), [walk-forward](resultados/walk_forward.csv), [tamaños](resultados/sensibilidad_volumen.csv) y [salidas](resultados/sensibilidad_proteccion.csv)
- [Precio](resultados/precio.svg), [patrimonio](resultados/patrimonio.svg), [frente a mantener](resultados/vs_mantener.svg), [órdenes](resultados/senales.svg), [inventario](resultados/inventario.svg), [caja](resultados/caja.svg) y [comisiones](resultados/comisiones.svg)

