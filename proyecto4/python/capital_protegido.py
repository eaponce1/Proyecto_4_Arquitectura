"""Referencia causal de los nuevos programas de conservación y riesgo acotado."""

import argparse
import csv
from pathlib import Path

from enfoques_finales import estrategia_reversion_media
from estrategia import Accion, Decision, MANTENER, estrategia_no_operar
from simulador import CAPITAL_INICIAL, COMISION, ejecutar_decision, leer_precios, simular_estrategia

CANTIDAD = 3
PISO = 9000
PRECIO_MAXIMO = 255
CAJA_PARA_COMPRAR = PISO + PRECIO_MAXIMO * CANTIDAD + 2 * COMISION
MARGEN_SUMA = 40
PERIODO_REVISION = 64


def crear_politica_activa():
    caja = CAPITAL_INICIAL
    posicion = 0
    pendiente = MANTENER

    def decidir(historial, acciones, tick, ultima_operacion):
        nonlocal caja, posicion, pendiente
        precio = historial[-1]
        fill = ejecutar_decision(caja, posicion, pendiente, precio)
        caja, posicion = fill.caja, fill.acciones
        if posicion != acciones or caja + posicion * precio < PISO:
            raise RuntimeError("La cartera activa incumplió el modelo o el piso")
        pendiente = MANTENER
        if len(historial) >= 10 and tick % PERIODO_REVISION == 0:
            delta = 10 * precio - sum(historial[-10:])
            if posicion == 0 and delta <= -MARGEN_SUMA and caja >= CAJA_PARA_COMPRAR:
                pendiente = Decision(Accion.COMPRAR, CANTIDAD)
            elif posicion and delta >= MARGEN_SUMA:
                pendiente = Decision(Accion.VENDER, posicion)
        return pendiente

    return decidir


def precios_prueba_reserva():
    """Vector sintético para coste máximo de compra, venta a pérdida y bloqueo de reentrada."""
    return [200]*64 + [150, 255] + [100]*62 + [255, 1] + [200]*62 + [150, 255]


def main():
    proyecto = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--serie", type=Path, default=proyecto / "data/practica_meta.csv")
    parser.add_argument("--salida", type=Path, default=proyecto / "resultados/capital_protegido.csv")
    args = parser.parse_args()
    precios = leer_precios(args.serie)
    with args.salida.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.writer(stream)
        writer.writerow(("serie", "modo", "ticks", "patrimonio_final", "retorno_pct",
                         "patrimonio_minimo", "ordenes", "compras", "ventas", "comisiones", "drawdown"))
        segmentos = {"completa": precios, "primeros_2000": precios[:2000]}
        segmentos.update({f"bloque_{i+1}": precios[i*5000:(i+1)*5000] for i in range(4)})
        for nombre, segmento in segmentos.items():
            for modo, politica in (("base", estrategia_reversion_media),
                                   ("conservar", estrategia_no_operar),
                                   ("activo", crear_politica_activa())):
                r = simular_estrategia(segmento, modo, politica)
                m = r.metricas
                writer.writerow((nombre, modo, len(segmento), m.patrimonio_final, m.rentabilidad_pct,
                                 min(CAPITAL_INICIAL, min(r.patrimonios)), m.ordenes, r.compras,
                                 r.ventas, m.comisiones, m.perdida_maxima))
    print(args.salida)


if __name__ == "__main__":
    main()
