# Validación de la imagen actual — 27/11/2026

- Política: tendencia lenta, SUM10/128 ticks/5%, 130 palabras RV32E.
- Top: `rtl/trade_spi_externo.v`; memoria: `sw/trade.hex`; Assembly: `sw/trade.s`.
- BIN SHA-256: `1f514301f1a7300351f4d3d8f48b77c2c85dcd2a274f44910d11d00df406db45`.
- HEX SHA-256: `830177bca9726621dc583195cbe0e4740c7993a3db59698c081d95bfa2552d2a`.
- Área: 1219/1280 LC, 9/16 BRAM. Espino opera a 12,5 MHz; entrada 25 MHz.
- Timing enrutado: 50,67 MHz en el dominio del SoC.
- Ocho series Python/RV32E/RTL: 160.000 ticks sin diferencias.
- Repetición directa del ZIP de práctica publicado: 8/8 PASS, otros 160.000 ticks, 98 compras y 92 ventas; mismos CSV y resultados conocidos. Fuente y archivo: `resultados_simulacion/testbench_zip_practica/` y `docs/referencia/Proyecto_4_Series_Practica_export.zip`.
- Campaña completa: 43 CSV, 78 escenarios, 1.557.620 ticks a 100 µs, 428 compras y 364 ventas; cero discrepancias.
- Máximo de la campaña: 259 ciclos/20,72 µs; incluyendo el estrés sintético previo: 263 ciclos/21,04 µs.
- Bancos oficiales adaptados: dos, 2.000 ticks cada uno y 4/4 preservando tarea financiera y criterios.
- Cadencias largas: integración de 396 ticks a 1 ms y 10 ms; no ocho series completas por cada cadencia.
- Netlist y BIN reconstruido: compras/ventas en 396 ticks, CS de 20/40/1000 ns. Modelo funcional de rutas con retardo uniforme de 1 ns; no timing físico.
- Reprogramación: reportada por el usuario y registrada en `evidencia_fisica/reprogramacion_tendencia_lenta.json`.

La comparación final de co-diseño completó 32 ejecuciones y 640.000 ticks sobre
cuatro variantes de la misma política, sin diferencias. Perfil regional,
Amdahl, roofline y recursos están en `evidencia_codisenio_final/`. Software:
127,07 ciclos medios; MMIO activo y barrido: 83,98 (1,513×). Los periféricos
caben con 1219 y 1227 LC. Custom-0, 1368 LC, no cabe en HX1K.

La comparación directa de flash dio VERIFY OK para el BIN vigente, sin escritura:
`evidencia_fisica/verificacion_flash_lenta_20261127T004337Z.json`. La posterior
conexión a maestra dejó solo D1 según el usuario; no acredita recepción SPI.

Las cifras financieras son del testbench y no se presentan como resultados de competencia física. Las dos escalas adicionales comparten datos y extremos retrospectivos. Siguen pendientes recepción física de la maestra, resultados oficiales de las tres rondas y defensa/plazo. Los tres apartados técnicos solicitados están documentados y verificados; eso no asigna una nota.

Comprobaciones: `python -B tools/trader.py verify`, `python -B tools/auditar_lenta.py` y `python -B tools/auditar_campania_acciones.py`. Ver resultados en el PDF principal y `resultados_simulacion/testbench_todas_acciones/`.
