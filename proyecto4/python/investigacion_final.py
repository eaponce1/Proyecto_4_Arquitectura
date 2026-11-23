"""Evalua tres enfoques finales en la serie completa y cuatro segmentos aislados."""

import argparse
import csv
from functools import partial
from pathlib import Path

try:
    from .enfoques_finales import (
        CANTIDAD_ORDEN,
        estrategia_momentum_umbral,
        estrategia_reversion_media,
        estrategia_tendencia_persistente,
    )
    from .estrategia import Decision, Accion, estrategia_mantener, estrategia_no_operar, estrategia_sma_umbral_cooldown
    from .metricas import graficar_patrimonios_v2
    from .simulador import BASE_PROYECTO, SALIDA_PREDETERMINADA, ejecutar_escenarios_v2, leer_precios, simular_estrategia
except ImportError:
    from enfoques_finales import CANTIDAD_ORDEN, estrategia_momentum_umbral, estrategia_reversion_media, estrategia_tendencia_persistente
    from estrategia import Decision, Accion, estrategia_mantener, estrategia_no_operar, estrategia_sma_umbral_cooldown
    from metricas import graficar_patrimonios_v2
    from simulador import BASE_PROYECTO, SALIDA_PREDETERMINADA, ejecutar_escenarios_v2, leer_precios, simular_estrategia


NOMBRE_PREVIO = "C umbral 2 cooldown 5 q=16"
SEGMENTO_TICKS = 5000
COMPLEJIDAD = {
    "No operar": (0, 0, "Sin aritmetica de estrategia; el core sigue atendiendo SPI."),
    "Comprar y mantener": (0, 0, "Orden preconfigurada; luego solo mantener."),
    "Mejor activa anterior C q=16": (34, 58, "SMA5/10, momentum, cooldown y estado de fill."),
    "A Momentum con umbral": (12, 22, "Buffer de 5 precios, resta, dos comparaciones y estado plano/largo."),
    "B Reversion a SMA10": (23, 38, "Buffer de 10 precios, suma y 4 sumas para 10*precio."),
    "C Tendencia persistente": (29, 49, "SMA5/10 con sumas rodantes y confirmacion de dos cierres."),
}


def _politicas():
    return {
        "No operar": estrategia_no_operar,
        "Comprar y mantener": estrategia_mantener,
        "Mejor activa anterior C q=16": partial(
            estrategia_sma_umbral_cooldown, cantidad=16, umbral=2, cooldown=5
        ),
        "A Momentum con umbral": estrategia_momentum_umbral,
        "B Reversion a SMA10": estrategia_reversion_media,
        "C Tendencia persistente": estrategia_tendencia_persistente,
    }


def _run_set(precios: list[int], etiquetas: list[str]) -> dict[str, object]:
    resultados = {}
    for nombre, politica in _politicas().items():
        initial = Decision(Accion.COMPRAR, 63) if nombre == "Comprar y mantener" else Decision()
        resultado = simular_estrategia(precios, nombre, politica, decision_inicial=initial)
        for tick, row in enumerate(resultado.decisiones):
            assert row["tick"] == tick and row["precio"] == precios[tick]
            assert row["patrimonio"] == row["caja"] + row["acciones"] * precios[tick]
            assert row["caja"] >= 0 and row["acciones"] >= 0
            if tick:
                assert row["decision_calculo_tick"] == tick - 1
                assert row["decision_recibida"] == resultado.decisiones[tick - 1]["decision_siguiente"]
        assert resultado.metricas.ordenes == resultado.compras + resultado.ventas
        assert resultado.metricas.comisiones == 5 * resultado.metricas.ordenes
        resultados[nombre] = resultado
    return resultados


def _metric_row(estrategia: str, segmento: str, resultado, ticks: int) -> dict[str, int | float | str]:
    m = resultado.metricas
    cyc_lo, cyc_hi, complejidad = COMPLEJIDAD[estrategia]
    # CPI de 2.35 tomado como referencia del enunciado; son ciclos del kernel,
    # no mediciones de hardware ni el tiempo total de espera SPI.
    cyc_lo = round(cyc_lo * 2.35)
    cyc_hi = round(cyc_hi * 2.35)
    return {
        "segmento": segmento,
        "ticks": ticks,
        "estrategia": estrategia,
        "patrimonio_final": m.patrimonio_final,
        "rentabilidad_pct": round(m.rentabilidad_pct, 4),
        "drawdown": m.perdida_maxima,
        "drawdown_pct": round(m.drawdown_maximo_pct, 4),
        "comisiones": m.comisiones,
        "operaciones": m.ordenes,
        "compras": resultado.compras,
        "ventas": resultado.ventas,
        "caja_final": m.caja_final,
        "acciones_finales": m.acciones_finales,
        "ciclos_kernel_tick_estimados_min": cyc_lo,
        "ciclos_kernel_tick_estimados_max": cyc_hi,
        "tiempo_kernel_tick_us_estimado_min": round(cyc_lo / 25, 3),
        "tiempo_kernel_tick_us_estimado_max": round(cyc_hi / 25, 3),
        "tiempo_kernel_segmento_ms_estimado_min": round(cyc_lo * ticks / 25000, 3),
        "tiempo_kernel_segmento_ms_estimado_max": round(cyc_hi * ticks / 25000, 3),
        "complejidad_RV32E": complejidad,
    }


def _fmt_money(n) -> str:
    return f"${n:,.2f}" if isinstance(n, float) else f"${n:,}"


def _make_report(precios: list[int], rows: list[dict], salida: Path) -> None:
    complete = {r["estrategia"]: r for r in rows if r["segmento"] == "Completa"}
    segs = [f"Segmento {i}" for i in range(1, 5)]
    names = list(_politicas())
    lines = [
        "# Investigación final de estrategias para Proyecto 4",
        "",
        f"Se evaluaron {len(precios):,} precios enteros. Las variantes y parámetros se congelaron antes de ejecutar "
        "las comparaciones. Cantidad por orden en las estrategias nuevas: 16; todas las cantidades cumplen el límite 63.",
        "",
        "## Metodología temporal y contable",
        "",
        "En cada tick se ejecuta a precio actual la decisión pendiente del tick anterior. Después se agrega el precio "
        "actual al historial y se genera la decisión siguiente. Cada segmento de 5.000 ticks se simula por separado "
        "con caja inicial de $10.000, cero acciones e historial vacío; no se pasa ningún dato de segmentos posteriores "
        "al anterior. La serie completa se simula en otra corrida cronológica única.",
        "",
        "Las compras se limitan por caja disponible después de reservar la comisión de $5; las ventas se limitan a "
        "las acciones existentes. Solo un fill cobra comisión. Patrimonio = caja + acciones × precio. El drawdown "
        "se mide desde el máximo histórico de cada corrida, incluyendo el capital inicial.",
        "",
        "## Definición de enfoques",
        "",
        "- **A — Momentum con umbral:** cambio entre el precio actual y el de cuatro ticks antes. Compra 16 estando "
        "plano cuando el cambio es al menos +1; vende la posición al detectar −1 o menos. El producto q×umbral es $16, "
        "mayor que $10 de comisiones de un ciclo; es un filtro de señal, no una garantía de ganancia realizada.",
        "- **B — Reversión a la media SMA10:** compra 16 estando plano si el precio está al menos $1 bajo SMA10; vende "
        "la posición si está al menos $1 sobre SMA10. Se compara 10×precio con la suma de diez precios; 10×precio se "
        "construye como 8p+2p con cuatro sumas, sin división ni multiplicador.",
        "- **C — Tendencia persistente:** SMA5 sobre SMA10 en dos cierres consecutivos abre una posición de 16; mantiene "
        "hasta que SMA5 queda bajo SMA10 durante dos cierres consecutivos y vende la posición. No reentra mientras ya esté larga.",
        "- **Mejor activa anterior:** variante C de la etapa previa (momentum con umbral 2 y cooldown 5), q=16, sin cambios.",
        "",
        "## Serie completa",
        "",
        "| Estrategia | Patrimonio | Retorno | Drawdown | Comisiones | Operaciones (C/V) | Caja | Acciones | Kernel estimado por tick |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for name in names:
        r = complete[name]
        lines.append(
            f"| {name} | {_fmt_money(r['patrimonio_final'])} | {r['rentabilidad_pct']:.2f}% | "
            f"{_fmt_money(r['drawdown'])} ({r['drawdown_pct']:.2f}%) | {_fmt_money(r['comisiones'])} | "
            f"{r['operaciones']} ({r['compras']}/{r['ventas']}) | {_fmt_money(r['caja_final'])} | "
            f"{r['acciones_finales']} | {r['ciclos_kernel_tick_estimados_min']}–{r['ciclos_kernel_tick_estimados_max']} ciclos "
            f"({r['tiempo_kernel_tick_us_estimado_min']}–{r['tiempo_kernel_tick_us_estimado_max']} µs) |"
        )
    lines.extend(["", "## Evaluación por segmentos independientes", ""])
    for seg in segs:
        lines.extend([
            f"### {seg}",
            "",
            "| Estrategia | Patrimonio | Retorno | Drawdown | Comisiones | Operaciones | Caja | Acciones |",
            "|---|---:|---:|---:|---:|---:|---:|---:|",
        ])
        for name in names:
            r = next(x for x in rows if x["segmento"] == seg and x["estrategia"] == name)
            lines.append(
                f"| {name} | {_fmt_money(r['patrimonio_final'])} | {r['rentabilidad_pct']:.2f}% | "
                f"{_fmt_money(r['drawdown'])} ({r['drawdown_pct']:.2f}%) | {_fmt_money(r['comisiones'])} | "
                f"{r['operaciones']} | {_fmt_money(r['caja_final'])} | {r['acciones_finales']} |"
            )
        lines.append("")
    lines.extend([
        "## Estimación de coste RV32E",
        "",
        "Los ciclos reportados son estimaciones del kernel de decisión: rango manual de instrucciones de la lógica "
        "de estrategia multiplicado por CPI=2,35 (referencia del enunciado), y convertido a tiempo con 25 MHz. No son "
        "mediciones del core. Excluyen sondeo de STATUS, espera de PRICE, latencia del banco síncrono, LSU, acceso SPI "
        "y escritura MMIO. Deben sustituirse por medición sobre trade.s antes de afirmar que cumple un deadline.",
        "",
        "- A necesita cuatro precios de horizonte, una resta y dos comparaciones; complejidad baja y buffer de cinco precios.",
        "- B suma diez precios y compara contra 10×precio; ese múltiplo constante toma cuatro sumas con el método descrito. "
        "Buffer de diez precios; es el kernel más costoso de los tres nuevos.",
        "- C requiere sumas SMA5/SMA10, comparación y dos estados de confirmación; un buffer de diez precios y un contador pequeño.",
        "- El control de cartera completo requiere estado de caja/acciones. Los enfoques usan q fijo 16 y el modelo de la maestra limita compras por caja.",
        "",
        "## Recomendación",
        "",
        "No recomiendo todavía una estrategia activa para competir. No operar conserva el capital y las tres propuestas "
        "pierden dinero en la serie completa y en los cuatro segmentos independientes. Entre los enfoques nuevos, B "
        "es el candidato más razonable para seguir investigando: terminó por encima de A y C en la serie completa y en "
        "los segmentos 1–3, aunque pierde en todos los segmentos y requiere una ventana de diez precios. No es una "
        "recomendación para desplegarla. Si se exige una decisión con la evidencia actual, elegir no operar.",
        "",
        "La serie es una sola práctica y los segmentos pertenecen a la misma trayectoria; esto no reemplaza una serie "
        "oculta. No se seleccionó estrategia maximizando solo el retorno de 20.000 ticks.",
        "",
        "## Archivos",
        "",
        "- `comparacion_final.csv`: corrida completa y cuatro corridas independientes por segmento.",
        "- `patrimonio_final.svg`: evolución de la corrida completa para referencias y estrategias activas.",
        "- `investigacion_final.md`: metodología, resultados, complejidad y recomendación.",
    ])
    (salida / "investigacion_final.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def generar(precios: list[int], salida: Path) -> list[dict]:
    salida.mkdir(parents=True, exist_ok=True)
    rows: list[dict] = []
    full = _run_set(precios, ["Completa"])
    for name, result in full.items():
        rows.append(_metric_row(name, "Completa", result, len(precios)))

    for indice in range(4):
        inicio = indice * SEGMENTO_TICKS
        segmento = precios[inicio:inicio + SEGMENTO_TICKS]
        if len(segmento) != SEGMENTO_TICKS:
            raise ValueError("La serie debe contener exactamente cuatro segmentos de 5.000 ticks")
        etiqueta = f"Segmento {indice + 1}"
        for name, result in _run_set(segmento, [etiqueta]).items():
            rows.append(_metric_row(name, etiqueta, result, len(segmento)))

    with (salida / "comparacion_final.csv").open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

    graph_names = list(_politicas())
    graficar_patrimonios_v2(
        [(name, full[name].patrimonios) for name in graph_names],
        salida / "patrimonio_final.svg",
    )
    _make_report(precios, rows, salida)
    print(f"Evaluados {len(precios)} ticks completos y cuatro segmentos; {len(rows)} filas de comparación.")
    for name in graph_names:
        r = next(x for x in rows if x["segmento"] == "Completa" and x["estrategia"] == name)
        print(f"{name}: final={r['patrimonio_final']}, return={r['rentabilidad_pct']:.2f}%, DD={r['drawdown']}, fees={r['comisiones']}, orders={r['operaciones']}")
    return rows


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--csv", type=Path, default=BASE_PROYECTO / "data" / "practica_meta.csv")
    parser.add_argument("--salida", type=Path, default=SALIDA_PREDETERMINADA)
    args = parser.parse_args()
    precios = leer_precios(args.csv)
    generar(precios, args.salida)


if __name__ == "__main__":
    main()
