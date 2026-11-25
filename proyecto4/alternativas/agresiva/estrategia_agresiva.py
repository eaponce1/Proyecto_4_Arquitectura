"""Políticas de exposición larga con tamaños enteros y ejecución al tick siguiente."""

from collections import deque
from dataclasses import dataclass
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
PYTHON_P4 = HERE.parents[1] / "python"
if str(PYTHON_P4) not in sys.path:
    sys.path.insert(0, str(PYTHON_P4))

from estrategia import Accion, Decision, MANTENER
from simulador import CAPITAL_INICIAL, COMISION, ejecutar_decision

FAMILIAS = ("momentum", "breakout", "trailing", "hibrida")
EXPOSICIONES = (25, 50, 75, 100)
LIMITE_ORDEN = 63
LOTE_MODERADO = 16
LOTE_MINIMO_ADICIONAL = 4


@dataclass(frozen=True, order=True)
class Parametros:
    familia: str
    exposicion: int
    progresiva: bool
    periodo: int
    umbral: int

    @property
    def distancia_stop(self) -> int:
        return 8 + 2 * self.umbral


def configuracion_congelada() -> Parametros:
    with (HERE / "resultados/seleccion.json").open(encoding="utf-8") as stream:
        return Parametros(**json.load(stream)["config"])


class Estado:
    """Estado causal acotado que solo recibe un precio aplicado por tick."""

    def __init__(self, parametros: Parametros):
        self.config = parametros
        self.recientes = deque(maxlen=10)
        self.muestras = deque(maxlen=4)
        self.suma10 = 0
        self.pico = 0
        self.liquidando = False
        self.tendencia = 0
        self.momentum = 0
        self.objetivo = 0

    def decidir(self, tick: int, precio: int, caja: int, acciones: int) -> Decision:
        cfg = self.config
        if len(self.recientes) == self.recientes.maxlen:
            self.suma10 -= self.recientes[0]
        self.recientes.append(precio)
        self.suma10 += precio
        lista = len(self.recientes) == 10
        self.momentum = 10 * precio - self.suma10 if lista else 0

        if acciones:
            self.pico = max(self.pico, precio)
        else:
            self.pico = 0
            self.liquidando = False

        compra = salida = False
        fuerza = 0
        if tick % cfg.periodo == 0:
            if self.muestras and lista:
                self.tendencia = precio - self.muestras[-1]
                fuerza = self.tendencia
                if cfg.familia == "breakout":
                    if len(self.muestras) == 4:
                        fuerza = precio - max(self.muestras)
                        compra = fuerza >= cfg.umbral
                        salida = precio <= min(self.muestras) - cfg.umbral
                else:
                    compra = fuerza >= cfg.umbral
                    salida = self.tendencia <= -cfg.umbral
                    if cfg.familia == "hibrida":
                        compra = compra and self.momentum >= 0
                        salida = salida and self.momentum <= 0
            self.muestras.append(precio)

        if cfg.familia in ("trailing", "hibrida") and lista:
            salida |= self.pico - precio >= cfg.distancia_stop and self.momentum <= 0
        if acciones and salida:
            self.liquidando = True
        self.objetivo = acciones
        if self.liquidando:
            self.objetivo = 0
            cantidad = min(acciones, LIMITE_ORDEN)
            if cantidad and caja + cantidad * precio >= COMISION:
                return Decision(Accion.VENDER, cantidad)
        elif compra and (acciones == 0 or cfg.progresiva):
            capital = caja + acciones * precio
            self.objetivo = (cfg.exposicion // 25 * capital) // (4 * precio)
            cantidad = min(LIMITE_ORDEN, self.objetivo - acciones, (caja - COMISION) // precio)
            if cfg.progresiva and fuerza < 2 * cfg.umbral:
                cantidad = min(cantidad, LOTE_MODERADO)
            if cantidad >= (LOTE_MINIMO_ADICIONAL if acciones else 1):
                return Decision(Accion.COMPRAR, cantidad)
        return MANTENER


def crear_politica(config: Parametros | None = None, traza: list | None = None):
    """Interfaz de simulador.py. Reconstruye cada fill al precio recibido."""
    if config is None:
        config = configuracion_congelada()
    estado = Estado(config)
    pendiente = MANTENER
    caja, posicion = CAPITAL_INICIAL, 0

    def decidir(historial, acciones, tick, ultima_operacion=None):
        nonlocal pendiente, caja, posicion
        precio = historial[-1]
        aplicado = ejecutar_decision(caja, posicion, pendiente, precio)
        caja, posicion = aplicado.caja, aplicado.acciones
        if posicion != acciones:
            raise RuntimeError(f"Inventario local distinto de la maestra en tick {tick}")
        pendiente = estado.decidir(tick, precio, caja, posicion)
        if traza is not None:
            traza.append({
                "suma10": estado.suma10, "tendencia": estado.tendencia,
                "momentum": estado.momentum, "pico_posicion": estado.pico,
                "liquidando": int(estado.liquidando), "posicion_objetivo": estado.objetivo,
            })
        return pendiente

    return decidir
