import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
ASSEMBLER = ROOT / "proyecto4" / "sw" / "assembler.py"
spec = importlib.util.spec_from_file_location("p4_assembler", ASSEMBLER)
assembler = importlib.util.module_from_spec(spec)
spec.loader.exec_module(assembler)


class Custom0AssemblerTests(unittest.TestCase):
    def test_smaupd_encoding(self):
        word = assembler.ensamblar("smaupd x10, x11, x3\n")[0]
        expected = (3 << 20) | (11 << 15) | (10 << 7) | 0x0B
        self.assertEqual(word, expected)

    def test_standard_add_encoding_unchanged(self):
        word = assembler.ensamblar("add x10, x11, x3\n")[0]
        expected = (3 << 20) | (11 << 15) | (10 << 7) | 0x33
        self.assertEqual(word, expected)

    def test_rejects_non_rv32e_and_shift(self):
        with self.assertRaises(ValueError):
            assembler.ensamblar("smaupd x16, x1, x2\n")
        with self.assertRaises(ValueError):
            assembler.ensamblar("slli x1, x2, 1\n")


if __name__ == "__main__":
    unittest.main()
