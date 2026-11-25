# Informe LaTeX

El PDF principal es [../INFORME_FINAL.pdf](../INFORME_FINAL.pdf).
La fuente es `informe_final.tex`; `datos_generados.tex` y las ocho figuras
se generan desde los CSV/JSON verificados del proyecto.

Desde la raiz del repositorio:

```powershell
python -X utf8 -B tools/generar_informe_latex.py
wsl.exe -d Ubuntu -- bash docs/informe/compilar.sh
```

En Ubuntu se necesitan `texlive-latex-base`, `texlive-latex-recommended`,
`texlive-lang-spanish`, `lmodern` y `poppler-utils`. Tambien puede ejecutarse
`bash compilar.sh` desde un entorno Linux con esas herramientas.

Se ejecuta pdfLaTeX tres veces para resolver indice, referencias e hipervinculos.
Los auxiliares y logs quedan en `build/`, excluido de Git. El PDF final se copia
a `docs/INFORME_FINAL.pdf`. El informe documenta la imagen activa de 1.268 LC
y sus limites, sin heredar una aprobacion fisica de otras versiones.
