"""Check the 16-tick selftest vectors and official round 3 against Python."""
import csv
import sys
from pathlib import Path

root = Path(__file__).resolve().parents[3]
project = root / "proyecto4"
sys.path.insert(0, str(project / "python"))
from simulador import leer_precios, simular_estrategia
from enfoques_finales import estrategia_reversion_media

fixture = Path(__file__).resolve().parent / "data"


def read_hex(name: str) -> list[int]:
    return [int(word, 16) for word in (fixture / name).read_text().split()]


local_prices = read_hex("prices.hex")
local = simular_estrategia(local_prices, "SMA10", estrategia_reversion_media)
local_writes = [row["decision_siguiente"] for row in local.decisiones]
local_miso = [row["decision_recibida"] for row in local.decisiones]
assert len(local_prices) == len(local_writes) == len(local_miso) == 16
assert local_writes == read_hex("expected_writes.hex"), "DECISION fixture differs from Python"
assert local_miso == read_hex("expected_decisions.hex"), "MISO fixture differs from Python"
print("selftest: 16 DECISION and 16 MISO reference bytes regenerated from Python, 0 differences")

prices = leer_precios()
reference = simular_estrategia(prices, "SMA10", estrategia_reversion_media)
expected = [(i, price, row["decision_recibida"])
            for i, (price, row) in enumerate(zip(prices, reference.decisiones))]
for variant in ("mmio_sma10_base", "software_original"):
    path = project / "resultados/validacion_oficial/corridas" / variant / "ronda_3/decisiones.csv"
    with path.open(newline="") as stream:
        got = [(int(row["tick"]), int(row["precio"]), int(row["decision"], 16))
               for row in csv.DictReader(stream)]
    assert len(got) == len(expected) == 20000
    differences = sum(a != b for a, b in zip(got, expected))
    print(f"{variant}: {len(got)} ticks, {differences} differences vs Python")
    assert differences == 0

