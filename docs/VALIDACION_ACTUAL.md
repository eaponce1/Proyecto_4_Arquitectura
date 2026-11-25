# Imagen activa despues del ordenamiento

- Top: `rtl/trade_spi_externo.v`.
- Firmware: `sw/trade.s` y `sw/trade.hex`.
- BIN SHA-256: `1d7f1b2d951b086e535e7f7fc77fe6525df9b30e403263770358db15bcb031bc`.
- HEX SHA-256: `27d895e1747120d5c4d1b3cc17a91e82ed87d772aeebae4fc5bdcda7d9e04058`.
- Recursos: 1268/1280 LC, 9/16 BRAM.
- Frecuencia real Espino: 12,5 MHz, entrada de 25 MHz.
- Pruebas de integracion: recuperacion 768 ticks, compra/venta 48 ticks,
  netlist 48 ticks en dos fases; cero discrepancias.
- Equivalencia previa de la misma politica/firmware: 160.000 ticks Python/RV32E/RTL.
- Programacion y ensayo fisico: pendientes hasta ejecutarlos y registrarlos.

El ordenamiento no cambia las fuentes de hardware ni el firmware; sus firmas
se comprueban con `python -B tools/trader.py verify`. La auditoria historica puede
recuperar del ZIP los artefactos que ya no estan en el arbol activo.

Los logs originales conservan rutas anteriores como evidencia; los ejecutores actuales
usan rutas relativas al proyecto consolidado. No se presentan las pruebas archivadas
como nuevas ejecuciones posteriores a la limpieza.
