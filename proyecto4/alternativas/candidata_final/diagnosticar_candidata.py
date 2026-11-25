"""Pruebas de mercado sintéticas y smoke de las rondas largas por SPI real en RTL."""

from concurrent.futures import ThreadPoolExecutor
import csv
from pathlib import Path
import shutil

from estrategia_referencia import crear_politica
from simulador import leer_precios, simular_estrategia
from validar_candidata import HERE, ROOT, HARDWARE, TRACE, MMIO, ejecutar, preparar, words_from_hex


def escenarios():
    ticks = range(386)
    return {
        "A_creciente": [60+i//8 for i in ticks],
        "B_decreciente": [180-i//8 for i in ticks],
        "C_lateral": [100+i%3-1 for i in ticks],
        "D_caida": [100]*128 + [130]*128 + [70]*130,
        "E_subida": [100]*128 + [130]*258,
        "F_recuperacion": [100]*64 + [80]*128 + [112]*128 + [90]*66,
    }


def main():
    out = HERE/"build/escenarios"
    out.mkdir(parents=True, exist_ok=True)
    run = {key: shutil.which(key) for key in ("iverilog", "vvp", "yosys")}
    if not all(run.values()):
        raise SystemExit("Icarus o Yosys no está en PATH")
    cells = Path(run["yosys"]).resolve().parents[1]/"share/yosys/ice40/cells_sim.v"
    rtl = [HARDWARE/"trade_spi_externo.v", TRACE/"rtl/pochoco_soc_cpu_trace.v",
           TRACE/"rtl/espino_core_cpu_trace.v"]
    rtl.extend(MMIO/f"rtl/{p}.v" for p in ("pochoco_ram", "pochoco_spi_slave", "pochoco_sma10"))
    rtl.extend(sorted((ROOT/"rtl/espino_core").glob("*.v")))
    fw = HERE/"trade_candidate.hex"
    words = words_from_hex(fw)

    def probar(nombre, precios, periodo):
        carpeta = out/nombre
        m = preparar(precios, carpeta, words)
        exe = carpeta/"tb.vvp"
        medir = carpeta/"rtl.csv"
        ejecutar([run["iverilog"], "-g2012", "-s", "tb_candidata", f"-Ptb_candidata.TICKS={len(precios)}",
                  f"-Ptb_candidata.PERIODO_NS={periodo}", f"-Ptb_candidata.PALABRAS_FIRMWARE={len(words)}",
                  f'-Ptb_candidata.ARCHIVO_FIRMWARE="{fw.relative_to(ROOT).as_posix()}"',
                  "-Ptb_candidata.REG_CAJA=15", "-Ptb_candidata.REG_ACCIONES=5",
                  "-o", exe, HERE/"tb/tb_candidata.sv", *rtl, cells], carpeta/"compilacion.log")
        log = ejecutar([run["vvp"], "-n", exe, f"+vectores={carpeta.as_posix()}",
                        f"+cartera={(carpeta/'cartera.hex').as_posix()}", f"+metricas={medir.as_posix()}"],
                       carpeta/"simulacion.log")
        if f"PASS {len(precios)} MISO frente a Python" not in log:
            raise RuntimeError(f"Escrituras incompletas: {nombre}")
        traza = []
        r = simular_estrategia(precios, nombre, crear_politica(traza=traza))
        with medir.open(newline="") as stream:
            datos = list(csv.DictReader(stream))
        with (carpeta/"traza.csv").open("w", encoding="utf-8", newline="") as stream:
            campos = (*datos[0], "tendencia_ref", "momentum_ref", "posicion_objetivo_ref",
                      "senal_compra", "senal_venta", "accion_recibida", "tick_ejecucion")
            writer = csv.DictWriter(stream, fieldnames=campos)
            writer.writeheader()
            for actual, ref, tick in zip(datos, traza, r.decisiones, strict=True):
                accion_siguiente = tick["accion_siguiente"]
                writer.writerow({
                    **actual, "tendencia_ref": ref["tendencia"], "momentum_ref": ref["momentum"],
                    "posicion_objetivo_ref": ref["posicion_objetivo"],
                    "senal_compra": int(accion_siguiente == "comprar"),
                    "senal_venta": int(accion_siguiente == "vender"),
                    "accion_recibida": tick["accion_recibida"],
                    "tick_ejecucion": tick["tick"] if tick["cantidad_ejecutada"] else "",
                })
        print(f"PASS {nombre}: {len(precios)} ticks, {r.compras} compras y {r.ventas} ventas", flush=True)
        return nombre, periodo, len(precios), r.compras, r.ventas, m.patrimonio_final, m.perdida_maxima

    tareas = [(nombre, precios, 30000) for nombre, precios in escenarios().items()]
    oficiales = leer_precios()
    tareas += [("ronda_1_smoke", oficiales[:4], 10_000_000), ("ronda_2_smoke", oficiales[:8], 1_000_000)]
    with ThreadPoolExecutor(max_workers=4) as pool:
        resultados = list(pool.map(lambda args: probar(*args), tareas))
    if not any(r[3] and r[4] for r in resultados[:6]):
        raise RuntimeError("La batería carece de un ciclo completo de compra y venta")
    with (out/"resumen.csv").open("w", encoding="utf-8", newline="") as stream:
        writer = csv.writer(stream)
        writer.writerow(("escenario", "periodo_ns", "ticks", "compras", "ventas", "patrimonio", "drawdown"))
        writer.writerows(resultados)


if __name__ == "__main__":
    main()
