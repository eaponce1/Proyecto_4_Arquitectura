# Proyecto 4: inicio rápido de la integración vigente

La imagen activa es **[competition.bin](../competition.bin)**, con decisiones
Momentum32 y trailing stop de 20 puntos calculadas por Espino RV32E.
La arquitectura MMIO SMA10 base y las regresiones del juego pertenecen a versiones
anteriores conservadas en el historial; sus resultados no se atribuyen al BIN actual.

Desde la raíz del repositorio:

```powershell
iceprog competition.bin
iceprog -c competition.bin
```

Para verificar fuentes y hash sin acceder a la placa:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\programar.ps1 -SoloVerificar
```

Para ver las ocho series:

```powershell
python -m pip install -r requirements.txt
python simular_competencia.py
```

Para las pruebas activas:

```powershell
python -B tools/trader.py verify
make test
make
```

El [README principal](../README.md) identifica los pines, estado y límites.
El [informe PDF](../docs/INFORME_FINAL.pdf) está compilado desde
[LaTeX](../docs/informe/informe_final.tex), con los ocho gráficos y las pruebas.

Los workflows de GitHub verifican la integración actual y recompilan el informe.
Publican sus logs/PDF como artefactos de Actions; no programan hardware ni modifican
automáticamente `main`. El PDF aprobado permanece versionado en `docs/INFORME_FINAL.pdf`.

La política supera a mantener en 6/8 muestras conocidas; las dos de Netflix pierden.
La validación física y la superioridad independiente en series secretas no están demostradas.
