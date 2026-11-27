# Auditoría de entrega — Proyecto 4

Revisión del 27/11/2026 contra el [enunciado oficial](referencia/enunciado_proyecto4.pdf).

| Apartado | Peso | Estado |
|---|---:|---|
| Algoritmo y referencias | 1,0 | Documentado y probado; política, contabilidad y referencias |
| Assembly, IC, ciclos, CPI y tiempos | 0,8 | Documentado y medido sobre la versión vigente |
| Co-diseño hardware/software | 1,2 | Comparación final cerrada: cuatro variantes, perfil regional, Amdahl, roofline, síntesis y enrutado |

Los pesos no constituyen una nota. Detalle en [PDF](AUDITORIA_ENTREGA.pdf),
[LaTeX](informe/auditoria_entrega.tex) y [JSON](AUDITORIA_ENTREGA.json).

El [estudio final](evidencia_codisenio_final/resumen.json) compara software
incremental, Custom-0 y dos periféricos MMIO sobre las mismas ocho series.
Son 32 ejecuciones y 640.000 ticks sin diferencias. Los periféricos caben:
1.219 y 1.227 LC. Custom-0 ocupa 1.368 LC y no cabe en HX1K, sin Fmax válido.
Se conserva MMIO incremental y el BIN activo. El estudio histórico queda separado.

Continúan vigentes los 78 escenarios y 1.557.620 ticks; la repetición del ZIP
usa los mismos ocho CSV. No garantiza rentabilidad: la lenta supera mantener en
5/8 conocidas y su media es menor que la anterior; el estrés termina con 69.

La [comparación directa de flash](evidencia_fisica/verificacion_flash_lenta_20261127T004337Z.json)
dio **VERIFY OK** para el BIN actual sin escribir memoria.
La prueba posterior con la maestra dejó [solo D1](evidencia_fisica/incidente_maestra_solo_d1.json):
no acredita recepción SPI. La causa sigue sin determinarse.

Para acreditar la entrega integral faltan:

- Recepción física desde la maestra y registro de precios/MISO.
- Patrimonio, referencia y resultado oficial de las tres rondas.
- Defensa y comprobante de entrega original en plazo; esta revisión es posterior al cierre del 24/11.
- Si se exige esa extensión, ocho series completas a 1 ms y 10 ms; hoy hay integración de 396 ticks por cadencia larga.

Reproducción desde la raíz del repositorio:

```powershell
python -B tools/auditar_codisenio_final.py
python -B tools/generar_informe_latex.py
wsl -d Ubuntu -- bash docs/informe/compilar.sh
python -B tools/auditar_pdf.py
```
