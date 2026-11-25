# Historial de cambios

## Investigación ATM — 25 de noviembre de 2026

- Rama `codex/atm-adaptativa` desde `07d0dd95`; main y firmware activos preservados.
- Protocolo previo, 191 configuraciones y selección por prefijos de 12.000 ticks.
- Reproducción de ocho series y selecciones históricas LOCO/LOSO/walk-forward.
- Folds nuevos, 56 ternas distintas y 120 con repetición por política.
- Contabilidad independiente, 160.000 ticks, nueve estreses y controles causales.
- Resultado **NO-GO**: 5/8 ventajas, menor mediana y peor pérdida relativa que
  Momentum32. No se habilitaron Assembly, RTL, síntesis ni BIN de ATM.
- Informe cuantitativo, curvas, matrices, CSV comprimido y manifiesto SHA-256.
- La programación y las compras/ventas confirmadas siguen correspondiendo al
  BIN activo `5e1579ca...63a606`. No hubo nueva programación física.
- Cambios propuestos mediante PR; requieren revisión antes de fusionar.
