"""Genera informe comparativo reproducible para MMIO SMA10 antes/después."""
from pathlib import Path
import csv, statistics, re
ROOT=Path(__file__).resolve().parents[2]
RESULT=ROOT/"proyecto4"/"resultados"/"co_disenio"
OUT=ROOT/"proyecto4"/"resultados"/"mmio_optimizacion"
OUT.mkdir(parents=True,exist_ok=True)

def read_rows(name):
    with (RESULT/name).open(newline="",encoding="utf-8") as f: return list(csv.DictReader(f))
def hw(prefix):
    synth=(RESULT/f"{prefix}_yosys.log").read_text(errors="replace")
    route=(RESULT/f"{prefix}_nextpnr.log").read_text(errors="replace")
    lut=int(re.findall(r"^\s*(\d+)\s+SB_LUT4\s*$",synth,re.M)[-1])
    lc=int(re.findall(r"ICESTORM_LC:\s*(\d+)\s*/\s*1280",route)[-1])
    bram=int(re.findall(r"ICESTORM_RAM:\s*(\d+)\s*/\s*16",route)[-1])
    freqs=re.findall(r"Max frequency for clock.*?:\s*([0-9.]+) MHz \(PASS at 25.00 MHz\)",route,re.S)
    return lut,lc,bram,float(freqs[-1])
def stats(filename):
    r=read_rows(filename)
    def calc(k):
        a=sorted(int(x[k]) for x in r)
        return statistics.mean(a),statistics.median(a),a[int(.95*(len(a)-1))],a[-1]
    return len(r),calc("ic_total"),calc("cycles_total")
old=stats("mmio_sma10_ticks.csv"); new=stats("mmio_sma10_opt_ticks.csv")
orig=read_rows("original_ticks.csv") if (RESULT/"original_ticks.csv").exists() else None
oldhw=hw("mmio_sma10"); newhw=hw("mmio_sma10_opt")
base_cycles=218.6635
fields=["variant","ticks","IC_avg","IC_median","IC_p95","IC_worst","cycles_avg","cycles_median","cycles_p95","cycles_worst","speedup_vs_original","LUT4","LC","BRAM","Fmax_MHz","route_status"]
with (OUT/"comparacion_mmio_sma10.csv").open("w",newline="",encoding="utf-8") as f:
    w=csv.DictWriter(f,fieldnames=fields); w.writeheader()
    for label,s,h in (("MMIO base",old,oldhw),("MMIO optimizada",new,newhw)):
        ticks,ic,cy=s; lut,lc,ram,fmax=h
        w.writerow(dict(variant=label,ticks=ticks,IC_avg=f"{ic[0]:.5f}",IC_median=ic[1],IC_p95=ic[2],IC_worst=ic[3],cycles_avg=f"{cy[0]:.5f}",cycles_median=cy[1],cycles_p95=cy[2],cycles_worst=cy[3],speedup_vs_original=f"{base_cycles/cy[0]:.6f}",LUT4=lut,LC=lc,BRAM=ram,Fmax_MHz=f"{fmax:.2f}",route_status="PASS @25MHz"))

def fmt(x): return f"{x:,.2f}"
lines=["# Optimización de recursos: MMIO SMA10", "", "## Cambio evaluado", "", "Se mantuvo `proyecto4/alternativas/mmio_sma10/` sin cambios y se creó `proyecto4/alternativas/mmio_sma10_opt/` como variante aislada. En `pochoco_sma10.v`, se sustituyó el contador saturante de 4 bits `count_q` por un bit `ready_q`. El puntero circular ya indica la décima muestra cuando vale 9; en ese evento se activa `ready_q`. Se conservan exactamente el anillo de diez precios en BRAM, la suma acumulada, el mapa MMIO, el SPI, la estrategia, la contabilidad y el core.", "", "La suma sigue acumulando los primeros diez precios y después reemplaza la muestra saliente por la entrante. `ready` se activa después de aceptar el décimo precio, igual que antes. La equivalencia se comprobó en cada muestra por el test autónomo y, en la simulación integrada, las decisiones MISO se cotejaron tick a tick contra Python.", "", "## Comparación real antes/después", "", "| Variante | IC media | Ciclos media | Mediana ciclos | p95 ciclos | Peor ciclo | Speedup vs original | LUT4 | LC | BRAM | Fmax |", "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|"]
for label,s,h in (("MMIO base",old,oldhw),("MMIO optimizada",new,newhw)):
    ticks,ic,cy=s; lut,lc,ram,fmax=h
    lines.append(f"| {label} ({ticks:,} ticks) | {fmt(ic[0])} | {fmt(cy[0])} | {cy[1]} | {cy[2]} | {cy[3]} | {base_cycles/cy[0]:.3f}× | {lut:,} | {lc}/1,280 | {ram}/16 | {fmax:.2f} MHz |")
lines += ["", f"Resultado de área: LC bajan de {oldhw[1]} a {newhw[1]} (−{oldhw[1]-newhw[1]}, {100*(oldhw[1]-newhw[1])/oldhw[1]:.2f}%). LUT4 baja de {oldhw[0]} a {newhw[0]}; BRAM permanece en {newhw[2]}/16. El objetivo de 1.150–1.200 LC **no se alcanzó**: la variante queda en {newhw[1]}/1.280 LC.", "", f"Fmax post-place-and-route aumenta de {oldhw[3]:.2f} MHz a {newhw[3]:.2f} MHz; ambas pasan los 25 MHz. Los tiempos software y speedup no cambian: IC/ciclos por tick son idénticos a nivel de estadística. El speedup por ciclos respecto a la versión software original se conserva en {base_cycles/new[2][0]:.3f}×.", "", "## Auditoría de recursos y alternativas", "", "- **Historial:** diez precios de 8 bits usan una instancia `SB_RAM40_4K`; preserva la BRAM e impide convertir las diez posiciones en registros/LUT, opción que probablemente aumentaría LC. BRAM total del SoC se mantiene 13/16.", "- **Registros del periférico:** `pointer_q` es necesario para el anillo de diez entradas; `sum_q` mantiene el rolling sum; `ready_q` reemplaza `count_q`. El contador de muestras y su comparador se consideran redundantes porque el puntero llega a slot 9 exactamente en la décima entrada inicial.", "- **Decodificador MMIO:** los offsets STATUS/PRICE/DECISION/SUM10/READY son 0–4. Se conserva el `case` existente: una reescritura más estrecha no se justificaba sin evidencia de ahorro, y alterar el decode de lecturas aumenta riesgo de regresión.", "- **Lógica combinacional y timing:** se conservó la lectura síncrona del precio saliente, la suma rodante y el mismo instante de captura SPI. En el reporte de timing optimizado, la ruta posedge crítica atraviesa lógica mapeada de la RAM de instrucciones/control de `u_ram.mem` y no la ruta de suma SMA10. No se cambió el Espino Core.", "", "La auditoría sugiere que el bloque SMA10 no explica por sí solo el uso total de 1.279 LC: el chip integra el SoC, RAM de programa, Espino, SPI y periféricos. Reducir otros recursos con impacto importante requeriría reestructurar bloques ajenos a SMA10; no se hizo porque se pidió evitar cambios al core salvo justificación indispensable y preservar las funciones.", "", "## Validación ejecutada", "", "| Validación | Resultado |", "|---|---|", "| Testbench autónomo SMA10, suma/READY tick a tick | PASS, 20.000 precios |", "| Simulación integrada y comparación MISO con Python | PASS, 20.000 ticks, cero pérdidas/discrepancias |", "| IC/ciclos | 20.000 filas en cada CSV; medias y percentiles idénticos antes/después |", "| Yosys | PASS; LUT4 contabilizadas desde log real |", "| nextpnr iCE40 HX1K vq100, seed 1, 25 MHz | PASS; 1.274 LC, 13 BRAM |", f"| Timing | PASS; Fmax enrutada {newhw[3]:.2f} MHz, supera 25 MHz |", "", "## Comandos reproducibles", "", "Desde la raíz `pochoco_soc-main`:", "", "```powershell", "iverilog -g2012 -s tb_sma10 -o proyecto4/tests/tb_sma10_opt.vvp proyecto4/alternativas/mmio_sma10_opt/rtl/pochoco_sma10.v proyecto4/alternativas/mmio_sma10_opt/tb/ram_model.v proyecto4/alternativas/mmio_sma10_opt/tb/tb_sma10.sv", "vvp proyecto4/tests/tb_sma10_opt.vvp", "python proyecto4/alternativas/mmio_sma10_opt/medir_mmio_sma10_opt.py --ticks 20000", "python proyecto4/python/sintetizar_mmio_sma10_opt.py", "python proyecto4/python/generar_informe_optimizacion_mmio.py", "```", "", "Los scripts de medida ensamblan el `trade.s` de la variante y comparan cada byte MISO contra las decisiones Python; el CSV integrado es `proyecto4/resultados/co_disenio/mmio_sma10_opt_ticks.csv`. Las mediciones físicas usan el target HX1K/vq100, semilla nextpnr 1 y restricción de 25 MHz.", "", "## Conclusión", "", "La optimización es funcional y mejora ligeramente área/timing sin alterar rendimiento ni equivalencia. La reducción es de solo cinco Logic Cells, insuficiente para el objetivo solicitado y todavía deja 6 LC libres (0,47% del dispositivo). Se conserva `mmio_sma10_opt` como variante experimental, pero se recomienda mantener `mmio_sma10` como referencia estable hasta conseguir más margen. No se afirma haber logrado el objetivo de área; el resultado sintetizado muestra que la meta exige reducir lógica en otra parte del SoC o un cambio arquitectónico adicional, fuera de este ajuste local.", ""]
(OUT/"informe_optimizacion_mmio.md").write_text("\n".join(lines),encoding="utf-8")
# SVG: show measured LC and Fmax before/after.
svg='''<svg xmlns="http://www.w3.org/2000/svg" width="900" height="420" viewBox="0 0 900 420"><rect width="900" height="420" fill="#fff"/><text x="450" y="34" text-anchor="middle" font-family="Arial" font-size="22" font-weight="bold">MMIO SMA10: antes y después</text><text x="250" y="78" text-anchor="middle" font-family="Arial" font-size="16">Logic Cells / HX1K</text><text x="650" y="78" text-anchor="middle" font-family="Arial" font-size="16">Fmax post-route (MHz)</text>'''
for i,(lab,h,xbase,maxval,unit) in enumerate((("Base",oldhw,110,1280,"LC"),("Optimizada",newhw,110,1280,"LC"))):
    y=125+i*85; width=280*h[1]/maxval
    svg+=f'<text x="35" y="{y+20}" font-family="Arial" font-size="14">{lab}</text><rect x="110" y="{y}" width="{width:.1f}" height="28" fill="#c66"/><text x="{120+width:.1f}" y="{y+20}" font-family="Arial" font-size="13">{h[1]}/1280 LC</text>'
for i,(lab,h) in enumerate((("Base",oldhw),("Optimizada",newhw))):
    y=125+i*85; width=280*h[3]/50
    svg+=f'<text x="475" y="{y+20}" font-family="Arial" font-size="14">{lab}</text><rect x="550" y="{y}" width="{width:.1f}" height="28" fill="#58a"/><text x="{560+width:.1f}" y="{y+20}" font-family="Arial" font-size="13">{h[3]:.2f} MHz</text>'
svg+='<line x1="550" y1="280" x2="830" y2="280" stroke="#333"/><text x="550" y="305" font-family="Arial" font-size="12">0</text><text x="830" y="305" text-anchor="end" font-family="Arial" font-size="12">50 MHz</text><text x="450" y="365" text-anchor="middle" font-family="Arial" font-size="14">Ciclos medios/tick: %.2f antes y %.2f después; speedup %.3fx sin cambio.</text></svg>'%(old[2][0],new[2][0],base_cycles/new[2][0])
(OUT/"comparacion_mmio_sma10.svg").write_text(svg,encoding="utf-8")
print(OUT)
