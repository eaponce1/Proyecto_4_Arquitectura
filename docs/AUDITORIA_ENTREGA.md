# Auditoría de entrega — Proyecto 4

La revisión completa está en [AUDITORIA_ENTREGA.pdf](AUDITORIA_ENTREGA.pdf),
generada desde [LaTeX](informe/auditoria_entrega.tex). La integridad, hashes y
comprobaciones están en [AUDITORIA_ENTREGA.json](AUDITORIA_ENTREGA.json).

Se contrastó el informe con el [enunciado oficial](referencia/enunciado_proyecto4.pdf),
incluida la rúbrica de la página 5. La misión inicial del usuario se distinguió
de los requisitos académicos.

**Dictamen:** cobertura documental amplia; no se acredita todavía toda la entrega.

El informe incluye autores, conclusión ampliada, no operar y mantener, ocho series,
assembly, registros/memoria, métricas de 160.000 ticks de práctica, 78 escenarios y 1.557.620 ticks RTL, recursos y timing. Se agregó
el estudio histórico de software/custom-0/MMIO, con Amdahl y roofline, cotejado con
60.000 filas originales. Esas cifras no se presentan como aceleraciones de la
política lenta final.

Se documenta además la nueva ejecución directa de
`Proyecto_4_Series_Practica_export.zip`: 8/8 PASS, 160.000 ticks, 98 compras y
92 ventas, sin discrepancias. El ZIP publicado y las trazas están ligados por
SHA-256 a las fuentes y al BIN actuales. Los CSV son idénticos al corpus y no
se contabilizan como nuevas muestras. Los gráficos del apéndice principal se
generan desde estas nuevas trazas RTL.

La programación y las compras/ventas anteriores corresponden a Momentum32
`5e1579ca...`; el [registro aportado](evidencia_fisica/registro_20261125.md)
no se reutiliza para la imagen lenta nueva `1f514301...`. El grupo confirmó posteriormente su reprogramación; la declaración está en [el registro actual](evidencia_fisica/reprogramacion_tendencia_lenta.json).

Falta acreditar:

- Traza de precios/MISO de la maestra correspondiente a la reprogramación reportada.
- Ocho series completas a 1 ms y 10 ms si se exige esa extensión: actualmente
  se validaron 160.000 ticks a 100 µs y 396 de integración por cadencia larga.
- Patrimonio, referencia y resultado de cada una de las tres rondas oficiales.
- Defensa de los integrantes y comprobante de entrega original dentro del plazo.
- Perfil regional y comparación de hardware con la misma política final, para
  extender Amdahl/roofline más allá del estudio histórico.

Esta revisión del 26/11 es posterior al plazo oficial del 24/11 a las 10:00.
No se asigna una nota ni se confunde simulación con competencia física.

Para recompilar y repetir las comprobaciones documentales:

```powershell
python -B tools/generar_informe_latex.py
wsl -d Ubuntu -- bash docs/informe/compilar.sh
python -B tools/auditar_pdf.py
```
