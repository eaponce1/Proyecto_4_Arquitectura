# Resultados de simulacion de Pochoco Trader

| Serie | Trader | Mantener | Ventaja | Ordenes | Comisiones | DD max. % |
|---|---:|---:|---:|---:|---:|---:|
| AMD enero 2022 | 19312 | 8315 | 10997 | 63 | 315 | 43.60 |
| AMD mayo 2022 | 11490 | 9647 | 1843 | 45 | 225 | 50.39 |
| Apple 2022 | 12528 | 11063 | 1465 | 64 | 320 | 44.31 |
| Apple 2023 | 13555 | 10371 | 3184 | 62 | 310 | 55.34 |
| Meta 2022 | 13700 | 9695 | 4005 | 56 | 280 | 52.85 |
| Netflix 2022 | 8615 | 9179 | -564 | 59 | 295 | 56.02 |
| Netflix 2023 | 8929 | 9170 | -241 | 41 | 205 | 61.11 |
| Tesla 2022 | 13671 | 9995 | 3676 | 43 | 215 | 37.19 |

Ventaja frente a mantener en 6/8 series ejecutadas.

Politica congelada: momentum 32, revision cada 8 ticks, salida -16, reentrada +6 y trailing stop 20. Capital $10.000, comision $5 por orden ejecutada, maximo 63 acciones por orden, ejecucion al tick siguiente.

- [AMD enero 2022: informe y grafico](amd_enero/INFORME.md)
- [AMD mayo 2022: informe y grafico](amd_mayo/INFORME.md)
- [Apple 2022: informe y grafico](apple_2022/INFORME.md)
- [Apple 2023: informe y grafico](apple_2023/INFORME.md)
- [Meta 2022: informe y grafico](meta_2022/INFORME.md)
- [Netflix 2022: informe y grafico](netflix_2022/INFORME.md)
- [Netflix 2023: informe y grafico](netflix_2023/INFORME.md)
- [Tesla 2022: informe y grafico](tesla_2022/INFORME.md)

Son series conocidas de desarrollo. No se afirma superioridad fuera de muestra ni aprobacion fisica. Los graficos son exportables a un informe y las trazas RTL previas se cotejan con el modelo cuando estan disponibles.
