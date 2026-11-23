"""Adapt IceStorm's generated port declarations to Icarus.

Use a uniform 1 ps delay on continuous assignments so the scheduler can
settle the reconstructed netlist. This is a functional simulation.
"""
from pathlib import Path
import re
import sys

raw = Path(sys.argv[1]).read_text(encoding="ascii")


def legacy_ports(match):
    ports = [entry.strip().split() for entry in match[1].split(",")]
    names = ", ".join(name for direction, name in ports)
    declarations = "\n".join(f"{direction} {name};" for direction, name in ports)
    return f"module chip({names});\n{declarations}"


converted, count = re.subn(r"module chip\s*\(([^)]*)\);", legacy_ports, raw, count=1)
if count != 1:
    raise ValueError("Missing IceStorm chip module")
converted = re.sub(r"^assign ", "assign #0.001 ", converted, flags=re.M)
Path(sys.argv[2]).write_text("`timescale 1ns/1ps\n" + converted, encoding="ascii")
