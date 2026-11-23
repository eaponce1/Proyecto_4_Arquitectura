# Informe – demo autónoma del agente en Go Board

Fecha de validación: 22 de noviembre de 2026. Esta es una validación de RTL y
herramientas de implementación; la placa no se programó ni se probó físicamente.

## Diseño

El top nuevo `demo_autonoma_top` conecta `price_spi_master` directamente con el
SPI Slave original. El SoC reducido `pochoco_soc_demo` conserva el Espino,
`pochoco_ram`, `pochoco_spi_slave`, `pochoco_sma10` y carga
`proyecto4/alternativas/mmio_sma10/sw/trade.hex`. Solo excluye del top el
periférico del juego, switches y displays, que el firmware de trading no usa.
Los módulos reutilizados se instancian desde sus archivos originales, sin
copiarlos ni modificarlos.

El maestro envía 16 precios fijos: `c8` diez veces, `5a` tres veces y `dc` tres
veces (200, 90 y 220 decimal). La tabla es compacta, decodificada por rangos del
índice. El maestro recibe MISO pero no interpreta ni produce decisiones. La
decisión es calculada por el Espino ejecutando el firmware; el verificador de
Python solo produce vectores esperados para el testbench.

## Simulación Icarus

Resultado: **PASS**, 16 ticks, sin pérdidas.

| Comprobación observada | Resultado |
|---|---:|
| Fetch del Espino | 49.155 |
| Commit del Espino | 36.902 |
| Lecturas STATUS | 12.160 |
| Lecturas PRICE | 16 |
| Lecturas SUM10 | 16 |
| Lecturas READY | 16 |
| Escrituras DECISION por el core | 16 |
| Bytes MISO revisados | 16 |
| Ticks perdidos | 0 |
| Órdenes en la secuencia | 1 compra, 1 venta |

Las 16 escrituras del Espino y las 16 respuestas MISO coinciden byte a byte con
los vectores producidos por `estrategia_reversion_media` y
`simular_estrategia`. Las escrituras por tick son
`00 00 00 00 00 00 00 00 00 00 50 00 00 90 00 00`. MISO devuelve la decisión
anterior: `00 00 00 00 00 00 00 00 00 00 00 50 00 00 90 00`. Así se comprueba el
desfase de una transacción.

El testbench además valida los 16 bytes de precio recibidos y falla ante una
decisión fuera de orden, duplicación o precio anterior aún sin consumir.

## Síntesis y place and route

Ejecutados con Yosys y nextpnr para **iCE40 HX1K/VQ100**, objetivo de reloj
**25 MHz**, seed 1. Place and route terminó normalmente y pasó el objetivo.

| Métrica | Medición |
|---|---:|
| LUT4 (Yosys) | 991 |
| Logic Cells (nextpnr) | 1174 / 1280 (91%) |
| Margen de LC | 106 |
| BRAM | 9 / 16 |
| Fmax estimada por nextpnr | 41,53 MHz |
| Restricción solicitada | 25 MHz, PASS |
| Binario empaquetado | Sí, independiente |

El margen confirma que esta versión cabe según el place-and-route realizado.
No es una comparación A/B sintetizada en la misma ejecución con la MMIO base;
como referencia histórica, el reporte de MMIO base indica 1279/1280 LC y 13/16
BRAM. La reducción en esta variante proviene principalmente de retirar del
wrapper los displays, switches y lógica de juego no usada y de mantener el
generador con contadores acotados, sin tabla de decisiones ni verificador
sintetizable. El intento diagnóstico anterior reportó 1550 LC; la variante
actual registra 376 LC menos, aunque no es una comparación aislada de una sola
modificación. El generador SPI compacto y los indicadores se mantienen.

El PCF asigna el reloj a pin 15 y LEDs a 56, 57, 59 y 60, siguiendo el PCF de la
Go Board del repositorio. nextpnr aceptó las cinco asignaciones. El SPI no usa
pines externos. La polaridad visual de los LEDs requiere confirmación durante
la prueba manual de placa.

El `.bin` está en `build/demo_autonoma.bin`. No se ejecutó herramienta de
programación de FPGA. El binario no reemplaza los bitstreams existentes.
SHA-256: `CF58AC1E4C4656A287CE168509B6D3CDB375C5C34183DC64CC7E68E572E20CE4`.

## Reproducción

Desde `pochoco_soc-main`:

```powershell
powershell -ExecutionPolicy Bypass -File proyecto4/pruebas_fisicas/demo_autonoma/ejecutar_pruebas.ps1
powershell -ExecutionPolicy Bypass -File proyecto4/pruebas_fisicas/demo_autonoma/sintetizar.ps1
```

Versiones observadas en este entorno: Python 3.13.3, Icarus Verilog 14.0
(devel, s20260301-626-g7e3d0c6bd-dirty), Yosys 0.70+176 y nextpnr-ice40
0.11.1-68-g1daf1f5c. El script solo genera el binario tras confirmar que
nextpnr termina normalmente, el diseño no supera 1280 LC y el objetivo de
25 MHz pasa.

## Pendientes y límites

- No se ha realizado prueba física ni programación manual de la placa.
- No se verificaron ópticamente los niveles activos de los LEDs.
- La secuencia de 16 ticks demuestra el flujo de extremo a extremo, no la serie
  de 20.000 ticks de la evaluación oficial.
- El testbench mide fetch y commit mediante señales internas jerárquicas; esos
  contadores son instrumentación de simulación, no periféricos añadidos al SoC.
- El binario es una variante demostrativa separada, no el bitstream final del
  agente MMIO base.
