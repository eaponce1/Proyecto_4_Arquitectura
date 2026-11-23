# Guion de presentación — Proyecto 4 (8–10 minutos)

Duración objetivo: aproximadamente 9 minutos. El texto entre corchetes es guía para quien presenta y no se lee en voz alta.

## 0:00–0:45 — Problema y alcance

“Este proyecto integra una entrada de precios por SPI, un procesador Espino RV32E y un programa que produce decisiones de compra, venta o mantener. El trabajo se construyó sobre Proyecto 2. Hoy presentaré qué está demostrado por software y simulación, qué se sintetizó para la Go Board y qué queda pendiente de validar físicamente.”

## 0:45–1:45 — Arquitectura

“El SoC combina Espino, RAM, periféricos y SPI slave. En el mapa MMIO auditado, STATUS está en 0x80010000, PRICE en 0x80010004 y DECISION en 0x80010008. La variante MMIO SMA10 añade SUM10 en 0x8001000C y READY en 0x80010010. Esas direcciones provienen del decoder RTL. La configuración de la variante habilita SPI explícitamente con EnableSpi=1.”

“El periférico SMA10 guarda diez precios y mantiene su suma. No elige una acción. El procesador consulta el estado, lee precio/suma y conserva la responsabilidad de la decisión final.”

## 1:45–2:50 — Causalidad y estrategia

“Hay un desfase propio de SPI. Durante la transacción actual recibimos un precio y MISO transmite la decisión que ya estaba guardada. Ejecutamos esa decisión contra el precio actual y calculamos otra para el siguiente tick. Por eso una señal nunca se aplica al mismo precio que la generó.”

“La estrategia SMA10 espera diez observaciones. Compara diez veces el precio actual con la suma de la ventana. Si no tenemos posición, compra hasta 16 cuando el precio está por debajo del promedio con un margen fijo; con posición vende hasta 16 cuando está por encima. Usa enteros, no divide y limita las compras por caja y las ventas por inventario. Cada orden ejecutada cuesta cinco dólares.”

## 2:50–3:50 — Firmware y validación

“El programa Assembly usa los registros RV32E x0 a x15 y un buffer circular de diez precios en RAM. Se generó trade.hex con el assembler. El subset utilizado incluye sumas, restas, cargas, stores y branches admitidos; no usa shifts ni multiplicación/división.”

“El intérprete ejecuta la imagen HEX contra Python en la serie completa de 20.000 precios y compara las decisiones tick a tick. También hay un caso para fills parciales y una integración RTL SPI corta con serie sintética. En el cierre documental se ejecutaron 32 pruebas Python: todas pasaron. Es importante precisar que la equivalencia completa de 20.000 ticks es del intérprete HEX; no fue una simulación RTL de 20.000 ticks del firmware original.”

## 3:50–5:00 — Rendimiento y validación oficial

“En RTL, el programa original promedió 91,9 instrucciones y 218,7 ciclos por tick, con CPI 2,379 y peor caso de 412 ciclos. La SMA consume aproximadamente 163,9 ciclos promedio. Se contaron instrucciones externamente en la condición de commit, sin cambiar el core.”

“La corrida de perfil fue de 20.000 ticks a 30 microsegundos entre transacciones; esa medición no sustituye las rondas oficiales. En la validación oficial de ronda 3, el testbench publicó 20.000 ticks y ambos diseños aprobaron 4 de 4 criterios. Las 20.000 decisiones de MMIO y software coincidieron.”

“Ambos cerraron con patrimonio de 4.577 dólares, 931 órdenes —466 compras y 465 ventas—, 4.655 dólares de comisiones y drawdown de 5.476. Es el mismo resultado financiero; MMIO reduce el trabajo computacional, no mejora la estrategia.”

“En el perfil de co-diseño, MMIO promedió 60,64 ciclos frente a 218,66 del software original: speedup medido de 3,606 veces. En la corrida oficial la instrumentación imprimió promedios enteros truncados de 60 y 218; los peores casos fueron 255 y 413 ciclos. No calculo el speedup de la corrida oficial dividiendo esos promedios truncados.”

“Las rondas oficiales 1 y 2, a 10 y 1 milisegundos, siguen pendientes: no las presentaré como aprobadas. Tampoco se completó la integración física con la FPGA maestra. La validación 4/4 citada es una simulación RTL de ronda 3.”

## 4:45–6:15 — Co-diseño

“Evaluamos dos aceleradores. La instrucción custom-0 baja el promedio a 70,7 ciclos, pero requiere 1350 Logic Cells, que exceden en 70 las 1280 del HX1K; por tanto no es una solución enrutable para esta placa.”

“MMIO SMA10 baja el promedio a 60,64 ciclos, 26,85 instrucciones y CPI 2,259. El speedup medido por ciclos es 3,606 veces. La síntesis informa 1055 LUT4, 1279 de 1280 Logic Cells, 13 de 16 BRAM y Fmax routeada de 40,5 MHz. Pasa 25 MHz, aunque deja una sola LC libre.”

“La variante optimizada sustituye un contador por un bit de ready. Conserva los mismos ciclos y las decisiones, baja a 1274 Logic Cells y mejora Fmax a 42,33 MHz. Solo libera cinco celdas y queda lejos del objetivo de 1150 a 1200. No la usamos como sustituto de la referencia base.”

## 6:15–7:00 — Modelo de análisis

“El speedup Amdahl del MMIO base fue 3,692 veces frente al speedup observado de 3,606. Es una predicción basada en la fracción de kernel medida, no otro resultado empírico. El roofline también es simplificado: cuenta sumas/restas y usa supuestos de tráfico BRAM. No se midió ancho de banda real del chip.”

## 7:00–8:00 — Estrategia financiera

“La investigación de estrategias mantuvo no operar y comprar y mantener como referencias. No recomendamos una estrategia activa como ganadora robusta. La simulación previa mostró cómo comisiones y frecuencia pueden consumir el capital; el drawdown absoluto puede ser mayor a los diez mil iniciales porque se mide desde un peak superior al capital inicial. Eso no implica saldo negativo.”

“Por lo tanto, la SMA10 del firmware sirve para estudiar el sistema digital y su costo, no para afirmar rentabilidad. No optimizamos con información futura ni presentamos las métricas históricas como pronóstico.”

## 8:00–9:00 — Estado de Go Board y cierre

“El flujo de MMIO base produjo un binario independiente y los logs reportan síntesis, place-and-route e icepack exitosos para HX1K/VQ100. El informe dice que iceprog no se ejecutó; el estado de placa programada con la base fue informado por el usuario, pero no hay en el repositorio un log VERIFY OK. La fixture interna de SPI pasó cinco tramas en simulación y P&R, pero no se programó ni se probó eléctricamente.”

“En conclusión, demostramos causalidad y equivalencia dentro del alcance registrado, aceleración de SMA por MMIO y cabida de esa versión en el dispositivo con margen muy estrecho. Para cerrar hardware faltan evidencia de programación/verificación y una prueba física independiente. Además permanece una prueba heredada de botones con expectativa de polaridad incompatible. Esas limitaciones se distinguen de lo que sí medimos.”

## Respaldo para preguntas

Si preguntan por evidencias concretas, abrir `resultados/co_disenio/comparacion_codisenio.csv`, `resultados/mmio_optimizacion/comparacion_mmio_sma10.csv`, `resultados/mediciones_software.csv`, `resultados/etapa3_assembly.md` y `programacion_fisica/informe_programacion_fisica.md`. No presentar simulación como prueba física.
