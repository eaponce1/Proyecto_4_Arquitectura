#!/usr/bin/env python3
"""Ejecuta el testbench publicado con solo parámetros de entorno adaptados.

No altera la contabilidad ni los cuatro checks del profesor. Conserva copias
del archivo oficial y genera una fuente derivada por variante/ronda.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import re
import shutil
import subprocess
from pathlib import Path

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[2]
OFFICIAL_TB = OUT / "tb_proyecto_4_profesor.sv"
SERIES = OUT / "practica_meta.csv"
RUNS = OUT / "corridas"


def prepare_tb(variant: str, round_no: int, ticks: int, output_csv: Path) -> Path:
    source = OFFICIAL_TB.read_text(encoding="utf-8-sig")
    periods = {1: 10_000_000, 2: 1_000_000, 3: 100_000}
    program = (
        "proyecto4/sw/trade.hex" if variant == "software" else
        "proyecto4/alternativas/mmio_sma10/sw/trade.hex"
    )
    replacements = {
        'localparam string PROGRAMA   = "sw/trade.hex";':
            f'localparam string PROGRAMA   = "{program}";',
        'localparam string SERIE      = "tb/practica.csv";':
            'localparam string SERIE      = "proyecto4/resultados/validacion_oficial/practica_meta.csv";',
        'localparam int    PERIODO_NS = 100000;':
            f'localparam int    PERIODO_NS = {periods[round_no]};',
        'localparam int    NTICKS     = 2000;':
            f'localparam int    NTICKS     = {ticks};',
        'pochoco_soc #(.MemFile(PROGRAMA)) dut (':
            'pochoco_soc #(.MemFile(PROGRAMA), .EnableSpi(1)) dut (',
        'fd = $fopen("decisiones.csv", "w");':
            f'fd = $fopen("{output_csv.as_posix()}", "w");',
    }
    for old, new in replacements.items():
        count = source.count(old)
        if count != 1:
            raise RuntimeError(f"Se esperaba exactamente una configuración {old!r}; encontradas {count}")
        source = source.replace(old, new)

    # Extensión de observabilidad, sin sustituir la métrica oficial de peor caso.
    source = source.replace(
        'int ciclos = 0, peor_caso = 0, respuestas = 0, precios_perdidos = 0;',
        'int ciclos = 0, peor_caso = 0, respuestas = 0, precios_perdidos = 0;\n'
        '  longint unsigned ciclos_acumulados = 0;'
    )
    source = source.replace(
        '      respuestas++;\n      esperando = 0;',
        '      respuestas++;\n      ciclos_acumulados = ciclos_acumulados + ciclos;\n      esperando = 0;'
    )
    source = source.replace(
        '$display("Peor caso precio->decision: %0d ciclos (disponibles: %0d)", peor_caso, presupuesto);',
        '$display("Peor caso precio->decision: %0d ciclos (disponibles: %0d)", peor_caso, presupuesto);\n'
        '    $display("Ciclos promedio precio->decision: %0.2f (%0d respuestas)", '
        'respuestas ? (1.0*ciclos_acumulados) / respuestas : 0.0, respuestas);\n'
        '    $display("Suma de ciclos de respuesta: %0d", ciclos_acumulados);'
    )

    # Asegurar que el banco derivado conserva literalmente los cuatro criterios.
    checks = re.findall(r'chequear\((.*?);', source, flags=re.DOTALL)
    expected = [
        'bits_x == 0',
        'respuestas > 0',
        'precios_perdidos == 0',
        'peor_caso < presupuesto',
    ]
    for check in expected:
        if sum(check in item for item in checks) != 1:
            raise RuntimeError(f"El check oficial no se preservó: {check}")

    run_dir = output_csv.parent
    run_dir.mkdir(parents=True, exist_ok=True)
    configured = run_dir / "tb_proyecto_4_configurado.sv"
    configured.write_text(source, encoding="utf-8")
    return configured


def validate_inputs() -> None:
    rows = list(csv.reader(SERIES.open(newline="", encoding="utf-8-sig")))
    if len(rows) != 20_001 or rows[0] != ["tick", "price"]:
        raise RuntimeError(f"CSV oficial esperado: header + 20000 filas, recibido {len(rows)-1} filas")
    for expected_tick, row in enumerate(rows[1:]):
        if len(row) != 2 or int(row[0]) != expected_tick or not 1 <= int(row[1]) <= 255:
            raise RuntimeError(f"Fila CSV inválida para tick {expected_tick}: {row}")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--variant", choices=("mmio", "software"), required=True)
    ap.add_argument("--round", type=int, choices=(1, 2, 3), required=True)
    ap.add_argument("--ticks", type=int, default=20_000)
    args = ap.parse_args()
    if not 1 <= args.ticks <= 20_000:
        ap.error("--ticks debe estar en 1..20000")
    for tool in ("iverilog", "vvp"):
        if not shutil.which(tool):
            raise SystemExit(f"No se encontró {tool} en PATH")
    validate_inputs()
    variant = "mmio_sma10_base" if args.variant == "mmio" else "software_original"
    run_dir = RUNS / variant / f"ronda_{args.round}"
    run_dir.mkdir(parents=True, exist_ok=True)
    output_csv = run_dir / "decisiones.csv"
    tb = prepare_tb(args.variant, args.round, args.ticks, output_csv)
    rtl_dir = ROOT / ("proyecto4/alternativas/mmio_sma10/rtl" if args.variant == "mmio" else "rtl")
    rtl = sorted(str(path) for path in rtl_dir.rglob("*.v"))
    executable = run_dir / "tb_proyecto_4.vvp"
    compile_cmd = [shutil.which("iverilog"), "-g2012", "-s", "tb_proyecto_4", "-o", str(executable),
                   *rtl, str(ROOT / "tests/ram_model.v"), str(tb)]
    with (run_dir / "compilacion.log").open("w", encoding="utf-8") as log:
        compiled = subprocess.run(compile_cmd, cwd=ROOT, text=True, stdout=log, stderr=subprocess.STDOUT)
    if compiled.returncode:
        print((run_dir / "compilacion.log").read_text(encoding="utf-8", errors="replace"))
        raise SystemExit(compiled.returncode)
    command = [shutil.which("vvp"), "-n", str(executable)]
    run = subprocess.run(command, cwd=ROOT, text=True, capture_output=True)
    (run_dir / "simulacion.log").write_text(run.stdout + run.stderr, encoding="utf-8")
    print(run.stdout, end="")
    if run.stderr:
        print(run.stderr, end="")
    if run.returncode:
        raise SystemExit(run.returncode)
    result = re.search(r"Testbenchs aprobados:\s*(\d+)\s*/\s*(\d+)", run.stdout)
    if not result or result.group(1) != result.group(2) or "FAIL " in run.stdout:
        raise SystemExit("El proceso terminó, pero los cuatro criterios oficiales no aprobaron; revisar simulacion.log")
    if not output_csv.is_file():
        raise RuntimeError("La simulación terminó sin crear decisiones.csv")
    print(f"Decisiones: {output_csv.relative_to(ROOT)}")
    print(f"Log: { (run_dir / 'simulacion.log').relative_to(ROOT) }")


if __name__ == "__main__":
    main()
