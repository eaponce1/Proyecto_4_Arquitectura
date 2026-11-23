# Validación oficial de tres rondas sin FPGA maestra

## Estado de ejecución

La prueba se ejecutó en simulación RTL usando el testbench publicado como emulador de la FPGA maestra. La copia del testbench oficial y la serie CSV se conservan en esta carpeta; el ejecutor crea una fuente configurada separada para cada corrida. No se editaron los cuatro criterios, la contabilidad, el firmware, el RTL ni los resultados previos.

La ronda 3 es la única con resultados completos. Las corridas de las rondas 1 y 2 están iniciadas en Icarus y sus CSV son parciales. Durante la revisión del 23 de noviembre se observaron 526 ticks de ronda 1 y 5.365 de ronda 2 en ambas arquitecturas. Esos avances no acreditan los cuatro criterios ni permiten calcular resultados finales. Icarus requiere muchas horas a los periodos largos. Una corrida con Verilator en dos estados dejaría sin acreditar el criterio oficial de MISO sin X.

## Resultados comparables disponibles

| Ronda | Variante | Ticks | Criterios | Patrimonio | Órdenes | Compras / ventas | Comisiones | Drawdown | Ciclos promedio truncado | Peor caso |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | Software original | — | Pendiente | — | — | — | — | — | — | — |
| 1 | MMIO SMA10 base | — | Pendiente | — | — | — | — | — | — | — |
| 2 | Software original | — | Pendiente | — | — | — | — | — | — | — |
| 2 | MMIO SMA10 base | — | Pendiente | — | — | — | — | — | — | — |
| 3 | Software original | 20.000 | 4/4 PASS | $4.577 | 931 | 466 / 465 | $4.655 | $5.476 | 218 | 413 |
| 3 | MMIO SMA10 base | 20.000 | 4/4 PASS | $4.577 | 931 | 466 / 465 | $4.655 | $5.476 | 60 | 255 |

En ronda 3, caja final = $2.017 y acciones finales = 16 en ambas variantes. La secuencia de decisiones coincide exactamente en **20.000 de 20.000 ticks**. El promedio de ciclos es el promedio impreso por la copia de ejecución con división entera truncada; no es un promedio decimal. La comparación completa y los CSV por tick están en `comparacion_oficial.csv` y `corridas/*/ronda_3/decisiones.csv`.

El periférico MMIO reduce ciclos de cálculo (promedio truncado 218→60; peor caso 413→255) sin alterar estrategia, decisiones ni resultado contable en ronda 3. Esto no demuestra el cumplimiento de los presupuestos de las rondas 1 y 2; dichos presupuestos y corridas siguen sin validarse.

## Auditoría del testbench y del ejecutor

El testbench recibido declara originalmente `NTICKS=2000` y periodo 100.000 ns. `ejecutar_validacion.py` valida por separado que el CSV tenga encabezado `tick,price`, exactamente 20.000 filas consecutivas y precios byte; deriva una copia con 20.000 ticks, rutas de programa/CSV, periodo de ronda, `EnableSpi=1`, ruta del CSV de decisiones y acumulación adicional de ciclos. La tarea de contabilidad `ejecutar` queda sin cambios.

Los cuatro checks que el ejecutor exige, y cuya expresión se conserva, son: `bits_x == 0`; `respuestas > 0`; `precios_perdidos == 0`; `peor_caso < presupuesto`. El banco no comprueba por sí mismo que cada byte de DECISION sea el esperado por Python; la comparación de decisiones entre variantes se hace en los CSV. En ronda 3 no hubo diferencias.

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

La extrapolación es solo una guía de planificación y no un resultado. La ayuda instalada de Icarus/VVP no ofrece una opción JIT o un modo de aceleración de runtime que conserve el mismo modelo de eventos. El comando actual ya evita trazas, compila con `-g2012` y ejecuta `vvp -n`; no se encontró un flag seguro que convierta las rondas lentas en corridas prácticas. Cambiar el reloj/sondeo o saltar eventos requeriría modificar el comportamiento temporal de la prueba y no se hizo.

## Comandos reproducibles

Desde la raíz `pochoco_soc-main` y con Icarus/VVP en `PATH`:

```powershell
python -B proyecto4/resultados/validacion_oficial/ejecutar_validacion.py --variant software --round 1
python -B proyecto4/resultados/validacion_oficial/ejecutar_validacion.py --variant mmio --round 1
python -B proyecto4/resultados/validacion_oficial/ejecutar_validacion.py --variant software --round 2
python -B proyecto4/resultados/validacion_oficial/ejecutar_validacion.py --variant mmio --round 2
python -B proyecto4/resultados/validacion_oficial/resumir_corridas.py
```

Cada comando de ronda tarda potencialmente días en esta configuración; sus salidas se guardan por variante/ronda y no sobrescriben ronda 3. Para la prueba completa equivalente del criterio MISO X se requiere un simulador de cuatro estados como Icarus.

## Pendientes y limitaciones

- Rondas 1 y 2 de ambas variantes: no ejecutadas; quedan pendientes por coste de simulación verificado y falta de ruta compatible más rápida.
- Verilator: traducción observada, build no completado (Make/C++ ausentes); aun instalado, no valida el check oficial de X en cuatro estados.
- Ronda 3: completa, cuatro criterios aprobados por variante, 20.000 ticks, decisiones equivalentes.
- FPGA maestra del profesor: no disponible. La integración física sigue pendiente; estas corridas son emulación RTL, no prueba física.
- No se modificaron resultados históricos, firmware, Assembly, HEX, RTL original ni criterios. No se hizo commit ni push.
