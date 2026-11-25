"""Check that trade.hex fits the autonomous demo's word-addressed fetch."""
import argparse
from pathlib import Path


def signed(value: int, width: int) -> int:
    return value - (1 << width) if value >> (width - 1) else value


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--firmware", type=Path)
    args = parser.parse_args()
    firmware = args.firmware or (Path(__file__).resolve().parents[2] /
                                 "alternativas/mmio_sma10/sw/trade.hex")
    words = [int(token, 16) for token in firmware.read_text(encoding="ascii").split()]
    if not 2 <= len(words) <= 512 or words[-1] & 0x7F != 0x6F:
        raise SystemExit("Expected a 2–512 word firmware ending in JAL")
    if args.firmware is None and len(words) != 71:
        raise SystemExit("Expected the original 71-word trade firmware")

    transfers = 0
    for index, insn in enumerate(words):
        opcode = insn & 0x7F
        if opcode == 0x63:
            encoded = ((insn >> 31) << 12) | (((insn >> 7) & 1) << 11)
            encoded |= (((insn >> 25) & 0x3F) << 5) | (((insn >> 8) & 0xF) << 1)
            offset = signed(encoded, 13)
        elif opcode == 0x6F:
            encoded = ((insn >> 31) << 20) | (((insn >> 12) & 0xFF) << 12)
            encoded |= (((insn >> 20) & 1) << 11) | (((insn >> 21) & 0x3FF) << 1)
            offset = signed(encoded, 21)
        elif opcode == 0x67:
            raise SystemExit(f"Indirect jump not allowed in demo ROM at 0x{index * 4:X}")
        else:
            continue
        target = 4 * index + offset
        if target % 4 or not 0 <= target < 4 * len(words):
            raise SystemExit(f"Invalid control target at 0x{index * 4:X}: {target}")
        transfers += 1

    print(f"PASS ROM fetch range: {transfers} aligned transfers inside 0x000..0x{4*(len(words)-1):03X}")


if __name__ == "__main__":
    main()
