"""Compila y mide custom-0 en el testbench SPI de rendimiento del Proyecto 4."""
import argparse
import csv
import shutil
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
PYTHON = ROOT / "proyecto4" / "python"
import sys
sys.path.insert(0, str(PYTHON))
from enfoques_finales import estrategia_reversion_media
from simulador import leer_precios, simular_estrategia

VARIANT = ROOT / "proyecto4" / "alternativas" / "custom0"
RESULTS = ROOT / "proyecto4" / "resultados" / "co_disenio"

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--ticks",type=int,default=20000)
    ap.add_argument("--period-ns",type=int,default=30000)
    ap.add_argument("--output",type=Path,default=RESULTS/"custom0_ticks.csv")
    args=ap.parse_args()
    if not 1 <= args.ticks <= 20000 or args.period_ns < 10000:
        raise SystemExit("ticks 1..20000 y period-ns >= 10000 requeridos")
    for tool in ("iverilog","vvp"):
        if not shutil.which(tool): raise SystemExit(f"Falta {tool}")
    subprocess.run([sys.executable,str(ROOT/"proyecto4"/"sw"/"assembler.py"),str(VARIANT/"sw"/"trade.s"),"-o",str(VARIANT/"sw"/"trade.hex")],cwd=ROOT,check=True)
    prices=leer_precios()
    expected=[int(r["decision_recibida"]) for r in simular_estrategia(prices,"SMA10",estrategia_reversion_media).decisiones]
    RESULTS.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="custom0-",dir=ROOT/"proyecto4"/"tests") as td:
        td=Path(td); pf=td/"prices.hex"; ef=td/"expected.hex"; raw=td/"raw.csv"; exe=td/"tb.vvp"
        pf.write_text("".join(f"{p:02x}\n" for p in prices),encoding="ascii")
        ef.write_text("".join(f"{d:02x}\n" for d in expected),encoding="ascii")
        rtl=sorted(str(p) for p in (VARIANT/"rtl").rglob("*.v"))
        subprocess.run([shutil.which("iverilog"),"-g2012","-s","tb_trade_custom0_performance","-o",str(exe),*rtl,str(ROOT/"tests"/"ram_model.v"),str(VARIANT/"tb"/"tb_trade_custom0_performance.sv")],cwd=ROOT,check=True)
        run=subprocess.run([shutil.which("vvp"),str(exe),f"+PERIOD_NS={args.period_ns}",f"+PRICE_FILE={pf.relative_to(ROOT).as_posix()}",f"+EXPECTED_FILE={ef.relative_to(ROOT).as_posix()}",f"+TICKS={args.ticks}",f"+OUTPUT_FILE={raw.relative_to(ROOT).as_posix()}"],cwd=ROOT,check=True,text=True,capture_output=True)
        print(run.stdout.strip())
        rows=list(csv.DictReader(raw.open(newline="",encoding="ascii")))
        if len(rows)!=args.ticks: raise AssertionError(f"ticks medidos={len(rows)} esperados={args.ticks}")
        args.output.parent.mkdir(parents=True,exist_ok=True)
        with args.output.open("w",newline="",encoding="utf-8") as f:
            w=csv.DictWriter(f,fieldnames=rows[0].keys()); w.writeheader(); w.writerows(rows)
        print(f"CSV de ciclos: {args.output}")

if __name__=="__main__": main()
