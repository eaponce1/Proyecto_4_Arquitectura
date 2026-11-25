"""Generate expected tick decisions from the project's Python SMA10 model."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[4]
sys.path.insert(0,str(ROOT/"proyecto4"/"python"))
from enfoques_finales import estrategia_reversion_media
from simulador import simular_estrategia
OUT=Path(__file__).resolve().parents[1]/"data"
PRICES=[200]*10+[90]*3+[220]*3
def write_hex(path,values): path.write_text("".join(f"{v:02x}\n" for v in values),encoding="ascii")
def main():
    OUT.mkdir(parents=True,exist_ok=True)
    result=simular_estrategia(PRICES,"SMA10 Python",estrategia_reversion_media)
    response=[0]+[r["decision_siguiente"] for r in result.decisiones[:-1]]
    writes=[r["decision_siguiente"] for r in result.decisiones]
    write_hex(OUT/"prices.hex",PRICES);write_hex(OUT/"expected_decisions.hex",response);write_hex(OUT/"expected_writes.hex",writes)
    print(f"Python reference vectors ready: {len(PRICES)} ticks")
if __name__=="__main__": main()
