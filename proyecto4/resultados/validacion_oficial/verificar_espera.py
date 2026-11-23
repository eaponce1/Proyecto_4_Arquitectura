#!/usr/bin/env python3
"""Compare short direct runs with verified-idle runs of the same length."""
import csv
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
METRICS = (
    "Patrimonio final:", "Ordenes ejecutadas:", "Perdida maxima:",
    "No operar:", "Comprar y mantener:", "Peor caso precio->decision:",
    "Ciclos promedio precio->decision:", "Suma de ciclos de respuesta:",
    "PASS ", "Testbenchs aprobados:",
)


def read_trial(path: Path) -> tuple[list[dict], list[str], str]:
    with (path / "decisiones.csv").open(encoding="utf-8", newline="") as stream:
        rows = list(csv.DictReader(stream))
    log = (path / "simulacion.log").read_text(encoding="utf-8", errors="replace")
    metrics = [line for line in log.splitlines() if line.startswith(METRICS)]
    finish = re.search(r"\$finish called at (\d+) \(1ps\)", log)
    if not rows or len(metrics) != 13 or "Testbenchs aprobados: 4/4" not in metrics or not finish:
        raise SystemExit(f"Corrida de contraste incompleta: {path}")
    return rows, metrics, finish.group(1)


def main() -> None:
    for variant in ("mmio_sma10_base", "software_original"):
        for round_no in (1, 2):
            relative = Path(variant) / f"ronda_{round_no}"
            direct = HERE / "contraste_directo" / relative
            fast = HERE / "contraste_rapido" / relative
            rows, metrics, finish = read_trial(fast)
            if (rows, metrics, finish) != read_trial(direct):
                raise SystemExit(f"Diferencia entre la espera verificada e Icarus directo: {relative}")
            log = (fast / "simulacion.log").read_text(encoding="utf-8")
            skipped = re.search(r"Espera verificada: (\d+) intervalos, (\d+) ciclos omitidos", log)
            if not skipped or int(skipped.group(1)) != len(rows) or not int(skipped.group(2)):
                raise SystemExit(f"El contraste no usó la espera verificada en todos los ticks: {relative}")
            print(f"PASS {variant} ronda {round_no}: {len(rows)} filas, contabilidad, "
                  f"ciclos, cuatro criterios y tiempo final {finish} ps idénticos")


if __name__ == "__main__":
    main()
