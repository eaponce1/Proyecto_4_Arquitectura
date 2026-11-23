# Auditoría contable y comparación de estrategias v2

Serie evaluada: 20,000 ticks; precio mínimo $100, máximo $255.
Capital inicial $10.000; comisión $5 por orden ejecutada; precio entero; sin deuda ni venta corta.

## Auditoría del drawdown reportado

El drawdown absoluto de $10.152 no es una deuda ni una pérdida medida desde el capital inicial. Es la caída desde el máximo histórico de patrimonio hasta un valle posterior:

- Peak: $10,254 en tick 535.
- Valle: $102 en tick 17106, con caja $102 y 0 acciones.
- Diferencia peak-valle: $10,254 - $102 = $10,152 (99.01% del peak).
- El mínimo de caja, acciones y patrimonio de la simulación base es no negativo; el drawdown supera $10.000 porque el peak previo fue $10.254, no porque la cartera tomara deuda.

La fórmula utilizada es `peak_t = max(capital_inicial, equity[0..t])`, `drawdown_t = peak_t - equity_t`; se reporta el mayor drawdown absoluto y el porcentaje respecto del peak.

## Revisión contable y temporal

- Compra: cantidad ejecutada = min(cantidad solicitada, max(0, floor((caja - 5) / precio))). La comisión se descuenta solo si se ejecuta al menos una acción.
- Venta: cantidad ejecutada = min(cantidad solicitada, acciones disponibles); la comisión también se cobra solo al ejecutar. El saldo y la posición permanecen no negativos.
- Patrimonio por tick: `caja + acciones * precio_del_tick`, después de ejecutar la orden recibida.
- Desfase SPI: la columna `tick_calculo_decision` de `operaciones_v2.csv` debe ser el tick anterior al de ejecución. La decisión se calcula después de agregar el precio actual al historial y queda pendiente para el siguiente tick.
- Las pruebas recomputan el patrimonio en cada tick, las comisiones, fills, caja, acciones y un ejemplo de FIFO.
- Costo base FIFO para P&L cerrado: incluye la comisión de compra asignada proporcionalmente al lote; al vender, el P&L realizado resta la comisión de venta. P&L por cierre se agrupa por orden de venta.

## Recuento de operaciones de la versión original

La estrategia SMA 5/10 + momentum q=1 reprodujo 2,022 órdenes: 1,011 compras y 1,011 ventas. Pagó $10,110 de comisión. El P&L promedio por orden de venta cerrada fue $-9.79; el intervalo medio entre órdenes fue 8.46 ticks.

## Variantes y cantidades

Las cantidades evaluadas se fijaron antes de ejecutar la comparación: 1, 2, 4, 8, 16, 32 y 63. Se reporta la grilla como análisis de sensibilidad; no se seleccionó una cantidad maximizando el resultado.

- **A:** SMA 5/10 y momentum a tres ticks con umbral absoluto de 2 unidades de precio.
- **B:** dos cierres consecutivos con la misma dirección de SMA, momentum coherente, una entrada estando plano y salida de la posición completa. Limita el número de operaciones y la posición a 63 acciones.
- **C:** umbral de 2 unidades y cooldown de 5 ticks desde la última orden ejecutada. Por el desfase, la próxima orden se ejecuta al menos un tick después de calcularla.
- También se incluye la estrategia original sin umbral (q=1) y las dos referencias obligatorias.

### Comparación completa

| Estrategia | Patrimonio | Retorno | Max DD | Fees | Órdenes (buy/sell) | Caja | Acciones | P&L medio cierre | ticks/orden |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| No operar | $10,000 | 0.00% | $0 (0.00%) | $0 | 0 (0/0) | $10,000 | 0 | — |  |
| Comprar y mantener | $9,695 | -3.05% | $9,300 (60.41%) | $5 | 1 (1/0) | $95 | 60 | — |  |
| Original SMA 5/10 + momentum q=1 | $102 | -98.98% | $10,152 (99.01%) | $10,110 | 2022 (1011/1011) | $102 | 0 | $-9.79 | 8.46 |
| A SMA+momentum umbral 2 q=1 | $1,592 | -84.08% | $8,614 (84.40%) | $8,850 | 1770 (885/885) | $1,592 | 0 | $-9.50 | 11.27 |
| A SMA+momentum umbral 2 q=2 | $1,459 | -85.41% | $9,350 (86.50%) | $8,260 | 1652 (829/823) | $1,459 | 0 | $-10.38 | 12.08 |
| A SMA+momentum umbral 2 q=4 | $2,695 | -73.05% | $8,580 (76.33%) | $7,515 | 1503 (754/749) | $2,695 | 0 | $-9.75 | 13.28 |
| A SMA+momentum umbral 2 q=8 | $3,901 | -60.99% | $7,908 (70.02%) | $6,245 | 1249 (627/622) | $3,901 | 0 | $-9.81 | 15.98 |
| A SMA+momentum umbral 2 q=16 | $4,581 | -54.19% | $7,401 (66.41%) | $4,745 | 949 (475/474) | $4,581 | 0 | $-11.43 | 21.03 |
| A SMA+momentum umbral 2 q=32 | $5,629 | -43.71% | $6,460 (59.26%) | $3,855 | 771 (386/385) | $5,629 | 0 | $-11.35 | 25.9 |
| A SMA+momentum umbral 2 q=63 | $6,709 | -32.91% | $5,905 (54.38%) | $2,490 | 498 (249/249) | $6,709 | 0 | $-13.22 | 40.12 |
| B tendencia confirmada q=1 | $5,180 | -48.20% | $4,820 (48.20%) | $4,860 | 972 (486/486) | $5,180 | 0 | $-9.92 | 20.57 |
| B tendencia confirmada q=2 | $5,220 | -47.80% | $4,780 (47.80%) | $4,860 | 972 (486/486) | $5,220 | 0 | $-9.84 | 20.57 |
| B tendencia confirmada q=4 | $5,300 | -47.00% | $4,711 (47.06%) | $4,860 | 972 (486/486) | $5,300 | 0 | $-9.67 | 20.57 |
| B tendencia confirmada q=8 | $5,460 | -45.40% | $4,647 (45.98%) | $4,860 | 972 (486/486) | $5,460 | 0 | $-9.34 | 20.57 |
| B tendencia confirmada q=16 | $5,780 | -42.20% | $5,150 (50.00%) | $4,860 | 972 (486/486) | $5,780 | 0 | $-8.68 | 20.57 |
| B tendencia confirmada q=32 | $6,420 | -35.80% | $6,270 (58.69%) | $4,860 | 972 (486/486) | $6,420 | 0 | $-7.37 | 20.57 |
| B tendencia confirmada q=63 | $6,678 | -33.22% | $7,427 (65.18%) | $4,860 | 972 (486/486) | $6,678 | 0 | $-6.84 | 20.57 |
| C umbral 2 cooldown 5 q=1 | $4,058 | -59.42% | $6,147 (60.24%) | $4,835 | 967 (490/477) | $1,978 | 13 | $-11.75 | 20.64 |
| C umbral 2 cooldown 5 q=2 | $4,551 | -54.49% | $6,333 (58.19%) | $4,745 | 949 (476/473) | $4,231 | 2 | $-11.48 | 21.03 |
| C umbral 2 cooldown 5 q=4 | $5,103 | -48.97% | $6,077 (54.36%) | $4,570 | 914 (459/455) | $4,463 | 4 | $-10.70 | 21.84 |
| C umbral 2 cooldown 5 q=8 | $5,607 | -43.93% | $6,350 (54.93%) | $4,260 | 852 (429/423) | $4,327 | 8 | $-10.26 | 23.43 |
| C umbral 2 cooldown 5 q=16 | $7,383 | -26.17% | $6,085 (53.10%) | $3,785 | 757 (380/377) | $4,823 | 16 | $-6.67 | 26.38 |
| C umbral 2 cooldown 5 q=32 | $7,138 | -28.62% | $5,814 (51.43%) | $3,235 | 647 (324/323) | $5,378 | 11 | $-8.65 | 30.87 |
| C umbral 2 cooldown 5 q=63 | $7,310 | -26.90% | $5,672 (51.85%) | $2,425 | 485 (243/242) | $7,310 | 0 | $-11.12 | 41.2 |

## Evolución de caja y posición

La serie completa por tick queda en memoria durante la simulación; el CSV de operaciones registra cada fill con caja/acciones antes y después. Rangos de las referencias, baseline y variantes q=1:

| Estrategia | Rango caja | Caja final | Rango acciones | Acciones finales |
|---|---:|---:|---:|---:|
| No operar | $10,000–$10,000 | $10,000 | 0–0 | 0 |
| Comprar y mantener | $95–$95 | $95 | 0–60 | 60 |
| Original SMA 5/10 + momentum q=1 | $0–$10,000 | $102 | 0–54 | 0 |
| A SMA+momentum umbral 2 q=1 | $14–$10,000 | $1,592 | 0–39 | 0 |
| B tendencia confirmada q=1 | $5,021–$10,000 | $5,180 | 0–1 | 0 |
| C umbral 2 cooldown 5 q=1 | $8–$10,000 | $1,978 | 0–42 | 13 |

## Operaciones cerradas con mayor pérdida

P&L realizado por orden de venta FIFO, con comisiones de compra/venta incluidas. Un P&L negativo es una pérdida realizada; no atribuye a una venta la caída no realizada de toda la cartera.

| Estrategia | Tick | Cantidad | Precio | Caja tras venta | Posición tras venta | P&L realizado |
|---|---:|---:|---:|---:|---:|---:|
| B tendencia confirmada q=63 | 431 | 60 | $176 | $10659 | 0 | $-670.00 |
| A SMA+momentum umbral 2 q=63 | 431 | 58 | $176 | $10205 | 0 | $-590.00 |
| C umbral 2 cooldown 5 q=63 | 431 | 58 | $176 | $10285 | 0 | $-590.00 |
| B tendencia confirmada q=63 | 3942 | 46 | $153 | $7039 | 0 | $-562.00 |
| C umbral 2 cooldown 5 q=63 | 17230 | 52 | $157 | $8251 | 0 | $-530.00 |
| C umbral 2 cooldown 5 q=63 | 19931 | 47 | $166 | $7930 | 0 | $-527.00 |
| A SMA+momentum umbral 2 q=63 | 17230 | 49 | $157 | $7799 | 0 | $-500.00 |
| A SMA+momentum umbral 2 q=63 | 19931 | 44 | $166 | $7318 | 0 | $-494.00 |
| C umbral 2 cooldown 5 q=63 | 7733 | 42 | $197 | $8357 | 0 | $-430.00 |
| C umbral 2 cooldown 5 q=63 | 4916 | 49 | $138 | $6871 | 0 | $-402.00 |

## Recomendación

En la serie de práctica, **no operar** conserva $10.000 y supera todas las estrategias activas evaluadas. Por rentabilidad, drawdown, cero comisiones y mínima complejidad, recomiendo no operar con la información y las reglas actuales. Comprar y mantener termina en $9.695.

Entre las activas, C con q=16 obtuvo el mayor patrimonio final de la grilla ($7.383), pero perdió 26,17% y pagó $3.785 en comisiones. No recomiendo seleccionar esa cantidad por ser la mejor de esta misma serie: sería optimización retrospectiva. B con q=1 reduce el número de órdenes frente al baseline, pero termina en $5.180 y no supera la referencia sin operar. La serie es una sola práctica; no justifica generalización ni ajuste de parámetros. Umbrales, confirmación, cooldown y grilla no consultan precios futuros.

## Coste estimado al portar a RV32E

Las variantes A/C requieren sumas de ventanas, comparación SMA, resta de momentum y branches; C agrega un contador/comparación de cooldown. B agrega una comparación con la señal anterior y un estado plano/largo, pero puede reducir fills y comisiones. Ninguna necesita multiplicación o división en la señal: `2 * suma_5` se implementa como suma consigo misma. Mantener SMA 5/10 y momentum requiere conservar diez precios (probablemente buffer circular) y actualizar índices/valores; la alternativa de recalcular ventanas añade lecturas y sumas por tick. La contabilidad completa de caja con precio por cantidad sí exigiría multiplicación; las estrategias evaluadas usan cantidades acotadas y la FPGA maestra aplica la regla de caja.

## Archivos de salida y límites

- `comparacion_estrategias_v2.csv`: 24 escenarios (referencias, baseline y 21 combinaciones de variantes/cantidad).
- `operaciones_v2.csv`: un registro por orden ejecutada, con origen de decisión, fill, saldos y P&L FIFO al cerrar.
- `patrimonio_estrategias_v2.svg`: referencias, baseline y variantes nuevas con q=1; la grilla completa está en CSV.
- `analisis_estrategias.md`: esta auditoría, resultados, sensibilidad y recomendación.

No se modificaron RTL, assembler ni testbench. No se implementó Assembly.
