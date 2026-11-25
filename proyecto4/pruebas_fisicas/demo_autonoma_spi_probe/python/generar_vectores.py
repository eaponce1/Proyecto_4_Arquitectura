"""Generate exact Python SMA10 vectors for the SPI edge/byte diagnostic."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[4]
sys.path.insert(0,str(ROOT/"proyecto4"/"python"))
from enfoques_finales import estrategia_reversion_media
from simulador import simular_estrategia
OUT=Path(__file__).resolve().parents[1]/"data"
PRICES=[200]*10+[90]*3+[220]*3
def write_hex(path,values): path.write_text("".join(f"{value:02x}\n" for value in values),encoding="ascii")
def main():
    OUT.mkdir(parents=True,exist_ok=True)
    result=simular_estrategia(PRICES,"SMA10 Python",estrategia_reversion_media)
    miso=[0]+[r["decision_siguiente"] for r in result.decisiones[:-1]]
    writes=[r["decision_siguiente"] for r in result.decisiones]
    write_hex(OUT/"prices.hex",PRICES)
    write_hex(OUT/"expected_decisions.hex",miso)
    write_hex(OUT/"expected_writes.hex",writes)
    print(f"Python vectors generated: {len(PRICES)} ticks; buys={result.compras}; sells={result.ventas}")
if __name__=="__main__": main()
