# Optimización de recursos: MMIO SMA10

## Cambio evaluado

Se mantuvo `proyecto4/alternativas/mmio_sma10/` sin cambios y se creó `proyecto4/alternativas/mmio_sma10_opt/` como variante aislada. En `pochoco_sma10.v`, se sustituyó el contador saturante de 4 bits `count_q` por un bit `ready_q`. El puntero circular ya indica la décima muestra cuando vale 9; en ese evento se activa `ready_q`. Se conservan exactamente el anillo de diez precios en BRAM, la suma acumulada, el mapa MMIO, el SPI, la estrategia, la contabilidad y el core.

La suma sigue acumulando los primeros diez precios y después reemplaza la muestra saliente por la entrante. `ready` se activa después de aceptar el décimo precio, igual que antes. La equivalencia se comprobó en cada muestra por el test autónomo y, en la simulación integrada, las decisiones MISO se cotejaron tick a tick contra Python.

## Comparación real antes/después

| Variante | IC media | Ciclos media | Mediana ciclos | p95 ciclos | Peor ciclo | Speedup vs original | LUT4 | LC | BRAM | Fmax |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| MMIO base (20,000 ticks) | 26.85 | 60.64 | 52.0 | 58 | 255 | 3.606× | 1,055 | 1279/1,280 | 13/16 | 40.50 MHz |
| MMIO optimizada (20,000 ticks) | 26.85 | 60.64 | 52.0 | 58 | 255 | 3.606× | 1,051 | 1274/1,280 | 13/16 | 42.33 MHz |

Resultado de área: LC bajan de 1279 a 1274 (−5, 0.39%). LUT4 baja de 1055 a 1051; BRAM permanece en 13/16. El objetivo de 1.150–1.200 LC **no se alcanzó**: la variante queda en 1274/1.280 LC.

Fmax post-place-and-route aumenta de 40.50 MHz a 42.33 MHz; ambas pasan los 25 MHz. Los tiempos software y speedup no cambian: IC/ciclos por tick son idénticos a nivel de estadística. El speedup por ciclos respecto a la versión software original se conserva en 3.606×.

## Auditoría de recursos y alternativas

- **Historial:** diez precios de 8 bits usan una instancia `SB_RAM40_4K`; preserva la BRAM e impide convertir las diez posiciones en registros/LUT, opción que probablemente aumentaría LC. BRAM total del SoC se mantiene 13/16.
- **Registros del periférico:** `pointer_q` es necesario para el anillo de diez entradas; `sum_q` mantiene el rolling sum; `ready_q` reemplaza `count_q`. El contador de muestras y su comparador se consideran redundantes porque el puntero llega a slot 9 exactamente en la décima entrada inicial.
- **Decodificador MMIO:** los offsets STATUS/PRICE/DECISION/SUM10/READY son 0–4. Se conserva el `case` existente: una reescritura más estrecha no se justificaba sin evidencia de ahorro, y alterar el decode de lecturas aumenta riesgo de regresión.
- **Lógica combinacional y timing:** se conservó la lectura síncrona del precio saliente, la suma rodante y el mismo instante de captura SPI. En el reporte de timing optimizado, la ruta posedge crítica atraviesa lógica mapeada de la RAM de instrucciones/control de `u_ram.mem` y no la ruta de suma SMA10. No se cambió el Espino Core.

La auditoría sugiere que el bloque SMA10 no explica por sí solo el uso total de 1.279 LC: el chip integra el SoC, RAM de programa, Espino, SPI y periféricos. Reducir otros recursos con impacto importante requeriría reestructurar bloques ajenos a SMA10; no se hizo porque se pidió evitar cambios al core salvo justificación indispensable y preservar las funciones.

## Validación ejecutada

| Validación | Resultado |
|---|---|
| Testbench autónomo SMA10, suma/READY tick a tick | PASS, 20.000 precios |
| Simulación integrada y comparación MISO con Python | PASS, 20.000 ticks, cero pérdidas/discrepancias |
| IC/ciclos | 20.000 filas en cada CSV; medias y percentiles idénticos antes/después |
| Yosys | PASS; LUT4 contabilizadas desde log real |
| nextpnr iCE40 HX1K vq100, seed 1, 25 MHz | PASS; 1.274 LC, 13 BRAM |
| Timing | PASS; Fmax enrutada 42.33 MHz, supera 25 MHz |

## Comandos reproducibles

Desde la raíz `pochoco_soc-main`:

```powershell
iverilog -g2012 -s tb_sma10 -o proyecto4/tests/tb_sma10_opt.vvp proyecto4/alternativas/mmio_sma10_opt/rtl/pochoco_sma10.v proyecto4/alternativas/mmio_sma10_opt/tb/ram_model.v proyecto4/alternativas/mmio_sma10_opt/tb/tb_sma10.sv
vvp proyecto4/tests/tb_sma10_opt.vvp
python proyecto4/alternativas/mmio_sma10_opt/medir_mmio_sma10_opt.py --ticks 20000
python proyecto4/python/sintetizar_mmio_sma10_opt.py
python proyecto4/python/generar_informe_optimizacion_mmio.py
```

Los scripts de medida ensamblan el `trade.s` de la variante y comparan cada byte MISO contra las decisiones Python; el CSV integrado es `proyecto4/resultados/co_disenio/mmio_sma10_opt_ticks.csv`. Las mediciones físicas usan el target HX1K/vq100, semilla nextpnr 1 y restricción de 25 MHz.

## Conclusión

La optimización es funcional y mejora ligeramente área/timing sin alterar rendimiento ni equivalencia. La reducción es de solo cinco Logic Cells, insuficiente para el objetivo solicitado y todavía deja 6 LC libres (0,47% del dispositivo). Se conserva `mmio_sma10_opt` como variante experimental, pero se recomienda mantener `mmio_sma10` como referencia estable hasta conseguir más margen. No se afirma haber logrado el objetivo de área; el resultado sintetizado muestra que la meta exige reducir lógica en otra parte del SoC o un cambio arquitectónico adicional, fuera de este ajuste local.
