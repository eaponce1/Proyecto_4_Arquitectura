"""Generate deterministic expected decisions from the shared Python reference."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "proyecto4" / "python"))

from enfoques_finales import estrategia_reversion_media
from simulador import simular_estrategia

OUT = Path(__file__).resolve().parents[1] / "data"
PRICES = [200] * 10 + [90] * 3 + [220] * 3

def write_hex(path: Path, values: list[int]) -> None:
    path.write_text("".join(f"{value:02x}\n" for value in values), encoding="ascii")

def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    result = simular_estrategia(PRICES, "SMA10 Python", estrategia_reversion_media)
    miso = [0] + [row["decision_siguiente"] for row in result.decisiones[:-1]]
    writes = [row["decision_siguiente"] for row in result.decisiones]
    write_hex(OUT / "prices.hex", PRICES)
    write_hex(OUT / "expected_decisions.hex", miso)
    write_hex(OUT / "expected_writes.hex", writes)
    print(f"Python vectors: ticks={len(PRICES)} buys={result.compras} sells={result.ventas}")

if __name__ == "__main__":
    main()
