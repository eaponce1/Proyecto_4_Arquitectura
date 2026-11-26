#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/../resultados_simulacion/testbench_todas_acciones"
pdflatex -interaction=nonstopmode -halt-on-error -jobname=INFORME_TESTBENCH informe_testbench.tex >compilacion1.log 2>&1
pdflatex -interaction=nonstopmode -halt-on-error -jobname=INFORME_TESTBENCH informe_testbench.tex >compilacion2.log 2>&1
pdfinfo INFORME_TESTBENCH.pdf >pdfinfo.txt
pdftotext -layout INFORME_TESTBENCH.pdf informe_extraido.txt
echo 'PASS anexo LaTeX: resultados_simulacion/testbench_todas_acciones/INFORME_TESTBENCH.pdf'
