#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p build
pdflatex -interaction=nonstopmode -halt-on-error -output-directory=build informe_final.tex >build/paso1.log 2>&1
pdflatex -interaction=nonstopmode -halt-on-error -output-directory=build informe_final.tex >build/paso2.log 2>&1
pdflatex -interaction=nonstopmode -halt-on-error -output-directory=build informe_final.tex >build/paso3.log 2>&1
cp build/informe_final.pdf ../INFORME_FINAL.pdf
pdfinfo ../INFORME_FINAL.pdf > build/pdfinfo.txt
pdftotext -layout ../INFORME_FINAL.pdf build/informe_extraido.txt
pdflatex -interaction=nonstopmode -halt-on-error -output-directory=build auditoria_entrega.tex >build/auditoria_paso1.log 2>&1
pdflatex -interaction=nonstopmode -halt-on-error -output-directory=build auditoria_entrega.tex >build/auditoria_paso2.log 2>&1
cp build/auditoria_entrega.pdf ../AUDITORIA_ENTREGA.pdf
pdfinfo ../AUDITORIA_ENTREGA.pdf >build/auditoria_pdfinfo.txt
pdftotext -layout ../AUDITORIA_ENTREGA.pdf build/auditoria_extraida.txt
echo 'PASS PDF LaTeX compilado: docs/INFORME_FINAL.pdf'
