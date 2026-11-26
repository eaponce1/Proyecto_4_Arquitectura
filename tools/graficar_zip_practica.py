"""Graficos, visor HTML y fuente LaTeX a partir de la nueva traza RTL del ZIP."""
from pathlib import Path
import csv,gzip,hashlib,html,io,json,os
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'resultados_simulacion/testbench_zip_practica'
def esc(s):return str(s).replace('_',r'\_').replace('&',r'\&').replace('%',r'\%')
def main():
    data=json.loads((OUT/'resumen.json').read_text(encoding='utf-8'))
    assert data['resultados'] and all(r['estado']=='PASS' for r in data['resultados'])
    assert hashlib.sha256((ROOT/'competition.bin').read_bytes()).hexdigest()==data['sha256_bin']
    os.environ.setdefault('MPLCONFIGDIR',str(ROOT/'resultados_simulacion/.matplotlib'))
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    figdir=OUT/'graficos';figdir.mkdir(exist_ok=True)
    plots=[];table=[];webrows=[]
    for r in data['resultados']:
        raw=gzip.decompress((ROOT/r['traza_archivada']).read_bytes())
        assert hashlib.sha256(raw).hexdigest()==r['sha256_traza']
        a=list(csv.DictReader(io.StringIO(raw.decode())))
        xs=[int(x['tick']) for x in a];prices=[int(x['precio']) for x in a]
        wealth=[int(x['patrimonio']) for x in a];q=9995//prices[0]
        bh=[9995-q*prices[0]+q*p for p in prices];peak=10000;dd=[]
        for w in wealth:peak=max(peak,w);dd.append(100*(peak-w)/peak)
        assert abs(max(dd)-r['drawdown_pct'])<1e-8
        fig,axes=plt.subplots(3,1,figsize=(12,9),sharex=True,layout='constrained')
        axes[0].plot(xs,prices,color='#334155',lw=.8,label='Precio recibido por SPI')
        for action,color,marker,label in [(1,'#15803d','^','Compra ejecutada'),(2,'#dc2626','v','Venta ejecutada')]:
            points=[x for x in a if int(x['fill'])>0 and int(x['miso_hex'],16)>>6==action]
            axes[0].scatter([int(x['tick']) for x in points],[int(x['precio']) for x in points],c=color,marker=marker,s=30,label=label)
        axes[0].set_ylabel('Precio');axes[0].legend(loc='best')
        axes[1].plot(xs,wealth,label='Patrimonio RTL',color='#2563eb')
        axes[1].plot(xs,bh,label='Mantener oficial',color='#ea580c')
        axes[1].axhline(10000,color='#64748b',ls=':',label='Capital inicial')
        axes[1].set_ylabel('Patrimonio ($)');axes[1].legend(loc='best')
        axes[2].fill_between(xs,dd,color='#dc2626',alpha=.25)
        axes[2].set_ylabel('Drawdown (%)');axes[2].set_xlabel('Tick (inicio en cero)')
        for ax in axes:ax.grid(alpha=.2)
        fig.suptitle(r['serie']+' | Nueva ejecucion RTL desde el ZIP; no telemetria fisica')
        filename=r['serie']+'.png';fig.savefig(figdir/filename,dpi=150);plt.close(fig)
        plots.append(r'\clearpage\subsection*{'+esc(r['serie'])+'}\n'+
            r'\begin{center}\includegraphics[width=\linewidth,height=0.78\textheight,keepaspectratio]{graficos/'+filename+r'}\end{center}'+'\n'+
            f"Primera compra: tick {r['primer_compra']}; primera venta: tick {r['primer_venta']}. "
            f"Patrimonio final: \\${r['patrimonio']}; comisiones: \\${r['comisiones']}.\n")
        table.append(' & '.join(map(str,[esc(r['serie']),r['patrimonio'],r['mantener_oficial'],r['compras'],r['ventas'],f"{r['drawdown_pct']:.2f}",r['primer_compra']]))+r' \\')
        webrows.append('<tr>'+''.join('<td>'+html.escape(str(v))+'</td>' for v in [r['serie'],r['estado'],r['patrimonio'],r['mantener_oficial'],r['ventaja'],r['compras'],r['ventas'],r['primer_compra'],f"{r['us_max']:.2f}"])+'</tr>')
    allpass=f"{len(data['resultados'])}/{len(data['resultados'])} PASS"
    tex=r'''\documentclass[10pt,a4paper]{article}
\usepackage[T1]{fontenc}\usepackage[utf8]{inputenc}\usepackage[spanish]{babel}
\usepackage{lmodern,geometry,graphicx,booktabs,hyperref}\geometry{margin=1.8cm}
\setlength{\parindent}{0pt}\setlength{\parskip}{6pt}\setlength{\emergencystretch}{3em}
\hypersetup{pdftitle={Proyecto 4: testbench del ZIP de practica},pdfauthor={Cristian Acevedo; Guillermo Arriaza; Eduardo Ponce}}
\begin{document}
\begin{center}{\LARGE Proyecto 4 -- Prueba del ZIP de práctica}\\[6pt]
Cristian Acevedo -- Guillermo Arriaza -- Eduardo Ponce\end{center}
\textbf{Entrada:} \path{'''+data['zip_nombre']+r'''}. Nueva ejecución del procesador,
SPI y firmware activos, leyendo los precios exactos del ZIP sin normalización.
Los CSV son idénticos a las ocho series conocidas; esta repetición no es una
prueba fuera de muestra. Cada caso comienza con \$10\,000 y cero acciones.
Se cobra \$5 por orden ejecutada y se comprueba cada tick frente al modelo.

\textbf{Resultado:} '''+f"{allpass}; {data['ticks']:,} ticks; {data['discrepancias']} discrepancias; {data['compras']} compras y {data['ventas']} ventas. Cadencia: {data['periodo_ns']/1000:g} microsegundos. "+r'''
\textbf{Máximo observado:} '''+f"{max(r['us_max'] for r in data['resultados']):.2f} microsegundos; margen conservador {min(r['margen_us'] for r in data['resultados']):.2f} microsegundos.\n"+r'''

\begin{center}\scriptsize\begin{tabular}{lrrrrrr}\toprule
Serie & Trader & Mantener & Compras & Ventas & DD (\%) & Primera compra \\\midrule
'''+('\n'.join(table))+r'''
\bottomrule\end{tabular}\end{center}
La estrategia supera a mantener en '''+f"{data['ventajas']}/{len(data['resultados'])}"+r''' series.
PASS indica coincidencia técnica, no rentabilidad. Los gráficos se calculan a
partir de las trazas RTL de esta ejecución. Los marcadores son operaciones
ejecutadas al precio siguiente al de la señal; los ticks empiezan en cero.

\textbf{Comportamiento.} SUM10 se revisa cada 128 ticks con umbral de 5\%.
Empieza en caja; la primera ejecución posible es en tick 257 y puede tardar más.
En Netflix 2023 ocurre en tick 2177: 21,77 segundos si la maestra usa 10 ms.
D4 apagado antes de una señal es esperable. Se verifican registros CPU,
STATUS/PRICE/SUM10/READY/DECISION, recepción única, reinicio y plazo de respuesta.

\textbf{Alcance.} Verilator simula en dos estados y complementa las pruebas
Icarus previas. Esta ejecución no lee la flash ni recibe telemetría física.
\par\smallskip\textbf{BIN SHA-256}\par
{\small\ttfamily '''+data['sha256_bin']+r'''}\par
\path{resumen.json} conserva hashes de ZIP, fuentes y trazas comprimidas.
'''+('\n'.join(plots))+r'\end{document}'
    (OUT/'informe_zip.tex').write_text(tex,encoding='utf-8')
    headers=['Serie','RTL','Trader','Mantener','Ventaja','Compras','Ventas','Primera compra','Máx. µs']
    page='''<!doctype html><html lang="es"><meta charset="utf-8"><title>Prueba del ZIP de práctica</title>
<style>body{font:16px system-ui;margin:24px;color:#182338}table{border-collapse:collapse}td,th{padding:8px;border:1px solid #ddd;text-align:right}td:first-child{text-align:left}img{max-width:100%;height:auto}th{background:#edf2fa}</style>
<h1>Testbench del ZIP de práctica</h1><p>'''+html.escape(data['zip_nombre'])+' · '+allpass+f" · {data['ticks']:,} ticks · {data['compras']} compras y {data['ventas']} ventas."+'''
</p><p>Nueva simulación RTL con el firmware actual y los precios exactos del ZIP. Los CSV coinciden con las ocho series conocidas. No es telemetría física ni una muestra nueva.</p>
<p><a href="INFORME_ZIP_PRACTICA.pdf">PDF</a> · <a href="resumen.csv">CSV</a> · <a href="INFORME.md">Informe</a></p>
<table><tr>'''+''.join('<th>'+h+'</th>' for h in headers)+'</tr>'+''.join(webrows)+'</table>'+''.join(
        '<h2>'+html.escape(r['serie'])+'</h2><img loading="lazy" src="graficos/'+html.escape(r['serie'])+'.png" alt="Precio, operaciones, patrimonio y drawdown">' for r in data['resultados'])+'</html>'
    (OUT/'ABRIR_RESULTADOS.html').write_text(page,encoding='utf-8')
    print('PASS ocho graficos de trazas RTL, visor HTML y fuente LaTeX')
if __name__=='__main__':main()
