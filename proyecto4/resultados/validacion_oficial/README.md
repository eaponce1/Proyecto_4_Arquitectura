# Validación oficial — Proyecto 4

Esta carpeta conserva copias byte a byte de los archivos entregados por el usuario/profesor (`tb_proyecto_4_profesor.sv` y `practica_meta.csv`), la herramienta reproducible, cada fuente derivada de configuración, logs y `decisiones.csv` por variante/ronda.

El runner **no cambia** la contabilidad del testbench ni sus cuatro criterios: MISO sin X, se observó escritura DECISION, no se perdieron precios y la respuesta llega antes del presupuesto del periodo. Solo configura rutas, 20.000 ticks, el periodo de la ronda, activa `EnableSpi=1` y añade acumulación observacional de ciclos promedio. La fuente original permanece intacta y se incluye en esta carpeta.

El CSV se valida externamente antes de simular: encabezado `tick,price`, 20.000 ticks consecutivos y precios dentro del rango byte. Los resultados se escriben por separado para software original y MMIO SMA10 base; los archivos históricos de otras etapas no se sobrescriben.

## Comandos

Desde la raíz `pochoco_soc-main`:

```powershell
python -B proyecto4/resultados/validacion_oficial/ejecutar_validacion.py --variant mmio --round 3
python -B proyecto4/resultados/validacion_oficial/ejecutar_validacion.py --variant software --round 3
python -B proyecto4/resultados/validacion_oficial/ejecutar_validacion.py --variant mmio --round 2
python -B proyecto4/resultados/validacion_oficial/ejecutar_validacion.py --variant software --round 2
python -B proyecto4/resultados/validacion_oficial/ejecutar_validacion.py --variant mmio --round 1
python -B proyecto4/resultados/validacion_oficial/ejecutar_validacion.py --variant software --round 1
python -B proyecto4/resultados/validacion_oficial/resumir_corridas.py
```

Para reproducir los periodos largos en Icarus con espera verificada, añade
`--fast-idle` a cada comando de las rondas 1 y 2. El ejecutor guarda las
corridas en `corridas_aceleradas/`. El banco derivado mantiene la fase de
reloj y el tiempo de simulación de 10 ms o 1 ms entre precios. Tras completar
DECISION y con CS_n inactivo, observa ocho ciclos y compara el estado del SoC.
Si detecta el mismo estado y solo lecturas de STATUS, avanza por periodos
enteros de sondeo y actualiza los contadores de forma exacta. Si la comprobación
falla, simula todo el intervalo. Las tramas SPI y los cuatro criterios siguen
ejecutándose en Icarus de cuatro estados.

Cuando estén las seis corridas completas, genera un CSV nuevo con
`python -B proyecto4/resultados/validacion_oficial/resumir_corridas.py --tres-rondas`.
Ese CSV distingue el promedio decimal del entero truncado histórico.

Rondas: 1=10 ms, 2=1 ms, 3=0,1 ms. Cada simulación completa ejecuta 20.000 ticks; Icarus simula el reloj de 25 MHz también durante los sondeos entre transacciones, por lo que las rondas lentas tienen un costo de cómputo muy alto.

Resultados, tiempos y pendientes registrados en `informe_validacion_oficial.md`.

## Corridas registradas

| Variante | Ronda | Serie | Checks | Ciclos promedio | Peor caso |
|---|---:|---:|---:|---:|---:|
| MMIO SMA10 base | 1 y 2 | 20.000 por ronda | 4/4 PASS | 60,66 | 254 |
| Software original | 1 y 2 | 20.000 por ronda | 4/4 PASS | 218,67 | 413 |
| MMIO SMA10 base | 3 | 20.000 | 4/4 PASS | 60 | 255 |
| Software original | 3 | 20.000 | 4/4 PASS | 218 | 413 |

Las seis secuencias de decisiones coinciden en 20.000/20.000 ticks y tienen igual contabilidad final. Los valores 60 y 218 de ronda 3 son promedios enteros truncados. Las rondas largas se validaron con espera verificada. Consulta [el CSV comparativo](comparacion_tres_rondas.csv) y [el informe de las tres rondas](informe_comparativo_tres_rondas.md) para conocer tiempos, comprobaciones y comandos.
