#!/usr/bin/env bash
set -euo pipefail
source "$(dirname "$0")/preparar_verilator_wsl.sh"
python3 -B tools/medir_codisenio_lento.py "$@"
