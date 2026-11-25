"""Relaciona Assembly, HEX y BIN mediante archivos de síntesis. Sin acceso USB."""

import csv
import argparse
import json
from hashlib import sha256
from pathlib import Path
import shutil
from subprocess import PIPE, STDOUT, run
import sys
from tempfile import TemporaryDirectory

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
P4 = ROOT / "proyecto4"
ROBUSTO = P4 / "pruebas_fisicas/spi_externo_robusto"
MMIO = P4 / "alternativas/mmio_sma10"
FISICA = P4 / "programacion_fisica"
COMPETENCIA = P4 / "pruebas_fisicas/demo_autonoma_bus_detail/build/competition"


def ejecutar(command, log):
    run_result = run(command, cwd=ROOT, stdout=PIPE, stderr=STDOUT)
    log.write_bytes(run_result.stdout)
    if run_result.returncode:
        raise RuntimeError(f"Fallo de {command[0]} en {log}: {run_result.stdout[-1600:].decode(errors='replace')}")


def huella(path):
    return sha256(path.read_bytes()).hexdigest().upper()


def simular_conservar_desde_bin(scratch):
    carpeta = scratch / "vectores"
    carpeta.mkdir()
    for nombre in ("precios.hex", "miso.hex", "escrituras.hex"):
        origen = HERE / "conservar/F_recuperacion" / nombre
        filas = origen.read_text(encoding="ascii").splitlines()[:70]
        (carpeta/nombre).write_text("\n".join(filas)+"\n", encoding="ascii")
    orig = ROBUSTO / "build_conservar/trade_conservar.bin"
    asc = scratch / "unpack.asc"
    netlist = scratch / "unpack.v"
    vvp = scratch / "unpack.vvp"
    ejecutar(["iceunpack", orig, asc], HERE/"bitstream_conservar_iceunpack.log")
    with netlist.open("wb") as stream:
        run(["icebox_vlog", "-d", "vq100", "-p", ROBUSTO/"goboard_spi_externo.pcf",
             "-c", "-n", "trade_spi_externo", asc], cwd=ROOT, stdout=stream, check=True)
    cells = Path(shutil.which("yosys")).resolve().parents[1] / "share/yosys/ice40/cells_sim.v"
    ejecutar(["iverilog", "-g2012", "-DNETLIST", "-s", "tb_trade_spi_externo",
              "-Ptb_trade_spi_externo.TICKS=70", "-Ptb_trade_spi_externo.PERIODO_NS=40000",
              "-o", vvp, ROBUSTO/"tb_trade_spi_externo.sv", netlist, cells],
             HERE/"bitstream_conservar_compilacion_vq100.log")
    log = HERE/"bitstream_conservar_simulacion.log"
    ejecutar(["vvp", "-n", vvp, f"+vectores={carpeta.as_posix()}"], log)
    if "PASS 70 MISO frente a Python" not in log.read_text(encoding="utf-8"):
        raise RuntimeError("La simulación del BIN no produjo su marca PASS")
    print("PASS Conservar reconstruido desde el BIN: 70 MISO iguales y LED 0111")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--netlist", action="store_true",
                        help="desempaquetar Conservar y simular el escenario F tras diagnosticar.py")
    args = parser.parse_args()
    entradas = (
        ("mmio_base", MMIO/"sw/trade.s", MMIO/"sw/trade.hex",
         FISICA/"trade_mmio_base.asc", FISICA/"trade_mmio_base.bin", None),
        ("competition_original", MMIO/"sw/trade.s", MMIO/"sw/trade.hex",
         COMPETENCIA/"competition.asc", COMPETENCIA/"competition.bin", None),
        ("spi_externo_base", MMIO/"sw/trade.s", MMIO/"sw/trade.hex",
         ROBUSTO/"build/trade.asc", ROBUSTO/"build/trade_spi_externo.bin", ROBUSTO/"build/resultados.json"),
        ("conservar", ROBUSTO/"sw/conservar.s", ROBUSTO/"build_conservar/trade.hex",
         ROBUSTO/"build_conservar/trade.asc", ROBUSTO/"build_conservar/trade_conservar.bin",
         ROBUSTO/"build_conservar/resultados.json"),
        ("activo", ROBUSTO/"sw/activo.s", ROBUSTO/"build_activo/trade.hex",
         ROBUSTO/"build_activo/trade.asc", ROBUSTO/"build_activo/trade_activo.bin",
         ROBUSTO/"build_activo/resultados.json"),
    )
    icepack = shutil.which("icepack")
    if not icepack:
        raise SystemExit("Falta icepack en PATH")
    with TemporaryDirectory(prefix="p4-sha-") as scratch, (
        HERE / "huellas_compiladas.csv"
    ).open("w", encoding="utf-8", newline="") as stream:
        writer = csv.writer(stream)
        writer.writerow(("modo", "palabras", "fuente_s", "sha256_s", "ruta_hex", "sha256_hex",
                         "ruta_asc", "sha256_asc", "ruta_bin", "sha256_bin", "bin_bytes"))
        for modo, fuente, hex_file, asc, binary, metadata in entradas:
            rehex = Path(scratch) / f"{modo}.hex"
            repacked = Path(scratch) / f"{modo}.bin"
            ejecutar([sys.executable, "-B", ROOT/"sw/assembler.py", fuente, "-o", rehex],
                     HERE/f"ensamblar_{modo}.log")
            if rehex.read_text(encoding="ascii").split() != hex_file.read_text(encoding="ascii").split():
                raise RuntimeError(f"El HEX guardado difiere para {modo}")
            ejecutar([icepack, asc, repacked], HERE/f"empacar_{modo}.log")
            if repacked.read_bytes() != binary.read_bytes():
                raise RuntimeError(f"El ASC guardado no reproduce el BIN para {modo}")
            words = hex_file.read_text(encoding="ascii").split()
            if metadata:
                result = json.loads(metadata.read_text(encoding="utf-8"))
                if result["sha256"] != huella(binary) or (
                    result.get("palabras_firmware", len(words)) != len(words)
                ):
                    raise RuntimeError(f"Manifiesto inesperado para {modo}")
            if modo == "conservar":
                stores = [int(word, 16) for word in words if int(word, 16) & 0x7F == 0x23]
                if stores != [0x0000A423]:
                    raise RuntimeError("Se esperaba una sola escritura literal SW x0, 8(x1)")
            print(f"PASS {modo}: {len(words)} palabras, BIN SHA-256 {huella(binary)}")
            writer.writerow((modo, len(words), fuente.relative_to(ROOT).as_posix(), huella(fuente),
                             hex_file.relative_to(ROOT).as_posix(), huella(hex_file),
                             asc.relative_to(ROOT).as_posix(), huella(asc),
                             binary.relative_to(ROOT).as_posix(), huella(binary), binary.stat().st_size))
        if args.netlist:
            simular_conservar_desde_bin(Path(scratch))


if __name__ == "__main__":
    main()
