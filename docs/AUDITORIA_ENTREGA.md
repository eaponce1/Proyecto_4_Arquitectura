# Auditoría de entrega — Proyecto 4

La revisión completa está en [AUDITORIA_ENTREGA.pdf](AUDITORIA_ENTREGA.pdf),
generada desde [LaTeX](informe/auditoria_entrega.tex). La integridad, hashes y
comprobaciones están en [AUDITORIA_ENTREGA.json](AUDITORIA_ENTREGA.json).

Se contrastó el informe con el [enunciado oficial](referencia/enunciado_proyecto4.pdf),
incluida la rúbrica de la página 5. La misión inicial del usuario se distinguió
de los requisitos académicos.

**Dictamen:** cobertura documental amplia; no se acredita todavía toda la entrega.

El informe incluye autores, conclusión ampliada, no operar y mantener, ocho series,
assembly, registros/memoria, métricas de 160.000 ticks, recursos y timing. Se agregó
el estudio histórico de software/custom-0/MMIO, con Amdahl y roofline, cotejado con
60.000 filas originales. Esas cifras no se presentan como aceleraciones de la
política lenta final.

La programación y las compras/ventas anteriores corresponden a Momentum32
`5e1579ca...`; el [registro aportado](evidencia_fisica/registro_20261125.md)
no confirma la imagen lenta nueva `1f514301...`.

Falta acreditar:

- Programación y prueba física del BIN nuevo de tendencia lenta.
- Ocho series completas a 1 ms y 10 ms si se exige esa extensión: actualmente
  se validaron 160.000 ticks a 100 µs y 396 de integración por cadencia larga.
- Patrimonio, referencia y resultado de cada una de las tres rondas oficiales.
- Defensa de los integrantes y comprobante de entrega original dentro del plazo.
- Perfil regional y comparación de hardware con la misma política final, para
  extender Amdahl/roofline más allá del estudio histórico.

Esta revisión del 25/11 es posterior al plazo oficial del 24/11 a las 10:00.
No se asigna una nota ni se confunde simulación con competencia física.

Para recompilar y repetir las comprobaciones documentales:

```powershell
python -B tools/generar_informe_latex.py
wsl -d Ubuntu -- bash docs/informe/compilar.sh
python -B tools/auditar_pdf.py
```
