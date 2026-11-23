"""Sintetiza y enruta únicamente la variante MMIO SMA10 optimizada."""
import shutil, subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/"proyecto4"/"resultados"/"co_disenio"
RTL=ROOT/"proyecto4"/"alternativas"/"mmio_sma10_opt"/"rtl"
TOP=ROOT/"proyecto4"/"alternativas"/"mmio_sma10_opt"/"trade_top.v"
for tool in ("yosys","nextpnr-ice40"):
    if not shutil.which(tool): raise SystemExit(f"Falta {tool} en PATH")
OUT.mkdir(parents=True,exist_ok=True)
sources=sorted(p.relative_to(ROOT).as_posix() for p in RTL.rglob("*.v"))+[TOP.relative_to(ROOT).as_posix()]
json=OUT/"mmio_sma10_opt.json"; asc=OUT/"mmio_sma10_opt.asc"
yosys=subprocess.run([shutil.which("yosys"),"-p",f'read_verilog {" ".join(sources)}; synth_ice40 -top trade_top -json {json.relative_to(ROOT).as_posix()}'],cwd=ROOT,text=True,capture_output=True)
(OUT/"mmio_sma10_opt_yosys.log").write_text(yosys.stdout+yosys.stderr,encoding="utf-8")
if yosys.returncode: raise SystemExit(f"Yosys falla: {yosys.returncode}")
print("Yosys PASS")
pn=subprocess.run([shutil.which("nextpnr-ice40"),"--seed","1","--freq","25","--hx1k","--package","vq100","--json",json.relative_to(ROOT).as_posix(),"--pcf","goboard.pcf","--asc",asc.relative_to(ROOT).as_posix()],cwd=ROOT,text=True,capture_output=True)
(OUT/"mmio_sma10_opt_nextpnr.log").write_text(pn.stdout+pn.stderr,encoding="utf-8")
print("nextpnr PASS 25MHz" if pn.returncode==0 else "nextpnr FAIL; ver registro")
raise SystemExit(pn.returncode)
