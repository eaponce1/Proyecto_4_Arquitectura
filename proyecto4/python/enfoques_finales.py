"""Tres estrategias finales causales, deterministas y RV32E-friendly."""

from collections.abc import Sequence

try:
    from .estrategia import Accion, Decision, MANTENER, VENTANA_LARGA, VENTANA_CORTA
except ImportError:
    from estrategia import Accion, Decision, MANTENER, VENTANA_LARGA, VENTANA_CORTA


CANTIDAD_ORDEN = 16
UMBRAL_MOMENTUM = 1
HORIZONTE_MOMENTUM = 4
UMBRAL_MEDIA = 1
CONFIRMACIONES_TENDENCIA = 2


def estrategia_momentum_umbral(
    historial: Sequence[int], acciones: int, tick: int = 0,
    ultimo_tick_operacion: int | None = None,
) -> Decision:
    """A: entra con momentum alcista y sale con momentum bajista de cuatro ticks.

    Usa q=16 y umbral de un punto de precio: el desplazamiento de señal por
    tamaño es $16, mayor que los $10 de comisión de un ciclo compra/venta.
    Se mantiene una sola posicion para no acumular órdenes del mismo lado.
    """
    if len(historial) <= HORIZONTE_MOMENTUM:
        return MANTENER
    cambio = historial[-1] - historial[-1 - HORIZONTE_MOMENTUM]
    if acciones == 0 and cambio >= UMBRAL_MOMENTUM:
        return Decision(Accion.COMPRAR, CANTIDAD_ORDEN)
    if acciones > 0 and cambio <= -UMBRAL_MOMENTUM:
        return Decision(Accion.VENDER, min(CANTIDAD_ORDEN, acciones))
    return MANTENER


def estrategia_reversion_media(
    historial: Sequence[int], acciones: int, tick: int = 0,
    ultimo_tick_operacion: int | None = None,
) -> Decision:
    """B: compra 1 unidad bajo SMA10 y vende 1 unidad sobre SMA10.

    Se compara 10*precio con la suma de diez precios. La multiplicación por
    diez se implementa en RV32E como (8*p)+(2*p), cuatro sumas, sin MUL/DIV.
    q=16 y una separación de un punto a cada lado del promedio fijan el umbral.
    """
    if len(historial) < VENTANA_LARGA:
        return MANTENER
    suma_media = sum(historial[-VENTANA_LARGA:])
    precio = historial[-1]
    precio_por_dos = precio + precio  # 2*p
    precio_por_cuatro = precio_por_dos + precio_por_dos  # 4*p
    precio_por_ocho = precio_por_cuatro + precio_por_cuatro  # 8*p
    precio_por_diez = precio_por_ocho + precio_por_dos  # 10*p, cuatro sumas
    margen = VENTANA_LARGA  # 10 * umbral_media; umbral_media queda fijo en 1
    if acciones == 0 and precio_por_diez <= suma_media - margen:
        return Decision(Accion.COMPRAR, CANTIDAD_ORDEN)
    if acciones > 0 and precio_por_diez >= suma_media + margen:
        return Decision(Accion.VENDER, min(CANTIDAD_ORDEN, acciones))
    return MANTENER


def _tendencia_sma(historial: Sequence[int], ticks_atras: int = 0) -> int:
    fin = len(historial) - ticks_atras
    if fin < VENTANA_LARGA:
        return 0
    suma_corta = sum(historial[fin - VENTANA_CORTA:fin])
    suma_larga = sum(historial[fin - VENTANA_LARGA:fin])
    doble_suma_corta = suma_corta + suma_corta
    diferencia = doble_suma_corta - suma_larga
    return 1 if diferencia > 0 else (-1 if diferencia < 0 else 0)


def estrategia_tendencia_persistente(
    historial: Sequence[int], acciones: int, tick: int = 0,
    ultimo_tick_operacion: int | None = None,
) -> Decision:
    """C: exige dos cierres consecutivos de la misma señal SMA5/SMA10.

    Abre q=16 estando plano y mantiene hasta una señal bajista confirmada en dos
    cierres consecutivos. La decisión no replica una señal intratick.
    """
    if len(historial) < VENTANA_LARGA + 1:
        return MANTENER
    actual = _tendencia_sma(historial)
    previo = _tendencia_sma(historial, ticks_atras=1)
    if acciones == 0 and actual > 0 and previo > 0:
        return Decision(Accion.COMPRAR, CANTIDAD_ORDEN)
    if acciones > 0 and actual < 0 and previo < 0:
        return Decision(Accion.VENDER, min(CANTIDAD_ORDEN, acciones))
    return MANTENER
