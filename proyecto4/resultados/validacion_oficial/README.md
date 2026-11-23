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

Rondas: 1=10 ms, 2=1 ms, 3=0,1 ms. Cada simulación completa ejecuta 20.000 ticks; Icarus simula el reloj de 25 MHz también durante los sondeos entre transacciones, por lo que las rondas lentas tienen un costo de cómputo muy alto.

Resultados, tiempos y pendientes registrados en `informe_validacion_oficial.md`.

## Corridas registradas

| Variante | Ronda | Serie | Checks | Ciclos promedio (truncado) | Peor caso |
|---|---:|---:|---:|---:|---:|
| MMIO SMA10 base | 3 | 20.000 | 4/4 PASS | 60 | 255 |
| Software original | 3 | 20.000 | 4/4 PASS | 218 | 413 |

Las dos secuencias de decisiones coinciden en 20.000/20.000 ticks y tienen igual contabilidad final. Rondas 1 y 2 están pendientes; la ronda 3 tomó aproximadamente 7 h 38 min (MMIO) y 2 h 30 min (software), y el informe explica la proyección por ciclos para los periodos más largos. El promedio impreso por la versión usada en estas corridas divide enteros y se etiqueta explícitamente como truncado.
