# Informe de co-diseño hardware/software — Proyecto 4

## Definición de operación y referencias

Una operación útil equivale a un tick: recibir un byte de precio por SPI,
consumirlo en Espino y escribir la decisión siguiente antes del precio
posterior. El testbench verifica MISO contra Python en cada transacción;
por ello mide la decisión anterior y conserva el desfase SPI.

La referencia software cubre 20.000 ticks: media 218.66 ciclos y 91.92 instrucciones por tick. La región SMA10 directa promedia 163.93 ciclos; para Amdahl defino kernel como actualización del historial + SMA + generación de señal, que ocupa 186.62 ciclos/tick (85.35% del total). El baseline del SoC con SPI habilitado usa 980 LUT4, 1200/1.280 LC, 12/16 BRAM y Fmax enrutada de 42.6 MHz; pasa a 25 MHz.

La CPI es ciclos medios / instrucciones medias. `ops/s @25MHz` es capacidad de servicio del core (25e6 / ciclos/tick); `ops/s @SPI` es el caudal real de entrada del test a 30 us/tick (33.333 ticks/s). La operación útil requiere una entrada SPI, así que el caudal del sistema en esta prueba queda limitado por SPI. `ops/s @Fmax` usa la frecuencia máxima enrutada cuando existe. Los speedups comparan ciclos/tick; `speedup_at_Fmax` compara capacidad a Fmax.

## Mediciones

| Versión | ticks | IC media | Ciclos media | Mediana | p95 | Peor | CPI | ticks/s core @25MHz | ticks/s SPI @30us | ticks/s @Fmax | speedup medido | speedup Amdahl | LUT4 | LC/1280 | BRAM/16 | Fmax | Ruta |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| Original SW | 20000 | 91.92 | 218.66 | 210 | 217 | 412 | 2.379 | 114331 | 33333 | 194820 | 1.000x | 1.000x | 980 | 1200 | 12 | 42.6 | PASS |
| custom-0 | 20000 | 30.94 | 70.73 | 62 | 69 | 266 | 2.286 | 353435 | 33333 | NA | 3.091x | 3.076x | 1133 | 1350 | 14 | NA | FAIL: 70 LC sobre HX1K |
| MMIO SMA10 | 20000 | 26.85 | 60.64 | 52 | 58 | 255 | 2.259 | 412270 | 33333 | 667878 | 3.606x | 3.692x | 1055 | 1279 | 13 | 40.5 | PASS |

## Alternativa 1: custom-0

Se añadió `smaupd rd,rs1,rs2` en opcode `0x0B`, funct3/funct7 cero, con operación módulo 2^32 `rd <- rd - rs1 + rs2`. El valor antiguo de rd se toma por un tercer puerto síncrono de lectura; rs1 y rs2 son el precio saliente y el entrante. El decoder rechaza codificaciones inválidas. Los códigos y el assembler están aislados en `proyecto4/alternativas/custom0/`; el RTL y assembler originales permanecen sin cambios.

La suma completa se construye una vez al llenar las diez muestras; después se aplica la actualización en una instrucción. El testbench unitario revisa aritmética/decode, y el testbench SoC compara MISO/Python. La síntesis Yosys termina, pero nextpnr informa 1350/1.280 LC y 14/16 BRAM en HX1K, así que no obtiene Fmax de placa.

## Alternativa 2: periférico MMIO

El nuevo módulo recibe el evento del byte completo SPI y conserva diez precios en una BRAM. SUM10 está en `0x8001000C` (offset 3) y READY bit 0 en `0x80010010` (offset 4), libres después de los offsets STATUS=0, PRICE=1 y DECISION=2 de `pochoco_spi_slave.v`. El periférico solo actualiza SMA10; el core lee SUM10/READY, aplica la contabilidad y decide. No se altera el dato MISO ni DECISION de la FPGA maestra.

El banco autónomo verificó 20.000 precios tick a tick. El testbench integrado compara decisión/MISO con Python y detecta ticks perdidos. Yosys sintetiza y nextpnr coloca 1279/1.280 LC y 13/16 BRAM, con Fmax final de 40.5 MHz; pasa el requisito de 25 MHz.

## Amdahl

Se toma P=0.8535, kernel (actualización del historial + SMA + señal) / tiempo total del baseline. Para cada variante, la aceleración local del kernel se calcula como 186.62 / ciclos de esa región por tick observados; `kernel_measurement_ticks` identifica si el perfil provino de la serie completa o de la muestra inicial de 100 ticks. Se aplica S = 1 / ((1-P)+P/Slocal). La predicción y el speedup medido se informan por separado.

## Roofline simplificado

Supuestos: 1 operación aritmética entera equivale a suma/resta; 1 byte SPI se mueve por tick; el límite de lectura de una BRAM iCE40 es 16 bits × 25 MHz = 50 MB/s; peak del core = 1 operación/ciclo × 25 MHz = 25 Mops/s. Se cuenta solo el kernel y se excluyen ramas, SPI de sondeo, registros/caches y señales de control. Es un roofline de cálculo, no una medición de ancho de banda.

| Kernel | Operaciones enteras/tick | Bytes/tick asumidos | Intensidad ops/B | Techo memoria (Mops/s) | Región estimada |
|---|---:|---:|---:|---:|---|
| Original | 14 (10 sumas + 4 para 10×precio) | 41 (10 LW × 4 B + precio) | 0,341 | 17,1 | limitado por memoria bajo el modelo |
| custom-0 | 6 (2 aritméticas fusionadas + 4 para 10×precio) | 5 (un precio saliente de palabra + precio SPI) | 1,200 | 60,0 | limitado por cómputo |
| MMIO | 6 (2 de actualización + 4 para 10×precio) | 11 (precio actual/saliente, BRAM y dos lecturas MMIO) | 0,545 | 27,3 | cerca del techo de cómputo |

Los bytes y conteos de operaciones son aproximaciones del kernel declaradas aquí; el movimiento interno exacto y los ciclos SPI no son tráfico DRAM. custom-0 no cabe en HX1K; MMIO sí se enrutó, aunque deja solo una LC libre.

## Validación y comandos

| Prueba | Resultado |
|---|---|
| Python Proyecto 4 | 32 pruebas pasan |
| testbench unitario custom-0 | pasa |
| assembler custom-0 | 3 pruebas pasan |
| periférico SMA10 autónomo | 20.000 entradas, suma/READY coinciden |
| SoC SPI custom-0 | PASS: 20.000 ticks, 0 perdidos, 0 discrepancias MISO/Python, 20.000 PRICE/DECISION |
| SoC SPI MMIO | PASS: 20.000 ticks, 0 perdidos, 0 discrepancias MISO/Python, 20.000 PRICE/DECISION |
| Proyecto 2: core_tb | pasa |
| Proyecto 2: spi_tb / decoder_tb / game_top compile | pasan manualmente |
| Proyecto 2: periph_tb | falla en `debounced buttons` (tests/periph_tb.v:27); RTL P2 verificado idéntico al snapshot previo |
| síntesis física | baseline y MMIO enrutan; custom-0 excede LC HX1K y no tiene Fmax enrutable |

Desde `pochoco_soc-main`:

```powershell
python -m unittest discover -s proyecto4/python -v
python -m unittest proyecto4.alternativas.custom0.tb.test_assembler_custom0 -v
python proyecto4/alternativas/custom0/medir_custom0.py --ticks 20000
python proyecto4/alternativas/mmio_sma10/medir_mmio_sma10.py --ticks 20000
python proyecto4/python/sintetizar_codisenio.py
python proyecto4/python/generar_codisenio.py
```

## Conclusión

En simulación ambas alternativas reducen el trabajo de SMA10 y preservan la estrategia. custom-0 excede HX1K (1350/1.280 LC) y no obtiene Fmax. MMIO enruta a 40.5 MHz con 1279/1.280 LC, dejando 1 LC libres; su margen es mínimo y debe tratarse con cautela ante cambios de versión o configuración.
