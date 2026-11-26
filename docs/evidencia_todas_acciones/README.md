# Campaña completa de acciones

`manifest.json` identifica los 78 CSV RTL completos, comprimidos en `trazas_rtl/`, sus hashes y los 1.557.620 ticks. Contienen precios, MISO, DECISION, fills, caja, acciones, patrimonio, comisiones y métricas del procesador. La campaña observó 428 compras y 364 ventas.

```powershell
python -B tools/auditar_campania_acciones.py
```

Comprueba fuentes, BIN, precios y todos los estados frente al modelo; no requiere el ZIP de origen. El resultado completo está en `resultados_simulacion/testbench_todas_acciones/`, con PDF, fuente LaTeX, gráfico, CSV, JSON y visor HTML.

Para volver a ejecutar el testbench con las entradas archivadas, desde Linux/WSL con Verilator >=5, Python, g++ y make:

```bash
python3 -B tools/repetir_acciones_archivadas.py
python3 -B tools/repetir_acciones_archivadas.py --serie practica_meta_2022
```

La repetición se guarda en `build/repeticion_acciones_archivadas/` y conserva la campaña original. Para repetir desde los CSV originales en lugar de las entradas archivadas, usar `probar_todas_acciones.ps1` con el `proyecto4.zip` aportado en Downloads.

Los 78 casos corresponden a ocho series de práctica y 35 CSV adicionales con dos escalas retrospectivas. Las escalas no son muestras independientes. Se usan hasta 20.000 ticks; GOOGL 2021 tiene 18.844 y Disney 2022 tiene 19.966. Las cifras son de simulación del firmware/RTL actual. La reprogramación de la placa fue reportada por el usuario y se registra por separado.
