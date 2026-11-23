# Manifiesto de entrega — Proyecto 4

Esta carpeta contiene el PDF solicitado y evita duplicar fuentes que ya viven en sus rutas canónicas dentro del repositorio. La rama de entrega es `main` de `eaponce1/Proyecto_4_Arquitectura`.

## Artefactos en esta carpeta

- `informe_final_proyecto4.pdf`: render de `../documentacion/informe_final_proyecto4.md`, generado con `python -B proyecto4/documentacion/generar_pdf.py`.

## Fuentes y evidencia canónica que forman parte de la entrega

- Código/firmware elegido: `proyecto4/alternativas/mmio_sma10/` (RTL MMIO SMA10 base, wrapper, `sw/trade.s`, `sw/trade.hex` y testbenches); `proyecto4/python/`; `sw/assembler.py`.
- Infraestructura y protocolo: `rtl/`, `tests/`, `goboard.pcf`, `proyecto4/tb/`, `proyecto4/data/practica_meta.csv` y el testbench oficial conservado en `proyecto4/resultados/validacion_oficial/tb_proyecto_4_profesor.sv`.
- Build físico reproducible: `proyecto4/programacion_fisica/generar_bitstream.py`, `informe_programacion_fisica.md`, PCF de la raíz, y `trade_mmio_base.bin` (32.220 bytes). El binario se generó para iCE40 HX1K/VQ100 y no demuestra programación física.
- Validación oficial de ronda 3 conservada: `proyecto4/resultados/validacion_oficial/informe_validacion_oficial.md`, `comparacion_oficial.csv` y las dos salidas de ronda 3 en `corridas/{software_original,mmio_sma10_base}/ronda_3/decisiones.csv`.
- Validación de las tres rondas de práctica: `proyecto4/resultados/validacion_oficial/comparacion_tres_rondas.csv`, `informe_comparativo_tres_rondas.md` y las cuatro corridas completas de rondas 1 y 2 en `corridas_aceleradas/`, con decisiones, cuatro criterios y duración de simulación.
- Documentación adicional: `proyecto4/README.md`, `proyecto4/documentacion/informe_final_proyecto4.md`, `guia_defensa.md`, `guion_presentacion.md` y `checklist_entrega.md`.

## Estado declarado en la fecha de cierre documental

- Tres rondas de práctica: 20.000 ticks y 4/4 criterios por ronda y arquitectura. Las seis secuencias de decisiones coinciden con Python.
- Integración física con FPGA maestra/competencia: pendiente.
- Demo autónoma de 16 ticks aprobada físicamente en Go Board a 12,5 MHz. Se verificó la flash, se observó 1010 y COM10 devolvió 0xAA en tres arranques. El ZIP incluye `selftest_fetch_rom_lento.bin`, los registros de simulación y timing y ambos logs físicos.

## Paquete reproducible y evidencia vigente

Ejecuta python -B proyecto4/entrega_final/preparar_entrega.py desde la raíz para construir el ZIP de entrega. El ZIP incluye las seis corridas completas, el informe PDF, la versión de competencia, las alternativas y sus bancos. El paquete excluye corridas parciales y ejecutables de simulación.

La imagen de competencia mantiene SPI externo y utiliza el firmware y SoC MMIO base. El autotest de 16 ticks aporta evidencia RTL, de implementación y de ejecución física con maestro interno. La [matriz de cierre](../documentacion/matriz_cierre_pochoco.md) registra el alcance por requisito.
