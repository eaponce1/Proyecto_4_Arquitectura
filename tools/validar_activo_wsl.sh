#!/usr/bin/env bash
set -euo pipefail
# Temporary extracted package, no apt install and no changes to system packages.
export VERILATOR_ROOT=/tmp/pochoco_verilator_20261125/extracted/usr/share/verilator
export POCH_VERILATOR=/tmp/pochoco_verilator_20261125/extracted/usr/bin/verilator_bin
if [ ! -x "$POCH_VERILATOR" ]; then
    mkdir -p /tmp/pochoco_verilator_20261125
    pushd /tmp/pochoco_verilator_20261125 >/dev/null
    apt-get download verilator > download.log 2>&1
    dpkg-deb -x verilator_*.deb extracted
    popd >/dev/null
fi
python3 -B tools/validar_activo_verilator.py "$@"
