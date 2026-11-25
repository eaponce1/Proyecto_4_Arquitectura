"""Estrategia híbrida causal y referencias de investigación del Proyecto 4."""

from dataclasses import dataclass
from pathlib import Path
import sys

PYTHON_P4 = Path(__file__).resolve().parents[2] / "python"
if str(PYTHON_P4) not in sys.path:
    sys.path.insert(0, str(PYTHON_P4))

from capital_protegido import crear_politica_activa
from enfoques_finales import estrategia_reversion_media
from estrategia import Accion, Decision, MANTENER, estrategia_no_operar
from simulador import CAPITAL_INICIAL, COMISION, ejecutar_decision

PRECIO_MAXIMO = 255
VENTANA_MOMENTUM = 10


@dataclass(frozen=True, order=True)
class Parametros:
    periodo: int = 128
    entrada: int = 8
    salida: int = 8
    confirmacion: int = 0
    cantidad_suave: int = 32
    cantidad_fuerte: int = 63
    reserva: int = 500


# Congelada contra desarrollo/validación; la prueba empieza en el tick 16000.
CANDIDATA = Parametros()


def senal_hibrida(
    tendencia: int,
    momentum: int,
    caja: int,
    manos: int,
    config: Parametros,
) -> Decision:
    """Decide en una revisión; tendencia en precios y momentum en suma escalada."""
    if manos:
        if tendencia <= -config.salida or (tendencia < 0 and momentum <= -config.confirmacion):
            return Decision(Accion.VENDER, manos)
        return MANTENER
    if tendencia < config.entrada or momentum < config.confirmacion:
        return MANTENER

    objetivo = config.cantidad_fuerte if tendencia >= 2 * config.entrada else config.cantidad_suave
    disponible = max(0, (caja - config.reserva - 2 * COMISION) // PRECIO_MAXIMO)
    cantidad = min(objetivo, disponible)
    return Decision(Accion.COMPRAR, cantidad) if cantidad else MANTENER


def crear_politica(config: Parametros = CANDIDATA, traza: list | None = None):
    """Genera una instancia de política con cartera local y órdenes pendientes."""
    caja, posicion = CAPITAL_INICIAL, 0
    ancla = None
    pendiente = MANTENER

    def decidir(historial, acciones, tick, ultima_operacion=None):
        nonlocal caja, posicion, ancla, pendiente
        precio = historial[-1]
        ejecucion = ejecutar_decision(caja, posicion, pendiente, precio)
        caja, posicion = ejecucion.caja, ejecucion.acciones
        if posicion != acciones or caja < config.reserva:
            raise RuntimeError("La cartera local difiere de la maestra o de la reserva")

        listo = len(historial) >= VENTANA_MOMENTUM
        tendencia = precio - ancla if ancla is not None else 0
        momentum = precio * VENTANA_MOMENTUM - sum(historial[-VENTANA_MOMENTUM:]) if listo else 0
        revision = tick % config.periodo == 0
        pendiente = MANTENER
        if revision:
            if ancla is not None and listo:
                pendiente = senal_hibrida(tendencia, momentum, caja, posicion, config)
            ancla = precio

        if traza is not None:
            objetivo = posicion
            if pendiente.accion == Accion.COMPRAR:
                objetivo += pendiente.cantidad
            elif pendiente.accion == Accion.VENDER:
                objetivo -= pendiente.cantidad
            traza.append({
                "revision": int(revision), "tendencia": tendencia, "momentum": momentum,
                "posicion_objetivo": objetivo, "caja_interna": caja,
                "acciones_internas": posicion,
            })
        return pendiente

    return decidir


def _orden_simple(acciones, comprar, vender, cantidad=16):
    if comprar and acciones == 0:
        return Decision(Accion.COMPRAR, cantidad)
    if vender and acciones:
        return Decision(Accion.VENDER, acciones)
    return MANTENER


def cruce_medias(historial, acciones, tick, _):
    if len(historial) < 40 or tick % 64:
        return MANTENER
    delta = 4 * sum(historial[-10:]) - sum(historial[-40:])
    return _orden_simple(acciones, delta >= 80, delta <= -80)


def momentum(historial, acciones, tick, _):
    if len(historial) <= 128 or tick % 64:
        return MANTENER
    cambio = historial[-1] - historial[-129]
    return _orden_simple(acciones, cambio >= 4, cambio <= -4)


def ruptura(historial, acciones, tick, _):
    if len(historial) <= 64 or tick % 16:
        return MANTENER
    pasado = historial[-65:-1]
    precio = historial[-1]
    return _orden_simple(acciones, precio >= max(pasado) + 2, precio <= min(pasado) - 2)


def reversion_filtrada(historial, acciones, tick, _):
    if len(historial) < 10 or tick % 64:
        return MANTENER
    delta = 10 * historial[-1] - sum(historial[-10:])
    return _orden_simple(acciones, delta <= -40, delta >= 40)


def familias(config=CANDIDATA, traza=None):
    """Políticas frescas y sus órdenes iniciales para una corrida independiente."""
    return {
        "No operar": (estrategia_no_operar, MANTENER),
        "Comprar y mantener": (estrategia_no_operar, Decision(Accion.COMPRAR, 63)),
        "SMA10 base": (estrategia_reversion_media, MANTENER),
        "Protección anterior": (crear_politica_activa(), MANTENER),
        "Cruce medias 10/40": (cruce_medias, MANTENER),
        "Momentum 128": (momentum, MANTENER),
        "Ruptura 64": (ruptura, MANTENER),
        "Reversión filtrada": (reversion_filtrada, MANTENER),
        "Híbrida fija 16": (
            crear_politica(Parametros(config.periodo, config.entrada, config.salida,
                                      config.confirmacion, 16, 16, config.reserva)),
            MANTENER,
        ),
        "Adaptativa RV32E": (crear_politica(config, traza), MANTENER),
    }
