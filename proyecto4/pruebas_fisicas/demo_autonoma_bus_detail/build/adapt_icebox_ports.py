from pathlib import Path
import re
import sys
raw = Path(sys.argv[1]).read_text()
def header(match):
    ports = [item.strip().split() for item in match[1].split(",")]
    assert all(len(item)==2 for item in ports)
    return ("module chip(" + ", ".join(name for direction, name in ports) + ");\n" +
            "\n".join(f"{direction} {name};" for direction, name in ports))
converted = re.sub(r"module chip\s*\(([^)]*)\);", header, raw, count=1)
Path(sys.argv[2]).write_text(converted)
