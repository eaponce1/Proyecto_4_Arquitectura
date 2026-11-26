# Corrección de ausencia de órdenes — 25 de noviembre de 2026

Se reprodujo un defecto que deja al procesador esperando precios: si CS baja
20–40 ns antes del primer SCLK, la selección y el primer flanco pueden coincidir
tras la sincronización. El receptor anterior priorizaba la selección y descartaba
ese bit; las tramas de ocho bits nunca completaban el precio. No se escribían
decisiones y MISO seguía en `0x00`.

La imagen anterior `1d7f1b2d951b086e535e7f7fc77fe6525df9b30e403263770358db15bcb031bc`
reproduce el defecto al reconstruir su circuito desde el BIN: falla con CS de
20 ns y pasa con 1 us. Los bancos anteriores esperaban 1 us y no detectaban
esta condición. Los logs originales quedan en `build/diagnostico_sin_ordenes/`.

El RTL activo ahora captura el primer bit cuando coinciden ambos eventos.
Además presenta el MSB de la respuesta antes del primer SCLK físico, incluso
mientras CS atraviesa los sincronizadores. El firmware de 150 instrucciones y
la política financiera conservan sus hashes anteriores.

La regresión `tb/tb_spi_margen.sv` recibe 48 precios y compara las 48 decisiones
contra Python. Espera compras de 63 y 36 acciones (`0x7f`, `0x64`) y ventas de
63 y 36 (`0xbf`, `0xa4`). Revisa diez combinaciones de CS y fase en RTL, y CS
de 20 ns, 40 ns y 1 us en la netlist y el BIN reconstruido. En estas dos últimas
pruebas se comprueban MISO y LED desde los puertos externos; los contadores
internos no están disponibles. El BIN reconstruido usa un retardo funcional
uniforme de 1 ps en las conexiones para resolver redes de puertas; no sustituye
el análisis de timing físico.

Las ocho series se repitieron contra el RTL activo corregido: 160.000 ticks,
cero diferencias en precios, decisiones, MISO, cartera o comisiones.
La evidencia nueva está en `build/trader/equivalencia_verilator.json` y
`build/trader/verilator/`. La validación de referencia se conserva sin modificar.

Para reproducir la prueba corta desde la raíz del proyecto:

```powershell
python -B tools/trader.py spi
```

Para generar el BIN, incluyendo los controles de RTL, síntesis, netlist y
configuración empaquetada:

```powershell
python -B tools/trader.py build
python -B tools/trader.py verify
```

La firma activa está en `competition.sha256` y los recursos y pruebas del build
en `build/trader/validacion.json`. La imagen anterior queda respaldada localmente
en `respaldos/`; no debe confundirse con la entrega vigente.

Para programar y comparar la flash:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\programar.ps1
```

Después reiniciar la Go Board, esperar D1 e iniciar una serie nueva en la maestra.
La placa necesita precios externos para negociar. SPI modo 0, MSB primero, ocho
bits y hasta 1 MHz. Como margen de conexión, mantener CS bajo 1 us antes del
primer SCLK cuando la maestra permita configurarlo.

Los LED acumulan hitos desde el arranque: D1 CPU ejecutó instrucciones, D2 precio recibido,
D3 precio leído y D4 decisión distinta de cero. Pueden quedar todos encendidos;
no indican compras o ventas individuales. El resultado financiero debe obtenerse
del registro de precios y MISO de la maestra.

Esta corrección tiene evidencia digital reproducible. Posteriormente, el grupo
aportó dos `VERIFY OK` y confirmó compras y ventas en la placa; el registro está
en `evidencia_fisica/registro_20261125.md`. Falta la traza de la maestra y el
patrimonio por ronda para una auditoría financiera. No se ejecutó `iceprog`
automáticamente durante la corrección.

## Integración posterior de tendencia lenta

La imagen `1f514301...` conserva la corrección SPI descrita y cambia el firmware a SUM10/128/5%. La primera ejecución posible es en tick 257; D4 puede permanecer apagado mientras no haya señal. Esta imagen pasó RTL, netlist y reconstrucción del BIN con compra y venta de 396 ticks. La confirmación física previa aplica exclusivamente a Momentum32 `5e1579ca...`; falta probar la nueva en placa.
