"""Genera grafico y anexo LaTeX desde los resultados completos del testbench."""
from pathlib import Path
import hashlib,json,os
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'resultados_simulacion/testbench_todas_acciones'
def esc(s):return str(s).replace('_',r'\_').replace('%',r'\%').replace('&',r'\&')
def main():
    data=json.loads((OUT/'resumen.json').read_text(encoding='utf-8'));rows=data['resultados']
    assert len(rows)==data['escenarios'] and all(r['estado']=='PASS' for r in rows)
    assert not any(r['discrepancias'] for r in rows)
    assert hashlib.sha256((ROOT/'competition.bin').read_bytes()).hexdigest()==data['sha256_bin']
    os.environ.setdefault('MPLCONFIGDIR',str(ROOT/'resultados_simulacion/.matplotlib'))
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    known=[r for r in rows if r['grupo']=='practica'];groups=data['grupos']
    fig,axes=plt.subplots(2,1,figsize=(12,8),layout='constrained')
    xs=list(range(len(known)))
    axes[0].bar([x-.2 for x in xs],[r['patrimonio'] for r in known],width=.4,label='Trader RTL')
    axes[0].bar([x+.2 for x in xs],[r['mantener_oficial'] for r in known],width=.4,label='Mantener')
    axes[0].axhline(10000,color='#64748b',linestyle=':',label='Capital inicial')
    labels=['AMD ene','AMD may','Apple 2022','Apple 2023','Meta','Netflix 2022','Netflix 2023','Tesla']
    axes[0].set_xticks(xs,labels,rotation=15);axes[0].set_ylabel('Patrimonio final ($)')
    axes[0].set_title('Ocho series conocidas: ejecuciones verificadas en RTL');axes[0].legend()
    series=[[100*r['ventaja']/r['mantener_oficial'] for r in rows if r['grupo']=='practica'],
        [100*r['ventaja']/r['mantener_oficial'] for r in rows if r['escala']=='prop'],
        [100*r['ventaja']/r['mantener_oficial'] for r in rows if r['escala']=='afin']]
    axes[1].boxplot(series,tick_labels=['Practica (8)','ZIP proporcional (35)','ZIP afin (35)'])
    axes[1].axhline(0,color='#64748b',linestyle=':');axes[1].set_ylabel('Ventaja frente a mantener (%)')
    axes[1].set_title('Distribucion por grupo; las dos escalas comparten los mismos CSV')
    fig.suptitle('Testbench del firmware activo: simulacion, no telemetria de la placa')
    fig.savefig(OUT/'grafico_resumen.png',dpi=160);plt.close(fig)
    grouptex='\n'.join(' & '.join(map(str,[esc(g['grupo']),g['casos'],g['pass_rtl'],g['ventajas'],g['sin_ordenes'],f"{g['media']:.2f}",g['peor'],f"{g['dd_max']:.2f}"]))+r' \\' for g in groups)
    table='\n'.join(' & '.join(map(str,[esc(r['serie']),r['ticks'],r['patrimonio'],r['mantener_oficial'],r['compras'],r['ventas'],f"{r['drawdown_pct']:.2f}",r['primer_compra'],f"{r['us_max']:.2f}"]))+r' \\' for r in rows)
    total=sum(r['ticks'] for r in rows);worst=max(r['us_max'] for r in rows)
    tex=r'''\documentclass[10pt,a4paper,landscape]{article}
\usepackage[T1]{fontenc}\usepackage[utf8]{inputenc}\usepackage[spanish]{babel}
\usepackage{lmodern,geometry,booktabs,longtable,graphicx,hyperref}
\geometry{margin=1.7cm}\setlength{\parindent}{0pt}\setlength{\parskip}{6pt}
\setlength{\emergencystretch}{3em}
\begin{document}
\begin{center}{\LARGE Proyecto 4 -- Testbench de todas las acciones}\\[5pt]
Cristian Acevedo -- Guillermo Arriaza -- Eduardo Ponce\end{center}
\textbf{Alcance.} Se simula Espino RV32E, el firmware de tendencia lenta y el
SPI activo; cada escenario comienza con caja de \$10\,000, cero acciones y
comisión de \$5 por orden ejecutada. Se comprueban MISO, DECISION, caja,
inventario, fills, comisiones y patrimonio por tick, secuencia MMIO, SUM10,
recepción única, registros internos, reinicio y plazo de respuesta.

\textbf{Placa real.} El usuario informó haber reprogramado la FPGA. Este ensayo
no lee la flash ni recibe telemetría de la placa; no certifica su cableado ni
el resultado de la competencia física. Verilator simula en dos estados y
complementa las pruebas previas de cuatro estados con Icarus.

\textbf{Datos.} Ocho series de práctica y 35 CSV adicionales del ZIP, cada uno
en dos escalas: proporcional y afín. Las escalas no son muestras independientes.
Se usan hasta 20\,000 ticks: GOOGL 2021 contiene 18\,844 y Disney 2022,
19\,966. Se prueban sin rellenar precios. Las filas sobrantes de otros archivos
quedan fuera de la ronda. La procedencia externa de los adicionales no se
verificó; su normalización utiliza extremos de la muestra completa como
preprocesamiento retrospectivo y no acredita una transformación causal en vivo.

\textbf{Resultado técnico.} '''+f'{len(rows)}/{len(rows)} PASS; {total:,} ticks; cero discrepancias. Cadencia: {data["periodo_ns"]/1000:g} microsegundos. Peor tiempo observado: {worst:.2f} microsegundos.\n'+r'''
\textbf{Resultado financiero.} PASS indica equivalencia técnica, no ganancia.
No operar conserva \$10\,000. Mantener es el benchmark ideal del curso, con
una comisión inicial y sin límite de 63. La estrategia empieza en caja, revisa
SUM10 cada 128 ticks y cambia de régimen con 5\%; puede no operar.

\begin{center}\begin{tabular}{lrrrrrrr}\toprule
Grupo & Casos & PASS & Supera mantener & Sin órdenes & Patrimonio medio & Peor & DD máx. (\%) \\\midrule
'''+grouptex+r'''
\bottomrule\end{tabular}\end{center}
\textbf{Trazabilidad.} BIN SHA-256: \texttt{'''+data['sha256_bin']+r'''}.
\path{resumen.json} conserva hashes de fuentes, ZIP y trazas. Los CSV por tick,
operaciones, vectores y logs están en \path{build/testbench_todas_acciones/}.
\clearpage\begin{center}\includegraphics[height=0.9\textheight,keepaspectratio]{grafico_resumen.png}\end{center}
\clearpage\section*{Resultados por escenario}
Los ticks comienzan en cero. Primera compra es el tick de ejecución, no el
de señal; $-1$ indica que no hubo compra en todo el escenario.
\begin{longtable}{lrrrrrrrr}\toprule
Serie y escala & Ticks & Trader & Mantener & Compras & Ventas & DD (\%) & Primera compra & Máx. ($\mu$s) \\\midrule\endhead
'''+table+r'''
\bottomrule\end{longtable}
\end{document}
'''
    (OUT/'informe_testbench.tex').write_text(tex,encoding='utf-8')
    print('PASS grafico y LaTeX del testbench generados')
if __name__=='__main__':main()
