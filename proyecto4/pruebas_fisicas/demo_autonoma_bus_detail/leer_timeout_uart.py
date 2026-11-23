"""Read the Go Board's last Espino commit through its USB UART."""
import argparse
from pathlib import Path
import struct
import subprocess
import sys
import time

import serial


def firmware_words() -> list[int]:
    firmware = (Path(__file__).resolve().parents[2] /
                "alternativas/mmio_sma10/sw/trade.hex")
    return [int(word, 16) for word in firmware.read_text(encoding="ascii").split()]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", default="COM10")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--contexto", action="store_true")
    mode.add_argument("--arranque", action="store_true")
    mode.add_argument("--fetch", action="store_true")
    mode.add_argument("--autotest", action="store_true")
    parser.add_argument("--bin", type=Path)
    args = parser.parse_args()
    name = ("selftest_fetch_rom_lento.bin" if args.autotest else
            "timeout_fetch.bin" if args.fetch else
            "timeout_arranque.bin" if args.arranque else
            "timeout_contexto.bin" if args.contexto else "timeout_uart.bin")
    image = args.bin or (Path(__file__).parent / "build" / name)
    with serial.Serial(args.port, 115200, timeout=0.1) as port:
        port.reset_input_buffer()
        # Verify the flash and release hardware reset. The port must already
        # be open because the report starts within a millisecond.
        check = subprocess.run(
            ["iceprog", "-c", str(image.resolve())],
            capture_output=True, text=True, timeout=15,
        )
        if check.returncode:
            sys.exit(check.stderr.strip() or check.stdout.strip() or "Flash verify failed")
        data = bytearray()
        expires = time.monotonic() + 5
        while time.monotonic() < expires:
            data.extend(port.read(64))
            if args.autotest:
                terminal = next((byte for byte in data if 0xAA <= byte <= 0xAF), None)
                if terminal is not None:
                    code = terminal & 0xF
                    result = ("PASS", "PRECIO", "DECISION", "MISO", "SECUENCIA", "WATCHDOG")[code - 10]
                    print(f"AUTOTEST LED={code:04b} UART=0x{terminal:02X} RESULT={result}")
                    if code != 10:
                        sys.exit(2)
                    return
                continue
            if args.fetch:
                start = next((i for i, byte in enumerate(data)
                              if byte & 0xFE == 0xB4), -1)
                if start >= 0 and len(data) >= start + 5:
                    word, = struct.unpack_from("<I", data, start + 1)
                    words = firmware_words()
                    expected = words[0x1C // 4]
                    addresses = ",".join(f"0x{i * 4:X}" for i, value in enumerate(words)
                                         if word == value) or "ninguna"
                    early_exit = data[start] & 1
                    print(f"FETCH PC_ID=0x0000001C WORD=0x{word:08X} "
                          f"EXPECTED=0x{expected:08X} XOR=0x{word ^ expected:08X} "
                          f"MATCH_PC={addresses} EARLY_EXIT={early_exit}")
                    return
                continue
            if args.arranque:
                flags = next((byte for byte in data if byte & 0x80), None)
                if flags is not None:
                    status_new = (flags >> 6) & 1
                    rs1_zero = (flags >> 5) & 1
                    rs2_zero = (flags >> 4) & 1
                    instruction_ok = (flags >> 3) & 1
                    branch_taken = (flags >> 2) & 1
                    pc_set = (flags >> 1) & 1
                    next_committed_poll = flags & 1
                    print("ARRANQUE PC_ID=0x0000001C "
                          f"RS1_ZERO={rs1_zero} RS2_ZERO={rs2_zero} "
                          f"STATUS_NEW={status_new} INSN_OK={instruction_ok} "
                          f"BRANCH_TAKEN={branch_taken} PC_SET={pc_set} "
                          f"NEXT_COMMIT_0X14={next_committed_poll}")
                    return
                continue
            if args.contexto:
                start = next((i for i, byte in enumerate(data)
                              if byte & 0xE0 == 0xC0), -1)
            else:
                start = data.find(b"\xa5")
            if start >= 0 and len(data) >= start + 9:
                pc, word = struct.unpack_from("<II", data, start + 1)
                if args.contexto:
                    header = data[start]
                    state = "DONE" if header & 0x10 else "WAIT_ACK"
                    branch_taken = pc & 1
                    print(f"TIMEOUT={state} TICK={(header & 0xF) + 1} "
                          f"PC_ID=0x{pc & ~1:08X} RS1_VALUE=0x{word:08X} "
                          f"BRANCH_TAKEN={branch_taken}")
                    return
                print(f"PC_ID=0x{pc:08X} INSN=0x{word:08X}")
                words = firmware_words()
                if pc % 4:
                    print("PC_ID no alineado a 4 bytes")
                elif pc // 4 >= len(words):
                    print(f"PC_ID fuera del firmware ({len(words)} palabras)")
                else:
                    expected = words[pc // 4]
                    print(f"Firmware en ese PC: 0x{expected:08X}, coincide={word == expected}")
                return
        sys.exit(f"No UART timeout record. Received {data.hex(' ') or 'no bytes'}")


if __name__ == "__main__":
    main()



