# Linea base antes del co-diseno

Se preservo una copia con hashes SHA-256 del RTL original del Proyecto 2 en `proyecto4/referencia/rtl_original/`. Tambien se guardaron `trade.s`, `trade.hex`, las mediciones software previas y los artefactos/logs de sintesis en esta carpeta.

## Configuracion sintetizada

Se sintetizo `trade_top`, que instancia el SoC original con `EnableSpi=1` y `proyecto4/sw/trade.hex`, usando el pinout `goboard.pcf` y el flujo del Makefile: Yosys `synth_ice40`, NextPNR `--hx1k --package vq100 --freq 25`.

| Recurso | Uso | Capacidad HX1K |
|---|---:|---:|
| LCs (LUT4/FF empaquetados) | 1195 | 1280 |
| BRAM (SB_RAM40_4K) | 12 | 16 |
| SB_IO | 27 | 72 |
| SB_GB | 3 | 8 |

Frecuencia maxima de NextPNR tras colocacion y ruteo: **38,71 MHz**, pasa el objetivo de 25 MHz. El valor inicial pre-place fue 39,28 MHz; se reporta el final para comparar variantes.

## Medicion software conservada

La corrida previa de `trade.hex` en RTL/Python cubrio 20.000 ticks a cadencia custom de 30 us. Respuesta desde `byte_done` a DECISION: promedio 218,66 ciclos, 91,92 commits (IC), CPI 2,380; peor caso 412 ciclos. SMA10 ocupa 163,93 ciclos medios. El CSV original se conserva como `mediciones_software.csv`.

## Hotspot SMA10 auditado

En cada tick despues del calentamiento, `trade.s` ejecuta el lazo `SUMA_SMA10_LOOP`: diez lecturas `lw x11,0(x8)`, diez acumulaciones `add x10,x10,x11`, incremento del puntero y rama por elemento, incluyendo el wrap de anillo. Luego calcula `10*precio` con cuatro `add` y compara los umbrales. La seccion completa SMA ocupa 163,93 ciclos medios medidos; la suma de diez precios domina ese costo.
