"""Selección temporal de estrategias con mayor exposición y turnos causales."""

import argparse
import csv
from dataclasses import asdict
from hashlib import sha256
from itertools import product
import json
from pathlib import Path

from estrategia_agresiva import EXPOSICIONES, FAMILIAS, Estado, Parametros, crear_politica
from estrategia import Accion, Decision, MANTENER, estrategia_mantener, estrategia_no_operar
from simulador import CAPITAL_INICIAL, COMISION, ejecutar_decision, leer_precios, simular_estrategia

HERE = Path(__file__).resolve().parent
PERIODOS = (16, 32, 64, 128)
UMBRALES = (2, 4, 8)
FIN_ENTRENAMIENTO = 12000
FIN_VALIDACION = 16000
LIMITE_DRAWDOWN = 5000
COMISION_ENTRENAMIENTO_MAX = 1000
COMISION_VALIDACION_MAX = 400


def comprar_mantener_oficial(precios):
    """Referencia teórica del profesor; su cantidad inicial puede superar 63."""
    cantidad = (CAPITAL_INICIAL - COMISION) // precios[0]
    vale = CAPITAL_INICIAL - cantidad * precios[0] - COMISION + cantidad * precios[-1]
    return vale, cantidad


def medir(precios, config):
    """Cartera ligera para grilla; comparte los fills oficiales con el simulador."""
    estado = Estado(config)
    caja = patrimonio = pico = CAPITAL_INICIAL
    acciones = compras = ventas = comisiones = drawdown = max_orden = 0
    max_exposicion = cantidad_comprada = 0
    pendiente = MANTENER
    for tick, precio in enumerate(precios):
        if pendiente.accion != Accion.MANTENER:
            fill = ejecutar_decision(caja, acciones, pendiente, precio)
            caja, acciones = fill.caja, fill.acciones
            if fill.cantidad_ejecutada:
                comisiones += fill.comision
                max_orden = max(max_orden, fill.cantidad_ejecutada)
                if pendiente.accion == Accion.COMPRAR:
                    compras += 1
                    cantidad_comprada += fill.cantidad_ejecutada
                else:
                    ventas += 1
        patrimonio = caja + acciones * precio
        pico = max(pico, patrimonio)
        drawdown = max(drawdown, pico - patrimonio)
        max_exposicion = max(max_exposicion, (10000 * acciones * precio) // max(1, patrimonio))
        pendiente = estado.decidir(tick, precio, caja, acciones)
    bh, _ = comprar_mantener_oficial(precios)
    return {
        "patrimonio": patrimonio, "neto_vs_mantener_oficial": patrimonio - bh,
        "drawdown": drawdown, "compras": compras, "ventas": ventas,
        "ordenes": compras + ventas, "comisiones": comisiones, "caja": caja,
        "acciones": acciones, "max_fill": max_orden, "acciones_compradas": cantidad_comprada,
        "exposicion_max_bps": max_exposicion,
    }


def escribir_csv(path, filas):
    filas = list(filas)
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(filas[0]))
        writer.writeheader()
        writer.writerows(filas)


def admisible(resultado, limite_comisiones):
    return resultado["drawdown"] <= LIMITE_DRAWDOWN and resultado["comisiones"] <= limite_comisiones


def seleccionar(entrenamiento, validacion, salida):
    """Ranking financiero; drawdown y comisiones sirven exclusivamente de filtros."""
    candidatos, filas = [], []
    poblacion = product(FAMILIAS, EXPOSICIONES, (False, True))
    for familia, exposicion, progresiva in poblacion:
        grupo = []
        for periodo, umbral in product(PERIODOS, UMBRALES):
            cfg = Parametros(familia, exposicion, progresiva, periodo, umbral)
            met = medir(entrenamiento, cfg)
            ok = admisible(met, COMISION_ENTRENAMIENTO_MAX)
            grupo.append((cfg, met, ok))
            filas.append({**asdict(cfg), **met, "admisible": int(ok)})
        aptos = [c for c in grupo if c[2]]
        config, ent, pasa_ent = max(aptos or grupo, key=lambda c: c[1]["neto_vs_mantener_oficial"])
        val = medir(validacion, config)
        candidatos.append({
            "config": asdict(config), "entrenamiento": ent, "validacion": val,
            "admisible_entrenamiento": pasa_ent,
            "admisible_validacion": admisible(val, COMISION_VALIDACION_MAX),
        })
    escribir_csv(salida/"grilla_entrenamiento.csv", filas)
    elegibles = [c for c in candidatos if c["admisible_entrenamiento"] and c["admisible_validacion"]]
    if not elegibles:
        raise RuntimeError("Ninguna política cumple las restricciones de riesgo predefinidas")
    ganador = max(elegibles, key=lambda c: (c["validacion"]["neto_vs_mantener_oficial"],
                                          c["entrenamiento"]["neto_vs_mantener_oficial"]))
    freeze = {
        **ganador, "finalistas": candidatos,
        "metodo": "Elegir por patrimonio neto el mejor admisible de cada familia/exposición/escalonado "
                  "en entrenamiento y seleccionar por diferencia neta en validación. "
                  "Si una celda carece de admisibles, su mejor resultado se conserva solo en la comparación.",
        "sha256_ajuste_y_validacion": sha256(bytes(entrenamiento + validacion)).hexdigest().upper(),
        "tramos": {"entrenamiento": [0, FIN_ENTRENAMIENTO], "validacion": [FIN_ENTRENAMIENTO, FIN_VALIDACION],
                   "prueba": [FIN_VALIDACION, 20000]},
        "riesgo": {"max_drawdown_absoluto": LIMITE_DRAWDOWN,
                   "max_comisiones_entrenamiento": COMISION_ENTRENAMIENTO_MAX,
                   "max_comisiones_validacion": COMISION_VALIDACION_MAX},
    }
    with (salida/"seleccion.json").open("x", encoding="utf-8") as stream:
        json.dump(freeze, stream, ensure_ascii=False, indent=2)
    return freeze


def resumen_referencia(nombre, r, bh_oficial, bh_ejecutable):
    m = r.metricas
    return {
        "nombre": nombre, "patrimonio": m.patrimonio_final, "rentabilidad_pct": m.rentabilidad_pct,
        "vs_mantener_oficial": m.patrimonio_final - bh_oficial,
        "vs_mantener_ejecutable": m.patrimonio_final - bh_ejecutable, "caja": m.caja_final,
        "acciones": m.acciones_finales, "compras": r.compras, "ventas": r.ventas, "ordenes": m.ordenes,
        "comisiones": m.comisiones, "drawdown": m.perdida_maxima,
    }


def evaluar(precios, freeze, salida):
    ganador = Parametros(**freeze["config"])
    resumen, finalistas = [], []
    cortes = (
        ("entrenamiento", 0, FIN_ENTRENAMIENTO), ("validacion", FIN_ENTRENAMIENTO, FIN_VALIDACION),
        ("prueba", FIN_VALIDACION, len(precios)), ("completa", 0, len(precios)),
    )
    for segmento, desde, hasta in cortes:
        muestra = precios[desde:hasta]
        bh = simular_estrategia(muestra, "Comprar y mantener (máximo 63)",
                                estrategia_mantener, Decision(Accion.COMPRAR, 63))
        cash = simular_estrategia(muestra, "No operar", estrategia_no_operar)
        traza = [] if segmento == "completa" else None
        cand = simular_estrategia(muestra, "Agresiva congelada", crear_politica(ganador, traza))
        oficial, q_oficial = comprar_mantener_oficial(muestra)
        for r in (cash, bh, cand):
            resumen.append({"segmento": segmento, "inicio": desde, "fin": hasta, "ticks": len(muestra),
                            "mantener_oficial": oficial, "cantidad_mantener_oficial": q_oficial,
                            **resumen_referencia(r.nombre, r, oficial, bh.metricas.patrimonio_final)})
        for f in freeze["finalistas"]:
            cfg = Parametros(**f["config"])
            met = medir(muestra, cfg)
            finalistas.append({"segmento": segmento, "ticks": len(muestra), **f["config"], **met,
                               "vs_mantener_ejecutable": met["patrimonio"] - bh.metricas.patrimonio_final,
                               "seleccionada": int(cfg == ganador)})
        met = medir(muestra, ganador)
        if (met["patrimonio"], met["ordenes"], met["drawdown"]) != (
                cand.metricas.patrimonio_final, cand.metricas.ordenes, cand.metricas.perdida_maxima):
            raise RuntimeError("La grilla ligera y la contabilidad oficial difieren")
        if traza is not None:
            escribir_csv(salida/"decisiones_tick.csv", ({**row, **t} for row, t in zip(cand.decisiones, traza, strict=True)))
    escribir_csv(salida/"comparacion.csv", resumen)
    escribir_csv(salida/"finalistas_todas_exposiciones.csv", finalistas)
    for fila in (r for r in resumen if r["nombre"] == "Agresiva congelada"):
        print(fila, flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--serie", type=Path, default=HERE.parents[1]/"resultados/validacion_oficial/practica_meta.csv")
    parser.add_argument("--salida", type=Path, default=HERE/"resultados")
    parser.add_argument("--fase", choices=("seleccionar", "evaluar", "completa"), default="completa")
    parser.add_argument("--congelada", type=Path, help="Selección previamente registrada; solo para evaluar")
    args = parser.parse_args()
    if args.congelada is not None and args.fase != "evaluar":
        parser.error("--congelada requiere --fase evaluar")
    precios = leer_precios(args.serie)
    args.salida.mkdir(parents=True, exist_ok=True)
    freeze_path = args.congelada or args.salida/"seleccion.json"
    if args.fase != "evaluar":
        if freeze_path.exists():
            raise SystemExit("La selección ya está congelada. Use --fase evaluar.")
        freeze = seleccionar(precios[:FIN_ENTRENAMIENTO], precios[FIN_ENTRENAMIENTO:FIN_VALIDACION], args.salida)
        print("Selección congelada antes de calcular el tramo reservado:", freeze["config"], flush=True)
    if args.fase != "seleccionar":
        with freeze_path.open(encoding="utf-8") as stream:
            evaluar(precios, json.load(stream), args.salida)


if __name__ == "__main__":
    main()
