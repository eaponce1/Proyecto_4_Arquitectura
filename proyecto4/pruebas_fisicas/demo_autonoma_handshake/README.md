# Demo autónoma con handshake de consumo PRICE

Variante independiente que impide emitir el siguiente precio hasta que el
Espino real lea PRICE. El SPI Master entra en `WAIT_ACK` tras cada byte; el SoC
produce una señal `price_read` durante el acceso MMIO, y el top la enclava como
`price_ack` hasta el siguiente `spi_byte_done`. Después de recibir el ACK se
conserva una separación mínima de 6000 ciclos, por lo que el retardo fijo ya no
es el mecanismo de control de flujo.

La secuencia permanece igual: 10×200, 3×90, 3×220 (16 precios). Se reutiliza el
SPI Slave, SMA10, SoC, Espino y `trade.hex` originales sin modificarlos. Solo el
master de esta carpeta agrega el handshake.

## Validación

Desde `pochoco_soc-main`:

```powershell
powershell -ExecutionPolicy Bypass -File proyecto4/pruebas_fisicas/demo_autonoma_handshake/ejecutar_pruebas.ps1
powershell -ExecutionPolicy Bypass -File proyecto4/pruebas_fisicas/demo_autonoma_handshake/sintetizar.ps1
```

Icarus pasó las pruebas de error sticky y la secuencia integrada. Se midió una
latencia máxima de 15 ciclos entre `spi_byte_done` y lectura PRICE (0,60 µs a
25 MHz), promedio 13,19 ciclos; el intervalo mínimo entre lectura PRICE y el
siguiente `spi_byte_done` fue 6500 ciclos. Fueron 16/16 decisiones, 16/16 MISO
equivalentes a Python y 0 ticks perdidos.

Yosys: 985 LUT4. nextpnr HX1K/VQ100: 1161/1280 LC, 9/16 BRAM y Fmax final
41,65 MHz; PASS a 25 MHz. Se generó el archivo independiente
`build/demo_autonoma_handshake.bin`. No se programa la placa automáticamente.
Resultados completos y hash: `informe_handshake.md`.
