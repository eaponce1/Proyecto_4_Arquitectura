# Ver Pochoco Trader en el computador

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

Para una comprobacion nueva corta con Icarus:

```powershell
python -X utf8 -B .\proyecto4\alternativas\competitiva_definitiva\validar_rtl.py --rapido
```

Para las ocho series completas con el RTL y Verilator en Ubuntu WSL:

```powershell
wsl.exe -d Ubuntu -- bash proyecto4/alternativas/competitiva_definitiva/ejecutar_verilator_wsl.sh
```

Requiere WSL Ubuntu con Python, g++ y make. Los logs y CSV de esa corrida quedan en
`proyecto4/alternativas/competitiva_definitiva/build/verilator/`. El comando vuelve
a ejecutar el testbench y sus aserciones. Para repetir todo en Icarus, ejecutar
`validar_rtl.py` sin opciones; es considerablemente mas lento.

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
