"""Estrategias causales para la simulacion del Proyecto 4.

Toda la aritmetica de señales es entera. Las decisiones usan el formato SPI:
00 mantener, 01 comprar, 10 vender; la cantidad ocupa seis bits (0..63).
"""

from dataclasses import dataclass
from enum import IntEnum
from typing import Sequence


class Accion(IntEnum):
    MANTENER = 0b00
    COMPRAR = 0b01
    VENDER = 0b10


@dataclass(frozen=True)
class Decision:
    accion: Accion = Accion.MANTENER
    cantidad: int = 0

    def __post_init__(self) -> None:
        object.__setattr__(self, "accion", Accion(self.accion))
        if not 0 <= self.cantidad <= 63:
            raise ValueError("La cantidad debe estar entre 0 y 63")

    @property
    def byte(self) -> int:
        return (int(self.accion) << 6) | self.cantidad

    @classmethod
    def desde_byte(cls, byte: int) -> "Decision":
        if not 0 <= byte <= 255:
            raise ValueError("El byte de decision debe estar entre 0 y 255")
        accion = (byte >> 6) & 0b11
        # La FPGA maestra interpreta 11 como mantener.
        if accion == 0b11:
            accion = Accion.MANTENER
        return cls(Accion(accion), byte & 0b111111)


MANTENER = Decision()
VENTANA_CORTA = 5
VENTANA_LARGA = 10
PERIODO_MOMENTUM = 3
CANTIDAD_TRADING = 1


def estrategia_no_operar(
    historial: Sequence[int], acciones: int, tick: int = 0,
    ultimo_tick_operacion: int | None = None,
) -> Decision:
    """Referencia A: conservar la caja y no enviar ordenes."""
    return MANTENER


def estrategia_mantener(
    historial: Sequence[int], acciones: int, tick: int = 0,
    ultimo_tick_operacion: int | None = None,
) -> Decision:
    """Mantiene la posicion existente; se usa despues de la compra inicial."""
    return MANTENER


def _momento_y_tendencia(historial: Sequence[int]) -> tuple[int, int]:
    """Devuelve (tendencia SMA, momentum); tendencia es -1, 0 o +1."""
    if len(historial) < VENTANA_LARGA:
        return 0, 0
    suma_corta = sum(historial[-VENTANA_CORTA:])
    suma_larga = sum(historial[-VENTANA_LARGA:])
    delta = 2 * suma_corta - suma_larga
    tendencia = 1 if delta > 0 else (-1 if delta < 0 else 0)
    momentum = historial[-1] - historial[-1 - PERIODO_MOMENTUM]
    return tendencia, momentum


def estrategia_trading(
    historial: Sequence[int], acciones: int, tick: int = 0,
    ultimo_tick_operacion: int | None = None, cantidad: int = CANTIDAD_TRADING,
) -> Decision:
    """Cruce SMA 5/10 confirmado por momentum de tres intervalos.

    Se comparan sumas escaladas (2 * suma_corta contra suma_larga), sin dividir.
    Momentum es el signo de precio_actual - precio_de_hace_tres_ticks. La
    decision se calcula al cerrar el tick recibido y solo podra ejecutarse en
    el tick siguiente. La estrategia compra o vende una accion por señal.
    """
    tendencia, momentum = _momento_y_tendencia(historial)

    if tendencia > 0 and momentum > 0:
        return Decision(Accion.COMPRAR, cantidad)
    if tendencia < 0 and momentum < 0 and acciones > 0:
        return Decision(Accion.VENDER, min(cantidad, acciones))
    return MANTENER


def estrategia_sma_umbral(
    historial: Sequence[int], acciones: int, tick: int = 0,
    ultimo_tick_operacion: int | None = None, cantidad: int = CANTIDAD_TRADING,
    umbral: int = 2,
) -> Decision:
    """Variante A: exige momentum absoluto minimo en unidades de precio."""
    if umbral < 0:
        raise ValueError("El umbral no puede ser negativo")
    tendencia, momentum = _momento_y_tendencia(historial)
    if tendencia > 0 and momentum >= umbral:
        return Decision(Accion.COMPRAR, cantidad)
    if tendencia < 0 and momentum <= -umbral and acciones > 0:
        return Decision(Accion.VENDER, min(cantidad, acciones))
    return MANTENER


def estrategia_tendencia_confirmada(
    historial: Sequence[int], acciones: int, tick: int = 0,
    ultimo_tick_operacion: int | None = None, cantidad: int = CANTIDAD_TRADING,
) -> Decision:
    """Variante B: confirma SMA por dos cierres y opera solo entrada/salida.

    Solo abre una posicion estando plano; solo cierra esa posicion ante dos
    tendencias bajistas consecutivas y momentum negativo. Esto limita la
    frecuencia y mantiene la posicion en un maximo de 63 acciones.
    """
    if len(historial) < VENTANA_LARGA + 1:
        return MANTENER
    tendencia_actual, momentum = _momento_y_tendencia(historial)
    tendencia_previa, _ = _momento_y_tendencia(historial[:-1])
    q = min(63, cantidad)
    if tendencia_actual > 0 and tendencia_previa > 0 and momentum > 0 and acciones == 0:
        return Decision(Accion.COMPRAR, q)
    if tendencia_actual < 0 and tendencia_previa < 0 and momentum < 0 and acciones > 0:
        return Decision(Accion.VENDER, min(63, acciones))
    return MANTENER


def estrategia_sma_umbral_cooldown(
    historial: Sequence[int], acciones: int, tick: int = 0,
    ultimo_tick_operacion: int | None = None, cantidad: int = CANTIDAD_TRADING,
    umbral: int = 2, cooldown: int = 5,
) -> Decision:
    """Variante C: umbral de momentum y pausa tras cada orden ejecutada."""
    if cooldown < 0:
        raise ValueError("El cooldown no puede ser negativo")
    if ultimo_tick_operacion is not None and tick - ultimo_tick_operacion < cooldown:
        return MANTENER
    return estrategia_sma_umbral(
        historial, acciones, tick, ultimo_tick_operacion, cantidad, umbral
    )
