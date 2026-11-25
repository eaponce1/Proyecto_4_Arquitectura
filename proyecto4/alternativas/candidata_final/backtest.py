"""Análisis de práctica con selección temporal y evaluación congelada de la candidata."""

import argparse
import csv
from dataclasses import replace
from itertools import product
from pathlib import Path
from statistics import median

from estrategia_referencia import CANDIDATA, Parametros, familias, senal_hibrida
from estrategia import Accion, Decision, MANTENER
from metricas import _grafico_lineas, graficar_precios
from simulador import CAPITAL_INICIAL, ejecutar_decision, leer_precios, simular_estrategia

CARPETA = Path(__file__).resolve().parent
SERIE_OFICIAL = CARPETA.parents[1] / "resultados/validacion_oficial/practica_meta.csv"
REFERENCIA = "Comprar y mantener"
ELEGIDA = "Adaptativa RV32E"


def escritura_csv(path, cabecera, filas):
    with path.open("w", newline="", encoding="utf-8") as stream:
        out = csv.writer(stream)
        out.writerow(cabecera)
        out.writerows(filas)


def preparar(precios):
    """Calcula momentum usando exclusivamente los 10 precios terminados en el tick."""
    return [(p, 10*p - sum(precios[i-9:i+1]) if i >= 9 else 0)
            for i, p in enumerate(precios)]


def medir_periodica(datos, config, stop=0):
    """Cartera sin trazas para la grilla, con ejecución oficial y decisión compartida."""
    caja = pico = CAPITAL_INICIAL
    acciones = ordenes = dd = 0
    pendiente = MANTENER
    ancla = datos[0][0]
    revision = config.periodo
    max_precio = 0
    for i, (precio, mom) in enumerate(datos):
        if pendiente.cantidad:
            fill = ejecutar_decision(caja, acciones, pendiente, precio)
            caja, acciones = fill.caja, fill.acciones
            ordenes += int(fill.cantidad_ejecutada > 0)
            pendiente = MANTENER
        patrimonio = caja + acciones * precio
        pico = max(pico, patrimonio)
        dd = max(dd, pico - patrimonio)
        if stop:
            max_precio = max(max_precio, precio) if acciones else 0
            if acciones and max_precio - precio >= stop:
                pendiente = Decision(Accion.VENDER, acciones)
        if i == revision:
            if not pendiente.cantidad:
                pendiente = senal_hibrida(precio - ancla, mom, caja, acciones, config)
            ancla = precio
            revision += config.periodo
    return patrimonio, dd, ordenes


def grilla():
    for paso, (entrada, salida), conf, (suave, fuerte), reserva in product(
        (32, 64, 128, 256, 512), ((1, 1), (2, 2), (4, 4), (8, 4), (8, 8), (12, 8)),
        (0, 10), ((3, 16), (8, 32), (16, 63), (32, 63)), (500, 1500),
    ):
        yield Parametros(paso, entrada, salida, conf, suave, fuerte, reserva)


def seleccionar(desarrollo, validacion):
    """Selecciona usando dos intervalos cronológicos y tres cortes de desarrollo."""
    dev, val = preparar(desarrollo), preparar(validacion)
    cortes = [preparar(desarrollo[i*len(dev)//3:(i+1)*len(dev)//3]) for i in range(3)]
    filas = []
    for config in grilla():
        dp, dd, dordenes = medir_periodica(dev, config)
        vp, vd, vordenes = medir_periodica(val, config)
        resultados = [medir_periodica(corte, config) for corte in cortes]
        patrimonios = [p for p, _, _ in resultados]
        peor_dd = max(dd, vd, *(d for _, d, _ in resultados))
        admisible = dp >= 10000 and dd <= 1700 and dordenes >= 4 and min(patrimonios) >= 9600 and vp >= 9700
        puntos = (100*(vp-10000) + 35*(dp-10000) +
                  20*(median(patrimonios)-10000) - 20*peor_dd)
        filas.append((config, dp, dd, dordenes, vp, vd, vordenes,
                      *patrimonios, peor_dd, int(admisible), puntos/100))
    elegibles = [r for r in filas if r[-2]]
    elegida = max(elegibles, key=lambda r: (r[-1], r[0]))[0] if elegibles else None
    return elegida, filas


def evaluar_familias(precios, config=CANDIDATA, traza=None):
    return {
        nombre: simular_estrategia(precios, nombre, politica, primera)
        for nombre, (politica, primera) in familias(config, traza).items()
    }


def filas_resumen(etiqueta, inicio, fin, resultados):
    mantener = resultados[REFERENCIA].metricas.patrimonio_final
    for nombre, r in resultados.items():
        m = r.metricas
        yield (etiqueta, inicio, fin, nombre, m.patrimonio_final, f"{m.rentabilidad_pct:.2f}",
               m.patrimonio_final - mantener, r.compras, r.ventas, m.ordenes,
               m.comisiones, m.perdida_maxima, m.acciones_finales, m.caja_final)


CONFIG_FIELDS = tuple(Parametros.__dataclass_fields__)


def guardar_busqueda(precios, salida):
    # La última quinta parte no entra a ninguna calibración.
    desarrollo, validacion = precios[:12000], precios[12000:16000]
    ganadora, filas = seleccionar(desarrollo, validacion)
    escritura_csv(
        salida/"busqueda_desarrollo_validacion.csv",
        (*CONFIG_FIELDS, "desarrollo", "dd_desarrollo", "ordenes_desarrollo", "validacion",
         "dd_validacion", "ordenes_validacion", "dev_1", "dev_2", "dev_3",
         "peor_drawdown", "admisible", "puntaje"),
        ((*(getattr(cfg, campo) for campo in CONFIG_FIELDS), *mediciones)
         for cfg, *mediciones in filas),
    )
    if ganadora != CANDIDATA:
        raise RuntimeError(f"La grilla oficial eligió {ganadora}. La ROM congelada usa {CANDIDATA}.")

    dev = preparar(desarrollo)
    # Barrido 1–63 con la configuración restante fija y dos intensidades.
    escritura_csv(
        salida/"sensibilidad_volumen.csv", ("suave", "fuerte", "patrimonio", "drawdown", "ordenes"),
        ((max(1, q//2), q, *medir_periodica(dev, replace(CANDIDATA, cantidad_suave=max(1, q//2),
                                                         cantidad_fuerte=q)))
         for q in range(1, 64)),
    )
    escritura_csv(
        salida/"sensibilidad_proteccion.csv",
        ("stop_distancia", "patrimonio_desarrollo", "drawdown", "ordenes"),
        ((stop, *medir_periodica(dev, CANDIDATA, stop)) for stop in (0, 12, 24, 36)),
    )

    walk = []
    for corte in (6000, 8000, 10000, 12000, 14000):
        config, _ = seleccionar(precios[:corte-2000], precios[corte-2000:corte])
        test = precios[corte:corte+2000]
        resultados = evaluar_familias(test, config or CANDIDATA)
        b = resultados[REFERENCIA].metricas.patrimonio_final
        r = resultados[ELEGIDA if config is not None else "No operar"].metricas
        parametros = [getattr(config, campo) for campo in CONFIG_FIELDS] if config else [""]*len(CONFIG_FIELDS)
        walk.append((corte-2000, corte, corte+2000, "Activa" if config else "No operar",
                     *parametros, r.patrimonio_final, b, r.patrimonio_final-b, r.perdida_maxima))
    escritura_csv(salida/"walk_forward.csv",
                  ("fin_ajuste", "fin_validacion", "fin_prueba", "modo", *CONFIG_FIELDS,
                   "patrimonio", "mantener", "diferencia", "drawdown"), walk)


def guardar_traza(salida, resultado, traza):
    campos = ("tick", "precio", "decision_recibida", "decision_siguiente", "accion_recibida",
              "cantidad_solicitada", "cantidad_ejecutada", "caja", "acciones",
              "comision", "patrimonio", "revision", "tendencia", "momentum",
              "posicion_objetivo", "caja_interna", "acciones_internas")
    escritura_csv(salida/"decisiones_tick.csv", campos,
                  ((fila[campo] if campo in fila else info[campo] for campo in campos)
                   for fila, info in zip(resultado.decisiones, traza, strict=True)))


def graficar(salida, precios, resultados):
    # La cuadrícula de tiempo y el escalado coinciden con la utilidad común de SVG.
    graficar_precios(precios, salida/"precio.svg")
    fuente = (salida/"precio.svg").read_text(encoding="utf-8")
    lo, hi = min(precios), max(precios)
    if lo == hi:
        lo, hi = lo-1, hi+1
    marcas = []
    candidato = resultados[ELEGIDA]
    for op in candidato.operaciones:
        t, p = op["tick_ejecucion"], op["precio_ejecucion"]
        x = 86 + 1190*t/(len(precios)-1)
        y = 70 + (hi-p)*298/(hi-lo)
        color = "#168449" if op["tipo"] == "comprar" else "#da3030"
        marcas.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="5" fill="{color}" stroke="#fff">'
                      f'<title>{op["tipo"]} {op["cantidad_ejecutada"]} a {p}, tick {t}</title></circle>')
    fuente = fuente.replace("</svg>", "\n" + "\n".join(marcas) +
                            '\n<text x="490" y="50" fill="#168449">Compras</text>'
                            '\n<text x="585" y="50" fill="#da3030">Ventas</text>\n</svg>')
    (salida/"senales.svg").write_text(fuente, encoding="utf-8")

    colores = ("#667085", "#16a34a", "#dc2626", "#0f766e", "#7c3aed", "#a16207",
               "#db2777", "#155e75", "#4338ca", "#2563eb")
    _grafico_lineas(salida/"patrimonio.svg", "Patrimonio por estrategia", "Patrimonio ($)",
                    [(nombre, r.patrimonios, color)
                     for (nombre, r), color in zip(resultados.items(), colores, strict=True)])
    mantener = resultados[REFERENCIA].patrimonios
    _grafico_lineas(salida/"vs_mantener.svg", "Diferencia frente a comprar y mantener", "Diferencia ($)",
                    [(nombre, [v-b for v, b in zip(resultados[nombre].patrimonios, mantener, strict=True)], color)
                     for nombre, color in ((ELEGIDA, "#2563eb"), ("SMA10 base", "#dc2626"), ("No operar", "#667085"))])

    comisiones = []
    total = 0
    for row in candidato.decisiones:
        total += row["comision"]
        comisiones.append(total)
    for filename, titulo, unidad, valores in (
        ("inventario", "Inventario de la candidata", "Acciones", candidato.posiciones),
        ("caja", "Caja de la candidata", "Caja ($)", candidato.cajas),
        ("comisiones", "Comisiones acumuladas de la candidata", "Comisiones ($)", comisiones),
    ):
        _grafico_lineas(salida/f"{filename}.svg", titulo, unidad, [(ELEGIDA, valores, "#2563eb")])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--serie", type=Path, default=SERIE_OFICIAL)
    parser.add_argument("--salida", type=Path, default=CARPETA/"resultados")
    parser.add_argument("--solo-evaluar", action="store_true", help="Evalúa la ROM congelada sin recalibrarla.")
    args = parser.parse_args()
    precios = leer_precios(args.serie)
    args.salida.mkdir(parents=True, exist_ok=True)
    if not args.solo_evaluar:
        guardar_busqueda(precios, args.salida)

    traza = []
    completo = evaluar_familias(precios, traza=traza)
    periodos = (("desarrollo", 0, 12000), ("validacion", 12000, 16000), ("prueba", 16000, 20000))
    resumen = list(filas_resumen("completa", 0, 20000, completo))
    for etiqueta, a, b in periodos:
        resumen.extend(filas_resumen(etiqueta, a, b, evaluar_familias(precios[a:b])))
    escritura_csv(
        args.salida/"comparacion.csv",
        ("segmento", "inicio_incluido", "fin_excluido", "estrategia", "patrimonio", "rentabilidad_pct",
         "diferencia_vs_mantener", "compras", "ventas", "ordenes", "comisiones", "drawdown",
         "acciones_finales", "caja_final"), resumen,
    )
    guardar_traza(args.salida, completo[ELEGIDA], traza)
    graficar(args.salida, precios, completo)
    for row in resumen:
        if row[3] == ELEGIDA:
            print(row)


if __name__ == "__main__":
    main()
