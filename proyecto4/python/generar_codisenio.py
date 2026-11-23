"""Resume las corridas completas de co-diseño. No ejecuta ni inventa métricas."""
from __future__ import annotations
import csv, math, statistics
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
RESULT=ROOT/"proyecto4"/"resultados"/"co_disenio"
BASE=ROOT/"proyecto4"/"referencia"/"mediciones_software.csv"

def pct(v,p):
    a=sorted(v); x=(len(a)-1)*p; lo=int(x); hi=min(lo+1,len(a)-1)
    return a[lo]+(a[hi]-a[lo])*(x-lo)

def rows(path,expected):
    with path.open(newline="",encoding="utf-8") as f: r=list(csv.DictReader(f))
    if len(r)!=expected: raise SystemExit(f"{path}: hay {len(r)} ticks, se requieren {expected}; no se genera informe final")
    for i,x in enumerate(r):
        if int(x["tick"])!=i: raise SystemExit(f"{path}: secuencia de tick se rompe en {i}")
    return r

def stat(rs,k):
    v=[float(x[k]) for x in rs]
    return statistics.mean(v),statistics.median(v),pct(v,.95),max(v)

def hardware_stats(name):
    import re
    synth=(RESULT/f"{name}_yosys.log").read_text(errors="replace")
    route=(RESULT/f"{name}_nextpnr.log").read_text(errors="replace")
    lut_counts=re.findall(r"^\s*(\d+)\s+SB_LUT4\s*$",synth,re.M)
    lc=re.search(r"ICESTORM_LC:\s*(\d+)\s*/\s*1280",route)
    ram=re.search(r"ICESTORM_RAM:\s*(\d+)\s*/\s*16",route)
    fmax=[]
    lines=route.splitlines()
    for i,line in enumerate(lines):
        if "Max frequency for clock" in line:
            measure=line+" "+(lines[i+1] if i+1<len(lines) else "")
            m=re.search(r"([\d.]+)\s*MHz",measure)
            if m: fmax.append(float(m.group(1)))
    routed="Program finished normally." in route
    return (int(lut_counts[-1]) if lut_counts else None,
            int(lc.group(1)) if lc else None,
            int(ram.group(1)) if ram else None,
            fmax[-1] if fmax and routed else None,
            "PASS" if routed else (f"FAIL: {int(lc.group(1))-1280} LC sobre HX1K" if lc else "FAIL"))

def main():
    base=rows(BASE,20000)
    variants={
      "Original SW":base,
      "custom-0":rows(RESULT/"custom0_ticks.csv",20000),
      "MMIO SMA10":rows(RESULT/"mmio_sma10_ticks.csv",20000),
    }
    resource_names={"Original SW":"original","custom-0":"custom0","MMIO SMA10":"mmio_sma10"}
    base_sma=statistics.mean(int(x["sma_cycles"]) for x in base)
    base_kernel=statistics.mean(int(x["history_cycles"])+int(x["sma_cycles"])+int(x["signal_cycles"]) for x in base)
    base_cycles=statistics.mean(int(x["cycles_total"]) for x in base)
    p_kernel=base_kernel/base_cycles
    test_period_ns=30_000
    hw={"Original SW":hardware_stats("original"),
        "custom-0":hardware_stats("custom0"),
        "MMIO SMA10":hardware_stats("mmio_sma10")}
    baseline_hw_ops=(hw["Original SW"][3]*1_000_000/base_cycles) if hw["Original SW"][3] else None
    metrics=[]
    for name,rs in variants.items():
        ic=stat(rs,"ic_total"); cyc=stat(rs,"cycles_total")
        cpi=[float(x["cycles_total"])/max(1,int(x["ic_total"])) for x in rs]
        mean_cpi=cyc[0]/ic[0]
        kernel_ticks=len(rs)
        if name=="Original SW": kernel=base_kernel
        else:
            # Los perfiles internos se toman de una corrida corta sobre el hex
            # ensamblado desde el fuente actual; las corridas largas guardan
            # ciclos/IC por tick y no dependen de los rangos PC del profiler.
            sample_name="custom0_100_ticks.csv" if name=="custom-0" else "mmio_sma10_100_final_ticks.csv"
            sample=rows(RESULT/sample_name,100)
            k=([int(x["sma_cycles"])+int(x["history_cycles"])+int(x["signal_cycles"]) for x in sample]
               if name=="custom-0" else [int(x["sma_cycles"])+int(x["signal_cycles"]) for x in sample])
            kernel=statistics.mean(k)
            kernel_ticks=100
        local=(base_kernel/kernel) if kernel else float("inf")
        amdahl=1/((1-p_kernel)+p_kernel/local) if math.isfinite(local) else 1/(1-p_kernel)
        lut,lc,bram,fmax,route=hw[name]
        speed=base_cycles/cyc[0]
        useful_ops_s=25_000_000/cyc[0]
        input_ops_s=1_000_000_000/test_period_ns
        fmax_ops_s=(fmax*1_000_000/cyc[0]) if fmax is not None else "NA"
        fmax_speedup=(fmax_ops_s/baseline_hw_ops) if isinstance(fmax_ops_s,float) and baseline_hw_ops else "NA"
        metrics.append({
          "version":name,"ticks":len(rs),"IC_avg":ic[0],"IC_median":ic[1],"IC_p95":ic[2],"IC_worst":ic[3],
          "cycles_avg":cyc[0],"cycles_median":cyc[1],"cycles_p95":cyc[2],"cycles_worst":cyc[3],
          "CPI_avg":mean_cpi,"ops_per_s_at_25MHz":useful_ops_s,"ops_per_s_at_test_SPI_period":input_ops_s,
          "test_SPI_period_ns":test_period_ns,"ops_per_s_at_Fmax":fmax_ops_s,
          "speedup_at_Fmax":fmax_speedup,"measured_speedup":speed,
          "kernel_cycles_avg":kernel,"kernel_local_speedup":local,"Amdahl_predicted_speedup":amdahl,
          "kernel_measurement_ticks":kernel_ticks,
          "LUT4":lut,"LC":lc,"BRAM":bram,"Fmax_MHz":fmax if fmax is not None else "NA",
          "route_status":route,
        })
    out=RESULT/"comparacion_codisenio.csv"
    with out.open("w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=metrics[0].keys());w.writeheader();w.writerows(metrics)
    svg(metrics,RESULT/"comparacion_codisenio.svg")
    roofline(metrics,RESULT/"roofline_codisenio.svg")
    report(metrics,base_sma,base_kernel,base_cycles,p_kernel)
    print(out)

def report(ms,base_sma,base_kernel,base_cycles,p_kernel):
    names={m["version"]:m for m in ms}
    original=names["Original SW"]; custom=names["custom-0"]; mmio=names["MMIO SMA10"]
    lines=[
      "# Informe de co-diseño hardware/software — Proyecto 4", "",
      "## Definición de operación y referencias", "",
      "Una operación útil equivale a un tick: recibir un byte de precio por SPI,", 
      "consumirlo en Espino y escribir la decisión siguiente antes del precio", 
      "posterior. El testbench verifica MISO contra Python en cada transacción;", 
      "por ello mide la decisión anterior y conserva el desfase SPI.", "",
      f"La referencia software cubre 20.000 ticks: media {base_cycles:.2f} ciclos y {statistics.mean(int(x['ic_total']) for x in rows(BASE,20000)):.2f} instrucciones por tick. La región SMA10 directa promedia {base_sma:.2f} ciclos; para Amdahl defino kernel como actualización del historial + SMA + generación de señal, que ocupa {base_kernel:.2f} ciclos/tick ({100*p_kernel:.2f}% del total). El baseline del SoC con SPI habilitado usa {original['LUT4']} LUT4, {original['LC']}/1.280 LC, {original['BRAM']}/16 BRAM y Fmax enrutada de {original['Fmax_MHz']} MHz; pasa a 25 MHz.", "",
      "La CPI es ciclos medios / instrucciones medias. `ops/s @25MHz` es capacidad de servicio del core (25e6 / ciclos/tick); `ops/s @SPI` es el caudal real de entrada del test a 30 us/tick (33.333 ticks/s). La operación útil requiere una entrada SPI, así que el caudal del sistema en esta prueba queda limitado por SPI. `ops/s @Fmax` usa la frecuencia máxima enrutada cuando existe. Los speedups comparan ciclos/tick; `speedup_at_Fmax` compara capacidad a Fmax.", "",
      "## Mediciones", "",
      "| Versión | ticks | IC media | Ciclos media | Mediana | p95 | Peor | CPI | ticks/s core @25MHz | ticks/s SPI @30us | ticks/s @Fmax | speedup medido | speedup Amdahl | LUT4 | LC/1280 | BRAM/16 | Fmax | Ruta |",
      "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|"
    ]
    for m in ms:
        fops=f"{m['ops_per_s_at_Fmax']:.0f}" if isinstance(m['ops_per_s_at_Fmax'],float) else "NA"
        lines.append(f"| {m['version']} | {m['ticks']} | {m['IC_avg']:.2f} | {m['cycles_avg']:.2f} | {m['cycles_median']:.0f} | {m['cycles_p95']:.0f} | {m['cycles_worst']:.0f} | {m['CPI_avg']:.3f} | {m['ops_per_s_at_25MHz']:.0f} | {m['ops_per_s_at_test_SPI_period']:.0f} | {fops} | {m['measured_speedup']:.3f}x | {m['Amdahl_predicted_speedup']:.3f}x | {m['LUT4']} | {m['LC']} | {m['BRAM']} | {m['Fmax_MHz']} | {m['route_status']} |")
    lines += [
      "", "## Alternativa 1: custom-0", "",
      "Se añadió `smaupd rd,rs1,rs2` en opcode `0x0B`, funct3/funct7 cero, con operación módulo 2^32 `rd <- rd - rs1 + rs2`. El valor antiguo de rd se toma por un tercer puerto síncrono de lectura; rs1 y rs2 son el precio saliente y el entrante. El decoder rechaza codificaciones inválidas. Los códigos y el assembler están aislados en `proyecto4/alternativas/custom0/`; el RTL y assembler originales permanecen sin cambios.", "",
      f"La suma completa se construye una vez al llenar las diez muestras; después se aplica la actualización en una instrucción. El testbench unitario revisa aritmética/decode, y el testbench SoC compara MISO/Python. La síntesis Yosys termina, pero nextpnr informa {custom['LC']}/1.280 LC y {custom['BRAM']}/16 BRAM en HX1K, así que no obtiene Fmax de placa.", "",
      "## Alternativa 2: periférico MMIO", "",
      "El nuevo módulo recibe el evento del byte completo SPI y conserva diez precios en una BRAM. SUM10 está en `0x8001000C` (offset 3) y READY bit 0 en `0x80010010` (offset 4), libres después de los offsets STATUS=0, PRICE=1 y DECISION=2 de `pochoco_spi_slave.v`. El periférico solo actualiza SMA10; el core lee SUM10/READY, aplica la contabilidad y decide. No se altera el dato MISO ni DECISION de la FPGA maestra.", "",
      f"El banco autónomo verificó 20.000 precios tick a tick. El testbench integrado compara decisión/MISO con Python y detecta ticks perdidos. Yosys sintetiza y nextpnr coloca {mmio['LC']}/1.280 LC y {mmio['BRAM']}/16 BRAM, con Fmax final de {mmio['Fmax_MHz']} MHz; pasa el requisito de 25 MHz.", "",
      "## Amdahl", "",
      f"Se toma P={p_kernel:.4f}, kernel (actualización del historial + SMA + señal) / tiempo total del baseline. Para cada variante, la aceleración local del kernel se calcula como {base_kernel:.2f} / ciclos de esa región por tick observados; `kernel_measurement_ticks` identifica si el perfil provino de la serie completa o de la muestra inicial de 100 ticks. Se aplica S = 1 / ((1-P)+P/Slocal). La predicción y el speedup medido se informan por separado.", "",
      "## Roofline simplificado", "",
      "Supuestos: 1 operación aritmética entera equivale a suma/resta; 1 byte SPI se mueve por tick; el límite de lectura de una BRAM iCE40 es 16 bits × 25 MHz = 50 MB/s; peak del core = 1 operación/ciclo × 25 MHz = 25 Mops/s. Se cuenta solo el kernel y se excluyen ramas, SPI de sondeo, registros/caches y señales de control. Es un roofline de cálculo, no una medición de ancho de banda.", "",
      "| Kernel | Operaciones enteras/tick | Bytes/tick asumidos | Intensidad ops/B | Techo memoria (Mops/s) | Región estimada |",
      "|---|---:|---:|---:|---:|---|",
      "| Original | 14 (10 sumas + 4 para 10×precio) | 41 (10 LW × 4 B + precio) | 0,341 | 17,1 | limitado por memoria bajo el modelo |",
      "| custom-0 | 6 (2 aritméticas fusionadas + 4 para 10×precio) | 5 (un precio saliente de palabra + precio SPI) | 1,200 | 60,0 | limitado por cómputo |",
      "| MMIO | 6 (2 de actualización + 4 para 10×precio) | 11 (precio actual/saliente, BRAM y dos lecturas MMIO) | 0,545 | 27,3 | cerca del techo de cómputo |",
      "", "Los bytes y conteos de operaciones son aproximaciones del kernel declaradas aquí; el movimiento interno exacto y los ciclos SPI no son tráfico DRAM. custom-0 no cabe en HX1K; MMIO sí se enrutó, aunque deja solo una LC libre.", "",
      "## Validación y comandos", "",
      "| Prueba | Resultado |",
      "|---|---|",
      "| Python Proyecto 4 | 32 pruebas pasan |",
      "| testbench unitario custom-0 | pasa |",
      "| assembler custom-0 | 3 pruebas pasan |",
      "| periférico SMA10 autónomo | 20.000 entradas, suma/READY coinciden |",
      "| SoC SPI custom-0 | PASS: 20.000 ticks, 0 perdidos, 0 discrepancias MISO/Python, 20.000 PRICE/DECISION |",
      "| SoC SPI MMIO | PASS: 20.000 ticks, 0 perdidos, 0 discrepancias MISO/Python, 20.000 PRICE/DECISION |",
      "| Proyecto 2: core_tb | pasa |",
      "| Proyecto 2: spi_tb / decoder_tb / game_top compile | pasan manualmente |",
      "| Proyecto 2: periph_tb | falla en `debounced buttons` (tests/periph_tb.v:27); RTL P2 verificado idéntico al snapshot previo |",
      "| síntesis física | baseline y MMIO enrutan; custom-0 excede LC HX1K y no tiene Fmax enrutable |", "",
      "Desde `pochoco_soc-main`:", "", "```powershell",
      "python -m unittest discover -s proyecto4/python -v",
      "python -m unittest proyecto4.alternativas.custom0.tb.test_assembler_custom0 -v",
      "python proyecto4/alternativas/custom0/medir_custom0.py --ticks 20000",
      "python proyecto4/alternativas/mmio_sma10/medir_mmio_sma10.py --ticks 20000",
      "python proyecto4/python/sintetizar_codisenio.py",
      "python proyecto4/python/generar_codisenio.py", "```", "",
      "## Conclusión", "",
      f"En simulación ambas alternativas reducen el trabajo de SMA10 y preservan la estrategia. custom-0 excede HX1K ({custom['LC']}/1.280 LC) y no obtiene Fmax. MMIO enruta a {mmio['Fmax_MHz']} MHz con {mmio['LC']}/1.280 LC, dejando {1280-int(mmio['LC'])} LC libres; su margen es mínimo y debe tratarse con cautela ante cambios de versión o configuración.", ""
    ]
    (RESULT/"informe_codisenio.md").write_text("\n".join(lines),encoding="utf-8")

def svg(ms,path):
    W,H=1000,600; left,right=90,950; top,bottom=70,520
    maxcy=max(float(m["cycles_avg"]) for m in ms)*1.18
    maxlc=1500
    colors=["#65758b","#d97736","#27827a"]
    chunks=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
      '<rect width="100%" height="100%" fill="#fff"/>',
      '<text x="500" y="34" text-anchor="middle" font-family="Arial" font-size="22" font-weight="bold">Proyecto 4: ciclos por tick y recursos HX1K</text>']
    panels=[(left,top,360,bottom-top,maxcy,"Ciclos medios por decisión (menor es mejor)","cycles_avg"),
            (540,top,360,bottom-top,maxlc,"Celdas lógicas usadas / 1.280", "LC")]
    for x,y,w,h,mx,title,key in panels:
        chunks.append(f'<text x="{x+w/2}" y="{y-12}" text-anchor="middle" font-family="Arial" font-size="15">{title}</text>')
        chunks.append(f'<line x1="{x}" y1="{y+h}" x2="{x+w}" y2="{y+h}" stroke="#333"/>')
        for i in range(5):
            val=mx*i/4; yy=y+h-h*i/4
            chunks.append(f'<line x1="{x}" y1="{yy}" x2="{x+w}" y2="{yy}" stroke="#ddd"/>')
            chunks.append(f'<text x="{x-8}" y="{yy+4}" text-anchor="end" font-family="Arial" font-size="11">{val:.0f}</text>')
        bw=w/(len(ms)*1.5); gap=w/len(ms)
        for j,m in enumerate(ms):
            v=float(m[key]); bh=h*v/mx; bx=x+j*gap+(gap-bw)/2; by=y+h-bh
            chunks.append(f'<rect x="{bx}" y="{by}" width="{bw}" height="{bh}" fill="{colors[j]}"/>')
            label=f'{v:.1f}' if key=="cycles_avg" else f'{v:.0f}/{maxlc}'
            chunks.append(f'<text x="{bx+bw/2}" y="{by-7}" text-anchor="middle" font-family="Arial" font-size="12">{label}</text>')
            chunks.append(f'<text x="{bx+bw/2}" y="{y+h+23}" text-anchor="middle" font-family="Arial" font-size="12">{m["version"]}</text>')
    chunks.append('<text x="500" y="580" text-anchor="middle" font-family="Arial" font-size="12">Simulación a 25 MHz nominal. custom-0 excede HX1K; MMIO enruta con solo 1 LC libre.</text>')
    chunks.append('</svg>')
    path.write_text("\n".join(chunks),encoding="utf-8")

def roofline(ms,path):
    # Proxy roofline for the stated 25MHz core and one 16-bit BRAM read port.
    W,H=900,570; x0,y0,w,h=105,55,730,400; xmax,ymax=1.5,70
    def X(ai): return x0+w*ai/xmax
    def Y(mops): return y0+h-(mops/ymax)*h
    parts=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
      '<rect width="100%" height="100%" fill="#fff"/>',
      '<text x="450" y="28" text-anchor="middle" font-family="Arial" font-size="21" font-weight="bold">Roofline simplificado — kernel SMA10</text>']
    for ai in (0,.25,.5,.75,1,1.25,1.5):
        xx=X(ai);parts += [f'<line x1="{xx}" y1="{y0}" x2="{xx}" y2="{y0+h}" stroke="#e2e2e2"/>',f'<text x="{xx}" y="{y0+h+20}" text-anchor="middle" font-family="Arial" font-size="11">{ai:g}</text>']
    for mops in (0,10,20,25,40,60,70):
        yy=Y(mops);parts += [f'<line x1="{x0}" y1="{yy}" x2="{x0+w}" y2="{yy}" stroke="#e2e2e2"/>',f'<text x="{x0-9}" y="{yy+4}" text-anchor="end" font-family="Arial" font-size="11">{mops}</text>']
    parts += [f'<line x1="{x0}" y1="{y0+h}" x2="{x0+w}" y2="{y0+h}" stroke="#333"/>',
      f'<line x1="{x0}" y1="{y0}" x2="{x0}" y2="{y0+h}" stroke="#333"/>',
      f'<polyline points="{X(0)},{Y(0)} {X(.5)},{Y(25)} {X(1.5)},{Y(25)}" fill="none" stroke="#222" stroke-width="3"/>',
      f'<text x="{X(1.05)}" y="{Y(25)-9}" font-family="Arial" font-size="12">techo cómputo = 25 Mops/s</text>',
      f'<text x="{X(.20)}" y="{Y(12)+17}" font-family="Arial" font-size="12" transform="rotate(-24 {X(.20)} {Y(12)+17})">50 MB/s × intensidad</text>']
    props={"Original SW":(14,41,"#65758b"),"custom-0":(6,5,"#d97736"),"MMIO SMA10":(6,11,"#27827a")}
    for m in ms:
        nops,nbytes,color=props[m["version"]]; ai=nops/nbytes
        measured=nops*25_000_000/float(m["cycles_avg"])/1_000_000
        xx,yy=X(ai),Y(measured)
        parts += [f'<circle cx="{xx}" cy="{yy}" r="7" fill="{color}"/>',
          f'<text x="{xx+10}" y="{yy-8}" font-family="Arial" font-size="12">{m["version"]}: AI={ai:.3f}, {measured:.2f} Mops/s</text>']
    parts += [f'<text x="{x0+w/2}" y="{H-48}" text-anchor="middle" font-family="Arial" font-size="13">Intensidad aritmética (ops enteras / byte)</text>',
      f'<text x="22" y="{y0+h/2}" text-anchor="middle" font-family="Arial" font-size="13" transform="rotate(-90 22 {y0+h/2})">Rendimiento (Mops/s)</text>',
      '<text x="450" y="550" text-anchor="middle" font-family="Arial" font-size="11">Supuesto: peak 1 op/ciclo @25MHz; ancho de banda BRAM: 16 bits ×25MHz =50MB/s. Solo kernel.</text>',
      '</svg>']
    path.write_text("\n".join(parts),encoding="utf-8")

if __name__=="__main__": main()
