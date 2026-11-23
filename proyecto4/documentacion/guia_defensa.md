# Guía de defensa técnica — Proyecto 4

## Preguntas y respuestas

1. **¿Qué problema resuelve el Proyecto 4?** Recibe precios por SPI, ejecuta una estrategia causal en Espino RV32E y deja una decisión para la siguiente transacción.
2. **¿Cuál es la unidad útil de trabajo?** Un tick: consumir el precio actual y escribir la decisión destinada al tick posterior.
3. **¿Qué significa el desfase SPI?** MISO de la transacción n entrega la decisión que ya estaba cargada antes de esa transacción; el precio n sirve para formar la decisión n+1.
4. **¿Qué evita aplicar la decisión al mismo precio que la generó?** El modelo ejecuta primero la decisión pendiente al precio actual y solo después calcula la nueva señal.
5. **¿Cuál es la estrategia SMA10?** Tras diez precios compara `10*p` con la suma de los últimos diez: compra 16 si está al menos 10 unidades de suma bajo el umbral; vende hasta 16 si está al menos 10 sobre el umbral.
6. **¿Por qué no divide para calcular el promedio?** Comparar `p` con `suma/10` equivale a comparar `10*p` con `suma`; multiplicar por diez se forma mediante sumas y no requiere división.
7. **¿Qué pasa durante el calentamiento?** Se mantiene hasta que existan diez muestras válidas.
8. **¿Cómo se evita deuda?** El fill de compra se limita por la caja disponible incluyendo fee; ventas se limitan por acciones mantenidas. Pruebas revisan saldos no negativos.
9. **¿Cuánto cuesta una orden?** Comisión fija de $5 por orden ejecutada; una decisión sin fill no cobra fee.
10. **¿Por qué una orden no supera 63 acciones?** La cantidad se transmite en seis bits en la codificación del protocolo.
11. **¿Dónde está STATUS?** `0x80010000`, según el RTL SPI.
12. **¿Dónde está PRICE?** `0x80010004`; leerlo limpia la bandera new-price conforme al RTL.
13. **¿Dónde está DECISION?** `0x80010008`; es un registro de escritura del procesador que alimenta el byte transmitido después.
14. **¿Qué registros añade MMIO SMA10?** SUM10 en `0x8001000C` y READY en `0x80010010`.
15. **¿Cómo se habilita SPI?** El wrapper de MMIO base instancia el SoC con `EnableSpi=1`; no se asume habilitado por el default del SoC.
16. **¿Qué hace el periférico MMIO?** Mantiene anillo de diez precios y suma móvil; no decide comprar/vender. Espino consume estado y conserva la decisión final.
17. **¿Qué es custom-0?** Una instrucción aislada que fusiona `rd - precio_saliente + precio_entrante`; acelera, pero su implementación excede el límite LC HX1K.
18. **¿Qué registros tiene RV32E aquí?** Dieciséis registros enteros x0–x15, con x0 constante en cero.
19. **¿Qué instrucciones usa trade.s?** `lui`, `addi`, `lw`, `sw`, `andi`, `add`, `sub`, `beq`, `bne`, `bge` y `jal`.
20. **¿Usa shifts o multiplicación/división?** No. El firmware evita esas operaciones y el Espino no ofrece una extensión M en esta configuración.
21. **¿Cómo se valida equivalencia?** Un intérprete del HEX compara decisiones tick por tick contra Python en 20.000 precios; hay además caso de fill parcial e integración RTL sintética SPI.
22. **¿Qué rondas oficiales se validaron con el testbench del profesor?** La ronda 3 (0,1 ms) se ejecutó con 20.000 ticks en ambas arquitecturas y aprobó 4/4 criterios. Las rondas 1 y 2 siguen pendientes. La medición a 30 μs es otro experimento.
23. **¿Cómo se midió IC?** Con condición externa de commit `instr_valid_id && !stall`, sin instrumentar/modificar el core.
24. **¿Cuál era el costo software?** 91,917 IC y 218,664 ciclos promedio por tick; SMA10 suma alrededor de 163,9 ciclos.
25. **¿Cuál es el speedup de MMIO?** 3,606× por ciclos medios frente a software (218,6635/60,6398), sobre simulación de 20.000 ticks.
26. **¿Por qué custom-0 no es la versión seleccionada?** Su síntesis/ruta requirió 1350 LC, 70 más que HX1K; no consiguió una ruta válida en ese dispositivo.
27. **¿Qué logra la optimización MMIO?** Reduce 5 LC y 4 LUT4, mantiene BRAM/ciclos y lleva Fmax 40,50→42,33 MHz; no alcanza el objetivo de 1150–1200 LC.
28. **¿Cuánto margen tiene MMIO base?** 1279/1280 LC: uno libre. Es funcional y enruta, pero el margen para cambios es mínimo.
29. **¿El roofline fue una medición de ancho de banda?** No. Es un modelo simplificado con supuestos explícitos de bytes, BRAM y operaciones aritméticas; no mide tráfico físico.
30. **¿Se programó la placa con el binario base?** El usuario informó que la placa ya estaba programada. El repositorio acredita build, no aporta log de `iceprog` ni VERIFY OK; no se presenta como verificación independiente.
31. **¿La prueba interna SPI confirma el SoC completo?** No; confirma SPI slave aislado con maestro interno, cinco patrones y desfase. No incluye Espino ni prueba eléctrica física.
32. **¿Se corrió la prueba interna físicamente?** No consta. El testbench y P&R pasaron; la placa no fue reprogramada para esa prueba.
33. **¿Cuál es el estado de los LEDs de la fixture interna?** La simulación reportó LED0 y LED3 encendidos (`1001`) para PASS y DONE; no es evidencia de lectura física en placa.
34. **¿Qué dicen los resultados de inversión?** La investigación final no recomienda una estrategia activa en esta serie: comisiones y pérdidas superan a las referencias; no operar es el baseline prudente.
35. **¿La SMA10 seleccionada promete rentabilidad?** No. Se seleccionó para evaluar compatibilidad y aceleración; no por rendimiento financiero demostrado fuera de la serie.
36. **¿Qué regresión queda en Proyecto 2?** La suite conjunta registra un fallo de expectativa `debounced buttons` en `periph_tb`; pruebas de core/SPI/decoder reportadas pasan por separado.
37. **¿Qué evidencia falta antes de una defensa de hardware?** Log de programación/verificación, prueba real de la fixture o integración con maestro externo, y evidencia eléctrica/temporal en placa.

38. **¿Cuál fue el resultado financiero de la validación oficial de ronda 3?** Ambas arquitecturas cerraron en $4.577, con 931 órdenes (466 compras y 465 ventas), $4.655 de comisiones y drawdown de $5.476.
39. **¿Coincidieron las decisiones de software y MMIO SMA10?** Sí. Las decisiones de las 20.000 transacciones fueron idénticas.
40. **¿Qué cambió MMIO SMA10 en rendimiento y estrategia?** Redujo el promedio entero truncado de 218 a 60 ciclos y el peor caso de 413 a 255. No cambió la secuencia de decisiones ni el resultado financiero.
41. **¿Qué significan los promedios 60 y 218?** Son promedios enteros truncados por la instrumentación del testbench; no son decimales exactos.
42. **¿La integración con la FPGA maestra ya se probó físicamente?** No. La validación oficial fue RTL; la integración física con la FPGA maestra sigue pendiente.
43. **¿La ronda 3 significa que todas las rondas oficiales están verificadas?** No. Solo se ejecutó ronda 3; rondas 1 y 2 siguen pendientes.

## Mensaje de cierre sugerido

El resultado principal es una comparación reproducible: las decisiones del firmware se contrastaron tick a tick, MMIO reduce los ciclos de SMA y cabe en HX1K, pero el uso de 1279 de 1280 Logic Cells hace que el margen sea mínimo. Separamos cuidadosamente simulación, place-and-route y estado físico reportado. La investigación financiera tampoco se presenta como éxito: en los datos disponibles, la estrategia activa no supera de forma convincente la referencia de no operar.

## Preguntas para el cierre

- ¿Cómo demuestras causalidad si MOSI y MISO viajan en la misma trama? Explica qué captura el esclavo al iniciar CS_n, cuándo lee PRICE Espino y por qué la nueva DECISION solo aparece en la trama siguiente.
- ¿Por qué el patrimonio de MMIO y software coincide aunque cambien los ciclos? Explica el cotejo de 20.000 bytes y qué ocurriría si una escritura pierde su deadline.
- ¿Por qué custom-0 no es la imagen final? Compara 1.350 LC con 1.280 disponibles y distingue speedup de frecuencia post-route.
- ¿Por qué Ops/s no es el número de ticks que envía la maestra? Distingue el costo de cálculo, el período SPI y la operación elemental del roofline.
- ¿Qué demuestra 1101? La primera causa retenida fue un bit MISO distinto de la referencia en el autotest. El patrón por sí solo no identifica el bit, la trama ni una causa eléctrica.
- ¿Cuáles rondas puedes defender con resultados completos? Solo la 3 en simulación oficial. Distingue los presupuestos de las rondas 1 y 2 de sus resultados y de la competencia en placa.
