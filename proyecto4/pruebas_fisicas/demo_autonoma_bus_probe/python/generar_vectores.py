from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[4]
sys.path.insert(0,str(ROOT/"proyecto4"/"python"))
from enfoques_finales import estrategia_reversion_media
from simulador import simular_estrategia
OUT=Path(__file__).resolve().parents[1]/"data"
PRICES=[200]*10+[90]*3+[220]*3
def emit(path,values): path.write_text("".join(f"{int(v):02x}\n" for v in values),encoding="ascii")
def main():
 OUT.mkdir(parents=True,exist_ok=True)
 result=simular_estrategia(PRICES,"SMA10 bus probe",estrategia_reversion_media)
 emit(OUT/"prices.hex",PRICES)
 emit(OUT/"expected_decisions.hex",[0]+[r["decision_siguiente"] for r in result.decisiones[:-1]])
 emit(OUT/"expected_writes.hex",[r["decision_siguiente"] for r in result.decisiones])
 print(f"Python reference generated: {len(PRICES)} prices")
if __name__=="__main__":main()
