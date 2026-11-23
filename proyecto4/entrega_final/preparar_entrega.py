#!/usr/bin/env python3
"""Build a portable source and evidence archive without copying partial runs."""
from __future__ import annotations

import argparse
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo

ROOT = Path(__file__).resolve().parents[2]
P4 = ROOT / "proyecto4"
DELIVERY = P4 / "entrega_final"
OFFICIAL = "proyecto4/resultados/validacion_oficial"
PHYSICAL = "proyecto4/pruebas_fisicas/demo_autonoma_bus_detail"
IGNORED = {"__pycache__", ".git", "obj_dir"}
SOURCE_EXTENSIONS = {
    ".v", ".sv", ".vh", ".s", ".hex", ".py", ".ps1", ".pcf", ".md",
    ".csv", ".svg", ".txt", ".log", ".pdf", ".png",
}


def include(relative: Path) -> bool:
    parts = relative.parts
    name = relative.as_posix()
    if IGNORED.intersection(parts) or relative.suffix.lower() not in SOURCE_EXTENSIONS:
        return False
    if name.startswith("proyecto4/tests/") and len(parts) > 3:
        return False
    if name.startswith(OFFICIAL + "/"):
        if "corridas" in parts:
            return "ronda_3" in parts and relative.name in {"decisiones.csv", "simulacion.log"}
        return len(parts) == 4 and not relative.name.startswith("verilator")
    if name.startswith("proyecto4/entrega_final/"):
        return relative.parent.as_posix() == "proyecto4/entrega_final"
    if name.startswith("proyecto4/programacion_fisica/"):
        return relative.name in {"generar_bitstream.py", "informe_programacion_fisica.md",
                                 "yosys.log", "nextpnr.log"}
    if name.startswith("proyecto4/pruebas_fisicas/"):
        return "build" not in parts and name.startswith((
            PHYSICAL + "/", "proyecto4/pruebas_fisicas/agente_completo/",
            "proyecto4/pruebas_fisicas/spi_slave/", "proyecto4/pruebas_fisicas/demo_autonoma/",
        ))
    return "build" not in parts and parts[0] in {"rtl", "sw", "tests", "proyecto4"}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=DELIVERY / "Pochoco_Trader_entrega.zip")
    output = parser.parse_args().output.resolve()
    required = [
        "README.md", "REVISION.md", "Makefile", "goboard.pcf", ".gitattributes", "pochoco_soc.svg",
        "proyecto4/.gitignore",
        "proyecto4/programacion_fisica/trade_mmio_base.bin",
        PHYSICAL + "/pc_probe_aprobado.zip",
        PHYSICAL + "/build/timeout_diagnostico.bin",
        PHYSICAL + "/build/timeout_diagnostico_nextpnr.log",
        "proyecto4/entrega_final/informe_final_proyecto4.pdf",
    ]
    if not all((ROOT / name).is_file() for name in required):
        parser.error("Falta al menos un archivo requerido")
    files = {ROOT / name for name in required}
    for tree in ("rtl", "sw", "tests", "proyecto4"):
        files.update(p for p in (ROOT / tree).rglob("*")
                     if p.is_file() and include(p.relative_to(ROOT)))
    files.discard(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    temporary = output.with_suffix(".tmp")
    try:
        with ZipFile(temporary, "w", ZIP_DEFLATED, compresslevel=9) as archive:
            for path in sorted(files):
                entry = ZipInfo(path.relative_to(ROOT).as_posix())
                archive.writestr(entry, path.read_bytes(), ZIP_DEFLATED, compresslevel=9)
        with ZipFile(temporary) as archive:
            corrupt = archive.testzip()
            if corrupt:
                raise RuntimeError(f"Archivo corrupto: {corrupt}")
        temporary.replace(output)
    finally:
        temporary.unlink(missing_ok=True)
    print(f"Entrega: {output} ({len(files)} archivos, {output.stat().st_size} bytes)")


if __name__ == "__main__":
    main()


