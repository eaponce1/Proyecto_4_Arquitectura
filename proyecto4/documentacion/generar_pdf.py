#!/usr/bin/env python3
"""Render informe_final_proyecto4.md as a searchable PDF using ReportLab."""
from __future__ import annotations

import html
import re
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    PageTemplate,
    Paragraph,
    Preformatted,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "proyecto4" / "documentacion" / "informe_final_proyecto4.md"
OUTPUT_DIR = ROOT / "proyecto4" / "entrega_final"
OUTPUT = OUTPUT_DIR / "informe_final_proyecto4.pdf"
CODE_FONT = "Courier"


def register_fonts() -> None:
    fonts = Path("C:/Windows/Fonts")
    regular = fonts / "arial.ttf"
    bold = fonts / "arialbd.ttf"
    italic = fonts / "ariali.ttf"
    mono = fonts / "consola.ttf"
    if all(p.exists() for p in (regular, bold, italic, mono)):
        pdfmetrics.registerFont(TTFont("Body", str(regular)))
        pdfmetrics.registerFont(TTFont("Body-Bold", str(bold)))
        pdfmetrics.registerFont(TTFont("Body-Italic", str(italic)))
        pdfmetrics.registerFont(TTFont("Code", str(mono)))
        pdfmetrics.registerFontFamily("Body", normal="Body", bold="Body-Bold", italic="Body-Italic")
    else:
        pdfmetrics.registerFontFamily("Helvetica", normal="Helvetica", bold="Helvetica-Bold", italic="Helvetica-Oblique")


def inline_markup(text: str) -> str:
    saved: list[str] = []

    def protect(value: str) -> str:
        token = f"ZZP4TOKEN{len(saved)}ZZ"
        saved.append(value)
        return token

    text = re.sub(
        r"`([^`]+)`",
        lambda m: protect(f'<font name="{CODE_FONT}" size="7.2">{html.escape(m.group(1), quote=False)}</font>'),
        text,
    )
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", lambda m: protect(f"{html.escape(m.group(1))} ({html.escape(m.group(2))})"), text)
    escaped = html.escape(text, quote=False)
    escaped = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", escaped)
    escaped = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<i>\1</i>", escaped)
    for index, value in enumerate(saved):
        escaped = escaped.replace(f"ZZP4TOKEN{index}ZZ", value)
    return escaped


def split_table_row(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def table_widths(rows: list[list[str]], width: float) -> list[float]:
    n = len(rows[0])
    weights = []
    for col in range(n):
        maximum = max((len(row[col]) if col < len(row) else 0) for row in rows)
        weights.append(max(4, min(maximum, 28)))
    total = sum(weights)
    return [width * weight / total for weight in weights]


def footer(canvas, doc) -> None:
    canvas.saveState()
    canvas.setFont("Body" if "Body" in pdfmetrics.getRegisteredFontNames() else "Helvetica", 8)
    canvas.setFillColor(colors.HexColor("#5f6b7a"))
    canvas.drawString(doc.leftMargin, 9 * mm, "Proyecto 4 · Informe técnico final")
    canvas.drawRightString(doc.pagesize[0] - doc.rightMargin, 9 * mm, f"Página {doc.page}")
    canvas.restoreState()


def build() -> None:
    global CODE_FONT
    register_fonts()
    CODE_FONT = "Code" if "Code" in pdfmetrics.getRegisteredFontNames() else "Courier"
    family = "Body" if "Body" in pdfmetrics.getRegisteredFontNames() else "Helvetica"
    code = "Code" if "Code" in pdfmetrics.getRegisteredFontNames() else "Courier"
    width, height = landscape(A4)
    left = right = 16 * mm
    top = 17 * mm
    bottom = 17 * mm

    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name="P4Title", parent=styles["Title"], fontName=f"{family}-Bold" if family == "Body" else "Helvetica-Bold", fontSize=22, leading=27, textColor=colors.HexColor("#12304a"), alignment=TA_LEFT, spaceAfter=12))
    for level, size in ((1, 17), (2, 13), (3, 10.5)):
        styles.add(ParagraphStyle(name=f"P4H{level}", parent=styles["Heading1"], fontName=f"{family}-Bold" if family == "Body" else "Helvetica-Bold", fontSize=size, leading=size + 3, textColor=colors.HexColor("#12304a" if level < 3 else "#315b78"), spaceBefore=10, spaceAfter=5, keepWithNext=True))
    styles.add(ParagraphStyle(name="P4Body", parent=styles["BodyText"], fontName=family, fontSize=8.6, leading=12, alignment=TA_LEFT, spaceAfter=5))
    styles.add(ParagraphStyle(name="P4Bullet", parent=styles["P4Body"], leftIndent=12, firstLineIndent=-9, spaceAfter=3))
    styles.add(ParagraphStyle(name="P4Code", parent=styles["Code"], fontName=code, fontSize=7.2, leading=9, leftIndent=8, rightIndent=8, borderColor=colors.HexColor("#d8e1e8"), borderWidth=0.4, borderPadding=5, backColor=colors.HexColor("#f4f7f9"), spaceBefore=3, spaceAfter=6))
    styles.add(ParagraphStyle(name="P4Table", parent=styles["P4Body"], fontSize=7.2, leading=9, spaceAfter=0))
    styles.add(ParagraphStyle(name="P4TableHead", parent=styles["P4Table"], fontName=f"{family}-Bold" if family == "Body" else "Helvetica-Bold", textColor=colors.white))

    doc = BaseDocTemplate(str(OUTPUT), pagesize=(width, height), leftMargin=left, rightMargin=right, topMargin=top, bottomMargin=bottom, title="Informe final del Proyecto 4 — Arquitectura de Computadores", author="Proyecto 4")
    frame = Frame(left, bottom, width - left - right, height - top - bottom, id="main")
    doc.addPageTemplates(PageTemplate(id="all", frames=frame, onPage=footer))

    lines = SOURCE.read_text(encoding="utf-8").splitlines()
    story = []
    i = 0
    in_code = False
    code_lines: list[str] = []
    while i < len(lines):
        line = lines[i]
        if line.strip().startswith("```"):
            if in_code:
                story.append(Preformatted("\n".join(code_lines), styles["P4Code"], maxLineLength=145))
                code_lines = []
                in_code = False
            else:
                in_code = True
            i += 1
            continue
        if in_code:
            code_lines.append(line)
            i += 1
            continue

        if line.startswith("|"):
            raw_rows = []
            while i < len(lines) and lines[i].startswith("|"):
                row = split_table_row(lines[i])
                if not all(re.fullmatch(r":?-{3,}:?", cell) for cell in row):
                    raw_rows.append(row)
                i += 1
            if raw_rows:
                columns = max(map(len, raw_rows))
                data = []
                for r, row in enumerate(raw_rows):
                    row = row + [""] * (columns - len(row))
                    data.append([Paragraph(inline_markup(cell), styles["P4TableHead"] if r == 0 else styles["P4Table"]) for cell in row])
                tbl = Table(data, colWidths=table_widths(raw_rows, width - left - right), repeatRows=1, hAlign="LEFT")
                tbl.setStyle(TableStyle([
                    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#315b78")),
                    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f2f6f8")]),
                    ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#cbd5dd")),
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("LEFTPADDING", (0, 0), (-1, -1), 4),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 4),
                    ("TOPPADDING", (0, 0), (-1, -1), 3),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
                ]))
                story.extend((tbl, Spacer(1, 5)))
            continue

        if not line.strip() or line.strip() == "---":
            story.append(Spacer(1, 3))
            i += 1
            continue
        heading = re.match(r"^(#{1,3})\s+(.*)$", line)
        if heading:
            level = min(len(heading.group(1)), 3)
            story.append(Paragraph(inline_markup(heading.group(2)), styles["P4Title"] if level == 1 and not story else styles[f"P4H{level}"]))
            i += 1
            continue
        if line.startswith("- ") or re.match(r"^\d+\.\s", line):
            bullet = "•" if line.startswith("- ") else re.match(r"^(\d+)\.", line).group(1) + "."
            text = line[2:] if line.startswith("- ") else re.sub(r"^\d+\.\s*", "", line)
            story.append(Paragraph(f"{bullet} {inline_markup(text)}", styles["P4Bullet"]))
            i += 1
            continue

        paragraph = [line.strip()]
        i += 1
        while i < len(lines) and lines[i].strip() and not lines[i].startswith(("#", "|", "```", "- ")) and not re.match(r"^\d+\.\s", lines[i]):
            paragraph.append(lines[i].strip())
            i += 1
        story.append(Paragraph(inline_markup(" ".join(paragraph)), styles["P4Body"]))

    if in_code:
        story.append(Preformatted("\n".join(code_lines), styles["P4Code"], maxLineLength=145))
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    doc.build(story)
    print(f"PDF generado: {OUTPUT} ({OUTPUT.stat().st_size} bytes)")


if __name__ == "__main__":
    build()
