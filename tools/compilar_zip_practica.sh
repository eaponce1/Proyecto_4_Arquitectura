#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/../resultados_simulacion/testbench_zip_practica"
pdflatex -interaction=nonstopmode -halt-on-error -jobname=INFORME_ZIP_PRACTICA informe_zip.tex >compilacion1.log 2>&1
pdflatex -interaction=nonstopmode -halt-on-error -jobname=INFORME_ZIP_PRACTICA informe_zip.tex >compilacion2.log 2>&1
pdfinfo INFORME_ZIP_PRACTICA.pdf >pdfinfo.txt
pdftotext -layout INFORME_ZIP_PRACTICA.pdf informe_extraido.txt
echo 'PASS PDF del ZIP de practica generado'
