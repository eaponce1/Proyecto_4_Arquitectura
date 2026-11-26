# Testbench del ZIP de practica

Entrada: `Proyecto_4_Series_Practica_export.zip`. SHA-256: `bd06c224316282c2be91f519b839d0a7cde505e035bebd4eedb24edd682c35d9`.
BIN: `1f514301f1a7300351f4d3d8f48b77c2c85dcd2a274f44910d11d00df406db45`; firmware: tendencia lenta SUM10/128/5%.
8/8 PASS; 160,000 ticks a 100 us; 0 discrepancias.

Nueva ejecucion del RTL desde los precios exactos del ZIP, sin normalizar. Cada serie reinicia caja en $10.000 e inventario cero. Comision $5 por orden ejecutada.
El banco comprueba MISO, DECISION, caja, inventario, fills, comisiones, patrimonio, MMIO, SUM10, registros CPU, reset y plazo. Verilator usa dos estados; los chequeos Icarus previos son complementarios.
Los CSV coinciden con los datos de practica existentes segun la comparacion byte por byte en resumen.json. Esta repeticion no constituye datos nuevos ni una prueba fuera de muestra. No es una lectura de la flash ni una traza de la maestra fisica.

| Serie | RTL | Trader | Mantener | Ventaja | Compras | Ventas | Comisiones | DD % | Primera compra |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| practica_amd_2022_ene | PASS | 10738 | 8315 | 2423 | 14 | 13 | 135 | 42.20 | 257 |
| practica_amd_2022_may | PASS | 8540 | 9647 | -1107 | 9 | 8 | 85 | 30.01 | 385 |
| practica_apple_2022 | PASS | 14263 | 11063 | 3200 | 19 | 19 | 190 | 38.82 | 385 |
| practica_apple_2023 | PASS | 9272 | 10371 | -1099 | 14 | 12 | 130 | 40.41 | 513 |
| practica_meta_2022 | PASS | 12836 | 9695 | 3141 | 5 | 5 | 50 | 28.13 | 385 |
| practica_netflix_2022 | PASS | 10346 | 9179 | 1167 | 15 | 15 | 150 | 46.72 | 257 |
| practica_netflix_2023 | PASS | 12432 | 9170 | 3262 | 14 | 12 | 130 | 50.55 | 2177 |
| practica_tesla_2022 | PASS | 9342 | 9995 | -653 | 8 | 8 | 80 | 48.52 | 257 |

Los ticks empiezan en cero; -1 indica ausencia de ejecucion. Una señal se ejecuta al precio de la siguiente trama. D4 registra orden no nula; los demas LED confirman CPU, recepcion y lectura.
Las trazas comprimidas se guardan junto al informe. Vectores, operaciones y logs completos estan en build/testbench_zip_practica/. PASS tecnico no garantiza beneficio financiero.
