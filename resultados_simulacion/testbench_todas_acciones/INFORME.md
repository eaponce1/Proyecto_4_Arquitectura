# Testbench de todas las acciones

RTL activo: 1f514301f1a7300351f4d3d8f48b77c2c85dcd2a274f44910d11d00df406db45. Periodo: 100 us. Reinicio independiente por escenario.

**78/78 PASS; 1,557,620 ticks completos; 0 discrepancias registradas.**

La prueba simula Espino, firmware y SPI; no lee la FPGA fisica. El usuario reporto haberla reprogramado, pero no aporto una traza de la maestra para cotejar esta sesion.

| Grupo | Casos | PASS | Supera mantener | Con ganancia | Sin ordenes | Media | Peor | DD maximo |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Ocho conocidas | 8 | 8 | 5 | 5 | 0 | $10971.12 | $8540 | 50.55% |
| ZIP proporcional | 35 | 35 | 16 | 14 | 15 | $10784.00 | $5863 | 45.34% |
| ZIP afin | 35 | 35 | 18 | 21 | 0 | $12150.57 | $5518 | 52.05% |

## Interpretacion

PASS acredita coincidencia tecnica y plazo de respuesta, no rentabilidad. No operar mantiene $10.000. Comprar y mantener es la referencia ideal del curso. Las comisiones se aplican solo a ejecuciones positivas.
Las dos escalas de cada CSV adicional no son muestras independientes. Se utilizan hasta 20.000 precios; si un archivo tiene menos, se prueban todos sus datos sin rellenar ni repetir precios. GOOGL 2021 tiene 18.844 ticks y DIS 2022 tiene 19.966: no equivalen a rondas completas de 20.000. Las filas originales y utilizadas se documentan en resumen.json. La escala proporcional es round(precio*255/max), minimo 1; la afin lleva minimo a 100 y maximo a 255. Ambas usan extremos de la muestra como preprocesamiento retrospectivo; no acreditan una normalizacion causal en vivo. La procedencia de estos CSV del ZIP no se verifico externamente.
Se comparan MISO, DECISION, caja, inventario, fills, comisiones y patrimonio por tick; el banco verifica una recepcion y decision por precio, SUM10, registros de CPU, reset y deadline. Verilator usa dos estados y complementa los chequeos Icarus previos.

## Todos los escenarios

| Serie | Escala | RTL | Trader | Mantener | Ventaja | Compras | Ventas | DD % | Primera compra |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| practica_amd_2022_ene | original | PASS | 10738 | 8315 | 2423 | 14 | 13 | 42.20 | 257 |
| practica_amd_2022_may | original | PASS | 8540 | 9647 | -1107 | 9 | 8 | 30.01 | 385 |
| practica_apple_2022 | original | PASS | 14263 | 11063 | 3200 | 19 | 19 | 38.82 | 385 |
| practica_apple_2023 | original | PASS | 9272 | 10371 | -1099 | 14 | 12 | 40.41 | 513 |
| practica_meta_2022 | original | PASS | 12836 | 9695 | 3141 | 5 | 5 | 28.13 | 385 |
| practica_netflix_2022 | original | PASS | 10346 | 9179 | 1167 | 15 | 15 | 46.72 | 257 |
| practica_netflix_2023 | original | PASS | 12432 | 9170 | 3262 | 14 | 12 | 50.55 | 2177 |
| practica_tesla_2022 | original | PASS | 9342 | 9995 | -653 | 8 | 8 | 48.52 | 257 |
| AAPL_2019-01-02_afin | afin | PASS | 16261 | 17585 | -1324 | 5 | 4 | 18.04 | 897 |
| AAPL_2020-03-23_afin | afin | PASS | 14403 | 21385 | -6982 | 4 | 4 | 15.14 | 257 |
| AAPL_2021-01-04_afin | afin | PASS | 7578 | 6927 | 651 | 16 | 16 | 46.77 | 1281 |
| AAPL_2022-01-03_afin | afin | PASS | 9256 | 5996 | 3260 | 11 | 10 | 37.84 | 2561 |
| AAPL_2023-08-01_afin | afin | PASS | 12053 | 7070 | 4983 | 8 | 7 | 31.15 | 6273 |
| AMD_2022-01-03_afin | afin | PASS | 13517 | 5813 | 7704 | 16 | 14 | 31.98 | 2305 |
| AMD_2023-05-01_afin | afin | PASS | 17992 | 16540 | 1452 | 6 | 4 | 31.94 | 1281 |
| AMZN_2020-03-02_afin | afin | PASS | 15032 | 15407 | -375 | 5 | 5 | 22.36 | 3585 |
| AMZN_2023-01-03_afin | afin | PASS | 18189 | 15058 | 3131 | 10 | 8 | 18.52 | 1409 |
| BA_2020-02-03_afin | afin | PASS | 11433 | 5417 | 6016 | 4 | 4 | 14.46 | 11905 |
| DIS_2022-01-03_afin | afin | PASS | 11903 | 6803 | 5100 | 8 | 6 | 41.75 | 5249 |
| GOOGL_2021-06-01_afin | afin | PASS | 14609 | 21470 | -6861 | 8 | 7 | 27.80 | 897 |
| GOOGL_2023-01-03_afin | afin | PASS | 9234 | 15995 | -6761 | 11 | 10 | 45.19 | 1537 |
| INTC_2022-06-01_afin | afin | PASS | 6589 | 4925 | 1664 | 8 | 7 | 49.20 | 3969 |
| JPM_2021-01-04_afin | afin | PASS | 20698 | 21949 | -1251 | 7 | 5 | 18.37 | 897 |
| JPM_2022-01-03_afin | afin | PASS | 7387 | 6361 | 1026 | 9 | 8 | 44.05 | 513 |
| KO_2019-01-02_afin | afin | PASS | 6756 | 7658 | -902 | 6 | 5 | 48.62 | 1665 |
| KO_2022-06-01_afin | afin | PASS | 7834 | 10670 | -2836 | 16 | 16 | 50.24 | 385 |
| META_2021-03-01_afin | afin | PASS | 9564 | 17129 | -7565 | 10 | 10 | 34.82 | 385 |
| META_2022-01-03_afin | afin | PASS | 5654 | 4847 | 807 | 4 | 3 | 52.05 | 5761 |
| META_2022-11-28_afin | afin | PASS | 16031 | 21015 | -4984 | 6 | 4 | 22.53 | 1153 |
| META_2023-06-01_afin | afin | PASS | 11872 | 16718 | -4846 | 8 | 7 | 25.65 | 257 |
| MSFT_2020-02-03_afin | afin | PASS | 13587 | 10534 | 3053 | 11 | 10 | 40.26 | 513 |
| MSFT_2022-01-03_afin | afin | PASS | 10550 | 5900 | 4650 | 11 | 9 | 26.83 | 4353 |
| MSFT_2023-01-03_afin | afin | PASS | 13756 | 15755 | -1999 | 10 | 9 | 24.76 | 1537 |
| NFLX_2022-01-03_afin | afin | PASS | 8535 | 4691 | 3844 | 5 | 3 | 36.27 | 5249 |
| NFLX_2022-04-01_afin | afin | PASS | 5518 | 4583 | 935 | 4 | 3 | 48.40 | 513 |
| NVDA_2022-01-03_afin | afin | PASS | 12621 | 6469 | 6152 | 18 | 16 | 31.17 | 2305 |
| NVDA_2022-09-01_afin | afin | PASS | 8851 | 12645 | -3794 | 11 | 10 | 42.03 | 385 |
| NVDA_2023-01-03_afin | afin | PASS | 16953 | 22826 | -5873 | 3 | 2 | 16.67 | 1665 |
| NVDA_2024-01-02_afin | afin | PASS | 16669 | 21557 | -4888 | 6 | 4 | 16.34 | 1665 |
| TSLA_2020-06-01_afin | afin | PASS | 19510 | 20383 | -873 | 6 | 4 | 24.00 | 2049 |
| TSLA_2021-01-04_afin | afin | PASS | 9665 | 9043 | 622 | 6 | 6 | 45.73 | 897 |
| TSLA_2022-01-03_afin | afin | PASS | 9905 | 6089 | 3816 | 6 | 5 | 33.26 | 5761 |
| TSLA_2023-01-03_afin | afin | PASS | 15305 | 16967 | -1662 | 5 | 5 | 18.37 | 513 |
| AAPL_2019-01-02_prop | prop | PASS | 10000 | 12063 | -2063 | 0 | 0 | 0.00 | -1 |
| AAPL_2020-03-23_prop | prop | PASS | 13440 | 14307 | -867 | 1 | 0 | 9.73 | 513 |
| AAPL_2021-01-04_prop | prop | PASS | 10000 | 9197 | 803 | 0 | 0 | 0.00 | -1 |
| AAPL_2022-01-03_prop | prop | PASS | 10000 | 8915 | 1085 | 0 | 0 | 0.00 | -1 |
| AAPL_2023-08-01_prop | prop | PASS | 10000 | 9293 | 707 | 0 | 0 | 0.00 | -1 |
| AMD_2022-01-03_prop | prop | PASS | 9558 | 7635 | 1923 | 1 | 1 | 24.33 | 7425 |
| AMD_2023-05-01_prop | prop | PASS | 10259 | 13073 | -2814 | 1 | 0 | 18.91 | 7041 |
| AMZN_2020-03-02_prop | prop | PASS | 12245 | 12245 | 0 | 1 | 0 | 8.53 | 5121 |
| AMZN_2023-01-03_prop | prop | PASS | 10000 | 11503 | -1503 | 0 | 0 | 0.00 | -1 |
| BA_2020-02-03_prop | prop | PASS | 9003 | 4367 | 4636 | 14 | 12 | 35.57 | 11009 |
| DIS_2022-01-03_prop | prop | PASS | 8995 | 8995 | 0 | 1 | 0 | 18.59 | 10241 |
| GOOGL_2021-06-01_prop | prop | PASS | 10000 | 11570 | -1570 | 0 | 0 | 0.00 | -1 |
| GOOGL_2023-01-03_prop | prop | PASS | 10000 | 11311 | -1311 | 0 | 0 | 0.00 | -1 |
| INTC_2022-06-01_prop | prop | PASS | 10000 | 8045 | 1955 | 0 | 0 | 0.00 | -1 |
| JPM_2021-01-04_prop | prop | PASS | 10000 | 12592 | -2592 | 0 | 0 | 0.00 | -1 |
| JPM_2022-01-03_prop | prop | PASS | 10000 | 8683 | 1317 | 0 | 0 | 0.00 | -1 |
| KO_2019-01-02_prop | prop | PASS | 10000 | 9708 | 292 | 0 | 0 | 0.00 | -1 |
| KO_2022-06-01_prop | prop | PASS | 10000 | 10115 | -115 | 0 | 0 | 0.00 | -1 |
| META_2021-03-01_prop | prop | PASS | 10000 | 11514 | -1514 | 0 | 0 | 0.00 | -1 |
| META_2022-01-03_prop | prop | PASS | 10184 | 6134 | 4050 | 1 | 0 | 3.13 | 19585 |
| META_2022-11-28_prop | prop | PASS | 14322 | 15929 | -1607 | 2 | 1 | 13.71 | 1153 |
| META_2023-06-01_prop | prop | PASS | 9410 | 11264 | -1854 | 1 | 0 | 8.10 | 14721 |
| MSFT_2020-02-03_prop | prop | PASS | 12035 | 10253 | 1782 | 1 | 0 | 11.39 | 12545 |
| MSFT_2022-01-03_prop | prop | PASS | 10000 | 8669 | 1331 | 0 | 0 | 0.00 | -1 |
| MSFT_2023-01-03_prop | prop | PASS | 10000 | 11480 | -1480 | 0 | 0 | 0.00 | -1 |
| NFLX_2022-01-03_prop | prop | PASS | 11568 | 5978 | 5590 | 3 | 1 | 13.72 | 5761 |
| NFLX_2022-04-01_prop | prop | PASS | 5863 | 4747 | 1116 | 3 | 2 | 45.34 | 513 |
| NVDA_2022-01-03_prop | prop | PASS | 11809 | 8155 | 3654 | 2 | 1 | 11.47 | 5761 |
| NVDA_2022-09-01_prop | prop | PASS | 10793 | 11271 | -478 | 1 | 0 | 2.69 | 19201 |
| NVDA_2023-01-03_prop | prop | PASS | 16043 | 17447 | -1404 | 1 | 0 | 11.03 | 1665 |
| NVDA_2024-01-02_prop | prop | PASS | 11387 | 18003 | -6616 | 1 | 0 | 12.73 | 13697 |
| TSLA_2020-06-01_prop | prop | PASS | 14385 | 17366 | -2981 | 3 | 2 | 17.79 | 2817 |
| TSLA_2021-01-04_prop | prop | PASS | 11289 | 9456 | 1833 | 2 | 1 | 15.96 | 1281 |
| TSLA_2022-01-03_prop | prop | PASS | 9885 | 7412 | 2473 | 1 | 0 | 24.41 | 7169 |
| TSLA_2023-01-03_prop | prop | PASS | 14967 | 15251 | -284 | 1 | 1 | 13.35 | 1665 |

Los ticks empiezan en cero; -1 significa que no hubo ejecucion de ese tipo. CSV de resultados junto a este archivo. Trazas por tick, operaciones, vectores y logs en build/testbench_todas_acciones/. No se cambia ni se programa competition.bin.
