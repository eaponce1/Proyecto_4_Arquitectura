# Manifiesto de entrega — Proyecto 4

Esta carpeta contiene el PDF solicitado y evita duplicar fuentes que ya viven en sus rutas canónicas dentro del repositorio. Para la entrega en GitHub, subir la raíz completa de `pochoco_soc-main` con los archivos requeridos que se enumeran aquí; no subir solamente esta carpeta.

## Artefactos en esta carpeta

- `informe_final_proyecto4.pdf`: render de `../documentacion/informe_final_proyecto4.md`, generado con `python -B proyecto4/documentacion/generar_pdf.py`.

## Fuentes y evidencia canónica que forman parte de la entrega

- Código/firmware elegido: `proyecto4/alternativas/mmio_sma10/` (RTL MMIO SMA10 base, wrapper, `sw/trade.s`, `sw/trade.hex` y testbenches); `proyecto4/python/`; `sw/assembler.py`.
- Infraestructura y protocolo: `rtl/`, `tests/`, `goboard.pcf`, `proyecto4/tb/`, `proyecto4/data/practica_meta.csv` y el testbench oficial conservado en `proyecto4/resultados/validacion_oficial/tb_proyecto_4_profesor.sv`.
- Build físico reproducible: `proyecto4/programacion_fisica/generar_bitstream.py`, `informe_programacion_fisica.md`, PCF de la raíz, y `trade_mmio_base.bin` (32.220 bytes). El binario se generó para iCE40 HX1K/VQ100 y no demuestra programación física.
- Validación oficial conservada: `proyecto4/resultados/validacion_oficial/informe_validacion_oficial.md`, `comparacion_oficial.csv` y las dos salidas de ronda 3 en `corridas/{software_original,mmio_sma10_base}/ronda_3/decisiones.csv`.
- Documentación adicional: `proyecto4/README.md`, `proyecto4/documentacion/informe_final_proyecto4.md`, `guia_defensa.md`, `guion_presentacion.md` y `checklist_entrega.md`.

## Estado declarado en la fecha de cierre documental

- Ronda 3: 20.000 ticks; 4/4 criterios para software y MMIO; decisiones idénticas.
- Rondas 1 y 2: pendientes, no se reportan como aprobadas.
- Integración física con FPGA maestra/competencia: pendiente.
- `iceprog`: no ejecutado.

El árbol de trabajo recibido no tiene metadata `.git`; verificar el checkout/remoto y el staging antes de entregar. No hacer commit ni push sin esa comprobación.

## Paquete reproducible y evidencia vigente

Ejecuta python -B proyecto4/entrega_final/preparar_entrega.py desde la raíz para construir el ZIP de entrega. La validación de ronda 3, el informe PDF, la versión de competencia, las alternativas y sus bancos se incluyen. Las corridas parciales de rondas 1 y 2 y los ejecutables de simulación quedan fuera.

La imagen diagnóstica anterior mostró D1 en placa. Icarus confirma los códigos de diagnóstico nuevos, cuya prueba física está pendiente. La imagen de competencia mantiene SPI externo y utiliza el firmware y SoC MMIO base. Consulta la matriz de cierre para distinguir cada evidencia.
