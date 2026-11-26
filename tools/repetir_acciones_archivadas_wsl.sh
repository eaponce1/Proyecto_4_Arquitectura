#!/usr/bin/env bash
set -euo pipefail
source "$(dirname "$0")/preparar_verilator_wsl.sh"
python3 -B tools/repetir_acciones_archivadas.py "$@"
