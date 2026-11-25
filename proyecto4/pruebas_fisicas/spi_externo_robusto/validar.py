"""Simula y construye el candidato SPI externo en HX1K, sin programar la placa."""

import argparse
from concurrent.futures import ThreadPoolExecutor
from hashlib import sha256
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
DEMO = HERE.parent / "demo_autonoma_bus_detail"
MMIO = ROOT / "proyecto4/alternativas/mmio_sma10"
SERIE = ROOT / "proyecto4/resultados/validacion_oficial/practica_meta.csv"
sys.path.insert(0, str(ROOT / "proyecto4/python"))
from enfoques_finales import estrategia_reversion_media
from capital_protegido import crear_politica_activa, precios_prueba_reserva
from estrategia import estrategia_no_operar
from simulador import leer_precios, simular_estrategia


def ejecutar(cmd, log: Path) -> str:
    run = subprocess.run(cmd, cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                         text=True, encoding="utf-8", errors="replace")
    log.write_text(run.stdout, encoding="utf-8")
    if run.returncode:
        raise SystemExit(f"FAIL ({run.returncode}): {log}\n" + "\n".join(run.stdout.splitlines()[-12:]))
    return run.stdout


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--serie", type=Path, default=SERIE)
    parser.add_argument("--modo", choices=("base", "conservar", "activo"), default="base")
    parser.add_argument("--salida", type=Path)
    args = parser.parse_args()
    default_dir = "build" if args.modo == "base" else f"build_{args.modo}"
    out = (args.salida or HERE / default_dir).resolve()
    out.mkdir(parents=True, exist_ok=True)
    bin_name = "trade_spi_externo.bin" if args.modo == "base" else f"trade_{args.modo}.bin"
    binary = out / bin_name
    if any(out.glob("*.bin")):
        raise SystemExit("La salida ya contiene un BIN. Indica otro directorio con --salida.")
    tools = {name: shutil.which(name) for name in ("iverilog", "vvp", "yosys", "nextpnr-ice40", "icepack")}
    if missing := [name for name, path in tools.items() if not path]:
        raise SystemExit(f"Faltan herramientas: {', '.join(missing)}")
    cells = Path(tools["yosys"]).resolve().parents[1] / "share/yosys/ice40/cells_sim.v"
    if not cells.is_file():
        raise SystemExit(f"Falta el modelo de primitivas: {cells}")
    firmware = MMIO/"sw/trade.hex"
    rom_args = []
    if args.modo != "base":
        firmware = out/"trade.hex"
        ejecutar([sys.executable, "-B", ROOT/"sw/assembler.py", HERE/f"sw/{args.modo}.s",
                  "-o", firmware], out/"assembler.log")
        rom_args = ["--firmware", firmware]
    ejecutar([sys.executable, "-B", DEMO/"verificar_pc_rom.py", *rom_args], out/"alcance_rom.log")
    words = len(firmware.read_text(encoding="ascii").split())
    firmware_parameter = firmware.as_posix()
    if firmware.is_relative_to(ROOT):
        firmware_parameter = firmware.relative_to(ROOT).as_posix()

    def preparar_vectores(precios, carpeta):
        politica = {"base": estrategia_reversion_media, "conservar": estrategia_no_operar,
                    "activo": crear_politica_activa()}[args.modo]
        referencia = simular_estrategia(precios, args.modo, politica)
        vectores = {
            "precios": precios,
            "miso": [r["decision_recibida"] for r in referencia.decisiones],
            "escrituras": [r["decision_siguiente"] for r in referencia.decisiones],
        }
        carpeta.mkdir(exist_ok=True)
        for name, valores in vectores.items():
            (carpeta/f"{name}.hex").write_text("".join(f"{v:02x}\n" for v in valores), encoding="ascii")
        return referencia

    serie = leer_precios(args.serie)
    preparar_vectores(serie[:2000], out)
    stress = out / "reserva"
    stress_ticks = 0
    if args.modo == "activo":
        precios = precios_prueba_reserva()
        stress_ticks = len(precios)
        ref = preparar_vectores(precios, stress)
        if (ref.decisiones[65]["decision_recibida"] != 0x43
                or ref.decisiones[129]["decision_recibida"] != 0x83
                or ref.decisiones[193]["decision_recibida"] != 0
                or ref.metricas.caja_final != 9228 or ref.metricas.ordenes != 2):
            raise SystemExit("El vector de reserva perdió cobertura")

    top = HERE/"trade_spi_externo.v"
    banco = HERE/"tb_trade_spi_externo.sv"
    rtl = [top, DEMO/"rtl/pochoco_soc_cpu_trace.v", DEMO/"rtl/espino_core_cpu_trace.v"]
    rtl.extend(MMIO/f"rtl/{name}.v" for name in ("pochoco_ram", "pochoco_spi_slave", "pochoco_sma10"))
    rtl.extend(sorted((ROOT/"rtl/espino_core").glob("*.v")))
    pcf = HERE/"goboard_spi_externo.pcf"
    constraint = re.compile(r"^set_io (\S+) (\d+)$", re.M)
    board_pins = dict(constraint.findall((ROOT/"goboard.pcf").read_text(encoding="utf-8")))
    pins = constraint.findall(pcf.read_text(encoding="utf-8"))
    if len(pins) != 9 or len({pin for _, pin in pins}) != 9 or any(board_pins.get(s) != p for s, p in pins):
        raise SystemExit("El PCF SPI difiere del pinout de la imagen base")

    def simular(ticks: int, fase: int, sources, nombre: str, *, vectores=out,
                periodo=100000, netlist=False) -> str:
        vvp = out/f"{nombre}.vvp"
        ajustes = ["-DNETLIST"] if netlist else [
            f"-Ptb_trade_spi_externo.PALABRAS_FIRMWARE={words}",
            f'-Ptb_trade_spi_externo.ARCHIVO_FIRMWARE="{firmware_parameter}"',
        ]
        ejecutar([tools["iverilog"], "-g2012", "-s", "tb_trade_spi_externo", *ajustes,
                  f"-Ptb_trade_spi_externo.TICKS={ticks}", f"-Ptb_trade_spi_externo.FASE_NS={fase}",
                  f"-Ptb_trade_spi_externo.PERIODO_NS={periodo}",
                  "-o", vvp, banco, *sources, cells], out/f"{nombre}_compilacion.log")
        result = ejecutar([tools["vvp"], "-n", vvp, f"+vectores={vectores.as_posix()}"], out/f"{nombre}.log")
        if f"PASS {ticks} MISO frente a Python" not in result:
            raise SystemExit(f"Falta la confirmacion de {ticks} transferencias en {nombre}")
        print("\n".join(line for line in result.splitlines() if line.startswith("PASS ")), flush=True)
        return result

    json_file, asc, timing = (out/name for name in ("trade.json", "trade.asc", "timing.json"))
    sources = " ".join(f'"{p.relative_to(ROOT).as_posix()}"' for p in rtl)
    override = ""
    if args.modo != "base":
        override = (f'chparam -set PALABRAS_FIRMWARE {words} '
                    f'-set ARCHIVO_FIRMWARE "{firmware_parameter}" trade_spi_externo; ')
    log_yosys = ejecutar([tools["yosys"], "-p",
                          f'read_verilog -sv {sources}; {override}synth_ice40 -dff -top trade_spi_externo; '
                          f'check -assert; stat; write_json "{json_file.as_posix()}"'], out/"yosys.log")
    log_pnr = ejecutar([tools["nextpnr-ice40"], "--hx1k", "--package", "vq100", "--freq", "25",
                       "--seed", "1", "--json", json_file, "--pcf", pcf, "--asc", asc, "--report", timing],
                      out/"nextpnr.log")
    cells_used = int(re.search(r"ICESTORM_LC:\s*(\d+)", log_pnr)[1])
    bram = int(re.search(r"ICESTORM_RAM:\s*(\d+)", log_pnr)[1])
    lut = int(re.findall(r"^\s*(\d+)\s+SB_LUT4\s*$", log_yosys, re.M)[-1])
    clocks = json.loads(timing.read_text(encoding="utf-8"))["fmax"]
    if cells_used > 1280 or len(clocks) != 2 or any(c["achieved"] < 25 for c in clocks.values()):
        raise SystemExit("El candidato no cumple area/timing")
    fmax = min(c["achieved"] for c in clocks.values())
    print(f"PASS implementacion: {cells_used}/1280 LC, {lut} LUT4, {bram} BRAM, Fmax minima {fmax:.2f} MHz", flush=True)

    mapped = out/"trade_netlist.v"
    ejecutar([tools["yosys"], "-Q", "-q", "-p",
              f'read_json "{json_file.as_posix()}"; write_verilog -noattr "{mapped.as_posix()}"'], out/"netlist.log")
    fases = [0, 19, 41, 63] if args.modo == "base" else [0, 41]
    ticks_netlist = stress_ticks or (16 if args.modo == "conservar" else 64)
    periodo_netlist = 24000 if stress_ticks else 100000
    with ThreadPoolExecutor(max_workers=4) as pool:
        real = pool.submit(simular, 2000, 0, rtl, "rtl_2000")
        tests = [pool.submit(simular, ticks_netlist, fase, [mapped], f"netlist_fase_{fase}",
                             vectores=stress if stress_ticks else out, periodo=periodo_netlist,
                             netlist=True) for fase in fases]
        if stress_ticks:
            tests.append(pool.submit(simular, stress_ticks, 27, rtl, "rtl_reserva", vectores=stress))
        rtl_logs = [real.result()]
        for test in tests:
            rtl_logs.append(test.result())
    ejecutar([tools["icepack"], asc, binary], out/"icepack.log")
    worst = max(int(latency) for log in rtl_logs for latency in re.findall(r"peor caso (\d+)/", log))
    result = {
        "modo": args.modo, "palabras_firmware": words, "lc": cells_used, "lut4": lut, "bram": bram,
        "relojes": clocks, "peor_caso_ciclos": worst, "ticks_rtl": 2000, "ticks_rtl_reserva": stress_ticks,
        "ticks_por_fase_netlist": ticks_netlist, "fases_netlist_ns": fases, "periodo_netlist_ns": periodo_netlist,
        "sha256": sha256(binary.read_bytes()).hexdigest().upper(),
    }
    (out/"resultados.json").write_text(json.dumps(result, indent=2)+"\n", encoding="utf-8")
    print(f"BIN {binary} SHA-256 {result['sha256']}")


if __name__ == "__main__":
    main()
