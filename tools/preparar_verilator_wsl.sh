#!/usr/bin/env bash
# Se carga con source; evita heredar el ejecutable Windows a traves de WSL.
if [ -x /usr/bin/verilator ]; then
    export POCH_VERILATOR=/usr/bin/verilator
else
    export VERILATOR_ROOT=/tmp/pochoco_verilator_20261125/extracted/usr/share/verilator
    export POCH_VERILATOR=/tmp/pochoco_verilator_20261125/extracted/usr/bin/verilator_bin
    if [ ! -x "$POCH_VERILATOR" ]; then
        mkdir -p /tmp/pochoco_verilator_20261125
        pushd /tmp/pochoco_verilator_20261125 >/dev/null
        apt-get download verilator >download.log 2>&1
        dpkg-deb -x verilator_*.deb extracted
        popd >/dev/null
    fi
fi
