# Ver Pochoco Trader en el computador

## Probar directamente el ZIP de práctica

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\probar_series_practica.ps1
```

Lee `Downloads/Proyecto_4_Series_Practica_export.zip` y ejecuta sus CSV exactos
contra el RTL y firmware actuales, sin normalizar precios. Para otra ruta usa
`-Zip 'C:\ruta\archivo.zip'`. Cada serie reinicia CPU y cartera.

La ejecución guarda sus propios CSV, trazas, operaciones y logs en
`build/testbench_zip_practica/`, y el resumen con ocho trazas comprimidas en
`resultados_simulacion/testbench_zip_practica/`. Esta repetición corresponde a
las mismas ocho series conocidas, verificadas byte por byte contra el corpus.
No se contabiliza como nuevos datos ni reemplaza una captura física de la maestra.

Para generar los gráficos desde esas trazas RTL y su PDF LaTeX:

```powershell
python -B tools/graficar_zip_practica.py
wsl -d Ubuntu -- bash tools/compilar_zip_practica.sh
```

Abre `resultados_simulacion/testbench_zip_practica/ABRIR_RESULTADOS.html`
o `INFORME_ZIP_PRACTICA.pdf` para ver precio, compras/ventas, patrimonio y drawdown.

Desde esta carpeta (`Proyecto_4_Arquitectura-main`) abre PowerShell y ejecuta:

```powershell
python .\simular_competencia.py
```

Se abre el visor con Meta 2022. Elige una serie en el selector y pulsa **Iniciar / Pausar**.
Puedes avanzar un tick, reiniciar, cambiar los ticks por paso y ver las compras/ventas.
El boton **Exportar informe** guarda la serie completa, incluso si pausaste la animacion.

Para comenzar con otra serie:

```powershell
python .\simular_competencia.py --serie tesla_2022
```

Opciones: `amd_enero`, `amd_mayo`, `apple_2022`, `apple_2023`, `meta_2022`,
`netflix_2022`, `netflix_2023`, `tesla_2022`. El programa cambia el CSV de entrada;
el algoritmo de la FPGA es el mismo para todas y no conoce el nombre de la empresa.

Para generar las ocho series sin abrir una ventana:

```powershell
python .\simular_competencia.py --todas --sin-ventana
```

El programa imprime la ruta de `resultados_simulacion/<ejecucion>/`. Cada ejecucion
conserva sus propios archivos:

- `INFORME_COMPARATIVO.md` y `comparacion.csv`: tabla de resultados.
- Por serie: `INFORME.md`, `grafico.png`, `grafico.svg`, `ticks.csv`, `operaciones.csv`,
  `resumen.json` y la traza previa `referencia_RTL.csv` si esta disponible.
- El PNG se puede insertar directamente en Word; el SVG conserva el dibujo vectorial.

Los resultados del modelo se cotejan contra la entrega congelada y, si existe,
contra los 20.000 ticks de la traza RTL anterior. La reproduccion visual es a velocidad
humana y usa una traza precalculada. No recibe datos de la Go Board y no mide su latencia.

## Volver a ejecutar el testbench RTL

Para comprobar el RTL activo, incluyendo CS corto y compras/ventas:

```powershell
python -B tools/trader.py spi
```

Para la recuperacion, contabilidad e integracion completa:

```powershell
python -B tools/trader.py test
```

Para las ocho series completas contra el RTL activo en Ubuntu WSL, desde esta carpeta:

```powershell
wsl.exe -d Ubuntu -- bash tools/validar_activo_wsl.sh
```

Requiere WSL Ubuntu con Python, g++ y make. Los logs y CSV nuevos quedan en
`build/trader/verilator/`, y su resumen con hashes en
`build/trader/equivalencia_verilator.json`. Los bancos de
`proyecto4/alternativas/competitiva_definitiva/` conservan la validacion de referencia
anterior a la correccion de SPI.

## Competencia con la placa fisica

Con el BIN programado y verificado, la maestra debe enviar precios por SPI modo 0,
8 bits, MSB primero. La Go Board calcula automaticamente las ordenes para cualquier
serie compatible. Reiniciar antes de cada serie y esperar D1 antes de que empiece la maestra.

Para observar resultados fisicos, la maestra debe registrar precios y bytes MISO;
despues se calcula la cartera con las reglas oficiales. El puerto usado por iceprog
no convierte por si solo el computador en un visor de esas operaciones SPI.
La animacion no sustituye ese registro ni demuestra como termino una ronda real.

En el informe identificar por separado simulacion Python, RTL y medicion fisica.
Incluir ganancias y perdidas: las dos muestras de Netflix pierden frente a mantener.
Las ocho series ya son conocidas y no constituyen una prueba independiente de series secretas.

## Comportamiento de la tendencia lenta activa

### Testbench de todos los archivos de acciones

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\probar_todas_acciones.ps1
```

Ejecuta el RTL activo con las ocho series conocidas y los 35 CSV adicionales de
`Downloads/proyecto4.zip`. Cada adicional se prueba en escala proporcional y afín:
78 escenarios. Usa hasta 20.000 ticks por archivo; los dos CSV más cortos se
prueban con su longitud real, sin repetir datos. La cadencia predeterminada es
100 µs, la más exigente. Cada escenario reinicia CPU y cartera.

El script busca el ZIP en Downloads, en la raíz del repositorio y en su carpeta
superior. Puedes indicar otra ruta: `.\probar_todas_acciones.ps1 -Zip 'C:\ruta\proyecto4.zip'`.
Para repetir sin el ZIP, usa las trazas publicadas:
`wsl -d Ubuntu -- bash tools/repetir_acciones_archivadas_wsl.sh`.

El banco envía precios por SPI y comprueba MISO, DECISION, registros de caja e
inventario, SUM10, una decisión por precio, contabilidad y plazo de respuesta.
No programa ni lee la placa real; Verilator simula el circuito en dos estados.

Abre `resultados_simulacion/testbench_todas_acciones/ABRIR_RESULTADOS.html` para
filtrar por acción. `resumen.csv`, `resumen.json` e `INFORME.md` conservan resultados
y alcance. Las trazas por tick, operaciones, vectores y logs están en
`build/testbench_todas_acciones/`. Los CSV externos no se descargan ni se validan
contra una fuente de mercado; sus dos escalas comparten los mismos datos y usan
normalización retrospectiva. No constituyen 70 muestras independientes.

El anexo `INFORME_TESTBENCH.pdf` se genera desde `informe_testbench.tex` y muestra
el resumen y los resultados de cada escenario. Para regenerar su gráfico y fuente,
una vez terminados todos los casos: `python tools/generar_informe_testbench.py`.
Luego compila el PDF con `wsl -d Ubuntu -- bash tools/compilar_informe_testbench.sh`.

El visor y el BIN usan SUM10, revisión cada 128 ticks y umbral del 5%. Se empieza en caja. Primera señal posible en tick 256 y ejecución en 257 (índice inicial cero). La ausencia inicial de compras es esperada. El ancla se renueva en cada revisión: una subida acumulada lenta puede no activar entrada.

Para repetir los dos bancos oficiales adaptados: `python -B tools/validar_oficial.py`. Para Python frente al HEX real: `python -B proyecto4/alternativas/tendencia_lenta/validar_equivalencia.py`.

Integración de compra y venta a las cadencias largas, desde esta carpeta:

```powershell
wsl.exe -d Ubuntu -- bash tools/validar_activo_wsl.sh --integracion --periodo-ns 1000000
wsl.exe -d Ubuntu -- bash tools/validar_activo_wsl.sh --integracion --periodo-ns 10000000
```

Sin `--integracion`, el parámetro `--periodo-ns` permite repetir las ocho series completas a otra cadencia. La entrega actual incluye 160.000 ticks a 100 µs y 396 ticks de integración por cada cadencia larga. Los gráficos vigentes están en `resultados_simulacion/informe_tendencia_lenta/`; `informe_ocho_series/` corresponde a Momentum32 histórico.
