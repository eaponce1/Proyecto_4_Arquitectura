# Manifiesto de entrega — Proyecto 4

## Informe técnico vigente

`informe_final_proyecto4.pdf` se genera desde `../documentacion/informe_final_proyecto4.md` mediante `../documentacion/generar_pdf.py`. El informe contiene el desarrollo técnico, la evidencia de validación y un anexo separado con investigación publicada el 25 de noviembre, después del plazo original.

El PDF incluye únicamente el informe técnico. La guía de defensa y el guion de presentación se mantienen como documentos independientes y no se incorporan al PDF.

## Variante final de la entrega original

La arquitectura seleccionada para la entrega del 24 de noviembre es **MMIO SMA10 base**, ubicada en `../alternativas/mmio_sma10/`, con su propio `sw/trade.s` y `sw/trade.hex`.

La evidencia publicada incluye seis corridas de práctica de 20.000 ticks, con tres rondas para software original y MMIO SMA10 base, 4/4 criterios por corrida y decisiones idénticas a Python. El co-diseño compara software original, custom-0 y MMIO SMA10 base. MMIO base completa P&R para iCE40 HX1K/VQ100 con 1.055 LUT4, 1.279/1.280 Logic Cells, 13/16 BRAM y Fmax de 40,50 MHz. Custom-0 excede el área disponible.

La demo autónoma de 16 ticks obtuvo PASS físico en la Go Board con maestro SPI interno, verificación de flash, LEDs `1010` y respuesta UART `0xAA` en tres arranques. Esta prueba no acredita la integración física del bitstream de competencia con la FPGA maestra.

## Investigación posterior al plazo

`../alternativas/candidata_final/` y `../alternativas/agresiva/` contienen variantes experimentales publicadas el 25 de noviembre. Se documentan en un anexo separado del PDF; ninguna reemplaza la arquitectura MMIO SMA10 base ni cuenta con validación física con la FPGA maestra.

## Paquetes publicados

`Pochoco_Trader_entrega.zip` y `Pochoco_Trader_cierre_auditado.zip` se conservan como paquetes históricos. La actualización del PDF y de su fuente no reconstruye ni modifica esos ZIP.

## Historial de publicación

El PDF y el manifiesto originales aparecen publicados el 23 de noviembre de 2026 a las 09:21, hora de Chile, antes del plazo del 24 de noviembre a las 10:00. Esta revisión se realiza el 25 de noviembre y no debe confundirse con el artefacto publicado antes del plazo.
