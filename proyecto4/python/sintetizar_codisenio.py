"""Reproduce Yosys y nextpnr para baseline, custom-0 y MMIO SMA10."""
import shutil, subprocess
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/"proyecto4"/"resultados"/"co_disenio"
CONFIGS={
 "original":(ROOT/"rtl",ROOT/"proyecto4"/"rtl"/"trade_top.v"),
 "custom0":(ROOT/"proyecto4"/"alternativas"/"custom0"/"rtl",ROOT/"proyecto4"/"alternativas"/"custom0"/"trade_top.v"),
 "mmio_sma10":(ROOT/"proyecto4"/"alternativas"/"mmio_sma10"/"rtl",ROOT/"proyecto4"/"alternativas"/"mmio_sma10"/"trade_top.v"),
 "mmio_sma10_opt":(ROOT/"proyecto4"/"alternativas"/"mmio_sma10_opt"/"rtl",ROOT/"proyecto4"/"alternativas"/"mmio_sma10_opt"/"trade_top.v"),
}

def main():
    for tool in ("yosys","nextpnr-ice40"):
        if not shutil.which(tool): raise SystemExit(f"Falta {tool} en PATH")
    OUT.mkdir(parents=True,exist_ok=True)
    for name,(rtl_dir,top) in CONFIGS.items():
        sources=sorted(p.relative_to(ROOT).as_posix() for p in rtl_dir.rglob("*.v"))+[top.relative_to(ROOT).as_posix()]
        json=OUT/f"{name}.json"; asc=OUT/f"{name}.asc"
        yosys=subprocess.run([shutil.which("yosys"),"-p",f'read_verilog {" ".join(sources)}; synth_ice40 -top trade_top -json {json.relative_to(ROOT).as_posix()}'],cwd=ROOT,text=True,capture_output=True)
        (OUT/f"{name}_yosys.log").write_text(yosys.stdout+yosys.stderr,encoding="utf-8")
        if yosys.returncode:
            print(f"{name}: Yosys FAILED ({yosys.returncode})")
            continue
        pn=subprocess.run([shutil.which("nextpnr-ice40"),"--seed","1","--freq","25","--hx1k","--package","vq100","--json",json.relative_to(ROOT).as_posix(),"--pcf","goboard.pcf","--asc",asc.relative_to(ROOT).as_posix()],cwd=ROOT,text=True,capture_output=True)
        (OUT/f"{name}_nextpnr.log").write_text(pn.stdout+pn.stderr,encoding="utf-8")
        status="PASS 25MHz" if pn.returncode==0 else "FAIL place-and-route; inspect log"
        print(f"{name}: Yosys PASS; nextpnr {status}")

if __name__=="__main__": main()
