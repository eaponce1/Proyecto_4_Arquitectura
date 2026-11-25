# Auditoría final de cierre del Proyecto 4

24 de noviembre de 2026. La arquitectura de entrega es **MMIO SMA10 base** en Go Board iCE40 HX1K/VQ100, con SPI externo y reloj de 25 MHz.

| Área | Estado | Evidencia |
|---|---|---|
| Validación funcional | **APROBADO** | Icarus completó 2.000/2.000 ticks, el banco aprobó 4/4 y Python coincidió en DECISION y MISO. Suite Python 32/32. |
| Validación de rendimiento | **APROBADO** | 253 ciclos de peor caso frente a 2.262 en la repetición. |
| Síntesis, enrutado y timing | **APROBADO** | Yosys, nextpnr e icepack completaron. El BIN reconstruido iguala la imagen de competencia por SHA-256. |
| Demo física con maestro interno | **APROBADO** | Evidencia previa en Go Board a 12,5 MHz, 16 ticks, flash verificada, LEDs `1010` y UART `0xAA` en tres arranques. |
| Validación física con FPGA maestra | **PENDIENTE** | Falta el ensayo del SPI externo con la imagen de competencia, el cableado del curso y el canal MISO del grupo. |
| Preparación de entrega local | **APROBADO** | Paquete auditado con las fuentes, el BIN de competencia, la guía Windows y las evidencias. |
| Identidad de dos artefactos históricos de diagnóstico | **FALLIDO** | La revisión del árbol Git publicado difiere de la que contiene el ZIP publicado y el árbol local. Las dos quedan identificadas por su hash. |

El cierre integral queda **PENDIENTE** hasta completar la prueba física con la maestra y registrar la competencia y la defensa.

## 1. Congelación y comparación con Git

El directorio descargado carece de `.git`. Allí `git status` y `git diff` devolvieron errores de contexto. El checkout de la entrega estaba limpio en `main`, sin diff en el árbol ni en el índice, en el commit `5229fdbd3d9d674fc9fec207d3e68f4370294017`. Se usó `git archive` de ese commit para repetir la prueba en un directorio aislado, con los tres archivos de `tb/` del árbol local.

En la fotografía anterior a las ediciones documentales se compararon 320 archivos publicados y 1.001 archivos locales. Se registraron 681 archivos locales sin seguimiento en el commit de referencia, 165 diferencias de finales de línea y dos diferencias de contenido. Los 681 incluyen artefactos y experimentos locales anteriores, además del banco nuevo. Se encontraron cero archivos publicados ausentes en el árbol descargado. El inventario excluye los tres checkouts de publicación anidados y registra rutas con SHA-256. [Inventario completo](../resultados/auditoria_final_cierre/inventario_git.csv) · [Estado Git y diffs](../resultados/auditoria_final_cierre/estado_git.log)

Los tres archivos funcionales que aporta el banco son `tb/tb_proyecto_4.sv`, `tb/ejecutar_tb_proyecto4.ps1` y `tb/comparar_tb_proyecto4.py`. La auditoría añadió documentación y evidencias. Se comprobaron 45 fuentes, configuraciones e imágenes protegidas, incluido Espino, MMIO SMA10 base, `trade.s`, `trade.hex` y la referencia Python, y 20 archivos de las corridas oficiales publicadas. [Verificación de repetición e integridad](../resultados/auditoria_final_cierre/verificacion_repeticion.log)

### Diferencia histórica registrada

Las dos diferencias de contenido están en `proyecto4/pruebas_fisicas/demo_autonoma_bus_detail/build/` y ya estaban presentes al iniciar la auditoría. El README de esa carpeta documenta el uso del mismo nombre para revisiones sucesivas.

| Archivo | SHA-256 local y del ZIP publicado | SHA-256 del árbol Git publicado |
|---|---|---|
| `timeout_diagnostico.bin` | `E02DAC67FC7D0DDE0C268D50D37A04FCBC19926AA0BCA22D21D89F6D91182BD3` | `FF757BD2942B489159B07F8D811E0F5B5F80F957B849E1FFD9F073BDD530899C` |
| `timeout_diagnostico_nextpnr.log` | `24C6D60A05A4C64C7FE5A4949EEF1159B3AC727EC30A1B16C455BEAFC20E775F` | `09A9E11D37B714ACC4E7D0AAD7AE54E1C32F682EB58DC53D4ACB834BB2FCCEDA` |

El paquete auditado conserva byte por byte las entradas del ZIP anterior para esos dos artefactos. El commit citado conserva la otra revisión en su árbol Git. Los archivos locales permanecen en sus rutas y la imagen de competencia se verificó por separado. [Historial de revisiones del diagnóstico](../pruebas_fisicas/demo_autonoma_bus_detail/README.md)

## 2. Arquitectura y ejecución

`proyecto4/alternativas/mmio_sma10/trade_top.v` instancia el SoC con `EnableSpi=1`. `pochoco_ram` carga las 71 palabras del HEX MMIO mediante `$readmemh`. Espino RV32E ejecuta el firmware, consulta STATUS hasta observar un precio, lee PRICE, actualiza su cartera local con la orden pendiente, consulta SUM10 y READY, calcula la decisión y escribe DECISION. Los accesos del procesador pasan por la unidad de carga y almacenamiento. El mapa SPI/MMIO observado en el RTL y el firmware es el siguiente.

| Registro | Dirección | Comportamiento |
|---|---|---|
| STATUS | `0x80010000` | Bit 0 indica precio nuevo. Bit 1 refleja CS activa. |
| PRICE | `0x80010004` | Precio de 8 bits. Su lectura consume el indicador de precio nuevo. |
| DECISION | `0x80010008` | El byte bajo escrito por Espino queda retenido para la trama posterior. |
| SUM10 | `0x8001000C` | Suma móvil de 12 bits, con máximo 2.550. |
| READY | `0x80010010` | Bit 0 indica que ya llegaron 10 muestras. |

El receptor SPI entrega `byte_done` junto al precio completo. El acelerador mantiene las diez últimas muestras en un buffer circular sobre BRAM. Acumula durante el llenado y, con la ventana llena, resta la muestra saliente y suma la nueva. Espino conserva la decisión final. Tras llenar la ventana, calcula `10*p` con cuatro sumas. Solicita comprar 16 acciones si está sin posición y `10*p <= SUM10-10`, o vende hasta 16 de las que posee si `10*p >= SUM10+10`. En los demás casos emite mantener. [RTL y firmware MMIO SMA10](../alternativas/mmio_sma10/) · [Referencia Python](../python/enfoques_finales.py)

SPI opera en modo 0, 8 bits y MSB primero. En el banco, SCLK es 1 MHz, CS_n es activa en bajo y la trama dura 9.500 ns. Un precio viaja por MOSI y el byte de DECISION retenido al inicio viaja por MISO. En el tick 0 se devuelve `0x00`. Para `n>0`, la maestra recibe la decisión calculada en el tick `n-1` y la aplica al precio del tick `n`. Los bits 7:6 codifican la acción y 5:0 la cantidad. La maestra emulada lleva la contabilidad con caja inicial de 10.000 y comisión de 5 por orden ejecutada.

## 3. Validación funcional y rendimiento

La repetición utilizó los primeros 2.000 precios de la serie oficial, con `NTICKS=2000`, `PERIODO_NS=100000` y reloj de 25 MHz. Compilación, VVP, comparador, ejecutor y suite Python devolvieron código `0`. El simulador ejecutó la secuencia completa de 200,004 ms sin omitir ciclos. Su tiempo de ejecución en el PC fue 272,00 s. El CSV de la repetición es idéntico byte por byte al de la corrida aprobada. Sus seis columnas comunes también coinciden con el prefijo de la ronda 3 oficial de MMIO.

| Métrica | Corrida aprobada y repetición |
|---|---:|
| Ticks, precios SPI, lecturas PRICE, escrituras DECISION y respuestas MISO | 2.000 de cada uno |
| Precios perdidos / bits MISO desconocidos | 0 / 0 |
| Diferencias DECISION / MISO frente a Python | 0 / 0 |
| Decisiones MISO con el desfase correcto | 2.000 / 2.000 |
| Criterios del profesor / pruebas de Python | 4/4 / 32/32 |
| Latencia precio → DECISION, mínimo / media / máximo | 35 / 62,1035 / 253 ciclos |
| Presupuesto efectivo / holgura en el peor caso | 2.262 / 2.009 ciclos |
| Patrimonio final / caja / acciones | 9.839 / 6.831 / 16 |
| Órdenes, compras / ventas | 109, 55 / 54 |
| Comisiones / drawdown absoluto | 545 / 396 |
| Referencias del banco, no operar / comprar y mantener | 10.000 / 11.375 |

El contador mide desde `byte_done` hasta la escritura DECISION. El máximo equivale a 10,12 µs. El presupuesto del profesor es `floor((100000 - 9500) / 40) = 2262` ciclos. La comparación revisó cada precio, cada decisión escrita, cada MISO y la contabilidad de cada tick, además del patrimonio, órdenes y drawdown del log. Las tareas `spi` y `ejecutar` y las expresiones de los cuatro criterios conservan el contenido del archivo del profesor.

[Log y CSV de referencia](../resultados/auditoria_final_cierre/referencia_2000/) · [Log, códigos de salida y CSV de la repetición](../resultados/auditoria_final_cierre/repeticion_2000/) · [32 pruebas Python](../resultados/auditoria_final_cierre/pruebas_python.log)

Las seis corridas históricas de 20.000 ticks corresponden a las tres rondas de práctica en el emulador y son independientes de esta repetición de 2.000. [Comparación de las tres rondas](../resultados/validacion_oficial/comparacion_tres_rondas.csv)

## 4. FPGA, configuración y reproducibilidad del BIN

Se ejecutó el flujo existente en una copia aislada a partir del RTL local y el HEX entregado. Yosys usó `synth_ice40 -top trade_top`. nextpnr usó `--hx1k --package vq100 --freq 25 --seed 1 --pcf goboard.pcf`. icepack empaquetó el ASC en la copia aislada.

| Magnitud | Reconstrucción |
|---|---:|
| LUT4 | 1.055 |
| Logic Cells | 1.279 / 1.280 |
| BRAM | 13 / 16 |
| Fmax final post-route | 40,50 MHz |
| Restricción de reloj | 25 MHz, PASS |
| Tamaño del BIN | 32.220 bytes |

La reconstrucción temporal, `proyecto4/programacion_fisica/trade_mmio_base.bin` y la copia `build/competition/competition.bin` tienen el mismo SHA-256 `0150BF6FCE608FD463B15EB945F84354B151E581C71A36B47629E889EC0B6DFD`. El ensamblador produjo 71 palabras y el HEX aislado igualó el de entrega por SHA-256 `B7611ED78166A6E503EB09E4082FDD0C5811118CF08E68DEF32CE1ECD9C77706`. El PCF no contiene pines físicos duplicados. [Logs completos de síntesis, enrutado y ensamblado](../resultados/auditoria_final_cierre/sintesis/)

El primer intento en la copia mínima terminó con salida 1 porque faltaba `sw/game.hex`, valor por defecto que Yosys consulta al elaborar la jerarquía. Se incorporó esa dependencia existente a la copia aislada y el flujo terminó con salida 0. El top final carga el HEX MMIO indicado arriba. Los logs de ambos intentos se conservan.

| Señal | Go Board | Pin FPGA | Sentido |
|---|---|---:|---|
| Reloj del SoC | Oscilador de placa | 15 | 25 MHz |
| CS_n | PMOD PS1 | 65 | Maestra → Go Board |
| MOSI | PMOD PS2 | 64 | Maestra → Go Board |
| MISO | PMOD PS3 | 63 | Go Board → canal del grupo |
| SCLK | PMOD PS4 | 62 | Maestra → Go Board |

Usar GND común y señales de 3,3 V. La Go Board se alimenta por USB y el VCC del PMOD se deja libre. El SoC tiene POR interno; el top carece de reset externo de usuario. [PCF](../../goboard.pcf) · [Esquema de Go Board](https://nandland.com/goboard/images/Go_Board_V1.pdf)

## 5. Límites y pruebas pendientes

- Icarus advierte que el HEX de 71 palabras no llena el rango de RAM `[0:511]`. El modelo `tests/ram_model.v` es funcional. El certificado de timing corresponde a nextpnr.
- El diseño ocupa 1.279 LC y deja **una celda libre**. La medición de Fmax se hizo con la semilla indicada.
- La advertencia histórica de la regresión heredada `periph_tb`, asociada a la polaridad de los botones, sigue registrada. Esta auditoría repitió el banco de 2.000 ticks y las 32 pruebas de Proyecto 4.
- La demo autónoma de 16 ticks fue física y usó un maestro interno y un BIN distinto a 12,5 MHz. El SPI externo de la imagen de competencia requiere su propio ensayo físico. [Verificación de flash de la demo](../pruebas_fisicas/demo_autonoma_bus_detail/build/confirmacion_rom_lento_flash.log) · [Tres PASS de la demo](../pruebas_fisicas/demo_autonoma_bus_detail/build/resultado_fisico_rom_lento.log)
- En la prueba con la maestra se debe registrar el canal MISO, comprobar una compra y una venta de una serie conocida y repetir tras reinicio a 0,1 ms por tick. En la serie de práctica el tick 17 devuelve `0x50` y el 50 devuelve `0x90`, contando desde cero. La serie oculta, la competencia y la defensa quedan pendientes.

## 6. Comandos en Windows

Usar la raíz del paquete auditado extraído. Herramientas observadas: Windows PowerShell 5.1.26100.10068, Python 3.13.3, Icarus/VVP 14.0 devel `s20260301-626-g7e3d0c6bd-dirty`, Yosys 0.70+176 `365bb887b`, nextpnr 0.11.1-68 `g1daf1f5c`. icepack queda identificado por SHA-256 `A5BEEC407C1A0AE8D22547DB91F9818A182CF3D2BB5BE552ACBF97A77227CB7F`.

```powershell
Get-Command python, iverilog, vvp
powershell -NoProfile -ExecutionPolicy Bypass -File .\tb\ejecutar_tb_proyecto4.ps1
if ($LASTEXITCODE -ne 0) { throw 'Fallo el banco integrado' }
python -B -m unittest discover -s proyecto4/python -v
if ($LASTEXITCODE -ne 0) { throw 'Fallo la suite Python' }
```

El banco carga `proyecto4/alternativas/mmio_sma10/sw/trade.hex` y `proyecto4/resultados/validacion_oficial/practica_meta.csv`. Sus salidas quedan en `tb/build/icarus.log` y `tb/build/decisiones.csv`.

Para repetir el build sin tocar la imagen entregada, desde la raíz copien las dependencias del flujo a un directorio nuevo. Conserven las rutas relativas y ejecuten el script dentro de esa copia.

```powershell
Get-Command python, yosys, nextpnr-ice40, icepack
$raiz = (Get-Location).Path
$copia = Join-Path $raiz ('_build_fpga_auditoria_' + [guid]::NewGuid().ToString('N').Substring(0, 8))
$variante = 'proyecto4/alternativas/mmio_sma10'
New-Item -ItemType Directory -Path "$copia/sw", "$copia/$variante", "$copia/proyecto4/programacion_fisica" | Out-Null
Copy-Item -LiteralPath 'goboard.pcf' -Destination $copia
Copy-Item -LiteralPath 'sw/game.hex' -Destination "$copia/sw"
Copy-Item -LiteralPath "$variante/rtl", "$variante/sw", "$variante/trade_top.v" -Destination "$copia/$variante" -Recurse
Copy-Item -LiteralPath 'proyecto4/programacion_fisica/generar_bitstream.py' -Destination "$copia/proyecto4/programacion_fisica"
$esperado = (Get-FileHash -Algorithm SHA256 'proyecto4/programacion_fisica/trade_mmio_base.bin').Hash
Push-Location -LiteralPath $copia
try {
    python -X utf8 -B proyecto4/programacion_fisica/generar_bitstream.py
    if ($LASTEXITCODE -ne 0) { throw 'Fallo la reconstruccion' }
    $hash = (Get-FileHash -Algorithm SHA256 'proyecto4/programacion_fisica/trade_mmio_base.bin').Hash
    if ($hash -ne $esperado) { throw 'El nuevo BIN difiere de la imagen de entrega' }
    $hash
} finally {
    Pop-Location
}
```

El paquete local añade el banco Windows, los README actualizados, la auditoría y los logs al ZIP de la publicación. El informe PDF, las seis corridas previas y los artefactos de placa se conservan en el paquete base.
