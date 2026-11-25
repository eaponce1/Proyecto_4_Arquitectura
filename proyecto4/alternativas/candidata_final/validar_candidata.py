"""Ensamblado, pruebas y construcción reproducible del candidato sin acceso a USB."""

import argparse
from concurrent.futures import ThreadPoolExecutor
import csv
from hashlib import sha256
import json
from pathlib import Path
import re
import shutil
import statistics
import subprocess
import sys

from estrategia_referencia import crear_politica
from estrategia import Decision
from simulador import ejecutar_decision, leer_precios, simular_estrategia
from test_capital_protegido import MaquinaMMIO, words_from_hex

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
HARDWARE = ROOT / "proyecto4/pruebas_fisicas/spi_externo_robusto"
TRACE = HARDWARE.parent / "demo_autonoma_bus_detail"
MMIO = HERE.parent / "mmio_sma10"
SERIE = ROOT / "proyecto4/resultados/validacion_oficial/practica_meta.csv"


def ejecutar(cmd, log):
    r = subprocess.run(cmd, cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                       text=True, encoding="utf-8", errors="replace")
    log.write_text(r.stdout, encoding="utf-8")
    if r.returncode:
        raise RuntimeError(f"Salida {r.returncode}, {log}\n" + "\n".join(r.stdout.splitlines()[-12:]))
    return r.stdout


def comparar_hex(words, precios, referencia):
    cpu = MaquinaMMIO(words)
    for p, tick in zip(precios, referencia.decisiones, strict=True):
        miso, _ = cpu.one_tick(p)
        obtenido = (miso, cpu.tx_hold, cpu.reg[15], cpu.reg[5])
        esperado = (tick["decision_recibida"], tick["decision_siguiente"], tick["caja"], tick["acciones"])
        if obtenido != esperado:
            raise RuntimeError(f"RV32E/Python en tick {tick['tick']}: {obtenido} != {esperado}")


def comprobar_fills(words):
    # Órdenes inyectadas en el intérprete para aislar la rutina ASM de cartera.
    casos = [
        ("compra_1", 0x41, 10000, 0, 165),
        ("compra_63", 0x7F, 10000, 0, 1),
        ("caja_insuficiente", 0x7F, 515, 0, 255),
        ("caja_sin_comision", 0x41, 4, 0, 50),
        ("venta_parcial", 0x81, 600, 4, 100),
        ("venta_total", 0x84, 600, 4, 100),
        ("venta_recortada", 0xBF, 600, 4, 100),
        ("venta_no_cubre_comision", 0x82, 1, 2, 1),
        ("venta_menor_a_comision", 0x82, 3, 2, 1),
        ("sin_acciones", 0xBF, 10000, 0, 255),
        ("reservada", 0xFF, 10000, 0, 1),
    ]
    log = []
    for nombre, byte, caja, acciones, precio in casos:
        cpu = MaquinaMMIO(words)
        cpu.one_tick(precio)
        cpu.tx_hold, cpu.reg[4], cpu.reg[15], cpu.reg[5] = byte, byte, caja, acciones
        miso, _ = cpu.one_tick(precio)
        fill = ejecutar_decision(caja, acciones, Decision.desde_byte(byte), precio)
        if (miso, cpu.reg[15], cpu.reg[5]) != (byte, fill.caja, fill.acciones):
            raise RuntimeError(f"Fallo al ejecutar {nombre}")
        log.append(f"PASS {nombre}: caja={fill.caja} acciones={fill.acciones} comision={fill.comision}")
    return log


def preparar(precios, directorio, words):
    directorio.mkdir(parents=True, exist_ok=True)
    referencia = simular_estrategia(precios, "candidata", crear_politica())
    comparar_hex(words, precios, referencia)
    vectores = {
        "precios": precios,
        "miso": [r["decision_recibida"] for r in referencia.decisiones],
        "escrituras": [r["decision_siguiente"] for r in referencia.decisiones],
        "cartera": [(r["caja"] << 32) | (r["patrimonio"] << 8) | r["acciones"] for r in referencia.decisiones],
    }
    for nombre, valores in vectores.items():
        (directorio/f"{nombre}.hex").write_text("".join(f"{i:02x}\n" for i in valores), encoding="ascii")
    return referencia.metricas


def resumir_metricas(path):
    with path.open(newline="") as f:
        rows = list(csv.DictReader(f))
    ciclos = [int(row["ciclos"]) for row in rows]
    ic = [int(row["ic"]) for row in rows]
    i = ciclos.index(max(ciclos))
    return {
        "ticks": len(rows), "ic_promedio": statistics.mean(ic), "ic_maximo": max(ic),
        "ciclos_promedio": statistics.mean(ciclos), "ciclos_peor": ciclos[i], "tick_peor": i,
        "cpi_agregado": sum(ciclos)/sum(ic), "cpi_peor_tick": ciclos[i]/ic[i],
        "us_promedio": statistics.mean(ciclos)*0.08, "us_max": ciclos[i]*0.08,
        "periodo_ns": int(rows[0]["periodo_ns"]),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--serie", type=Path, default=SERIE)
    parser.add_argument("--salida", type=Path, default=HERE/"build")
    args = parser.parse_args()
    out = args.salida.resolve()
    out.mkdir(parents=True, exist_ok=True)
    binary = out/"competition.bin"
    if binary.exists():
        raise SystemExit("La salida ya contiene competition.bin; elige otra carpeta.")
    tools = {name: shutil.which(name) for name in ("iverilog", "vvp", "yosys", "nextpnr-ice40", "icepack")}
    if missing := [name for name, path in tools.items() if not path]:
        raise SystemExit(f"Faltan herramientas: {', '.join(missing)}")
    cells = Path(tools["yosys"]).resolve().parents[1]/"share/yosys/ice40/cells_sim.v"
    if not cells.exists():
        raise SystemExit(f"Falta {cells}")
    firmware = out/"trade_candidate.hex"
    ejecutar([sys.executable, "-B", ROOT/"sw/assembler.py", HERE/"trade_candidate.s",
             "-o", firmware], out/"ensamblado.log")
    if firmware.read_bytes() != (HERE/"trade_candidate.hex").read_bytes():
        raise RuntimeError("El HEX de referencia difiere del ensamblado")
    ejecutar([sys.executable, "-B", TRACE/"verificar_pc_rom.py", "--firmware", firmware],
             out/"alcance_rom.log")
    words = words_from_hex(firmware)
    real, stress = out/"practica", out/"estres"
    precios = leer_precios(args.serie)
    m = preparar(precios, real, words)
    sinteticos = [100]*128 + [130, 255] + [100]*126 + [99, 1] + [100]*126 + [150, 255]
    s = preparar(sinteticos, stress, words)
    if s.ordenes != 2 or s.caja_final != 592 or s.acciones_finales != 0:
        raise RuntimeError("El vector extremo perdió cobertura de compra, venta o reserva")
    log = [f"PASS RV32E/Python {len(precios)} ticks: MISO, DECISION, caja y acciones",
           f"PASS reserva: {len(sinteticos)} ticks, cierre en {s.caja_final}", *comprobar_fills(words)]
    (out/"equivalencia_hex.log").write_text("\n".join(log)+"\n", encoding="utf-8")
    print("\n".join(log[:2]), flush=True)

    banco = HERE/"tb/tb_candidata.sv"
    rtl = [HARDWARE/"trade_spi_externo.v", TRACE/"rtl/pochoco_soc_cpu_trace.v",
           TRACE/"rtl/espino_core_cpu_trace.v"]
    rtl.extend(MMIO/f"rtl/{nombre}.v" for nombre in ("pochoco_ram", "pochoco_spi_slave", "pochoco_sma10"))
    rtl.extend(sorted((ROOT/"rtl/espino_core").glob("*.v")))
    pcf = HARDWARE/"goboard_spi_externo.pcf"
    pines = re.compile(r"^set_io (\S+) (\d+)$", re.M)
    base = dict(pines.findall((ROOT/"goboard.pcf").read_text(encoding="utf-8")))
    asignaciones = pines.findall(pcf.read_text(encoding="utf-8"))
    if len(asignaciones) != 9 or len({pin for _, pin in asignaciones}) != 9 or any(
            base.get(señal) != pin for señal, pin in asignaciones):
        raise RuntimeError("El PCF difiere de la asignación auditada")
    fw_path = firmware.relative_to(ROOT).as_posix() if firmware.is_relative_to(ROOT) else firmware.as_posix()
    yo, asc, timing = (out/name for name in ("trade.json", "trade.asc", "timing.json"))
    fuentes = " ".join(f'"{p.relative_to(ROOT).as_posix()}"' for p in rtl)
    y = ejecutar([tools["yosys"], "-p",
                  f'read_verilog -sv {fuentes}; chparam -set PALABRAS_FIRMWARE {len(words)} '
                  f'-set ARCHIVO_FIRMWARE "{fw_path}" trade_spi_externo; '
                  f'synth_ice40 -dff -top trade_spi_externo; check -assert; stat; write_json "{yo.as_posix()}"'],
                 out/"yosys.log")
    n = ejecutar([tools["nextpnr-ice40"], "--hx1k", "--package", "vq100", "--freq", "25",
                  "--seed", "1", "--json", yo, "--pcf", pcf, "--asc", asc, "--report", timing],
                 out/"nextpnr.log")
    lcs = int(re.search(r"ICESTORM_LC:\s*(\d+)", n)[1])
    bram = int(re.search(r"ICESTORM_RAM:\s*(\d+)", n)[1])
    luts = int(re.findall(r"^\s*(\d+)\s+SB_LUT4\s*$", y, re.M)[-1])
    clocks = json.loads(timing.read_text(encoding="utf-8"))["fmax"]
    if lcs > 1280 or len(clocks) != 2 or min(c["achieved"] for c in clocks.values()) < 25:
        raise RuntimeError("No cumple área o timing")
    mapped = out/"trade_netlist.v"
    ejecutar([tools["yosys"], "-Q", "-q", "-p",
              f'read_json "{yo.as_posix()}"; write_verilog -noattr "{mapped.as_posix()}"'], out/"netlist.log")
    print(f"PASS P&R {lcs}/1280 LC, {luts} LUT4, {bram} BRAM", flush=True)

    def simular(nombre, vectors, ticks, periodo, fase=0, netlist=False):
        exe, metricas = out/f"{nombre}.vvp", out/f"{nombre}.csv"
        opts = ["-DNETLIST"] if netlist else [
            f"-Ptb_candidata.PALABRAS_FIRMWARE={len(words)}",
            f'-Ptb_candidata.ARCHIVO_FIRMWARE="{fw_path}"',
            "-Ptb_candidata.REG_CAJA=15", "-Ptb_candidata.REG_ACCIONES=5",
        ]
        ejecutar([tools["iverilog"], "-g2012", "-s", "tb_candidata", *opts,
                  f"-Ptb_candidata.TICKS={ticks}", f"-Ptb_candidata.PERIODO_NS={periodo}",
                  f"-Ptb_candidata.FASE_NS={fase}", "-o", exe, banco,
                  *([mapped] if netlist else rtl), cells], out/f"{nombre}_compilacion.log")
        result = ejecutar([tools["vvp"], "-n", exe, f"+vectores={vectors.as_posix()}",
                           f"+cartera={(vectors/'cartera.hex').as_posix()}", f"+metricas={metricas.as_posix()}"],
                          out/f"{nombre}.log")
        if f"PASS {ticks} MISO frente a Python" not in result:
            raise RuntimeError(f"Falta la confirmación de {ticks} MISO en {nombre}")
        print("\n".join(line for line in result.splitlines() if "PASS" in line), flush=True)
        return metricas

    with ThreadPoolExecutor(max_workers=4) as pool:
        corto = pool.submit(simular, "rtl_ronda3_estres", stress, len(sinteticos), 100000, 27)
        gates = [pool.submit(simular, f"puertas_{fase}", stress, len(sinteticos), 30000, fase, True)
                 for fase in (0, 41)]
        largo = pool.submit(simular, "rtl_practica_20000", real, len(precios), 30000)
        cortos = resumir_metricas(corto.result())
        for gate in gates:
            gate.result()
        largos = resumir_metricas(largo.result())
    if largos["ticks"] != 20000:
        raise RuntimeError("El RTL no registró la serie completa")
    ejecutar([tools["icepack"], asc, binary], out/"icepack.log")
    resumen = {
        "lc": lcs, "lut4": luts, "bram": bram, "relojes": clocks, "practica_rtl": largos,
        "estres_rtl": cortos, "patrimonio_practica": m.patrimonio_final,
        "sha256_bin": sha256(binary.read_bytes()).hexdigest().upper(),
        "sha256_hex": sha256(firmware.read_bytes()).hexdigest().upper(),
    }
    (out/"resultados.json").write_text(json.dumps(resumen, indent=2)+"\n", encoding="utf-8")
    print(f"PASS competition.bin {resumen['sha256_bin']}", flush=True)


if __name__ == "__main__":
    main()
