"""Physical UART echo check for Go Board FTDI channel, default COM10."""
import argparse
import sys
import time

try:
    import serial
except ImportError:
    print("FAIL: falta pyserial. Instale con: python -m pip install pyserial", file=sys.stderr)
    raise SystemExit(2)

BYTES = bytes((0x41, 0x42, 0x43, 0x55, 0xAA))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", default="COM10")
    parser.add_argument("--timeout", type=float, default=2.0)
    args = parser.parse_args()
    print(f"UART echo {args.port} @115200 8N1; TX -> FPGA RX, FPGA TX -> PC RX")
    try:
        with serial.Serial(args.port, 115200, bytesize=serial.EIGHTBITS,
                           parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE,
                           timeout=args.timeout, write_timeout=args.timeout,
                           xonxoff=False, rtscts=False, dsrdtr=False) as port:
            time.sleep(0.1)
            port.reset_input_buffer()
            for index, sent in enumerate(BYTES):
                port.write(bytes((sent,)))
                port.flush()
                received = port.read(1)
                if len(received) != 1:
                    print(f"FAIL byte {index}: timeout; enviado={sent:02X}")
                    return 1
                if received[0] != sent:
                    print(f"FAIL byte {index}: enviado={sent:02X}, recibido={received[0]:02X}")
                    return 1
                print(f"PASS byte {index}: TX={sent:02X} RX={received[0]:02X}")
        print("PASS UART: 5/5 bytes recibidos sin discrepancias")
        return 0
    except (serial.SerialException, OSError) as exc:
        print(f"FAIL UART {args.port}: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
