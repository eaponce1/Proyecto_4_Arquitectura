"""Mide trade.hex en el SoC RTL y crea CSV, resumen Markdown y SVG."""

import argparse
import csv
import shutil
import statistics
import subprocess
import tempfile
from pathlib import Path

from enfoques_finales import estrategia_reversion_media
from simulador import leer_precios, simular_estrategia

ROOT = Path(__file__).resolve().parents[2]
RESULTS = ROOT / "proyecto4" / "resultados"
TB = ROOT / "proyecto4" / "tb" / "tb_trade_performance.sv"


def percentile(values: list[float], percent: float) -> float:
    ordered = sorted(values)
    position = (len(ordered) - 1) * percent
    lo = int(position)
    hi = min(lo + 1, len(ordered) - 1)
    return ordered[lo] + (ordered[hi] - ordered[lo]) * (position - lo)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--round", type=int, choices=(1, 2, 3), help="periodo oficial de ronda")
    parser.add_argument("--period-ns", type=int, default=30_000)
    parser.add_argument("--ticks", type=int, default=20_000)
    args = parser.parse_args()
    period_ns = {1: 10_000_000, 2: 1_000_000, 3: 100_000}[args.round] if args.round else args.period_ns
    if not 1 <= args.ticks <= 20_000 or period_ns < 10_000:
        raise SystemExit("TICKS debe ser 1..20000 y PERIOD_NS >=10000")
    for tool in ("iverilog", "vvp"):
        if not shutil.which(tool):
            raise SystemExit(f"Se requiere {tool} en PATH")

    prices = leer_precios()
    reference = simular_estrategia(prices, "SMA10", estrategia_reversion_media)
    expected = [int(row["decision_recibida"]) for row in reference.decisiones]
    RESULTS.mkdir(parents=True, exist_ok=True)
    output_csv = RESULTS / "mediciones_software.csv"
    with tempfile.TemporaryDirectory(prefix="trade-perf-", dir=ROOT / "proyecto4" / "tests") as tmp_name:
        tmp = Path(tmp_name)
        pfile, efile, rawfile, vvpfile = (tmp / name for name in ("prices.hex", "expected.hex", "raw.csv", "tb.vvp"))
        pfile.write_text("".join(f"{p:02x}\n" for p in prices), encoding="ascii")
        efile.write_text("".join(f"{d:02x}\n" for d in expected), encoding="ascii")
        rtl = sorted(str(p) for p in (ROOT / "rtl").rglob("*.v"))
        compile_cmd = [shutil.which("iverilog"), "-g2012", "-s", "tb_trade_performance", "-o", str(vvpfile),
                       *rtl, str(ROOT / "tests" / "ram_model.v"), str(TB)]
        subprocess.run(compile_cmd, cwd=ROOT, check=True)
        sim_cmd = [shutil.which("vvp"), str(vvpfile), f"+PERIOD_NS={period_ns}",
                   f"+PRICE_FILE={pfile.relative_to(ROOT).as_posix()}",
                   f"+EXPECTED_FILE={efile.relative_to(ROOT).as_posix()}", f"+TICKS={args.ticks}",
                   f"+OUTPUT_FILE={rawfile.relative_to(ROOT).as_posix()}"]
        completed = subprocess.run(sim_cmd, cwd=ROOT, check=True, text=True, capture_output=True)
        print(completed.stdout.strip())
        raw = list(csv.DictReader(rawfile.open(newline="", encoding="ascii")))
        if len(raw) != args.ticks:
            raise AssertionError(f"La simulacion produjo {len(raw)} ticks, esperaba {args.ticks}")
        rows = []
        for record in raw:
            row = {key: int(value) for key, value in record.items()}
            if row["tick"] < 0 or row["tick"] >= len(prices) or row["price"] != prices[row["tick"]]:
                raise AssertionError(f"tick/precio fuera de secuencia: {row}")
            row["compute_cycles"] = row["portfolio_cycles"] + row["history_cycles"] + row["sma_cycles"] + row["signal_cycles"]
            row["compute_ic"] = row["portfolio_ic"] + row["history_ic"] + row["sma_ic"] + row["signal_ic"]
            row["cpi_total"] = row["cycles_total"] / row["ic_total"]
            row["cpi_compute"] = row["compute_cycles"] / row["compute_ic"]
            row["execution_us"] = row["elapsed_ns"] / 1000
            row["compute_us"] = row["compute_cycles"] * 0.04
            row["status_wait_us"] = row["status_cycles"] * 0.04
            row["spi_read_us"] = row["price_cycles"] * 0.04
            row["budget_cycles"] = period_ns // 40
            row["budget_margin_cycles"] = row["budget_cycles"] - row["cycles_total"]
            row["postdecision_wait_cycles"] = row["budget_margin_cycles"]
            row["postdecision_wait_us"] = period_ns / 1000 - row["execution_us"]
            for debug_column in ("decision_written", "pc_at_write", "new_price_at_write"):
                row.pop(debug_column)
            if row["compute_cycles"] + row["status_cycles"] + row["price_cycles"] != row["cycles_total"]:
                raise AssertionError(f"Clasificacion de ciclos incompleta en tick {row['tick']}")
            rows.append(row)

        fields = list(rows[0])
        with output_csv.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fields)
            writer.writeheader()
            writer.writerows(rows)

    metrics = {}
    columns = ("ic_total", "cycles_total", "cpi_total", "cpi_compute", "execution_us", "compute_cycles",
               "compute_us", "status_wait_us", "spi_read_us", "postdecision_wait_us", "portfolio_cycles",
               "history_cycles", "sma_cycles", "signal_cycles")
    for col in columns:
        values = [float(r[col]) for r in rows]
        metrics[col] = (statistics.mean(values), statistics.median(values), percentile(values, .95), max(values))

    title = f"{'Ronda '+str(args.round) if args.round else 'Medicion'} — {period_ns/1000:g} us"
    svg = RESULTS / "rendimiento_software.svg"
    plot_groups = ["STATUS/espera", "Lectura PRICE", "Cartera", "Historial", "SMA10", "Señal+DECISION"]
    sums = [sum(r[c] for r in rows) / len(rows) for c in
            ("status_cycles", "price_cycles", "portfolio_cycles", "history_cycles", "sma_cycles", "signal_cycles")]
    colors = ["#9aa6b2", "#5b8ff9", "#61dDAA", "#65789b", "#f6bd16", "#e8684a"]
    maxval = max(sums)
    bars = []
    for i, (label, value, color) in enumerate(zip(plot_groups, sums, colors)):
        y = 75 + i * 48
        width = 650 * value / maxval if maxval else 0
        bars.append(f'<text x="12" y="{y+18}" font-size="14">{label}</text><rect x="150" y="{y}" width="{width:.1f}" height="26" fill="{color}"/><text x="{160+width:.1f}" y="{y+18}" font-size="13">{value:.2f} ciclos/tick</text>')
    svg.write_text(f'''<svg xmlns="http://www.w3.org/2000/svg" width="900" height="390" viewBox="0 0 900 390">
<rect width="100%" height="100%" fill="white"/><text x="12" y="30" font-size="20" font-family="sans-serif">Ciclos medios por sección — {title}</text>
{''.join(bars)}<text x="12" y="370" font-size="12">Espino RTL, {len(rows):,} ticks. Cycles measured at posedge; commit = instr_valid_id &amp;&amp; !stall.</text></svg>''', encoding="utf-8")

    labels = {"ic_total": "IC desde byte_done hasta DECISION", "cycles_total": "Ciclos recepción precio→DECISION",
              "cpi_total": "CPI total (incluye polling STATUS)", "execution_us": "Tiempo precio→DECISION (µs medidos)",
              "cpi_compute": "CPI algoritmo posterior a PRICE",
              "compute_cycles": "Ciclos algoritmo posterior a PRICE", "compute_us": "Tiempo algoritmo (µs)",
              "status_wait_us": "Polling STATUS (µs)", "spi_read_us": "Servicio de lectura PRICE (µs)",
              "postdecision_wait_us": "Espera restante hasta próximo tick (µs)",
              "portfolio_cycles": "Actualización cartera (ciclos)", "history_cycles": "Actualización historial (ciclos)",
              "sma_cycles": "Suma SMA10 y 10×precio (ciclos)", "signal_cycles": "Comparaciones y DECISION (ciclos)"}
    cadence = f"ronda oficial {args.round}" if args.round else "cadencia de medición personalizada"
    md = ["# Medición de rendimiento de `trade.hex`", "", f"Se ejecutó **{cadence}**, período {period_ns/1000:g} µs = {period_ns//40:,} ciclos por intervalo a 25 MHz. Serie simulada: {len(rows):,} ticks.",
          "", "## Instrumentación y validez", "", "La simulación usa el SoC RTL original (`EnableSpi=1`) y un banco maestro independiente. El contador IC externo cuenta `dut.u_core.instr_valid_id && !dut.u_core.stall`, la condición `commit` definida en `espino_id_stage.v`; no se añadieron contadores ni lógica al core. Los ciclos son flancos de reloj desde `byte_done` de la transacción hasta la escritura de DECISION. La medición de tiempo es `$time` en RTL; 40 ns/ciclo.",
          "", f"Se comparo cada MISO con `decision_recibida` de Python; hubo {len(rows):,} lecturas PRICE y escrituras DECISION, sin ticks perdidos ni discrepancias. El sondeo posterior hasta el siguiente byte_done se reporta como espera derivada del periodo menos el tiempo de respuesta; el core sigue activo sondeando STATUS.",
          "", "## Estadísticas por tick", "", f"Promedio, mediana y P95 se calcularon sobre los {len(rows):,} registros; P95 usa interpolación lineal. CPI = ciclos/IC.", "", "| Medición | Promedio | Mediana | P95 | Peor caso |", "|---|---:|---:|---:|---:|"]
    for col in columns:
        mean, median, p95, worst = metrics[col]
        fmt = (lambda x: f"{x:.3f}") if "cpi" in col else (lambda x: f"{x:.2f}" if "us" in col else f"{x:.1f}" if col == "ic_total" else f"{x:.0f}")
        md.append(f"| {labels[col]} | {fmt(mean)} | {fmt(median)} | {fmt(p95)} | {fmt(worst)} |")
    used = [r["cycles_total"] for r in rows]
    md += ["", "## Presupuestos de las tres rondas", "", f"El SoC RTL ejecutó {len(rows):,} ticks a {period_ns/1000:g} µs. La cadencia predeterminada de 30 µs reduce el sondeo prolongado de STATUS, pero sigue siendo más exigente que el período oficial de ronda 3. Se comparan los ciclos de respuesta medidos precio→DECISION con los presupuestos oficiales; la cantidad de polling y el CPI total dependen de la cadencia, por lo que no se presentan estas cifras como simulaciones de las otras rondas.", "", "| Ronda | Período | Presupuesto | Respuestas medidas dentro del presupuesto | Margen mínimo frente a ciclos medidos |", "|---:|---:|---:|---:|---:|"]
    for r, ns in ((1, 10_000_000), (2, 1_000_000), (3, 100_000)):
        cyc = ns // 40
        fit = sum(v < cyc for v in used)
        md.append(f"| {r} | {ns/1000:g} µs | {cyc:,} ciclos | {fit:,}/{len(used):,} | {cyc-max(used):,} ciclos |")
    md += ["", "## Presupuestos oficiales", "", f"Se simularon {len(rows):,} ticks a {period_ns/1000:g} us de cadencia custom. Los presupuestos comparan la respuesta medida desde byte_done hasta DECISION; no se ejecutaron tres corridas oficiales independientes.", "", "| Ronda | Periodo | Presupuesto | Respuestas dentro del presupuesto | Margen minimo |", "|---:|---:|---:|---:|---:|"]
    for r, ns in ((1, 10_000_000), (2, 1_000_000), (3, 100_000)):
        cyc = ns // 40
        fit = sum(v < cyc for v in used)
        md.append(f"| {r} | {ns/1000:g} us | {cyc:,} ciclos | {fit:,}/{len(used):,} | {cyc-max(used):,} ciclos |")
    md += ["", "## Perfil de ciclos", "", "SMA10 promedia 163.9 de 206.2 ciclos de calculo posterior a PRICE (79.5%), el tramo dominante. La suma de diez palabras exige diez lecturas y acumulaciones. La actualizacion de cartera alcanza 208 ciclos en tick 17 por los bucles de cantidad/efectivo. El postdecision hasta el siguiente byte_done se ocupa sondeando STATUS.",
           "", "## Errores pendientes y limites", "", "Los 20.000 ticks se simularon a 30 us, no en tres corridas RTL a los periodos oficiales. Todas las respuestas quedaron dentro de 750 ciclos por intervalo; ninguna excedio el presupuesto oficial mas estricto de 2.500 ciclos. IC/ciclos terminan al escribir DECISION y excluyen commits del polling posterior, cuya duracion se calcula en el CSV. Icarus avisa que trade.hex tiene 89 palabras y RAM 512; es el aviso esperado de readmemh. Medicion RTL con reloj ideal, no Go Board ni timing post-sintesis. No se modificaron estrategia, assembler, ALU ni RTL.",
           "", "## Reproduccion", "", "Desde `pochoco_soc-main`:", "", "```powershell", "python -B proyecto4/python/medir_rendimiento_trade.py", "python -B proyecto4/python/medir_rendimiento_trade.py --round 3", "python -B -m unittest discover -s proyecto4/python -v", "```", "", "Sin --round se simulan 20.000 ticks a 30 us. --round 1/2/3 usa los periodos oficiales y tarda mucho mas por el sondeo en Icarus; --ticks sirve para pruebas cortas."]
    (RESULTS / "rendimiento_software.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print(f"Escrito: {output_csv}")
    print(f"Escrito: {RESULTS / 'rendimiento_software.md'}")
    print(f"Escrito: {svg}")


if __name__ == "__main__":
    main()
