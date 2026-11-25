"""Equivalencia RV32E y validación de la estrategia agresiva en HX1K/VQ100."""

import argparse
from concurrent.futures import ThreadPoolExecutor
import csv
from dataclasses import asdict
from hashlib import sha256
import json
from pathlib import Path
import re
import shutil
import statistics
import subprocess
import sys

from estrategia_agresiva import Parametros, crear_politica
from simulador import leer_precios, simular_estrategia
from test_capital_protegido import MaquinaMMIO, words_from_hex

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
MMIO = HERE.parent / "mmio_sma10"
HARDWARE = ROOT / "proyecto4/pruebas_fisicas/spi_externo_robusto"
TRACE = HARDWARE.parent / "demo_autonoma_bus_detail"
TB = HERE.parent / "candidata_final/tb/tb_candidata.sv"
SERIE = ROOT / "proyecto4/resultados/validacion_oficial/practica_meta.csv"
NS_CICLO = 80
NS_SPI = 9500


def ejecutar(cmd, log):
    resultado = subprocess.run(cmd, cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                               text=True, encoding="utf-8", errors="replace")
    log.write_text(resultado.stdout + f"\nSalida={resultado.returncode}\n", encoding="utf-8")
    if resultado.returncode:
        raise RuntimeError(f"Salida {resultado.returncode}, {log}\n" +
                           "\n".join(resultado.stdout.splitlines()[-12:]))
    return resultado.stdout


def firma(archivo):
    return sha256(archivo.read_bytes()).hexdigest().upper()


def comprobar_hex(words, precios, referencia):
    cpu = MaquinaMMIO(words)
    for precio, tick in zip(precios, referencia.decisiones, strict=True):
        miso, _ = cpu.one_tick(precio)
        real = (miso, cpu.tx_hold, cpu.reg[15], cpu.reg[5])
        esperado = (tick["decision_recibida"], tick["decision_siguiente"], tick["caja"], tick["acciones"])
        if real != esperado:
            raise RuntimeError(f"Diferencia RV32E/Python en tick {tick['tick']}: "
                               f"MISO/DECISION/caja/inventario {real} != {esperado}")


def crear_estres(config, reintento=False):
    """Hace crecer la posición en escalones y la liquida con una reversión."""
    p = config.periodo
    if config == Parametros("momentum", 100, False, 16, 8):
        precios = [100]*16 + [116, 255] + [100]*14 + [80, 1]
        if reintento:
            precios += [1]*30 + [10, 79] + [5]*14 + [2, 5, 1, 5, 5]
    else:
        if reintento:
            raise RuntimeError("El caso de reintento requiere momentum(100 %, directo, 16, 8)")
        espera = max(4 if config.familia == "breakout" else 1, (10+p-1)//p)
        moderada = max(1, config.umbral)
        fuerte = max(20, 2*config.umbral)
        escalones = (105, min(105+moderada, 175), min(105+moderada+fuerte, 220))
        precios = [escalones[0]]*(p*espera)
        for precio in escalones[1:]:
            precios.extend([precio]*p)
        precios.extend([70]*(p+16))

    referencia = simular_estrategia(precios, "estrés", crear_politica(config))
    if referencia.compras < 1 or referencia.ventas < 1 or referencia.metricas.acciones_finales:
        raise RuntimeError("El estímulo de estrés debe ejecutar compras y liquidación completa")
    if reintento and (referencia.metricas.caja_final != 0 or not any(
            f["accion_recibida"] == "vender" and f["cantidad_ejecutada"] == 0
            for f in referencia.decisiones)):
        raise RuntimeError("Falta cobertura de rechazo y reintento de venta por comisión")
    fin = max(row["tick"] for row in referencia.decisiones if row["cantidad_ejecutada"]) + 2
    precios = precios[:fin]
    return precios, simular_estrategia(precios, "estrés", crear_politica(config))


def vectores(carpeta, precios, referencia):
    carpeta.mkdir(parents=True, exist_ok=True)
    filas = referencia.decisiones[:len(precios)]
    datos = {
        "precios": precios,
        "miso": [fila["decision_recibida"] for fila in filas],
        "escrituras": [fila["decision_siguiente"] for fila in filas],
    }
    for nombre, valores in datos.items():
        (carpeta/f"{nombre}.hex").write_text("".join(f"{i:02x}\n" for i in valores), encoding="ascii")
    if all(f["caja"] < 1 << 32 and f["patrimonio"] < 1 << 24 and f["acciones"] < 1 << 8 for f in filas):
        cartera = carpeta/"cartera.hex"
        cartera.write_text("".join(f"{(f['caja'] << 32) | (f['patrimonio'] << 8) | f['acciones']:016x}\n"
                                  for f in filas), encoding="ascii")
        return [f"+cartera={cartera.as_posix()}"]
    # El cotejo del CSV del banco usa enteros completos incluso si no se empaqueta.
    return []


def comprobar_traza(path, referencia, ticks, puertas):
    with path.open(newline="", encoding="utf-8") as stream:
        filas = list(csv.DictReader(stream))
    if len(filas) != ticks:
        raise RuntimeError(f"{path}: {len(filas)} transacciones, se esperaban {ticks}")
    comisiones = 0
    for real, esperado in zip(filas, referencia.decisiones[:ticks], strict=True):
        comisiones += esperado["comision"]
        for columna, valor in (
            ("tick", esperado["tick"]), ("precio", esperado["precio"]), ("caja", esperado["caja"]),
            ("acciones", esperado["acciones"]), ("patrimonio", esperado["patrimonio"]),
            ("fill", esperado["cantidad_ejecutada"]), ("comisiones_acum", comisiones),
        ):
            if int(real[columna]) != valor:
                raise RuntimeError(f"{path}: tick {esperado['tick']} {columna} {real[columna]} != {valor}")
        if int(real["miso_hex"], 16) != esperado["decision_recibida"]:
            raise RuntimeError(f"{path}: MISO desigual, tick {esperado['tick']}")
        if not puertas and int(real["decision_hex"], 16) != esperado["decision_siguiente"]:
            raise RuntimeError(f"{path}: DECISION desigual, tick {esperado['tick']}")
    if puertas:
        return {"ticks": ticks, "periodo_ns": int(filas[0]["periodo_ns"])}
    ciclos = [int(f["ciclos"]) for f in filas]
    ic = [int(f["ic"]) for f in filas]
    periodo = int(filas[0]["periodo_ns"])
    peor = ciclos.index(max(ciclos))
    return {
        "ticks": ticks, "periodo_ns": periodo, "presupuesto": (periodo-NS_SPI)//NS_CICLO,
        "ic_promedio": statistics.mean(ic), "ic_max": max(ic), "ciclos_promedio": statistics.mean(ciclos),
        "ciclos_max": ciclos[peor], "tick_peor": peor, "cpi_agregado": sum(ciclos)/sum(ic),
        "cpi_tick_peor": ciclos[peor]/ic[peor], "us_max": ciclos[peor]*NS_CICLO/1000,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--serie", type=Path, default=SERIE)
    parser.add_argument("--seleccion", type=Path, default=HERE/"resultados/seleccion.json")
    parser.add_argument("--salida", type=Path, default=HERE/"build")
    etapas = parser.add_mutually_exclusive_group()
    etapas.add_argument("--solo-hex", action="store_true")
    etapas.add_argument("--solo-rtl", action="store_true")
    parser.add_argument("--estres-reintento", action="store_true")
    parser.add_argument("--ticks-rtl", type=int, default=2000)
    parser.add_argument("--periodo-rtl-ns", type=int, default=100000)
    parser.add_argument("--periodo-puertas-ns", type=int, default=30000,
                        help="Período mínimo del netlist; aumenta si lo exige el peor caso RTL")
    args = parser.parse_args()
    out = args.salida.resolve()
    if not out.is_relative_to(HERE) or out == HERE:
        parser.error("--salida debe ser una subcarpeta de agresiva")
    if not 2000 <= args.ticks_rtl <= 20000:
        parser.error("--ticks-rtl debe estar entre 2000 y 20000")
    if min(args.periodo_rtl_ns, args.periodo_puertas_ns) < NS_SPI+NS_CICLO:
        parser.error("El período debe permitir una trama más al menos un ciclo de SoC")
    if (out/"competition.bin").exists():
        raise SystemExit("La carpeta ya contiene competition.bin; elige otra salida")
    out.mkdir(parents=True, exist_ok=True)

    config = Parametros(**json.loads(args.seleccion.read_text(encoding="utf-8"))["config"])
    fuente = HERE/"trade.s"
    firmware = out/"trade.hex"
    ejecutar([sys.executable, "-B", ROOT/"sw/assembler.py", fuente, "-o", firmware], out/"ensamblado.log")
    ejecutar([sys.executable, "-B", TRACE/"verificar_pc_rom.py", "--firmware", firmware],
             out/"alcance_rom.log")
    words = words_from_hex(firmware)
    precios = leer_precios(args.serie)
    referencia = simular_estrategia(precios, "agresiva", crear_politica(config))
    comprobar_hex(words, precios, referencia)
    estres, referencia_estres = crear_estres(config, args.estres_reintento)
    comprobar_hex(words, estres, referencia_estres)
    evidencia = {
        "config": asdict(config), "sha256_seleccion": firma(args.seleccion), "sha256_serie": firma(args.serie),
        "sha256_s": firma(fuente), "sha256_hex": firma(firmware), "palabras": len(words),
        "ticks_interprete": len(precios), "ticks_interprete_estres": len(estres),
        "mercado_practica": asdict(referencia.metricas),
        "mercado_estres": asdict(referencia_estres.metricas),
        "compras_estres": referencia_estres.compras, "ventas_estres": referencia_estres.ventas,
    }
    (out/"equivalencia.json").write_text(json.dumps(evidencia, indent=2)+"\n", encoding="utf-8")
    print(f"PASS intérprete RV32E {len(precios)} ticks de práctica y {len(estres)} de estrés; "
          "MISO, DECISION, caja e inventario", flush=True)
    if args.solo_hex:
        return

    tools = {n: shutil.which(n) for n in ("iverilog", "vvp", "yosys", "nextpnr-ice40", "icepack")}
    if faltan := [n for n, ruta in tools.items() if not ruta]:
        raise SystemExit(f"Faltan herramientas: {', '.join(faltan)}")
    celdas = Path(tools["yosys"]).resolve().parents[1]/"share/yosys/ice40/cells_sim.v"
    if not celdas.is_file():
        raise SystemExit(f"Falta el modelo de primitivas {celdas}")
    rtl = [HARDWARE/"trade_spi_externo.v", TRACE/"rtl/pochoco_soc_cpu_trace.v",
           TRACE/"rtl/espino_core_cpu_trace.v"]
    rtl.extend(MMIO/f"rtl/{nombre}.v" for nombre in ("pochoco_ram", "pochoco_spi_slave", "pochoco_sma10"))
    rtl.extend(sorted((ROOT/"rtl/espino_core").glob("*.v")))
    pcf = HARDWARE/"goboard_spi_externo.pcf"
    asignar = re.compile(r"^set_io (\S+) (\d+)$", re.M)
    base = dict(asignar.findall((ROOT/"goboard.pcf").read_text(encoding="utf-8")))
    pines = asignar.findall(pcf.read_text(encoding="utf-8"))
    if len(pines) != 9 or len({p for _, p in pines}) != 9 or any(base.get(s) != p for s, p in pines):
        raise RuntimeError("El PCF difiere de los pines auditados de Go Board")
    fw = firmware.relative_to(ROOT).as_posix()
    seleccion = out/"practica"
    sintetico = out/"estres"
    # El prefijo usa exactamente los mismos precios y estado causal que los 20.000 ticks.
    cartera_practica = vectores(seleccion, precios[:args.ticks_rtl], referencia)
    cartera_estres = vectores(sintetico, estres, referencia_estres)
    mapeado = out/"trade_netlist.v"

    def simular(nombre, carpeta, ticks, ref, cartera, periodo, fase=0, puertas=False):
        vvp = out/f"{nombre}.vvp"
        csv_out = out/f"{nombre}.csv"
        opts = ["-DNETLIST"] if puertas else [
            f"-Ptb_candidata.PALABRAS_FIRMWARE={len(words)}",
            f'-Ptb_candidata.ARCHIVO_FIRMWARE="{fw}"',
            "-Ptb_candidata.REG_CAJA=15", "-Ptb_candidata.REG_ACCIONES=5",
        ]
        ejecutar([tools["iverilog"], "-g2012", "-s", "tb_candidata", *opts,
                  f"-Ptb_candidata.TICKS={ticks}", f"-Ptb_candidata.PERIODO_NS={periodo}",
                  f"-Ptb_candidata.FASE_NS={fase}", "-o", vvp, TB,
                  *([mapeado] if puertas else rtl), celdas], out/f"{nombre}_compilacion.log")
        log = ejecutar([tools["vvp"], "-n", vvp, f"+vectores={carpeta.as_posix()}", *cartera,
                        f"+metricas={csv_out.as_posix()}"], out/f"{nombre}.log")
        if f"PASS {ticks} MISO frente a Python" not in log:
            raise RuntimeError(f"Falta la aceptación de {ticks} ticks en {nombre}")
        resultado = comprobar_traza(csv_out, ref, ticks, puertas)
        print("\n".join(line for line in log.splitlines() if line.startswith("PASS ")), flush=True)
        return resultado

    # El HEX y ambas corridas RTL son precondiciones de Yosys.
    with ThreadPoolExecutor(max_workers=2) as pool:
        stress = pool.submit(simular, "rtl_estres", sintetico, len(estres), referencia_estres,
                             cartera_estres, args.periodo_rtl_ns, 27)
        real = pool.submit(simular, "rtl_practica", seleccion, args.ticks_rtl, referencia,
                           cartera_practica, args.periodo_rtl_ns)
        evidencia["estres_rtl"] = stress.result()
        evidencia["practica_rtl"] = real.result()
    if args.solo_rtl:
        (out/"resultados.json").write_text(json.dumps(evidencia, indent=2)+"\n", encoding="utf-8")
        return

    yo, asc, timing = (out/n for n in ("trade.json", "trade.asc", "timing.json"))
    fuentes = " ".join(f'"{p.relative_to(ROOT).as_posix()}"' for p in rtl)
    y = ejecutar([tools["yosys"], "-p", f'read_verilog -sv {fuentes}; '
                  f'chparam -set PALABRAS_FIRMWARE {len(words)} -set ARCHIVO_FIRMWARE "{fw}" trade_spi_externo; '
                  f'synth_ice40 -dff -top trade_spi_externo; check -assert; stat; write_json "{yo.as_posix()}"'],
                 out/"yosys.log")
    n = ejecutar([tools["nextpnr-ice40"], "--hx1k", "--package", "vq100", "--freq", "25", "--seed", "1",
                  "--json", yo, "--pcf", pcf, "--asc", asc, "--report", timing], out/"nextpnr.log")
    lc = int(re.search(r"ICESTORM_LC:\s*(\d+)", n)[1])
    bram = int(re.search(r"ICESTORM_RAM:\s*(\d+)", n)[1])
    lut4 = int(re.findall(r"^\s*(\d+)\s+SB_LUT4\s*$", y, re.M)[-1])
    relojes = json.loads(timing.read_text(encoding="utf-8"))["fmax"]
    if lc > 1280 or bram > 16 or len(relojes) != 2 or min(c["achieved"] for c in relojes.values()) < 25:
        raise RuntimeError("La candidata no cumple área o timing")
    evidencia.update(lc=lc, bram=bram, lut4=lut4, relojes=relojes)
    print(f"PASS HX1K/VQ100: {lc}/1280 LC, {lut4} LUT4, {bram}/16 BRAM", flush=True)
    ejecutar([tools["yosys"], "-Q", "-q", "-p",
              f'read_json "{yo.as_posix()}"; write_verilog -noattr "{mapeado.as_posix()}"'],
             out/"netlist.log")

    periodo = max(args.periodo_puertas_ns, NS_SPI+(evidencia["estres_rtl"]["ciclos_max"]+8)*NS_CICLO)
    periodo = ((periodo+NS_CICLO-1)//NS_CICLO)*NS_CICLO
    with ThreadPoolExecutor(max_workers=2) as pool:
        gates = [pool.submit(simular, f"puertas_{fase}", sintetico, len(estres), referencia_estres,
                             cartera_estres, periodo, fase, True) for fase in (0, 41)]
        evidencia["netlist"] = [gate.result() for gate in gates]
    empaquetado = out/"competition.tmp"
    ejecutar([tools["icepack"], asc, empaquetado], out/"icepack.log")
    if empaquetado.stat().st_size != 32220:
        raise RuntimeError("Tamaño inesperado de la imagen HX1K")
    empaquetado.rename(out/"competition.bin")
    evidencia["sha256_bin"] = firma(out/"competition.bin")
    (out/"resultados.json").write_text(json.dumps(evidencia, indent=2)+"\n", encoding="utf-8")
    print(f"PASS competition.bin {evidencia['sha256_bin']}", flush=True)


if __name__ == "__main__":
    main()
