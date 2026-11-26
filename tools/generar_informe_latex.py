"""Tablas y figuras de la tendencia lenta activa; no ajusta parametros."""
from pathlib import Path
import csv,json,shutil,statistics as st
ROOT=Path(__file__).resolve().parents[1]
ALT=ROOT/'proyecto4/alternativas/tendencia_lenta'
OUT=ROOT/'docs/informe'
LABELS={'practica_amd_2022_ene':'AMD enero 2022','practica_amd_2022_may':'AMD mayo 2022',
 'practica_apple_2022':'Apple 2022','practica_apple_2023':'Apple 2023','practica_meta_2022':'Meta 2022',
 'practica_netflix_2022':'Netflix 2022','practica_netflix_2023':'Netflix 2023','practica_tesla_2022':'Tesla 2022'}
KEYS=['amd_enero','amd_mayo','apple_2022','apple_2023','meta_2022','netflix_2022','netflix_2023','tesla_2022']
def read(path):
    with path.open(encoding='utf-8',newline='') as f:return list(csv.DictReader(f))
def n(x):return f'{int(float(x)):,}'.replace(',',r'\,')
def f(x):return f'{float(x):.2f}'.replace('.',',')
def table(rows):return '\n'.join(' & '.join(map(str,r))+r' \\' for r in rows)
def main():
    OUT.mkdir(parents=True,exist_ok=True);fig=OUT/'figuras';fig.mkdir(exist_ok=True)
    rows=read(ALT/'resultados/comparacion_final.csv')
    old=read(ROOT/'proyecto4/alternativas/competitiva_definitiva/resultados/comparacion_final.csv')
    active=json.loads((ROOT/'build/trader/validacion.json').read_text())
    assert active['politica']=='tendencia_lenta_128_5pct'
    full=json.loads((ROOT/'build/trader/equivalencia_verilator.json').read_text())['series']
    times=json.loads((ROOT/'docs/evidencia_informe/metricas_finales.json').read_text())['series']
    def macro(key,val):return '\\newcommand{'+chr(92)+key+'}{'+str(val)+'}\n'
    tex=macro('BinSHA',active['sha256_bin'])+macro('HexSHA',active['sha256_hex'])
    tex+=macro('Celdas',active['lc'])+macro('Bram',active['bram'])+macro('Fmax',f(active['clocks']['clk_soc']['achieved']))
    tex+=macro('TablaResultados',table([[LABELS[r['serie']],n(r['patrimonio']),n(r['mantener_oficial']),n(r['ventaja']),r['ordenes'],r['comisiones'],f(r['drawdown_pct'])] for r in rows]))
    tex+=macro('TablaComparacion',table([[LABELS[r['serie']],n(a['patrimonio']),n(r['patrimonio']),n(int(r['patrimonio'])-int(a['patrimonio']))] for a,r in zip(old,rows,strict=True)]))
    tex+=macro('TablaInventario',table([[LABELS[r['serie']],n(r['caja']),r['acciones'],r['ticks_caja'],r['ticks_invertido'],n(r['drawdown'])] for r in rows]))
    tex+=macro('TablaLatencias',table([[LABELS[r['serie']],f(r['ciclos_media']),r['ciclos_max'],r['ic_max'],f(r['cpi'])] for r in full]))
    tex+=macro('TablaTiempos',table([[LABELS[r['serie']],f(r['cpi_max']),f(r['tiempo_medio_us']),f(r['tiempo_max_us'])] for r in times]))
    synth=json.loads((ALT/'resultados/equivalencia_rv32e.json').read_text())['series'][8:]
    tex+=macro('TablaSinteticos',table([[r['serie'].replace('_',r'\_'),n(r['patrimonio']),n(r['mantener_oficial']),r['ordenes'],f(r['drawdown_pct'])] for r in synth]))
    tex+=macro('MediaLenta',f(st.mean(int(r['patrimonio']) for r in rows)))
    tex+=macro('MediaAnterior',f(st.mean(int(r['patrimonio']) for r in old)))
    campaign=json.loads((ROOT/'resultados_simulacion/testbench_todas_acciones/resumen.json').read_text(encoding='utf-8'))
    assert campaign['sha256_bin']==active['sha256_bin'] and len(campaign['resultados'])==78
    assert all(r['estado']=='PASS' and r['discrepancias']==0 for r in campaign['resultados'])
    tex+=macro('TablaCampania',table([[g['grupo'],f"{g['pass_rtl']}/{g['casos']}",f"{g['ventajas']}/{g['casos']}",
        g['sin_ordenes'],f(g['media']),n(g['peor']),f(g['dd_max'])] for g in campaign['grupos']]))
    shutil.copy2(ROOT/'resultados_simulacion/testbench_todas_acciones/grafico_resumen.png',fig/'todas_acciones_resumen.png')
    allrows=table([[r['serie'].replace('_',r'\_'),n(r['ticks']),n(r['patrimonio']),n(r['mantener_oficial']),
        f"{r['compras']}/{r['ventas']}",f(r['drawdown_pct'])] for r in campaign['resultados']])
    (OUT/'resultados_todas_acciones.tex').write_text(r'''\small
\begin{longtable}{lrrrrr}\toprule
Serie y escala & Ticks & Trader & Mantener & C/V & DD (\%) \\\midrule\endhead
'''+allrows+r'''
\bottomrule\end{longtable}\normalsize
''',encoding='utf-8')
    (OUT/'datos_generados.tex').write_text('% Generado desde evidencia de tendencia lenta\n'+tex,encoding='utf-8')
    appendix=[]
    for key,r in zip(KEYS,rows,strict=True):
        shutil.copy2(ROOT/'resultados_simulacion/informe_tendencia_lenta'/key/'grafico.png',fig/f'{key}.png')
        appendix.append(r'\clearpage\subsection{'+LABELS[r['serie']]+'}\n'+
            r'\begin{center}\includegraphics[width=\linewidth,height=0.70\textheight,keepaspectratio]{figuras/'+key+'.png}'+r'\end{center}'+'\n'+
            f"Trader: \\${n(r['patrimonio'])}; mantener: \\${n(r['mantener_oficial'])}; ventaja: \\${n(r['ventaja'])}. "
            f"Órdenes: {r['ordenes']}; comisiones: \\${n(r['comisiones'])}; drawdown máximo: {f(r['drawdown_pct'])}\\%.\n\n"+
            'Los marcadores representan ejecuciones al precio siguiente al que generó la señal. Es simulación sobre datos conocidos; no es telemetría de la placa.\n')
    (OUT/'graficos_series.tex').write_text('\n'.join(appendix),encoding='utf-8')
    print('PASS tablas y ocho figuras de tendencia lenta generadas')
if __name__=='__main__':main()
