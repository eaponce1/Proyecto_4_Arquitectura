#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p informe_build
pdflatex -interaction=nonstopmode -halt-on-error -output-directory=informe_build INFORME_CUANTITATIVO.tex >informe_build/paso1.log 2>&1
pdflatex -interaction=nonstopmode -halt-on-error -output-directory=informe_build INFORME_CUANTITATIVO.tex >informe_build/paso2.log 2>&1
cp informe_build/INFORME_CUANTITATIVO.pdf INFORME_CUANTITATIVO.pdf
pdfinfo INFORME_CUANTITATIVO.pdf >informe_build/pdfinfo.txt
pdftotext -layout INFORME_CUANTITATIVO.pdf informe_build/extraido.txt
if grep -q 'Overfull' informe_build/INFORME_CUANTITATIVO.log; then
    echo 'Revisar cajas desbordadas en el informe'; exit 1
fi
