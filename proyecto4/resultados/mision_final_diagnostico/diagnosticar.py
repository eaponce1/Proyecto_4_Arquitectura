"""Diagnóstico RTL A–F de la imagen base y los dos modos de capital."""

import csv
from concurrent.futures import ThreadPoolExecutor
from hashlib import sha256
from pathlib import Path
import shutil
from subprocess import PIPE, STDOUT, run
import sys
from tempfile import TemporaryDirectory

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
P4 = ROOT / "proyecto4"
MMIO = P4 / "alternativas/mmio_sma10"
EXTERNO = P4 / "pruebas_fisicas/spi_externo_robusto"
TRAZAS = P4 / "pruebas_fisicas/demo_autonoma_bus_detail"
sys.path.insert(0, str(P4 / "python"))

from capital_protegido import CAJA_PARA_COMPRAR, crear_politica_activa
from enfoques_finales import estrategia_reversion_media
from estrategia import estrategia_no_operar
from simulador import simular_estrategia

TICKS = 194


def escenarios():
    return {
        "A_creciente": [70 + n // 2 for n in range(TICKS)],
        "B_decreciente": [240 - n for n in range(TICKS)],
        "C_lateral": [100] * TICKS,
        "D_caida_brusca": [200] * 64 + [150] * (TICKS - 64),
        "E_subida_brusca": [100] * 64 + [170] * (TICKS - 64),
        "F_recuperacion": [200] * 64 + [150] * 64 + [210] * (TICKS - 128),
    }


def politica(modo):
    if modo == "conservar":
        return estrategia_no_operar
    if modo == "activo":
        return crear_politica_activa()
    return estrategia_reversion_media


def ejecutar(cmd, log):
    job = run(cmd, cwd=ROOT, stdout=PIPE, stderr=STDOUT, text=True, encoding="utf-8", errors="replace")
    log.write_text(job.stdout, encoding="utf-8")
    if job.returncode:
        raise RuntimeError(f"Fallo de {cmd[0]} ({job.returncode}) en {log}\n{job.stdout[-1200:]}")
    return job.stdout


def escribir_vectores(path, precios, referencia):
    vectores = {
        "precios": precios,
        "escrituras": [d["decision_siguiente"] for d in referencia.decisiones],
        "miso": [d["decision_recibida"] for d in referencia.decisiones],
    }
    for name, values in vectores.items():
        (path / f"{name}.hex").write_text("".join(f"{n:02x}\n" for n in values), encoding="ascii")


def cotejar(path, modo, caso, precios, referencia):
    with (path / "rtl.csv").open(encoding="ascii", newline="") as f:
        filas = list(csv.DictReader(f))
    if len(filas) != TICKS:
        raise RuntimeError(f"Traza incompleta {modo}/{caso}")
    max_ciclos = 0
    with (path / "ticks.csv").open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(("tick", "precio_spi", "precio_x3", "sum10_rtl", "ready_rtl", "delta_x10",
                         "contador_x6", "caja_rtl", "acciones_rtl", "caja_modelo", "acciones_modelo",
                         "senal_compra", "senal_venta", "decision_python_hex", "decision_mmio_hex",
                         "miso_hex", "tick_ejecucion", "acciones_ejecutadas", "comision",
                         "patrimonio", "latencia_ciclos"))
        for tick, (fila, d) in enumerate(zip(filas, referencia.decisiones, strict=True)):
            precio = precios[tick]
            sma = sum(precios[max(0, tick - 9):tick + 1])
            listo = tick >= 9
            delta = 10 * precio - sma
            if (int(fila["tick"]) != tick or int(fila["x3"]) != precio
                    or int(fila["suma10"]) != sma or int(fila["ready"]) != listo):
                raise RuntimeError(f"Estado MMIO inesperado {modo}/{caso}/{tick}")
            caja = acciones = ""
            compra = venta = False
            if modo != "conservar":
                caja, acciones = int(fila["x15"]), int(fila["x5"])
                if (caja, acciones) != (d["caja"], d["acciones"]):
                    raise RuntimeError(f"Contabilidad RTL desigual {modo}/{caso}/{tick}")
                muestra = listo
                umbral = 10
                fondos = True
                if modo == "activo":
                    if int(fila["x6"]) != tick % 64:
                        raise RuntimeError(f"Fase RTL desigual {modo}/{caso}/{tick}")
                    muestra = listo and tick % 64 == 0
                    umbral = 40
                    fondos = caja >= CAJA_PARA_COMPRAR
                compra = muestra and acciones == 0 and delta <= -umbral and fondos
                venta = muestra and acciones > 0 and delta >= umbral
            publicado = int(fila["decision_mmio"], 16)
            miso = int(fila["miso"], 16)
            if ((publicado, miso) != (d["decision_siguiente"], d["decision_recibida"])
                    or compra != (publicado >> 6 == 1) or venta != (publicado >> 6 == 2)):
                raise RuntimeError(f"Señal o desfase inesperado {modo}/{caso}/{tick}")
            ciclos = int(fila["latencia_ciclos"])
            max_ciclos = max(max_ciclos, ciclos)
            writer.writerow((tick, precio, fila["x3"], sma, int(listo), delta, fila["x6"], caja,
                             acciones, d["caja"], d["acciones"], int(compra), int(venta),
                             f"{d['decision_siguiente']:02x}", f"{publicado:02x}", f"{miso:02x}",
                             tick if d["cantidad_ejecutada"] else "", d["cantidad_ejecutada"],
                             d["comision"], d["patrimonio"], ciclos))
    r = referencia.metricas
    return (modo, caso, TICKS, r.patrimonio_final, referencia.compras, referencia.ventas, r.ordenes,
            r.comisiones, r.perdida_maxima, max_ciclos)


def main():
    tools = {name: shutil.which(name) for name in ("iverilog", "vvp", "yosys")}
    if not all(tools.values()):
        raise SystemExit("Faltan iverilog, vvp o yosys en PATH")
    cells = Path(tools["yosys"]).resolve().parents[1] / "share/yosys/ice40/cells_sim.v"
    firmware = {
        "base": MMIO/"sw/trade.hex",
        "conservar": EXTERNO/"build_conservar/trade.hex",
        "activo": EXTERNO/"build_activo/trade.hex",
    }
    rtl = [EXTERNO/"trade_spi_externo.v", TRAZAS/"rtl/pochoco_soc_cpu_trace.v",
           TRAZAS/"rtl/espino_core_cpu_trace.v"]
    rtl.extend(MMIO/f"rtl/{name}.v" for name in ("pochoco_ram", "pochoco_spi_slave", "pochoco_sma10"))
    rtl.extend(sorted((ROOT/"rtl/espino_core").glob("*.v")))
    contextos = []
    with TemporaryDirectory(prefix="diag-p4-") as tmp:
        for modo, hex_file in firmware.items():
            carpeta = HERE / modo
            carpeta.mkdir(exist_ok=True)
            vvp = Path(tmp) / f"{modo}.vvp"
            words = len(hex_file.read_text(encoding="ascii").split())
            path_hex = hex_file.relative_to(ROOT).as_posix()
            ejecutar([tools["iverilog"], "-g2012", "-s", "tb_diagnostico",
                      f"-Ptb_diagnostico.PALABRAS={words}",
                      f'-Ptb_diagnostico.FIRMWARE="{path_hex}"',
                      "-o", vvp, HERE/"tb_diagnostico.sv", *rtl, cells],
                     carpeta / "compilacion.log")
            print(f"HEX {modo} SHA-256 {sha256(hex_file.read_bytes()).hexdigest().upper()}", flush=True)
            for caso, precios in escenarios().items():
                path = carpeta / caso
                path.mkdir(exist_ok=True)
                ref = simular_estrategia(precios, modo, politica(modo))
                escribir_vectores(path, precios, ref)
                contextos.append((modo, caso, path, precios, ref, vvp))

        def probar(ctx):
            modo, caso, path, precios, ref, vvp = ctx
            log = ejecutar([tools["vvp"], "-n", vvp, f"+vectores={path.as_posix()}"],
                           path / "icarus.log")
            if f"PASS {TICKS} ticks" not in log:
                raise RuntimeError(f"Falta PASS RTL {modo}/{caso}")
            resultados = cotejar(path, modo, caso, precios, ref)
            print(f"PASS {modo}/{caso}: compras={ref.compras} ventas={ref.ventas}", flush=True)
            return resultados

        with ThreadPoolExecutor(max_workers=4) as pool:
            resultados = list(pool.map(probar, contextos))

    with (HERE / "resumen_escenarios.csv").open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(("modo", "escenario", "ticks", "patrimonio_final", "compras", "ventas",
                         "ordenes", "comisiones", "drawdown", "peor_ciclo"))
        writer.writerows(resultados)


if __name__ == "__main__":
    main()
