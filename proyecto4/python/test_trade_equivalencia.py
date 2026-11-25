"""Equivalencia tick a tick del HEX RV32E contra la estrategia Python.

La serie completa se verifica ejecutando las palabras ensambladas en un
intérprete RV32E del subconjunto usado por trade.s. Un segundo caso corto pasa
por el SoC RTL/Icarus e incluye fills parciales por caja insuficiente.
"""

import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

from enfoques_finales import estrategia_reversion_media
from simulador import leer_precios, simular_estrategia


ROOT = Path(__file__).resolve().parents[2]
TRADE_HEX = ROOT / "proyecto4" / "sw" / "trade.hex"
RTL_DIR = ROOT / "rtl"
RAM_MODEL = ROOT / "tests" / "ram_model.v"
TB_RTL = ROOT / "proyecto4" / "tb" / "tb_trade_equivalencia.sv"


def u32(value: int) -> int:
    return value & 0xFFFFFFFF


def s32(value: int) -> int:
    value &= 0xFFFFFFFF
    return value - 0x100000000 if value & 0x80000000 else value


def sext(value: int, bits: int) -> int:
    sign = 1 << (bits - 1)
    return (value ^ sign) - sign


def words_from_hex(path: Path) -> list[int]:
    return [int(line, 16) for line in path.read_text(encoding="ascii").splitlines() if line.strip()]


class TradeMachine:
    """Functional RV32E interpreter for the exact opcodes emitted by trade.s."""

    def __init__(self, words: list[int]):
        if len(words) >= 500:
            raise AssertionError("trade.hex overlaps the reserved history buffer at RAM word 500")
        self.code = words
        self.mem = [0] * 512
        self.mem[:len(words)] = words
        self.reg = [0] * 16
        self.pc = 0
        self.price = 0
        self.new_price = 0
        self.tx_hold = 0
        self.stores_decision = 0

    def load_word(self, address: int) -> int:
        address = u32(address)
        if address == 0x80010000:
            return self.new_price  # CS is inactive when the CPU polls.
        if address == 0x80010004:
            self.new_price = 0
            return self.price
        if address & 0x80000000:
            return 0
        if address & 3 or address >= 2048:
            raise AssertionError(f"LW fuera de RAM/MMIO alineado: 0x{address:08x}")
        return self.mem[address >> 2]

    def store_word(self, address: int, value: int) -> bool:
        address, value = u32(address), u32(value)
        if address == 0x80010008:
            self.tx_hold = value & 0xFF
            self.stores_decision += 1
            return True
        if address & 0x80000000:
            return False
        if address & 3 or address >= 2048:
            raise AssertionError(f"SW fuera de RAM/MMIO alineado: 0x{address:08x}")
        self.mem[address >> 2] = value
        return False

    def step(self) -> bool:
        if self.pc & 3 or self.pc // 4 >= len(self.code):
            raise AssertionError(f"PC fuera de trade.hex: 0x{self.pc:08x}")
        insn = self.code[self.pc >> 2]
        old_pc = self.pc
        next_pc = u32(old_pc + 4)
        opcode = insn & 0x7F
        rd = (insn >> 7) & 0x1F
        funct3 = (insn >> 12) & 7
        rs1 = (insn >> 15) & 0x1F
        rs2 = (insn >> 20) & 0x1F
        funct7 = (insn >> 25) & 0x7F
        event = False

        if opcode == 0x37:  # LUI
            self.reg[rd] = u32(insn & 0xFFFFF000)
        elif opcode == 0x13:  # OP-IMM
            if rs1 > 15 or rd > 15:
                raise AssertionError("Registro fuera de RV32E en OP-IMM")
            imm = sext(insn >> 20, 12)
            if funct3 == 0:  # ADDI
                value = self.reg[rs1] + imm
            elif funct3 == 7:  # ANDI
                value = self.reg[rs1] & u32(imm)
            else:
                raise AssertionError(f"OP-IMM no soportada funct3={funct3}")
            self.reg[rd] = u32(value)
        elif opcode == 0x33:  # OP
            if rd > 15 or rs1 > 15 or rs2 > 15:
                raise AssertionError("Registro fuera de RV32E en OP")
            if funct3 == 0 and funct7 == 0:
                self.reg[rd] = u32(self.reg[rs1] + self.reg[rs2])
            elif funct3 == 0 and funct7 == 0x20:
                self.reg[rd] = u32(self.reg[rs1] - self.reg[rs2])
            else:
                raise AssertionError(f"OP no soportada funct3={funct3} funct7={funct7}")
        elif opcode == 0x03:  # LW
            if rs1 > 15 or rd > 15 or funct3 != 2:
                raise AssertionError("LOAD no soportado o registro fuera de RV32E")
            address = self.reg[rs1] + sext(insn >> 20, 12)
            self.reg[rd] = self.load_word(address)
        elif opcode == 0x23:  # SW
            if rs1 > 15 or rs2 > 15 or funct3 != 2:
                raise AssertionError("STORE no soportado o registro fuera de RV32E")
            imm = ((insn >> 25) << 5) | ((insn >> 7) & 0x1F)
            address = self.reg[rs1] + sext(imm, 12)
            event = self.store_word(address, self.reg[rs2])
        elif opcode == 0x63:  # conditional branches
            if rs1 > 15 or rs2 > 15:
                raise AssertionError("Registro fuera de RV32E en branch")
            imm = (((insn >> 31) & 1) << 12) | (((insn >> 7) & 1) << 11)
            imm |= (((insn >> 25) & 0x3F) << 5) | (((insn >> 8) & 0xF) << 1)
            offset = sext(imm, 13)
            a, b = self.reg[rs1], self.reg[rs2]
            taken = (
                (funct3 == 0 and a == b)
                or (funct3 == 1 and a != b)
                or (funct3 == 4 and s32(a) < s32(b))
                or (funct3 == 5 and s32(a) >= s32(b))
            )
            if funct3 not in (0, 1, 4, 5):
                raise AssertionError(f"Branch no soportado funct3={funct3}")
            if taken:
                next_pc = u32(old_pc + offset)
        elif opcode == 0x6F:  # JAL
            if rd > 15:
                raise AssertionError("Registro fuera de RV32E en JAL")
            imm = (((insn >> 31) & 1) << 20) | (((insn >> 12) & 0xFF) << 12)
            imm |= (((insn >> 20) & 1) << 11) | (((insn >> 21) & 0x3FF) << 1)
            self.reg[rd] = next_pc
            next_pc = u32(old_pc + sext(imm, 21))
        else:
            raise AssertionError(f"Opcode no implementado: 0x{opcode:02x} en PC 0x{old_pc:08x}")

        self.reg[0] = 0
        self.pc = next_pc
        return event

    def one_tick(self, price: int, max_instructions: int = 20000) -> tuple[int, int]:
        received = self.tx_hold
        self.price = price
        self.new_price = 1
        for instructions in range(1, max_instructions + 1):
            if self.step():
                if self.new_price:
                    raise AssertionError("trade.s escribio DECISION antes de leer PRICE")
                return received, instructions
        raise AssertionError("Timeout esperando escritura de DECISION")


def assert_hex_matches_python(prices: list[int]) -> tuple[int, int, int]:
    reference = simular_estrategia(prices, "Python SMA10", estrategia_reversion_media)
    cpu = TradeMachine(words_from_hex(TRADE_HEX))
    fills_buy, fills_sell, max_steps = 0, 0, 0
    for tick, price in enumerate(prices):
        expected = reference.decisiones[tick]
        received, steps = cpu.one_tick(price)
        max_steps = max(max_steps, steps)
        if received != expected["decision_recibida"]:
            raise AssertionError(
                f"Tick {tick}: HEX transmitio 0x{received:02x}; Python esperaba "
                f"0x{expected['decision_recibida']:02x}"
            )
        if cpu.tx_hold != expected["decision_siguiente"]:
            raise AssertionError(
                f"Tick {tick}: HEX calculo 0x{cpu.tx_hold:02x}; Python esperaba "
                f"0x{expected['decision_siguiente']:02x}"
            )
        if expected["accion_siguiente"] == "comprar":
            fills_buy += 1
        if expected["accion_siguiente"] == "vender":
            fills_sell += 1
    return fills_buy, fills_sell, max_steps


class TradeEquivalenciaTests(unittest.TestCase):
    def test_hex_igual_a_python_tick_a_tick_en_los_20000_precios(self):
        prices = leer_precios()
        buys, sells, max_steps = assert_hex_matches_python(prices)
        self.assertGreater(buys, 0)
        self.assertGreater(sells, 0)
        self.assertLess(max_steps, 1000)

    def test_hex_iguala_fills_parciales_en_caja_insuficiente(self):
        prices = [200] * 10 + [90, 255] * 20
        result = simular_estrategia(prices, "Python partial", estrategia_reversion_media)
        self.assertTrue(any(
            op["tipo"] == "comprar" and op["cantidad_ejecutada"] < 16
            for op in result.operaciones
        ))
        buys, sells, _ = assert_hex_matches_python(prices)
        self.assertGreater(buys, 0)
        self.assertGreater(sells, 0)

    @unittest.skipUnless(shutil.which("iverilog") and shutil.which("vvp"), "Icarus Verilog no disponible")
    def test_integracion_rtl_spi_con_decisiones_python(self):
        prices = [200] * 10 + [90, 255] * 10
        result = simular_estrategia(prices, "RTL SMA10", estrategia_reversion_media)
        vector_dir = ROOT / "proyecto4" / "tests"
        vector_dir.mkdir(parents=True, exist_ok=True)
        price_path = vector_dir / "trade_prices.hex"
        expected_path = vector_dir / "trade_expected.hex"
        try:
            price_path.write_text("".join(f"{p:02x}\n" for p in prices), encoding="ascii")
            expected_path.write_text(
                "".join(f"{int(row['decision_recibida']):02x}\n" for row in result.decisiones),
                encoding="ascii",
            )
            rtl = [str(path) for path in RTL_DIR.rglob("*.v")]
            with tempfile.TemporaryDirectory(prefix="trade-rtl-") as tmp:
                out = Path(tmp) / "tb_trade.vvp"
                compile_cmd = [
                    shutil.which("iverilog"), "-g2012", "-s", "tb_trade_equivalencia", "-o", str(out),
                    *rtl, str(RAM_MODEL), str(TB_RTL),
                ]
                subprocess.run(compile_cmd, cwd=ROOT, check=True, capture_output=True, text=True)
                completed = subprocess.run(
                    [shutil.which("vvp"), str(out), f"+TICKS={len(prices)}",
                     "+PRICE_FILE=proyecto4/tests/trade_prices.hex",
                     "+EXPECTED_FILE=proyecto4/tests/trade_expected.hex"],
                    cwd=ROOT, check=True, capture_output=True, text=True,
                )
                self.assertIn("PASS trade RTL/Python", completed.stdout)
        finally:
            price_path.unlink(missing_ok=True)
            expected_path.unlink(missing_ok=True)


if __name__ == "__main__":
    unittest.main()
