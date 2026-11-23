# Investigación final de estrategias para Proyecto 4

Se evaluaron 20,000 precios enteros. Las variantes y parámetros se congelaron antes de ejecutar las comparaciones. Cantidad por orden en las estrategias nuevas: 16; todas las cantidades cumplen el límite 63.

## Metodología temporal y contable

En cada tick se ejecuta a precio actual la decisión pendiente del tick anterior. Después se agrega el precio actual al historial y se genera la decisión siguiente. Cada segmento de 5.000 ticks se simula por separado con caja inicial de $10.000, cero acciones e historial vacío; no se pasa ningún dato de segmentos posteriores al anterior. La serie completa se simula en otra corrida cronológica única.

Las compras se limitan por caja disponible después de reservar la comisión de $5; las ventas se limitan a las acciones existentes. Solo un fill cobra comisión. Patrimonio = caja + acciones × precio. El drawdown se mide desde el máximo histórico de cada corrida, incluyendo el capital inicial.

## Definición de enfoques

- **A — Momentum con umbral:** cambio entre el precio actual y el de cuatro ticks antes. Compra 16 estando plano cuando el cambio es al menos +1; vende la posición al detectar −1 o menos. El producto q×umbral es $16, mayor que $10 de comisiones de un ciclo; es un filtro de señal, no una garantía de ganancia realizada.
- **B — Reversión a la media SMA10:** compra 16 estando plano si el precio está al menos $1 bajo SMA10; vende la posición si está al menos $1 sobre SMA10. Se compara 10×precio con la suma de diez precios; 10×precio se construye como 8p+2p con cuatro sumas, sin división ni multiplicador.
- **C — Tendencia persistente:** SMA5 sobre SMA10 en dos cierres consecutivos abre una posición de 16; mantiene hasta que SMA5 queda bajo SMA10 durante dos cierres consecutivos y vende la posición. No reentra mientras ya esté larga.
- **Mejor activa anterior:** variante C de la etapa previa (momentum con umbral 2 y cooldown 5), q=16, sin cambios.

## Serie completa

| Estrategia | Patrimonio | Retorno | Drawdown | Comisiones | Operaciones (C/V) | Caja | Acciones | Kernel estimado por tick |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| No operar | $10,000 | 0.00% | $0 (0.00%) | $0 | 0 (0/0) | $10,000 | 0 | 0–0 ciclos (0.0–0.0 µs) |
| Comprar y mantener | $9,695 | -3.05% | $9,300 (60.41%) | $5 | 1 (1/0) | $95 | 60 | 0–0 ciclos (0.0–0.0 µs) |
| Mejor activa anterior C q=16 | $7,383 | -26.17% | $6,085 (53.10%) | $3,785 | 757 (380/377) | $4,823 | 16 | 80–136 ciclos (3.2–5.44 µs) |
| A Momentum con umbral | $103 | -98.97% | $9,908 (98.97%) | $10,050 | 2010 (1005/1005) | $103 | 0 | 28–52 ciclos (1.12–2.08 µs) |
| B Reversion a SMA10 | $4,577 | -54.23% | $5,476 (54.47%) | $4,655 | 931 (466/465) | $2,017 | 16 | 54–89 ciclos (2.16–3.56 µs) |
| C Tendencia persistente | $1,710 | -82.90% | $8,387 (83.06%) | $8,620 | 1724 (862/862) | $1,710 | 0 | 68–115 ciclos (2.72–4.6 µs) |

## Evaluación por segmentos independientes

### Segmento 1

| Estrategia | Patrimonio | Retorno | Drawdown | Comisiones | Operaciones | Caja | Acciones |
|---|---:|---:|---:|---:|---:|---:|---:|
| No operar | $10,000 | 0.00% | $0 (0.00%) | $0 | 0 | $10,000 | 0 |
| Comprar y mantener | $8,495 | -15.05% | $3,900 (32.41%) | $5 | 1 | $95 | 60 |
| Mejor activa anterior C q=16 | $7,677 | -23.23% | $4,056 (35.40%) | $1,020 | 204 | $117 | 54 |
| A Momentum con umbral | $6,473 | -35.27% | $3,592 (35.88%) | $3,415 | 683 | $4,233 | 16 |
| B Reversion a SMA10 | $8,828 | -11.72% | $1,268 (12.61%) | $1,220 | 244 | $8,828 | 0 |
| C Tendencia persistente | $7,461 | -25.39% | $2,706 (26.80%) | $2,155 | 431 | $5,221 | 16 |

### Segmento 2

| Estrategia | Patrimonio | Retorno | Drawdown | Comisiones | Operaciones | Caja | Acciones |
|---|---:|---:|---:|---:|---:|---:|---:|
| No operar | $10,000 | 0.00% | $0 (0.00%) | $0 | 0 | $10,000 | 0 |
| Comprar y mantener | $15,287 | 52.87% | $1,260 (8.90%) | $5 | 1 | $1,112 | 63 |
| Mejor activa anterior C q=16 | $12,295 | 22.95% | $1,085 (8.56%) | $825 | 165 | $5,095 | 32 |
| A Momentum con umbral | $7,108 | -28.92% | $2,892 (28.92%) | $3,180 | 636 | $7,108 | 0 |
| B Reversion a SMA10 | $9,519 | -4.81% | $618 (6.10%) | $1,025 | 205 | $5,919 | 16 |
| C Tendencia persistente | $8,706 | -12.94% | $1,505 (14.74%) | $2,110 | 422 | $8,706 | 0 |

### Segmento 3

| Estrategia | Patrimonio | Retorno | Drawdown | Comisiones | Operaciones | Caja | Acciones |
|---|---:|---:|---:|---:|---:|---:|---:|
| No operar | $10,000 | 0.00% | $0 (0.00%) | $0 | 0 | $10,000 | 0 |
| Comprar y mantener | $7,575 | -24.25% | $3,740 (33.18%) | $5 | 1 | $51 | 44 |
| Mejor activa anterior C q=16 | $8,413 | -15.87% | $1,861 (18.30%) | $715 | 143 | $5,677 | 16 |
| A Momentum con umbral | $6,844 | -31.56% | $3,156 (31.56%) | $3,060 | 612 | $6,844 | 0 |
| B Reversion a SMA10 | $8,726 | -12.74% | $1,436 (14.19%) | $1,050 | 210 | $8,726 | 0 |
| C Tendencia persistente | $7,301 | -26.99% | $2,726 (27.19%) | $2,155 | 431 | $4,565 | 16 |

### Segmento 4

| Estrategia | Patrimonio | Retorno | Drawdown | Comisiones | Operaciones | Caja | Acciones |
|---|---:|---:|---:|---:|---:|---:|---:|
| No operar | $10,000 | 0.00% | $0 (0.00%) | $0 | 0 | $10,000 | 0 |
| Comprar y mantener | $9,299 | -7.01% | $4,408 (43.10%) | $5 | 1 | $19 | 58 |
| Mejor activa anterior C q=16 | $9,554 | -4.46% | $3,121 (31.12%) | $1,355 | 271 | $6,994 | 16 |
| A Momentum con umbral | $4,712 | -52.88% | $5,316 (53.02%) | $3,720 | 744 | $4,712 | 0 |
| B Reversion a SMA10 | $7,471 | -25.29% | $2,530 (25.30%) | $1,345 | 269 | $4,911 | 16 |
| C Tendencia persistente | $8,108 | -18.92% | $1,892 (18.92%) | $2,180 | 436 | $8,108 | 0 |

## Estimación de coste RV32E

Los ciclos reportados son estimaciones del kernel de decisión: rango manual de instrucciones de la lógica de estrategia multiplicado por CPI=2,35 (referencia del enunciado), y convertido a tiempo con 25 MHz. No son mediciones del core. Excluyen sondeo de STATUS, espera de PRICE, latencia del banco síncrono, LSU, acceso SPI y escritura MMIO. Deben sustituirse por medición sobre trade.s antes de afirmar que cumple un deadline.

- A necesita cuatro precios de horizonte, una resta y dos comparaciones; complejidad baja y buffer de cinco precios.
- B suma diez precios y compara contra 10×precio; ese múltiplo constante toma cuatro sumas con el método descrito. Buffer de diez precios; es el kernel más costoso de los tres nuevos.
- C requiere sumas SMA5/SMA10, comparación y dos estados de confirmación; un buffer de diez precios y un contador pequeño.
- El control de cartera completo requiere estado de caja/acciones. Los enfoques usan q fijo 16 y el modelo de la maestra limita compras por caja.

## Recomendación

No recomiendo todavía una estrategia activa para competir. No operar conserva el capital y las tres propuestas pierden dinero en la serie completa y en los cuatro segmentos independientes. Entre los enfoques nuevos, B es el candidato más razonable para seguir investigando: terminó por encima de A y C en la serie completa y en los segmentos 1–3, aunque pierde en todos los segmentos y requiere una ventana de diez precios. No es una recomendación para desplegarla. Si se exige una decisión con la evidencia actual, elegir no operar.

La serie es una sola práctica y los segmentos pertenecen a la misma trayectoria; esto no reemplaza una serie oculta. No se seleccionó estrategia maximizando solo el retorno de 20.000 ticks.

## Archivos

- `comparacion_final.csv`: corrida completa y cuatro corridas independientes por segmento.
- `patrimonio_final.svg`: evolución de la corrida completa para referencias y estrategias activas.
- `investigacion_final.md`: metodología, resultados, complejidad y recomendación.
