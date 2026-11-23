"""Simulacion causal de las tres estrategias bajo el desfase SPI del proyecto."""

import argparse
import csv
import inspect
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, Sequence

try:
    from .estrategia import (
        Accion,
        Decision,
        MANTENER,
        estrategia_mantener,
        estrategia_no_operar,
        estrategia_trading,
        estrategia_sma_umbral,
        estrategia_tendencia_confirmada,
        estrategia_sma_umbral_cooldown,
    )
    from .metricas import Metricas, calcular_metricas, graficar_patrimonios, graficar_precios
except ImportError:  # Permite ejecutar directamente este archivo desde cualquier cwd.
    from estrategia import (Accion, Decision, MANTENER, estrategia_mantener,
                            estrategia_no_operar, estrategia_trading,
                            estrategia_sma_umbral, estrategia_tendencia_confirmada,
                            estrategia_sma_umbral_cooldown)
    from metricas import Metricas, calcular_metricas, graficar_patrimonios, graficar_precios


CAPITAL_INICIAL = 10000
COMISION = 5
MAX_TICKS = 20000
BASE_PROYECTO = Path(__file__).resolve().parents[1]
CSV_PREDETERMINADO = BASE_PROYECTO / "data" / "practica_meta.csv"
SALIDA_PREDETERMINADA = BASE_PROYECTO / "resultados"


@dataclass(frozen=True)
class Ejecucion:
    caja: int
    acciones: int
    cantidad_ejecutada: int
    comision: int


@dataclass
class Cartera:
    caja: int = CAPITAL_INICIAL
    acciones: int = 0
    ordenes: int = 0
    comisiones: int = 0


@dataclass
class ResultadoSimulacion:
    nombre: str
    metricas: Metricas
    patrimonios: list[int] = field(default_factory=list)
    decisiones: list[dict[str, int | str]] = field(default_factory=list)
    operaciones: list[dict[str, int | str | float]] = field(default_factory=list)
    cajas: list[int] = field(default_factory=list)
    posiciones: list[int] = field(default_factory=list)
    compras: int = 0
    ventas: int = 0
    cantidad_comprada: int = 0
    cantidad_vendida: int = 0
    ganancia_perdida_cierres: list[float] = field(default_factory=list)
    intervalos_operaciones: list[int] = field(default_factory=list)


Politica = Callable[..., Decision]


@dataclass
class LoteCompra:
    cantidad: int
    costo_centavos: int


def _consumir_lotes_fifo(lotes: list[LoteCompra], cantidad: int) -> int:
    """Retira lotes FIFO y devuelve su costo base en centavos, comision incluida."""
    costo_total = 0
    pendiente = cantidad
    while pendiente:
        if not lotes:
            raise AssertionError("Se intenta vender mas acciones que las registradas")
        lote = lotes[0]
        tomar = min(pendiente, lote.cantidad)
        costo = lote.costo_centavos if tomar == lote.cantidad else lote.costo_centavos * tomar // lote.cantidad
        costo_total += costo
        lote.cantidad -= tomar
        lote.costo_centavos -= costo
        pendiente -= tomar
        if lote.cantidad == 0:
            lotes.pop(0)
    return costo_total


def leer_precios(ruta: Path = CSV_PREDETERMINADO) -> list[int]:
    """Lee y valida tick,price; exige la serie completa y ordenada de 20 000 ticks."""
    precios: list[int] = []
    with ruta.open("r", encoding="utf-8-sig", newline="") as archivo:
        lector = csv.DictReader(archivo)
        if lector.fieldnames != ["tick", "price"]:
            raise ValueError("El CSV debe tener encabezados tick,price")
        for esperado, fila in enumerate(lector):
            try:
                tick = int(fila["tick"])
                precio = int(fila["price"])
            except (TypeError, ValueError) as error:
                raise ValueError(f"Fila invalida para tick {esperado}") from error
            if tick != esperado:
                raise ValueError(f"Se esperaba tick {esperado}, se encontro {tick}")
            if not 1 <= precio <= 255:
                raise ValueError(f"Precio fuera de 1..255 en tick {tick}: {precio}")
            precios.append(precio)
    if len(precios) != MAX_TICKS:
        raise ValueError(f"Se esperaban {MAX_TICKS} ticks y se leyeron {len(precios)}")
    return precios


def ejecutar_decision(caja: int, acciones: int, decision: Decision, precio: int) -> Ejecucion:
    """Aplica una orden con comisión fija, límite de caja y sin ventas en corto."""
    if precio <= 0:
        raise ValueError("El precio debe ser positivo")
    nueva_caja, nuevas_acciones = caja, acciones
    cantidad = 0
    comision = 0

    if decision.accion == Accion.COMPRAR:
        asequible = max(0, (caja - COMISION) // precio)
        cantidad = min(decision.cantidad, asequible)
        if cantidad > 0:
            nueva_caja -= cantidad * precio + COMISION
            nuevas_acciones += cantidad
            comision = COMISION
    elif decision.accion == Accion.VENDER:
        cantidad = min(decision.cantidad, acciones)
        if cantidad > 0 and caja + cantidad * precio >= COMISION:
            nueva_caja += cantidad * precio - COMISION
            nuevas_acciones -= cantidad
            comision = COMISION
        else:
            cantidad = 0

    if nueva_caja < 0 or nuevas_acciones < 0:
        raise AssertionError("La ejecucion genero deuda o una posicion corta")
    return Ejecucion(nueva_caja, nuevas_acciones, cantidad, comision)


def simular_estrategia(
    precios: Sequence[int],
    nombre: str,
    politica: Politica,
    decision_inicial: Decision = MANTENER,
) -> ResultadoSimulacion:
    """Ejecuta decision pendiente y calcula la siguiente tras observar el precio.

    Orden temporal por tick n: se ejecuta `pendiente` a precio[n]; luego el
    precio[n] se agrega al historial y `politica` produce la decision de n+1.
    La decision calculada tras el ultimo tick queda sin ejecutar.
    """
    if not precios:
        raise ValueError("La serie de precios esta vacia")
    cartera = Cartera()
    pendiente = decision_inicial
    pendiente_origen_tick = -1
    pendiente_origen_precio: int | str = "preconfigurada"
    historial: list[int] = []
    patrimonios: list[int] = []
    detalle: list[dict[str, int | str]] = []
    operaciones: list[dict[str, int | str | float]] = []
    cajas: list[int] = []
    posiciones: list[int] = []
    lotes: list[LoteCompra] = []
    compras = ventas = cantidad_comprada = cantidad_vendida = 0
    ganancias_cierres: list[float] = []
    ticks_operacion: list[int] = []
    ultimo_tick_operacion: int | None = None
    try:
        inspect.signature(politica).bind([], 0, 0, None)
        politica_con_contexto = True
    except (TypeError, ValueError):
        politica_con_contexto = False

    for tick, precio in enumerate(precios):
        recibida = pendiente
        caja_antes, acciones_antes = cartera.caja, cartera.acciones
        ejecucion = ejecutar_decision(cartera.caja, cartera.acciones, recibida, precio)
        cartera.caja = ejecucion.caja
        cartera.acciones = ejecucion.acciones
        if ejecucion.cantidad_ejecutada:
            cartera.ordenes += 1
            cartera.comisiones += ejecucion.comision
            ticks_operacion.append(tick)
            ultimo_tick_operacion = tick
            if recibida.accion == Accion.COMPRAR:
                compras += 1
                cantidad_comprada += ejecucion.cantidad_ejecutada
                lotes.append(LoteCompra(
                    ejecucion.cantidad_ejecutada,
                    (ejecucion.cantidad_ejecutada * precio + ejecucion.comision) * 100,
                ))
                pnl_cierre: float | str = ""
            else:
                ventas += 1
                cantidad_vendida += ejecucion.cantidad_ejecutada
                base_centavos = _consumir_lotes_fifo(lotes, ejecucion.cantidad_ejecutada)
                pnl_centavos = (
                    ejecucion.cantidad_ejecutada * precio * 100
                    - ejecucion.comision * 100
                    - base_centavos
                )
                pnl_cierre = pnl_centavos / 100.0
                ganancias_cierres.append(pnl_cierre)

            if len(ticks_operacion) > 1:
                # El intervalo se añade una sola vez en el tick de la nueva orden.
                intervalo = ticks_operacion[-1] - ticks_operacion[-2]
            else:
                intervalo = ""
            operaciones.append({
                "tick_ejecucion": tick,
                "numero_orden": cartera.ordenes,
                "tick_calculo_decision": pendiente_origen_tick,
                "precio_al_calcular": pendiente_origen_precio,
                "decision_byte": recibida.byte,
                "tipo": recibida.accion.name.lower(),
                "cantidad_ejecutada": ejecucion.cantidad_ejecutada,
                "precio_ejecucion": precio,
                "comision": ejecucion.comision,
                "caja_antes": caja_antes,
                "acciones_antes": acciones_antes,
                "caja_despues": cartera.caja,
                "acciones_despues": cartera.acciones,
                "patrimonio_despues": cartera.caja + cartera.acciones * precio,
                "ganancia_perdida_realizada": pnl_cierre,
                "intervalo_desde_orden_anterior": intervalo,
            })

        if sum(l.cantidad for l in lotes) != cartera.acciones:
            raise AssertionError("El registro FIFO no coincide con las acciones de la cartera")

        patrimonio = cartera.caja + cartera.acciones * precio
        patrimonios.append(patrimonio)
        cajas.append(cartera.caja)
        posiciones.append(cartera.acciones)
        historial.append(precio)
        if politica_con_contexto:
            siguiente = politica(historial, cartera.acciones, tick, ultimo_tick_operacion)
        else:
            siguiente = politica(historial, cartera.acciones)
        detalle.append({
            "tick": tick,
            "precio": precio,
            "decision_recibida": recibida.byte,
            "decision_calculo_tick": pendiente_origen_tick,
            "decision_calculo_precio": pendiente_origen_precio,
            "accion_recibida": recibida.accion.name.lower(),
            "cantidad_solicitada": recibida.cantidad,
            "cantidad_ejecutada": ejecucion.cantidad_ejecutada,
            "comision": ejecucion.comision,
            "caja": cartera.caja,
            "acciones": cartera.acciones,
            "patrimonio": patrimonio,
            "decision_siguiente": siguiente.byte,
            "accion_siguiente": siguiente.accion.name.lower(),
            "cantidad_siguiente": siguiente.cantidad,
        })
        pendiente = siguiente
        pendiente_origen_tick = tick
        pendiente_origen_precio = precio

        if cartera.caja < 0 or cartera.acciones < 0:
            raise AssertionError(f"Saldo o posicion negativa en tick {tick}")

    metricas = calcular_metricas(
        patrimonios, cartera.caja, cartera.acciones, cartera.ordenes,
        cartera.comisiones, CAPITAL_INICIAL,
    )
    intervalos = [b - a for a, b in zip(ticks_operacion, ticks_operacion[1:])]
    return ResultadoSimulacion(
        nombre=nombre, metricas=metricas, patrimonios=patrimonios,
        decisiones=detalle, operaciones=operaciones, cajas=cajas,
        posiciones=posiciones, compras=compras, ventas=ventas,
        cantidad_comprada=cantidad_comprada, cantidad_vendida=cantidad_vendida,
        ganancia_perdida_cierres=ganancias_cierres,
        intervalos_operaciones=intervalos,
    )


def ejecutar_simulacion(precios: Sequence[int]) -> dict[str, ResultadoSimulacion]:
    """Simula referencias A/B y la estrategia SMA+momentum."""
    return {
        "No operar": simular_estrategia(precios, "No operar", estrategia_no_operar),
        "Comprar y mantener": simular_estrategia(
            precios, "Comprar y mantener", estrategia_mantener,
            decision_inicial=Decision(Accion.COMPRAR, 63),
        ),
        "Trading SMA 5/10 + momentum": simular_estrategia(
            precios, "Trading SMA 5/10 + momentum", estrategia_trading,
        ),
    }


def ejecutar_escenarios_v2(precios: Sequence[int]) -> dict[str, ResultadoSimulacion]:
    """Corre referencias, baseline original y grilla ex ante de tres variantes.

    Las cantidades se fijan antes de comparar resultados. La grilla es una
    sensibilidad descriptiva, no un procedimiento que elija el maximo retorno.
    """
    from functools import partial

    resultados: dict[str, ResultadoSimulacion] = {
        "No operar": simular_estrategia(precios, "No operar", estrategia_no_operar),
        "Comprar y mantener": simular_estrategia(
            precios, "Comprar y mantener", estrategia_mantener,
            decision_inicial=Decision(Accion.COMPRAR, 63),
        ),
        "Original SMA 5/10 + momentum q=1": simular_estrategia(
            precios, "Original SMA 5/10 + momentum q=1", estrategia_trading,
        ),
    }
    cantidades = (1, 2, 4, 8, 16, 32, 63)
    for cantidad in cantidades:
        nombre = f"A SMA+momentum umbral 2 q={cantidad}"
        resultados[nombre] = simular_estrategia(
            precios, nombre, partial(estrategia_sma_umbral, cantidad=cantidad)
        )
    for cantidad in cantidades:
        nombre = f"B tendencia confirmada q={cantidad}"
        resultados[nombre] = simular_estrategia(
            precios, nombre, partial(estrategia_tendencia_confirmada, cantidad=cantidad)
        )
    for cantidad in cantidades:
        nombre = f"C umbral 2 cooldown 5 q={cantidad}"
        resultados[nombre] = simular_estrategia(
            precios, nombre, partial(estrategia_sma_umbral_cooldown, cantidad=cantidad)
        )
    return resultados


def escribir_resultados(
    precios: Sequence[int], resultados: dict[str, ResultadoSimulacion], salida: Path
) -> None:
    salida.mkdir(parents=True, exist_ok=True)
    trading = resultados["Trading SMA 5/10 + momentum"]
    with (salida / "decisiones_trading.csv").open("w", encoding="utf-8", newline="") as archivo:
        campos = list(trading.decisiones[0])
        escritor = csv.DictWriter(archivo, fieldnames=campos)
        escritor.writeheader()
        escritor.writerows(trading.decisiones)

    with (salida / "comparacion_estrategias.csv").open("w", encoding="utf-8", newline="") as archivo:
        campos = ["estrategia", "patrimonio_final", "caja_final", "acciones_finales",
                  "rentabilidad_pct", "ordenes", "comisiones", "perdida_maxima",
                  "drawdown_maximo_pct"]
        escritor = csv.DictWriter(archivo, fieldnames=campos)
        escritor.writeheader()
        for nombre, resultado in resultados.items():
            escritor.writerow({"estrategia": nombre, **resultado.metricas.__dict__})

    graficar_precios(precios, salida / "precio_serie.svg")
    graficar_patrimonios(resultados, salida / "patrimonio_estrategias.svg")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--csv", type=Path, default=CSV_PREDETERMINADO)
    parser.add_argument("--salida", type=Path, default=SALIDA_PREDETERMINADA)
    args = parser.parse_args()

    precios = leer_precios(args.csv)
    resultados = ejecutar_simulacion(precios)
    escribir_resultados(precios, resultados, args.salida)
    print(f"Ticks leidos: {len(precios)} (precio min={min(precios)}, max={max(precios)})")
    for nombre, resultado in resultados.items():
        m = resultado.metricas
        print(
            f"{nombre}: patrimonio=${m.patrimonio_final}; caja=${m.caja_final}; "
            f"acciones={m.acciones_finales}; rentabilidad={m.rentabilidad_pct:.2f}%; "
            f"ordenes={m.ordenes}; comisiones=${m.comisiones}; "
            f"max_drawdown=${m.perdida_maxima} ({m.drawdown_maximo_pct:.2f}%)"
        )
    print(f"Resultados escritos en: {args.salida}")


if __name__ == "__main__":
    main()
