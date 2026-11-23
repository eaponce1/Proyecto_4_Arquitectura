#!/usr/bin/env python3
"""Extrae resultados contables y compara las corridas oficiales disponibles."""
from __future__ import annotations

import csv
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
RUNS = HERE / "corridas"
OUT_CSV = HERE / "comparacion_oficial.csv"


def number(log: str, pattern: str) -> int | None:
    match = re.search(pattern, log)
    return int(match.group(1)) if match else None


def summarize(path: Path) -> dict[str, object]:
    log = (path / "simulacion.log").read_text(encoding="utf-8", errors="replace")
    orders_official = number(log, r"Ordenes ejecutadas:\s*(\d+)")
    worst = number(log, r"Peor caso precio->decision:\s*(\d+)")
    avg_match = re.search(r"Ciclos promedio precio->decision:\s*(\d+(?:\.\d+)?)", log)
    avg = avg_match.group(1) if avg_match else None
    checks = re.search(r"Testbenchs aprobados:\s*(\d+)\s*/\s*(\d+)", log)
    decision_path = path / "decisiones.csv"
    with decision_path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    if len(rows) != 20_000:
        raise RuntimeError(f"{decision_path}: {len(rows)} filas de decisiones; se esperaban 20000")
    peak, max_dd = 10_000, 0
    for row in rows:
        wealth = int(row["patrimonio"])
        peak = max(peak, wealth)
        max_dd = max(max_dd, peak - wealth)
    # Las decisiones de venta ejecutadas se cuentan por cambio en inventario.
    previous_shares = 0
    buy_orders = sell_orders = 0
    for row in rows:
        action = int(row["decision"], 16) >> 6
        shares = int(row["acciones"])
        if action == 1 and shares > previous_shares:
            buy_orders += 1
        elif action == 2 and shares < previous_shares:
            sell_orders += 1
        previous_shares = shares
    if orders_official is None or buy_orders + sell_orders != orders_official:
        raise RuntimeError(
            f"Conteo de fills no concuerda: compras={buy_orders}, ventas={sell_orders}, "
            f"órdenes oficiales={orders_official} en {path}"
        )
    last = rows[-1]
    final_wealth = int(last["patrimonio"])
    return {
        "variante": path.parent.name,
        "ronda": path.name,
        "ticks": len(rows),
        "patrimonio_final": final_wealth,
        "caja_final": int(last["caja"]),
        "acciones_finales": int(last["acciones"]),
        "rentabilidad_pct": round((final_wealth - 10_000) * 100 / 10_000, 6),
        "ordenes": orders_official,
        "compras": buy_orders,
        "ventas": sell_orders,
        "comisiones": (orders_official or 0) * 5,
        "drawdown_maximo": max_dd,
        "ciclos_promedio_tb_truncado": avg,
        "ciclos_peor_caso": worst,
        "criterios_aprobados": checks.group(1) if checks else "sin resultado",
        "criterios_totales": checks.group(2) if checks else "sin resultado",
        "diferencias_decision_vs_otra": "sin corrida pareada",
        "CSV_decisiones": decision_path.relative_to(HERE).as_posix(),
    }


def main() -> None:
    rows = []
    for path in sorted(RUNS.glob("*/ronda_*")):
        if (path / "simulacion.log").is_file() and (path / "decisiones.csv").is_file():
            rows.append(summarize(path))
    if not rows:
        raise SystemExit("No hay corridas completas para resumir")
    by_key = {(row["variante"], row["ronda"]): row for row in rows}
    for row in rows:
        peer = "software_original" if row["variante"] == "mmio_sma10_base" else "mmio_sma10_base"
        other = by_key.get((peer, row["ronda"]))
        if other:
            current = list(csv.DictReader((HERE / row["CSV_decisiones"]).open(newline="", encoding="utf-8")))
            matched = list(csv.DictReader((HERE / other["CSV_decisiones"]).open(newline="", encoding="utf-8")))
            row["diferencias_decision_vs_otra"] = sum(
                a["decision"].lower() != b["decision"].lower() for a, b in zip(current, matched)
            )
    fields = list(rows[0])
    with OUT_CSV.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    print(f"Corridas resumidas: {len(rows)}")
    print(f"Comparación: {OUT_CSV}")
    for row in rows:
        print(row)


if __name__ == "__main__":
    main()
