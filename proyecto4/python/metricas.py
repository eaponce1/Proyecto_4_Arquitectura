"""Metricas de cartera y graficos SVG, implementados con la biblioteca estandar."""

from dataclasses import dataclass
from pathlib import Path
from typing import Sequence
from xml.sax.saxutils import escape


@dataclass(frozen=True)
class Metricas:
    patrimonio_final: int
    caja_final: int
    acciones_finales: int
    rentabilidad_pct: float
    ordenes: int
    comisiones: int
    perdida_maxima: int
    drawdown_maximo_pct: float


def calcular_metricas(
    patrimonio: Sequence[int],
    caja_final: int,
    acciones_finales: int,
    ordenes: int,
    comisiones: int,
    capital_inicial: int = 10000,
) -> Metricas:
    if not patrimonio:
        raise ValueError("Se necesita al menos una valoracion de cartera")
    if capital_inicial <= 0:
        raise ValueError("El capital inicial debe ser positivo")

    peak = capital_inicial
    max_dd = 0
    max_dd_pct = 0.0
    for valor in patrimonio:
        peak = max(peak, valor)
        dd = peak - valor
        max_dd = max(max_dd, dd)
        if peak:
            max_dd_pct = max(max_dd_pct, dd * 100.0 / peak)

    final = patrimonio[-1]
    return Metricas(
        patrimonio_final=final,
        caja_final=caja_final,
        acciones_finales=acciones_finales,
        rentabilidad_pct=(final - capital_inicial) * 100.0 / capital_inicial,
        ordenes=ordenes,
        comisiones=comisiones,
        perdida_maxima=max_dd,
        drawdown_maximo_pct=max_dd_pct,
    )


def _grafico_lineas(
    destino: Path,
    titulo: str,
    eje_y: str,
    series: Sequence[tuple[str, Sequence[int], str]],
) -> None:
    """Escribe un grafico SVG sin requerir matplotlib ni otras dependencias."""
    width, height = 1300, 680
    left, right, bottom = 86, 34, 74
    legend_rows = (len(series) + 2) // 3
    top = 58 + legend_rows * 22
    plot_w, plot_h = width - left - right, height - top - bottom
    all_values = [value for _, values, _ in series for value in values]
    if not all_values:
        raise ValueError("No hay datos para graficar")
    low, high = min(all_values), max(all_values)
    if low == high:
        padding = max(1, abs(low) // 20)
        low, high = low - padding, high + padding
    else:
        padding = (high - low) * 0.06
        low, high = low - padding, high + padding

    def x_pos(index: int, count: int) -> float:
        return left + (plot_w * index / max(1, count - 1))

    def y_pos(value: int) -> float:
        return top + plot_h * (high - value) / (high - low)

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="#ffffff"/>',
        f'<text x="{width/2:.1f}" y="34" text-anchor="middle" font-family="Arial" font-size="23" font-weight="bold">{escape(titulo)}</text>',
    ]
    for tick in range(6):
        value = low + (high - low) * tick / 5
        y = y_pos(round(value))
        parts.append(f'<line x1="{left}" y1="{y:.1f}" x2="{width-right}" y2="{y:.1f}" stroke="#d9dee7"/>')
        parts.append(f'<text x="{left-12}" y="{y+5:.1f}" text-anchor="end" font-family="Arial" font-size="13">{value:,.0f}</text>')
    parts.extend([
        f'<line x1="{left}" y1="{top}" x2="{left}" y2="{height-bottom}" stroke="#344054"/>',
        f'<line x1="{left}" y1="{height-bottom}" x2="{width-right}" y2="{height-bottom}" stroke="#344054"/>',
        f'<text x="22" y="{top+plot_h/2:.1f}" transform="rotate(-90 22 {top+plot_h/2:.1f})" text-anchor="middle" font-family="Arial" font-size="15">{escape(eje_y)}</text>',
        f'<text x="{left+plot_w/2:.1f}" y="{height-22}" text-anchor="middle" font-family="Arial" font-size="15">Tick</text>',
    ])
    max_count = max(len(values) for _, values, _ in series)
    for label_tick in range(5):
        idx = round((max_count - 1) * label_tick / 4)
        x = x_pos(idx, max_count)
        parts.append(f'<text x="{x:.1f}" y="{height-bottom+24}" text-anchor="middle" font-family="Arial" font-size="12">{idx}</text>')

    legend_col_width = plot_w / 3
    for series_index, (name, values, color) in enumerate(series):
        legend_col = series_index % 3
        legend_row = series_index // 3
        legend_x = left + legend_col * legend_col_width + 4
        legend_y = 48 + legend_row * 21
        points = " ".join(
            f"{x_pos(i, len(values)):.1f},{y_pos(value):.1f}"
            for i, value in enumerate(values)
        )
        parts.append(f'<polyline fill="none" stroke="{color}" stroke-width="2" points="{points}"/>')
        parts.append(f'<line x1="{legend_x}" y1="{legend_y-4}" x2="{legend_x+24}" y2="{legend_y-4}" stroke="{color}" stroke-width="3"/>')
        parts.append(f'<text x="{legend_x+30}" y="{legend_y}" font-family="Arial" font-size="12">{escape(name)}</text>')
    parts.append("</svg>")
    destino.write_text("\n".join(parts), encoding="utf-8")


def graficar_precios(precios: Sequence[int], destino: Path) -> None:
    _grafico_lineas(destino, "Precio de la serie de practica", "Precio ($)", [("Precio", precios, "#2563eb")])


def graficar_patrimonios(
    resultados: dict[str, object], destino: Path
) -> None:
    colores = {
        "No operar": "#667085",
        "Comprar y mantener": "#16a34a",
        "Trading SMA 5/10 + momentum": "#dc2626",
    }
    series = [
        (nombre, resultado.patrimonios, colores[nombre])
        for nombre, resultado in resultados.items()
    ]
    _grafico_lineas(destino, "Evolucion del patrimonio", "Patrimonio ($)", series)


def graficar_patrimonios_v2(
    series: Sequence[tuple[str, Sequence[int]]], destino: Path
) -> None:
    """Grafica las referencias y variantes q=1 para comparar forma y drawdown."""
    paleta = ["#667085", "#16a34a", "#dc2626", "#2563eb", "#9333ea", "#d97706", "#0891b2"]
    datos = [(nombre, valores, paleta[i % len(paleta)]) for i, (nombre, valores) in enumerate(series)]
    _grafico_lineas(destino, "Patrimonio: referencias y variantes q=1", "Patrimonio ($)", datos)
