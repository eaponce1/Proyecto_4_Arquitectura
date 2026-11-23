# Validación oficial de tres rondas sin FPGA maestra

## Estado de ejecución

La prueba se ejecutó en simulación RTL usando el testbench publicado como emulador de la FPGA maestra. La copia del testbench oficial y la serie CSV se conservan en esta carpeta; el ejecutor crea una fuente configurada separada para cada corrida. No se editaron los cuatro criterios, la contabilidad, el firmware, el RTL ni los resultados previos.

Las seis corridas completaron 20.000 ticks y aprobaron los cuatro criterios. Ronda 3 conserva su corrida directa. Las rondas 1 y 2 se completaron con espera verificada en Icarus de cuatro estados. Las corridas directas parciales siguen archivadas por separado. El comparativo está en `comparacion_tres_rondas.csv`.

## Resultados comparables disponibles

| Ronda | Variante | Ticks | Criterios | Patrimonio | Órdenes | Compras / ventas | Comisiones | Drawdown | Ciclos promedio | Peor caso |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | Software original | 20.000 | 4/4 PASS | $4.577 | 931 | 466 / 465 | $4.655 | $5.476 | 218,67 | 413 |
| 1 | MMIO SMA10 base | 20.000 | 4/4 PASS | $4.577 | 931 | 466 / 465 | $4.655 | $5.476 | 60,66 | 254 |
| 2 | Software original | 20.000 | 4/4 PASS | $4.577 | 931 | 466 / 465 | $4.655 | $5.476 | 218,67 | 413 |
| 2 | MMIO SMA10 base | 20.000 | 4/4 PASS | $4.577 | 931 | 466 / 465 | $4.655 | $5.476 | 60,66 | 254 |
| 3 | Software original | 20.000 | 4/4 PASS | $4.577 | 931 | 466 / 465 | $4.655 | $5.476 | 218 | 413 |
| 3 | MMIO SMA10 base | 20.000 | 4/4 PASS | $4.577 | 931 | 466 / 465 | $4.655 | $5.476 | 60 | 255 |

En las seis corridas la caja final fue $2.017 y el inventario final fue de 16 acciones. La secuencia completa de decisiones y la contabilidad por tick coincidieron con la ronda 3 ya contrastada con Python. Las rondas 1 y 2 muestran el promedio con dos decimales. Ronda 3 conserva el promedio entero truncado de la corrida histórica.

Los presupuestos efectivos del banco son 249.762, 24.762 y 2.262 ciclos en las rondas 1, 2 y 3. El peor caso de cada arquitectura estuvo por debajo de su presupuesto en los 20.000 ticks de práctica.

| Ronda | Tiempo simulado | Icarus software | Icarus MMIO |
|---|---:|---:|---:|
| 1 | 200,000004 s | 659,79 s | 470,43 s |
| 2 | 20,000004 s | 643,56 s | 470,08 s |
| 3 | 2,000004 s | 2 h 30 min 11 s | 7 h 37 min 39 s |

Los tiempos de Icarus de las rondas 1 y 2 se midieron alrededor del proceso `vvp`. Los de ronda 3 proceden de marcas de tiempo de los artefactos históricos.

## Auditoría del testbench y del ejecutor

El testbench recibido declara originalmente `NTICKS=2000` y periodo 100.000 ns. `ejecutar_validacion.py` valida por separado que el CSV tenga encabezado `tick,price`, exactamente 20.000 filas consecutivas y precios byte; deriva una copia con 20.000 ticks, rutas de programa/CSV, periodo de ronda, `EnableSpi=1`, ruta del CSV de decisiones y acumulación adicional de ciclos. La tarea de contabilidad `ejecutar` queda sin cambios.

El ejecutor conserva las expresiones `bits_x == 0`, `respuestas > 0`, `precios_perdidos == 0` y `peor_caso < presupuesto`. Los CSV de las seis corridas coinciden exactamente. `verificacion_tres_rondas.log` registra 20.000 respuestas por corrida acelerada, el tiempo simulado exacto y la coincidencia con las filas ya producidas por las corridas directas de rondas 1 y 2.

## Viabilidad de Verilator en Windows

En este entorno se detectó Verilator 5.053 y se consiguió traducir el diseño y el testbench derivado con `--binary --timing`, tras configurar `VERILATOR_ROOT`. La compilación se detuvo al intentar invocar `make`: el ejecutable no está instalado. Tampoco se detectaron `g++`, `clang++`, `cl.exe` ni `nmake.exe`. Icarus 14.0 y `vvp` sí están disponibles.

Hay una limitación semántica independiente de las dependencias: Verilator es principalmente un simulador de dos estados. Su documentación explica que X se sustituye por un valor 0/1 y que comparaciones de identidad frente a X no se comportan como en un simulador de cuatro estados. Por eso `miso !== 1'b0 && miso !== 1'b1` no puede acreditar con Verilator el mismo criterio oficial “MISO sin valores X”. Instalar Make y C++ permitiría construirlo y acelerar la simulación, pero no haría que el criterio X fuese una validación equivalente. [Documentación de estados desconocidos de Verilator](https://verilator.org/guide/latest/languages.html#unknown-states), [opción `--binary`](https://verilator.org/guide/latest/exe_verilator.html#binary).

### Instalación posible (no ejecutada)

Ruta WSL/Ubuntu, si WSL y una distribución están habilitados:

```bash
sudo apt-get update
sudo apt-get install verilator make g++
```

Verilator ya está presente; la guía oficial enumera `make` y `g++` (o `clang`) como paquetes estándar para ejecutar/build del simulador. [Guía oficial de instalación](https://verilator.org/guide/latest/install.html#install-prerequisites).

Ruta Windows con MSYS2: instalar el entorno y, en la terminal UCRT64, añadir GNU Make y GCC:

```powershell
winget install --exact --id MSYS2.MSYS2
# En la terminal MSYS2 UCRT64:
pacman -Syu
pacman -S make mingw-w64-ucrt-x86_64-gcc
```

En UCRT64, agregar `C:\msys64\ucrt64\bin` y `C:\msys64\usr\bin` al `PATH`. Verilator documenta compilación nativa Windows con MSVC y MinGW; `--binary` necesita GNU Make y un compilador C++. [Instalación de Verilator](https://verilator.org/guide/latest/install.html#os-requirements).

En esta sesión `winget` no pudo ejecutarse por permisos del entorno y WSL devolvió `E_ACCESSDENIED`; no se instaló software ni se modificó el sistema. No se recomienda sustituir el check X por una interpretación de dos estados ni cambiar el banco para hacer que Verilator lo apruebe.

## Coste de Icarus y opciones de optimización

Los registros de las corridas completas de ronda 3 marcan aproximadamente **7 h 37 min 39 s** para MMIO y **2 h 30 min 11 s** para software. Son duraciones observadas por marcas de tiempo de creación/fin de los artefactos, no benchmarks controlados.

El periodo de ronda 2 es diez veces el de ronda 3 y el de ronda 1 cien veces. Si el runtime escalara linealmente con los ciclos de reloj simulados, la extrapolación sería:

| Variante | Ronda 3 observada | Ronda 2 extrapolada, no medida | Ronda 1 extrapolada, no medida |
|---|---:|---:|---:|
| MMIO | 7 h 37 min | ~3 d 4 h | ~31 d 19 h |
| Software | 2 h 30 min | ~1 d 1 h | ~10 d 10 h |

La extrapolación corresponde al reloj continuo. El modo `--fast-idle` usa Icarus de cuatro estados y actúa en la copia derivada del banco. Tras completar DECISION y con CS_n inactivo, simula ocho ciclos de sondeo STATUS. Solo omite periodos enteros cuando el estado del procesador, SPI, RAM y SMA10 vuelve a su valor anterior. Durante la comprobación permite una lectura STATUS, admite escrituras únicamente a x2 y exige ausencia de `byte_done`. Los contadores de tiempo y el filtro de botones avanzan su valor exacto. Si el estado no se repite, el banco conserva toda la espera directa.

El reloj reanuda en su fase original y la simulación conserva los 10 ms o 1 ms entre tramas. Icarus ejecuta cada transacción SPI, el código de contabilidad y las expresiones de los cuatro criterios del profesor. El ejecutor verifica una huella de las fuentes, del HEX, del modelo de RAM y del original del profesor antes de habilitar la reducción. La opción deja resultados separados en `corridas_aceleradas/`.

Los contrastes directos de 8 ticks de ronda 1 y 16 de ronda 2 coincidieron con el modo acelerado en cada fila, contabilidad, promedio, suma, peor caso, cuatro criterios y tiempo de simulación. En esos contrastes, Icarus directo tardó entre 152,98 y 155,78 s en ronda 1 y entre 34,66 y 35,01 s en ronda 2. La espera verificada tardó entre 0,35 y 0,36 s y entre 0,62 y 0,68 s, respectivamente. Son tiempos medidos de contrastes cortos. El registro está en `contraste_esperas.log`.

## Comandos reproducibles

Desde la raíz `pochoco_soc-main` y con Icarus/VVP en `PATH`:

```powershell
python -B proyecto4/resultados/validacion_oficial/ejecutar_validacion.py --variant software --round 1 --fast-idle
python -B proyecto4/resultados/validacion_oficial/ejecutar_validacion.py --variant mmio --round 1 --fast-idle
python -B proyecto4/resultados/validacion_oficial/ejecutar_validacion.py --variant software --round 2 --fast-idle
python -B proyecto4/resultados/validacion_oficial/ejecutar_validacion.py --variant mmio --round 2 --fast-idle
python -B proyecto4/resultados/validacion_oficial/resumir_corridas.py --tres-rondas
```

Para repetir el contraste corto, ejecuta las mismas variantes y rondas con `--ticks 8` en ronda 1 y `--ticks 16` en ronda 2. Usa `--output-root proyecto4/resultados/validacion_oficial/contraste_directo` en el modo directo, y `--output-root proyecto4/resultados/validacion_oficial/contraste_rapido` junto con `--fast-idle` en el modo acelerado. Ejecuta después `python -B proyecto4/resultados/validacion_oficial/verificar_espera.py`.

## Pendientes y limitaciones

- Rondas 1 y 2 de ambas variantes: 20.000 ticks y 4/4 PASS por corrida en Icarus con espera verificada.
- Verilator: traducción observada, build no completado (Make/C++ ausentes); aun instalado, no valida el check oficial de X en cuatro estados.
- Ronda 3: completa, cuatro criterios aprobados por variante, 20.000 ticks, decisiones equivalentes.
- FPGA maestra del profesor: no disponible. La integración física sigue pendiente; estas corridas son emulación RTL, no prueba física.
- Los resultados históricos de ronda 3 y los insumos originales se conservan en sus rutas canónicas.
