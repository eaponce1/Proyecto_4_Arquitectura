"""Comprueba el banco con MMIO SMA10 base y una prueba negativa de deadline."""
import argparse
from pathlib import Path
import shutil
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
PROYECTO = ROOT / "proyecto4"
sys.path.insert(0, str(PROYECTO / "python"))
from enfoques_finales import estrategia_reversion_media
from simulador import leer_precios, simular_estrategia


def ejecutar(cmd, log, *, fallo_esperado=None):
    result = subprocess.run(
        [str(part) for part in cmd], cwd=ROOT, stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT, text=True, encoding="utf-8", errors="replace",
    )
    log.write_text(result.stdout, encoding="utf-8")
    if fallo_esperado is None:
        correct = result.returncode == 0
    else:
        correct = result.returncode != 0 and fallo_esperado in result.stdout
    if not correct:
        raise RuntimeError(f"Resultado inesperado en {log}\n{result.stdout}")
    return result.stdout


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--salida", type=Path, required=True)
    parser.add_argument("--netlist", type=Path, help="Opcional. Netlist de MMIO SMA10 base.")
    args = parser.parse_args()
    out = args.salida.resolve()
    out.mkdir(parents=True, exist_ok=True)

    tools = {name: shutil.which(name) for name in ("iverilog", "vvp", "yosys")}
    if not all(tools.values()):
        raise SystemExit("Se requieren iverilog, vvp y yosys en PATH")
    cells = Path(tools["yosys"]).resolve().parents[1] / "share/yosys/ice40/cells_sim.v"
    if not cells.is_file():
        raise SystemExit(f"No se encontró el modelo iCE40 en {cells}")

    prices = leer_precios()[:64]
    ref = simular_estrategia(prices, "MMIO SMA10 base", estrategia_reversion_media)
    arrays = {
        "precios": prices,
        "miso": [row["decision_recibida"] for row in ref.decisiones],
        "escrituras": [row["decision_siguiente"] for row in ref.decisiones],
        "cartera": [
            (row["caja"] << 32) | (row["patrimonio"] << 8) | row["acciones"]
            for row in ref.decisiones
        ],
    }
    for name, values in arrays.items():
        width = 16 if name == "cartera" else 2
        (out / f"{name}.hex").write_text("".join(f"{v:0{width}x}\n" for v in values), encoding="ascii")

    physical = PROYECTO / "pruebas_fisicas"
    trace = physical / "demo_autonoma_bus_detail/rtl"
    mmio = PROYECTO / "alternativas/mmio_sma10/rtl"
    rtl = [
        physical / "spi_externo_robusto/trade_spi_externo.v",
        trace / "pochoco_soc_cpu_trace.v", trace / "espino_core_cpu_trace.v",
        mmio / "pochoco_ram.v", mmio / "pochoco_spi_slave.v", mmio / "pochoco_sma10.v",
        *sorted((ROOT / "rtl/espino_core").glob("*.v")),
    ]
    banco = HERE / "tb_candidata.sv"

    def compilar(nombre, pns, *, ticks=64, gates=False):
        vvp = out / f"{nombre}.vvp"
        if gates:
            sources = [args.netlist.resolve()]
            flags = ["-DNETLIST", "-Ptb_candidata.FASE_NS=41"]
        else:
            sources = rtl
            flags = ["-Ptb_candidata.REG_CAJA=15", "-Ptb_candidata.REG_ACCIONES=5"]
        ejecutar([
            tools["iverilog"], "-g2012", "-s", "tb_candidata", *flags,
            f"-Ptb_candidata.PERIODO_NS={pns}", f"-Ptb_candidata.TICKS={ticks}",
            "-o", vvp, banco, *sources, cells,
        ], out / f"{nombre}_compilacion.log")
        return vvp

    vectores = f"+vectores={out.as_posix()}"
    cartera = f"+cartera={(out / 'cartera.hex').as_posix()}"
    normal = compilar("rtl", 100000)
    contabilidad = ejecutar([tools["vvp"], "-n", normal, "+contabilidad_sola"], out / "contabilidad.log")
    if "PASS contabilidad" not in contabilidad:
        raise RuntimeError("No ejecutó los casos límite del modelo de la maestra")
    print(contabilidad.rstrip())
    resultado = ejecutar([
        tools["vvp"], "-n", normal, vectores, cartera,
        f"+metricas={(out / 'metricas.csv').as_posix()}",
    ], out / "rtl.log")
    if "PASS 64 MISO frente a Python" not in resultado or "status_y_byte_done=0 " in resultado:
        raise RuntimeError("Falta integración completa o no se observó concurrencia STATUS/byte_done")
    print(resultado.rstrip())

    corto = compilar("deadline_negativo", 9660, ticks=1)
    ejecutar([tools["vvp"], "-n", corto, vectores], out / "deadline_negativo.log",
             fallo_esperado="TIMEOUT tick=0")
    print("PASS el banco rechaza el deadline negativo")

    if args.netlist is not None:
        gate = compilar("netlist", 30000, gates=True)
        resultado = ejecutar([tools["vvp"], "-n", gate, vectores, cartera], out / "netlist.log")
        if "PASS 64 MISO frente a Python" not in resultado:
            raise RuntimeError("El netlist no completó las 64 transacciones")
        print(resultado.rstrip())


if __name__ == "__main__":
    main()

