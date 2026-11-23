"""Auditoria, comparacion ex ante y artefactos de la segunda investigacion."""

import argparse
import csv
from pathlib import Path

try:
    from .metricas import graficar_patrimonios_v2
    from .simulador import (
        BASE_PROYECTO,
        SALIDA_PREDETERMINADA,
        ejecutar_escenarios_v2,
        leer_precios,
    )
except ImportError:
    from metricas import graficar_patrimonios_v2
    from simulador import BASE_PROYECTO, SALIDA_PREDETERMINADA, ejecutar_escenarios_v2, leer_precios


SALIDA_ANALISIS = SALIDA_PREDETERMINADA
NOMBRE_ORIGINAL = "Original SMA 5/10 + momentum q=1"


def _drawdown_detallado(valores: list[int], capital: int = 10000) -> dict[str, int | float]:
    peak, peak_tick = capital, -1
    max_dd, max_dd_pct, valle_tick, peak_del_dd = 0, 0.0, -1, capital
    for tick, valor in enumerate(valores):
        if valor > peak:
            peak, peak_tick = valor, tick
        dd = peak - valor
        pct = dd * 100.0 / peak if peak else 0.0
        if dd > max_dd:
            max_dd, max_dd_pct = dd, pct
            valle_tick, peak_del_dd = tick, peak
            peak_tick_del_dd = peak_tick
    return {
        "perdida": max_dd,
        "pct": max_dd_pct,
        "peak": peak_del_dd,
        "tick_peak": locals().get("peak_tick_del_dd", -1),
        "valle": valores[valle_tick] if valle_tick >= 0 else capital,
        "tick_valle": valle_tick,
    }


def _validar_cartera(resultado, precios: list[int]) -> None:
    if len(resultado.decisiones) != len(precios):
        raise AssertionError(f"{resultado.nombre}: faltan filas de decisiones")
    if resultado.metricas.ordenes != resultado.compras + resultado.ventas:
        raise AssertionError(f"{resultado.nombre}: ordenes no coinciden con compras + ventas")
    if resultado.metricas.comisiones != resultado.metricas.ordenes * 5:
        raise AssertionError(f"{resultado.nombre}: comisiones no son $5 por fill")
    for tick, (fila, precio) in enumerate(zip(resultado.decisiones, precios)):
        if fila["precio"] != precio or fila["tick"] != tick:
            raise AssertionError(f"{resultado.nombre}: desalineacion de tick/precio")
        if fila["patrimonio"] != fila["caja"] + fila["acciones"] * precio:
            raise AssertionError(f"{resultado.nombre}: patrimonio incorrecto en tick {tick}")
        if fila["caja"] < 0 or fila["acciones"] < 0:
            raise AssertionError(f"{resultado.nombre}: deuda/venta corta en tick {tick}")
        if tick and fila["decision_calculo_tick"] != tick - 1:
            raise AssertionError(f"{resultado.nombre}: decision fuera de desfase en tick {tick}")
        if tick + 1 < len(resultado.decisiones):
            siguiente = resultado.decisiones[tick + 1]
            if siguiente["decision_recibida"] != fila["decision_siguiente"]:
                raise AssertionError(f"{resultado.nombre}: la decision calculada no coincide con la recibida")
            if (siguiente["decision_calculo_tick"] != tick
                    or siguiente["decision_calculo_precio"] != precio):
                raise AssertionError(f"{resultado.nombre}: precio/tick de origen de decision incorrecto")
    for op in resultado.operaciones:
        if op["tick_calculo_decision"] >= 0 and op["tick_ejecucion"] != op["tick_calculo_decision"] + 1:
            raise AssertionError(f"{resultado.nombre}: orden no respeta el tick de desfase")


def _fila_comparacion(nombre: str, resultado) -> dict[str, int | float | str]:
    m = resultado.metricas
    cerradas = resultado.ganancia_perdida_cierres
    intervals = resultado.intervalos_operaciones
    return {
        "estrategia": nombre,
        "patrimonio_final": m.patrimonio_final,
        "rentabilidad_pct": round(m.rentabilidad_pct, 4),
        "drawdown_maximo": m.perdida_maxima,
        "drawdown_maximo_pct": round(m.drawdown_maximo_pct, 4),
        "comisiones": m.comisiones,
        "ordenes": m.ordenes,
        "compras": resultado.compras,
        "ventas": resultado.ventas,
        "caja_final": m.caja_final,
        "acciones_finales": m.acciones_finales,
        "acciones_compradas": resultado.cantidad_comprada,
        "acciones_vendidas": resultado.cantidad_vendida,
        "cierres": len(cerradas),
        "pnl_promedio_cierre": round(sum(cerradas) / len(cerradas), 2) if cerradas else "",
        "peor_cierre": min(cerradas) if cerradas else "",
        "ticks_promedio_entre_operaciones": round(sum(intervals) / len(intervals), 2) if intervals else "",
        "caja_minima": min(resultado.cajas),
        "caja_maxima": max(resultado.cajas),
        "acciones_maximas": max(resultado.posiciones),
    }


def _escribir_comparacion(resultados, salida: Path) -> list[dict[str, int | float | str]]:
    filas = [_fila_comparacion(nombre, resultado) for nombre, resultado in resultados.items()]
    with (salida / "comparacion_estrategias_v2.csv").open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(filas[0]))
        writer.writeheader()
        writer.writerows(filas)
    return filas


def _escribir_operaciones(resultados, salida: Path) -> list[dict[str, int | float | str]]:
    filas: list[dict[str, int | float | str]] = []
    for nombre, resultado in resultados.items():
        for op in resultado.operaciones:
            filas.append({"estrategia": nombre, **op})
    campos = [
        "estrategia", "numero_orden", "tick_ejecucion", "tick_calculo_decision",
        "precio_al_calcular", "decision_byte", "tipo", "cantidad_ejecutada",
        "precio_ejecucion", "comision", "caja_antes", "acciones_antes",
        "caja_despues", "acciones_despues", "patrimonio_despues",
        "ganancia_perdida_realizada", "intervalo_desde_orden_anterior",
    ]
    with (salida / "operaciones_v2.csv").open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=campos)
        writer.writeheader()
        writer.writerows(filas)
    return filas


def _fmt_money(valor) -> str:
    if valor == "":
        return "—"
    return f"${valor:,.2f}" if isinstance(valor, float) else f"${valor:,}"


def _crear_informe(precios, resultados, filas, operaciones, salida: Path) -> None:
    original = resultados[NOMBRE_ORIGINAL]
    dd = _drawdown_detallado(original.patrimonios)
    tick_valle = int(dd["tick_valle"])
    valle = original.decisiones[tick_valle]
    max_wealth = int(dd["peak"])
    min_wealth = int(dd["valle"])

    lines = [
        "# Auditoría contable y comparación de estrategias v2",
        "",
        f"Serie evaluada: {len(precios):,} ticks; precio mínimo ${min(precios)}, máximo ${max(precios)}.",
        "Capital inicial $10.000; comisión $5 por orden ejecutada; precio entero; sin deuda ni venta corta.",
        "",
        "## Auditoría del drawdown reportado",
        "",
        "El drawdown absoluto de $10.152 no es una deuda ni una pérdida medida desde el capital inicial. "
        "Es la caída desde el máximo histórico de patrimonio hasta un valle posterior:",
        "",
        f"- Peak: ${max_wealth:,} en tick {dd['tick_peak']}.",
        f"- Valle: ${min_wealth:,} en tick {tick_valle}, con caja ${valle['caja']:,} y {valle['acciones']} acciones.",
        f"- Diferencia peak-valle: ${max_wealth:,} - ${min_wealth:,} = ${dd['perdida']:,} "
        f"({dd['pct']:.2f}% del peak).",
        "- El mínimo de caja, acciones y patrimonio de la simulación base es no negativo; el drawdown supera $10.000 "
        "porque el peak previo fue $10.254, no porque la cartera tomara deuda.",
        "",
        "La fórmula utilizada es `peak_t = max(capital_inicial, equity[0..t])`, "
        "`drawdown_t = peak_t - equity_t`; se reporta el mayor drawdown absoluto y el porcentaje respecto del peak.",
        "",
        "## Revisión contable y temporal",
        "",
        "- Compra: cantidad ejecutada = min(cantidad solicitada, max(0, floor((caja - 5) / precio))). "
        "La comisión se descuenta solo si se ejecuta al menos una acción.",
        "- Venta: cantidad ejecutada = min(cantidad solicitada, acciones disponibles); la comisión también se cobra "
        "solo al ejecutar. El saldo y la posición permanecen no negativos.",
        "- Patrimonio por tick: `caja + acciones * precio_del_tick`, después de ejecutar la orden recibida.",
        "- Desfase SPI: la columna `tick_calculo_decision` de `operaciones_v2.csv` debe ser el tick anterior al de ejecución. "
        "La decisión se calcula después de agregar el precio actual al historial y queda pendiente para el siguiente tick.",
        "- Las pruebas recomputan el patrimonio en cada tick, las comisiones, fills, caja, acciones y un ejemplo de FIFO.",
        "- Costo base FIFO para P&L cerrado: incluye la comisión de compra asignada proporcionalmente al lote; "
        "al vender, el P&L realizado resta la comisión de venta. P&L por cierre se agrupa por orden de venta.",
        "",
        "## Recuento de operaciones de la versión original",
        "",
    ]
    base_row = next(row for row in filas if row["estrategia"] == NOMBRE_ORIGINAL)
    lines.append(
        f"La estrategia SMA 5/10 + momentum q=1 reprodujo {base_row['ordenes']:,} órdenes: "
        f"{base_row['compras']:,} compras y {base_row['ventas']:,} ventas. Pagó "
        f"${base_row['comisiones']:,} de comisión. El P&L promedio por orden de venta cerrada fue "
        f"{_fmt_money(base_row['pnl_promedio_cierre'])}; el intervalo medio entre órdenes fue "
        f"{base_row['ticks_promedio_entre_operaciones']} ticks."
    )
    lines.extend([
        "",
        "## Variantes y cantidades",
        "",
        "Las cantidades evaluadas se fijaron antes de ejecutar la comparación: 1, 2, 4, 8, 16, 32 y 63. "
        "Se reporta la grilla como análisis de sensibilidad; no se seleccionó una cantidad maximizando el resultado.",
        "",
        "- **A:** SMA 5/10 y momentum a tres ticks con umbral absoluto de 2 unidades de precio.",
        "- **B:** dos cierres consecutivos con la misma dirección de SMA, momentum coherente, una entrada estando plano "
        "y salida de la posición completa. Limita el número de operaciones y la posición a 63 acciones.",
        "- **C:** umbral de 2 unidades y cooldown de 5 ticks desde la última orden ejecutada. Por el desfase, "
        "la próxima orden se ejecuta al menos un tick después de calcularla.",
        "- También se incluye la estrategia original sin umbral (q=1) y las dos referencias obligatorias.",
        "",
        "### Comparación completa",
        "",
        "| Estrategia | Patrimonio | Retorno | Max DD | Fees | Órdenes (buy/sell) | Caja | Acciones | P&L medio cierre | ticks/orden |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ])
    for row in filas:
        lines.append(
            f"| {row['estrategia']} | {_fmt_money(row['patrimonio_final'])} | {row['rentabilidad_pct']:.2f}% | "
            f"{_fmt_money(row['drawdown_maximo'])} ({row['drawdown_maximo_pct']:.2f}%) | {_fmt_money(row['comisiones'])} | "
            f"{row['ordenes']} ({row['compras']}/{row['ventas']}) | {_fmt_money(row['caja_final'])} | "
            f"{row['acciones_finales']} | {_fmt_money(row['pnl_promedio_cierre'])} | {row['ticks_promedio_entre_operaciones']} |"
        )

    lines.extend([
        "",
        "## Evolución de caja y posición",
        "",
        "La serie completa por tick queda en memoria durante la simulación; el CSV de operaciones registra cada fill "
        "con caja/acciones antes y después. Rangos de las referencias, baseline y variantes q=1:",
        "",
        "| Estrategia | Rango caja | Caja final | Rango acciones | Acciones finales |",
        "|---|---:|---:|---:|---:|",
    ])
    trayectoria_nombres = [
        "No operar", "Comprar y mantener", NOMBRE_ORIGINAL,
        "A SMA+momentum umbral 2 q=1", "B tendencia confirmada q=1",
        "C umbral 2 cooldown 5 q=1",
    ]
    for nombre in trayectoria_nombres:
        r = resultados[nombre]
        lines.append(
            f"| {nombre} | ${min(r.cajas):,}–${max(r.cajas):,} | ${r.metricas.caja_final:,} | "
            f"0–{max(r.posiciones)} | {r.metricas.acciones_finales} |"
        )
    lines.extend([
        "",
        "## Operaciones cerradas con mayor pérdida",
        "",
        "P&L realizado por orden de venta FIFO, con comisiones de compra/venta incluidas. Un P&L negativo es una "
        "pérdida realizada; no atribuye a una venta la caída no realizada de toda la cartera.",
        "",
        "| Estrategia | Tick | Cantidad | Precio | Caja tras venta | Posición tras venta | P&L realizado |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ])
    peores = sorted(
        (op for op in operaciones if isinstance(op.get("ganancia_perdida_realizada"), (int, float))
         and op["ganancia_perdida_realizada"] < 0),
        key=lambda op: float(op["ganancia_perdida_realizada"]),
    )[:10]
    for op in peores:
        lines.append(
            f"| {op['estrategia']} | {op['tick_ejecucion']} | {op['cantidad_ejecutada']} | ${op['precio_ejecucion']} | "
            f"${op['caja_despues']} | {op['acciones_despues']} | {_fmt_money(float(op['ganancia_perdida_realizada']))} |"
        )
    if not peores:
        lines.append("| No hubo cierres con pérdida realizada | — | — | — | — | — | — |")

    lines.extend([
        "",
        "## Recomendación",
        "",
        "En la serie de práctica, **no operar** conserva $10.000 y supera todas las estrategias activas evaluadas. "
        "Por rentabilidad, drawdown, cero comisiones y mínima complejidad, recomiendo no operar con la información "
        "y las reglas actuales. Comprar y mantener termina en $9.695.",
        "",
        "Entre las activas, C con q=16 obtuvo el mayor patrimonio final de la grilla ($7.383), pero perdió 26,17% "
        "y pagó $3.785 en comisiones. No recomiendo seleccionar esa cantidad por ser la mejor de esta misma serie: "
        "sería optimización retrospectiva. B con q=1 reduce el número de órdenes frente al baseline, pero termina "
        "en $5.180 y no supera la referencia sin operar. La serie es una sola práctica; no justifica generalización "
        "ni ajuste de parámetros. Umbrales, confirmación, cooldown y grilla no consultan precios futuros.",
        "",
        "## Coste estimado al portar a RV32E",
        "",
        "Las variantes A/C requieren sumas de ventanas, comparación SMA, resta de momentum y branches; C agrega un "
        "contador/comparación de cooldown. B agrega una comparación con la señal anterior y un estado plano/largo, "
        "pero puede reducir fills y comisiones. Ninguna necesita multiplicación o división en la señal: `2 * suma_5` "
        "se implementa como suma consigo misma. Mantener SMA 5/10 y momentum requiere conservar diez precios "
        "(probablemente buffer circular) y actualizar índices/valores; la alternativa de recalcular ventanas añade "
        "lecturas y sumas por tick. La contabilidad completa de caja con precio por cantidad sí exigiría multiplicación; "
        "las estrategias evaluadas usan cantidades acotadas y la FPGA maestra aplica la regla de caja.",
        "",
        "## Archivos de salida y límites",
        "",
        "- `comparacion_estrategias_v2.csv`: 24 escenarios (referencias, baseline y 21 combinaciones de variantes/cantidad).",
        "- `operaciones_v2.csv`: un registro por orden ejecutada, con origen de decisión, fill, saldos y P&L FIFO al cerrar.",
        "- `patrimonio_estrategias_v2.svg`: referencias, baseline y variantes nuevas con q=1; la grilla completa está en CSV.",
        "- `analisis_estrategias.md`: esta auditoría, resultados, sensibilidad y recomendación.",
        "",
        "No se modificaron RTL, assembler ni testbench. No se implementó Assembly.",
    ])
    (salida / "analisis_estrategias.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def generar(ruta_csv: Path, salida: Path) -> None:
    precios = leer_precios(ruta_csv)
    resultados = ejecutar_escenarios_v2(precios)
    for resultado in resultados.values():
        _validar_cartera(resultado, precios)
    filas = _escribir_comparacion(resultados, salida)
    operaciones = _escribir_operaciones(resultados, salida)

    graficar_nombres = [
        "No operar", "Comprar y mantener", NOMBRE_ORIGINAL,
        "A SMA+momentum umbral 2 q=1", "B tendencia confirmada q=1",
        "C umbral 2 cooldown 5 q=1",
    ]
    graficar_patrimonios_v2(
        [(nombre, resultados[nombre].patrimonios) for nombre in graficar_nombres],
        salida / "patrimonio_estrategias_v2.svg",
    )
    _crear_informe(precios, resultados, filas, operaciones, salida)
    print(f"Ticks analizados: {len(precios)}; escenarios: {len(resultados)}; operaciones: {len(operaciones)}")
    print(f"Archivos v2 escritos en {salida}")
    for nombre in ("No operar", "Comprar y mantener", NOMBRE_ORIGINAL,
                   "A SMA+momentum umbral 2 q=1", "B tendencia confirmada q=1",
                   "C umbral 2 cooldown 5 q=1"):
        m = resultados[nombre].metricas
        print(f"{nombre}: wealth={m.patrimonio_final}, orders={m.ordenes}, fees={m.comisiones}, DD={m.perdida_maxima}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--csv", type=Path, default=BASE_PROYECTO / "data" / "practica_meta.csv")
    parser.add_argument("--salida", type=Path, default=SALIDA_ANALISIS)
    args = parser.parse_args()
    generar(args.csv, args.salida)


if __name__ == "__main__":
    main()
