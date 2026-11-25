import subprocess
import sys
import tempfile
import unittest
from collections import deque
from pathlib import Path

from capital_protegido import (
    CAJA_PARA_COMPRAR, CANTIDAD, PISO, crear_politica_activa, precios_prueba_reserva,
)
from estrategia import Accion, Decision, estrategia_no_operar
from simulador import ejecutar_decision, leer_precios, simular_estrategia
from test_trade_equivalencia import TradeMachine, words_from_hex

ROOT = Path(__file__).resolve().parents[2]
ASM = ROOT / "proyecto4/pruebas_fisicas/spi_externo_robusto/sw"


class MaquinaMMIO(TradeMachine):
    def __init__(self, words):
        super().__init__(words)
        self.ventana = deque(maxlen=10)

    def one_tick(self, price, max_instructions=20000):
        self.ventana.append(price)
        return super().one_tick(price, max_instructions)

    def load_word(self, address):
        if address == 0x8001000C:
            return sum(self.ventana)
        if address == 0x80010010:
            return int(len(self.ventana) == 10)
        return super().load_word(address)


class CapitalProtegidoTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.words = {}
        with tempfile.TemporaryDirectory(prefix="capital-p4-") as tmp:
            for modo in ("conservar", "activo"):
                out = Path(tmp) / f"{modo}.hex"
                subprocess.run([sys.executable, "-B", str(ROOT / "sw/assembler.py"),
                                str(ASM / f"{modo}.s"), "-o", str(out)],
                               cwd=ROOT, check=True, capture_output=True, text=True)
                cls.words[modo] = words_from_hex(out)

    def cotejar(self, precios, modo):
        politica = crear_politica_activa() if modo == "activo" else estrategia_no_operar
        referencia = simular_estrategia(precios, modo, politica)
        cpu = MaquinaMMIO(self.words[modo])
        for precio, tick in zip(precios, referencia.decisiones, strict=True):
            recibido, _ = cpu.one_tick(precio)
            esperado = (tick["decision_recibida"], tick["decision_siguiente"])
            self.assertEqual((recibido, cpu.tx_hold), esperado, f"tick {tick['tick']}")
            if modo == "activo":
                self.assertEqual(cpu.reg[15], tick["caja"], f"caja tick {tick['tick']}")
                self.assertEqual(cpu.reg[5], tick["acciones"], f"acciones tick {tick['tick']}")
        return referencia

    def test_hex_conservar_20000(self):
        r = self.cotejar(leer_precios(), "conservar")
        self.assertEqual(set(r.patrimonios), {10000})
        self.assertEqual(r.metricas.ordenes, 0)

    def test_hex_activo_20000(self):
        r = self.cotejar(leer_precios(), "activo")
        self.assertEqual(r.metricas.patrimonio_final, 10224)
        self.assertEqual(r.metricas.ordenes, 2)
        self.assertGreaterEqual(min(r.patrimonios), PISO)

    def test_hex_activo_peor_compra_venta_y_bloqueo(self):
        r = self.cotejar(precios_prueba_reserva(), "activo")
        self.assertEqual(r.decisiones[65]["decision_recibida"], 0x43)
        self.assertEqual(r.decisiones[129]["decision_recibida"], 0x83)
        self.assertEqual(r.decisiones[193]["decision_recibida"], 0)
        self.assertEqual(r.metricas.caja_final, 9228)
        self.assertEqual(r.metricas.ordenes, 2)

    def test_reserva_cubre_los_65025_pares_de_precios(self):
        compra = Decision(Accion.COMPRAR, CANTIDAD)
        venta = Decision(Accion.VENDER, CANTIDAD)
        for p_compra in range(1, 256):
            fill = ejecutar_decision(CAJA_PARA_COMPRAR, 0, compra, p_compra)
            self.assertEqual(fill.acciones, CANTIDAD)
            self.assertGreaterEqual(fill.caja, PISO)
            for p_venta in range(1, 256):
                cerrado = ejecutar_decision(fill.caja, fill.acciones, venta, p_venta)
                self.assertGreaterEqual(cerrado.caja, PISO)
                self.assertEqual(cerrado.acciones, 0)
