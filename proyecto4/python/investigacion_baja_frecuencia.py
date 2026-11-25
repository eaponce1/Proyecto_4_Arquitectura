"""Evalúa reglas causales con menor rotación usando las reglas oficiales."""

import argparse
import csv
from pathlib import Path

from enfoques_finales import estrategia_reversion_media
from estrategia import Accion, Decision, MANTENER, estrategia_mantener, estrategia_no_operar
from simulador import leer_precios, simular_estrategia

PROYECTO = Path(__file__).resolve().parents[1]
PERIODO_REVISION = 64
HORIZONTE_TENDENCIA = 256
MARGEN_PRECIO = 4
CANTIDAD = 16


def sma10_margen_alto(historial, acciones, tick, ultimo):
    if len(historial) < 10:
        return MANTENER
    diferencia = 10 * historial[-1] - sum(historial[-10:])
    if acciones == 0 and diferencia <= -10 * MARGEN_PRECIO:
        return Decision(Accion.COMPRAR, CANTIDAD)
    if acciones > 0 and diferencia >= 10 * MARGEN_PRECIO:
        return Decision(Accion.VENDER, min(CANTIDAD, acciones))
    return MANTENER


def sma10_periodica(historial, acciones, tick, ultimo):
    if tick % PERIODO_REVISION == 0:
        return estrategia_reversion_media(historial, acciones, tick, ultimo)
    return MANTENER


def tendencia_lenta(historial, acciones, tick, ultimo):
    if tick % PERIODO_REVISION != 0 or len(historial) <= HORIZONTE_TENDENCIA:
        return MANTENER
    diferencia = historial[-1] - historial[-1 - HORIZONTE_TENDENCIA]
    if acciones == 0 and diferencia >= MARGEN_PRECIO:
        return Decision(Accion.COMPRAR, CANTIDAD)
    if acciones > 0 and diferencia <= -MARGEN_PRECIO:
        return Decision(Accion.VENDER, min(CANTIDAD, acciones))
    return MANTENER


def comparar(precios):
    estrategias = (
        ("No operar", estrategia_no_operar, MANTENER),
        ("Comprar y mantener", estrategia_mantener, Decision(Accion.COMPRAR, 63)),
        ("SMA10 base", estrategia_reversion_media, MANTENER),
        ("SMA10 umbral 4", sma10_margen_alto, MANTENER),
        ("SMA10 cada 64", sma10_periodica, MANTENER),
        ("Tendencia 256 cada 64", tendencia_lenta, MANTENER),
    )
    segmentos = {"completa": precios, "primeros_2000": precios[:2000]}
    segmentos.update({f"segmento_{i+1}": precios[i*5000:(i+1)*5000] for i in range(4)})
    for segmento, serie in segmentos.items():
        for nombre, politica, inicial in estrategias:
            resultado = simular_estrategia(serie, nombre, politica, decision_inicial=inicial)
            m = resultado.metricas
            yield (segmento, nombre, len(serie), m.patrimonio_final, m.caja_final, m.acciones_finales,
                   m.rentabilidad_pct, m.perdida_maxima, m.ordenes, resultado.compras,
                   resultado.ventas, m.comisiones)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--serie", type=Path, default=PROYECTO / "data/practica_meta.csv")
    parser.add_argument("--salida", type=Path, default=PROYECTO / "resultados/ensayo_baja_frecuencia.csv")
    args = parser.parse_args()
    with args.salida.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.writer(stream)
        writer.writerow(("segmento", "estrategia", "ticks", "patrimonio", "caja", "acciones",
                         "retorno_pct", "drawdown", "ordenes", "compras", "ventas", "comisiones"))
        writer.writerows(comparar(leer_precios(args.serie)))
    print(args.salida)


if __name__ == "__main__":
    main()
