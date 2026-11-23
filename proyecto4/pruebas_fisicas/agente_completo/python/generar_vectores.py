"""Genera precios de prueba y respuestas SPI esperadas desde la estrategia Python."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "proyecto4" / "python"))
from simulador import simular_estrategia
from enfoques_finales import estrategia_reversion_media

OUT = Path(__file__).resolve().parents[1] / "data"
prices = [200] * 10 + [90] * 3 + [220] * 3
result = simular_estrategia(prices, "SMA10", estrategia_reversion_media)
OUT.mkdir(parents=True, exist_ok=True)
(OUT / "prices.hex").write_text("".join(f"{p:02x}\n" for p in prices), encoding="ascii")
(OUT / "expected_decisions.hex").write_text(
    "".join(f"{int(row['decision_recibida']):02x}\n" for row in result.decisiones), encoding="ascii"
)
(OUT / "expected_writes.hex").write_text(
    "".join(f"{int(row['decision_siguiente']):02x}\n" for row in result.decisiones), encoding="ascii"
)
print(f"Precios={len(prices)}; compras={result.compras}; ventas={result.ventas}; órdenes={result.metricas.ordenes}")
