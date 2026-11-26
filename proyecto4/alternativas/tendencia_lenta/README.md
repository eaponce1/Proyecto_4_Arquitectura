# Tendencia lenta activa

Firmware original de `alternativas/momentum_lento` del `proyecto4.zip` aportado. `origen.json` identifica ZIP y fuentes. Se conserva la lógica original de 130 palabras y se integra con el SPI corregido del proyecto actual.

| Criterio | Momentum32 + stop anterior | Tendencia lenta activa |
|---|---|---|
| Inicio | Invierte desde el comienzo | Comienza en caja |
| Indicador | Precio menos precio de 32 ticks atrás | SUM10: suma de los diez últimos precios |
| Revisión | Cada 8 ticks | Cada 128 ticks |
| Compra/reentrada | Delta >= +6 | SUM10 >= 105% del ancla de revisión anterior |
| Venta | Delta <= -16 o caída de 20 desde el pico | SUM10 <= 95% del ancla de revisión anterior |
| Ancla | Historial de 32 y pico de posición | Se renueva en toda revisión, aunque no haya señal |
| Cantidad | Hasta 63 por orden | Hasta 63; compra adicional mínima de 8 si ya hay acciones |
| Primera ejecución posible | Tick 1 | Tick 257 |
| Ejecución de señales | Precio siguiente | Precio siguiente |
| Ventajas frente a mantener | 6/8 conocidas | 5/8 conocidas |
| Patrimonio medio | $12.725 | $10.971,13 |
| Peor patrimonio | $8.615 | $8.540 |
| Máximo drawdown | 61,11% | 50,55% |

Los índices comienzan en cero. En tick 128 se guarda el primer ancla; en 256 puede emitirse señal y en 257 ejecutarse. Las comparaciones usan `20 * diferencia >= ancla`, sin división. Si ninguna supera 5%, se conserva el régimen. No existe trailing stop en esta política.

El estrés sintético de saltos extremos termina con **$69** y drawdown **99,31%**; pasa equivalencia técnica porque modelo, instrucciones y RTL coinciden, pero es una pérdida financiera severa. El drawdown de 50,55% de la tabla solo corresponde a las ocho series conocidas.

La mejora de Netflix convive con pérdidas en otras series. Esta integración se realiza por elección del grupo y no demuestra que siempre sea mejor. En lateralidad o con aumentos pequeños por ventana puede no comprar en toda la ronda.

## Reproducir desde la raíz del repositorio

```powershell
python -B proyecto4/alternativas/tendencia_lenta/test_invariantes.py
python -B proyecto4/alternativas/tendencia_lenta/validar_equivalencia.py
python -B tools/trader.py test
python -B tools/validar_oficial.py
wsl -d Ubuntu -- bash tools/validar_activo_wsl.sh
python -B tools/trader.py build
python -B tools/auditar_lenta.py
```

Windows requiere OSS CAD Suite en PATH. Las puertas y Verilator utilizan Ubuntu WSL con Python, g++ y make. En Linux los ejecutores Python pueden usarse directamente con sus herramientas instaladas. `build` reutiliza una imagen vigente si todas sus fuentes coinciden; para fuentes nuevas exige repetir la evidencia que quedó desactualizada. No ejecuta `iceprog`.

La equivalencia ejecuta el HEX en un intérprete RV32E real y coteja MISO, DECISION, caja, acciones y régimen en 160.000 ticks más sintéticos. El RTL activo completa las ocho series a 100 µs. La integración de 396 ticks pasa también a 1 ms y 10 ms; no equivale a ocho series completas en cada cadencia larga. Los bancos oficiales adaptados pasan 4/4 cada uno; originales y tareas financieras se preservan.

El escenario `[100]*128 + [110]*128 + [100]*140` compra 63 en tick 257 y 36 en 258; vende 63 en 385 y 36 en 386. Termina con $9.980, cuatro órdenes y $20 en comisiones. RTL, netlist y BIN reconstruido verifican esos bytes. El modelo del BIN tiene retardos funcionales uniformes de 1 ns; el timing físico procede de nextpnr.

## Programar y observar

El archivo vigente está en `competition.bin`, en la raíz del proyecto. Reiniciar antes de cada serie/ronda, esperar D1 e iniciar una serie nueva en la maestra.

```powershell
iceprog competition.bin
iceprog -c competition.bin
```

La programación y prueba física de **esta imagen** están pendientes. La sesión anterior con dos `VERIFY OK` aplica a Momentum32. El respaldo local está en `respaldos/momentum32_fisico_5e1579ca/`; en Git corresponde al commit `07d0dd95d491f7b7f08a6f1b813d998e53a8c123`.

`python simular_competencia.py` abre el visor del modelo activo. `resultados_simulacion/informe_tendencia_lenta/` contiene los ocho gráficos e informes; el PDF principal está en `docs/INFORME_FINAL.pdf`. No son telemetría de la placa.
