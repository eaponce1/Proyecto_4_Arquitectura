"""Genera tablas LaTeX desde CSV/JSON de evidencia; no recalibra la estrategia."""
from pathlib import Path
import csv,json,shutil,statistics as st

ROOT=Path(__file__).resolve().parents[1]
ALT=ROOT/'proyecto4/alternativas/competitiva_definitiva'
OUT=ROOT/'docs/informe'
LABELS={'practica_amd_2022_ene':'AMD enero 2022','practica_amd_2022_may':'AMD mayo 2022',
 'practica_apple_2022':'Apple 2022','practica_apple_2023':'Apple 2023','practica_meta_2022':'Meta 2022',
 'practica_netflix_2022':'Netflix 2022','practica_netflix_2023':'Netflix 2023','practica_tesla_2022':'Tesla 2022'}
KEYS=['amd_enero','amd_mayo','apple_2022','apple_2023','meta_2022','netflix_2022','netflix_2023','tesla_2022']
def read(name):
    with (ALT/'resultados'/name).open(encoding='utf-8',newline='') as f:return list(csv.DictReader(f))
def esc(s):
    return str(s).replace('&',r'\&').replace('_',r'\_').replace('%',r'\%')
def n(x):return f'{int(float(x)):,}'.replace(',',r'\,')
def f(x):return f'{float(x):.2f}'.replace('.',',')
def table(rows):return '\n'.join(' & '.join(map(str,r))+r' \\' for r in rows)

def main():
    OUT.mkdir(parents=True,exist_ok=True);fig=OUT/'figuras';fig.mkdir(exist_ok=True)
    metrics=read('comparacion_final.csv');active=json.loads((ROOT/'build/trader/validacion.json').read_text())
    macro=lambda key,val:'\\newcommand{'+chr(92)+key+'}{'+str(val)+'}\n'
    tex=macro('BinSHA',active['sha256_bin'])+macro('HexSHA',active['sha256_hex'])
    tex+=macro('Celdas',active['lc'])+macro('Bram',active['bram'])+macro('Fmax',f(active['clocks']['clk_soc']['achieved']))
    tex+=macro('TablaResultados',table([[LABELS[r['serie']],n(r['patrimonio']),n(r['mantener_oficial']),n(r['ventaja']),
        r['ordenes'],r['comisiones'],f(r['drawdown_pct'])] for r in metrics]))
    tex+=macro('TablaInventario',table([[LABELS[r['serie']],n(r['caja']),r['acciones'],r['ticks_caja'],r['ticks_exposicion_alta'],n(r['drawdown'])] for r in metrics]))
    baselines=read('comparacion_existentes.csv');families=[]
    for strategy in ['Conservar','SMA10','candidata_final','agresiva','Momentum32','Mantener_SPI']:
        rows=[r for r in baselines if r['estrategia']==strategy]
        families.append([esc(strategy),f(st.mean(int(r['patrimonio']) for r in rows)),n(min(int(r['patrimonio']) for r in rows)),
            f"{sum(int(r['ventaja'])>0 for r in rows)}/8",f(st.mean(int(r['comisiones']) for r in rows))])
    families.append(['Momentum32 + stop 20',f(st.mean(int(r['patrimonio']) for r in metrics)),n(min(int(r['patrimonio']) for r in metrics)),
                     '6/8',f(st.mean(int(r['comisiones']) for r in metrics))])
    tex+=macro('TablaFamilias',table(families))
    folds=read('validacion_por_grupos.csv');walk=read('walk_forward.csv');validation=[]
    for label,rows in [('Excluir empresa',[r for r in folds if r['metodo']=='leave_one_company_out']),
                       ('Excluir serie',[r for r in folds if r['metodo']=='leave_one_series_out']),('Walk-forward',walk)]:
        xs=[float(r['ventaja_pct']) for r in rows]
        validation.append([label,f"{sum(x>0 for x in xs)}/{len(xs)}",f(st.median(xs)),f(st.mean(xs)),f(min(xs))])
    tex+=macro('TablaValidacion',table(validation))
    sensitivity=read('sensibilidad.csv');ss=[]
    for field,label in [('entry','Entrada'),('exit','Salida'),('stop','Stop')]:
        for off in [-2,0,2]:
            rows=[r for r in sensitivity if r['campo']==field and int(r['offset'])==off];xs=[float(r['ventaja_pct']) for r in rows]
            ss.append([label,str(off),f"{sum(x>0 for x in xs)}/8",f(st.median(xs)),f(min(xs))])
    tex+=macro('TablaSensibilidad',table(ss))
    labels={'caida_gradual':'Caída gradual','caida_brusca':'Caída brusca','subida':'Subida','lateral':'Lateral',
       'recuperacion':'Recuperación','limites_inventario':'Saltos e inventario','alternancia':'Alternancia 100/255','integracion_cadencias':'Integración de 48 ticks'}
    tex+=macro('TablaSinteticos',table([[labels[r['escenario']],n(r['patrimonio']),n(r['mantener_oficial']),n(r['drawdown']),r['comisiones']] for r in read('sinteticos.csv')]))
    tex+=macro('TablaDatos',table([[LABELS[r['serie']],r['inicial'],r['final'],f(r['repetidos_pct']),f(r['volatilidad']),r['cambios_significativos_2']] for r in read('estadisticas_series.csv')]))
    tex+=macro('TablaRondas',table([[r['ronda'],n(r['periodo_us']),n(r['disponibles']),r['consumidos_max'],n(r['margen_ciclos']),f(r['margen_us_con_sync'])] for r in read('timing_rondas.csv')]))
    full=json.loads((ROOT/'build/trader/equivalencia_verilator.json').read_text())['series']
    tex+=macro('TablaLatencias',table([[LABELS[r['serie']],f(r['ciclos_media']),r['ciclos_max'],f(r['ic_media']),r['ic_max'],f(r['cpi'])] for r in full]))
    times=json.loads((ROOT/'docs/evidencia_informe/metricas_finales.json').read_text())['series']
    tex+=macro('TablaTiempos',table([[LABELS[r['serie']],f(r['cpi_max']),f(r['tiempo_medio_us']),f(r['tiempo_max_us'])] for r in times]))
    tex+=macro('TablaMomentum',table([[LABELS[r['serie']],r['documentado'],r['reproducido'],r['diferencia']] for r in read('reproduccion_momentum32.csv')]))
    (OUT/'datos_generados.tex').write_text('% Generado automaticamente por tools/generar_informe_latex.py\n'+tex,encoding='utf-8')
    appendix=[]
    for key,r in zip(KEYS,metrics,strict=True):
        shutil.copy2(ROOT/'resultados_simulacion/informe_ocho_series'/key/'grafico.png',fig/f'{key}.png')
        label=LABELS[r['serie']]
        appendix.append(r'\clearpage\subsection{'+label+'}\n'+
            r'\begin{center}\includegraphics[width=\linewidth,height=0.70\textheight,keepaspectratio]{figuras/'+key+'.png}'+r'\end{center}'+'\n'+
            f"Trader: \\${n(r['patrimonio'])}; mantener: \\${n(r['mantener_oficial'])}; ventaja: \\${n(r['ventaja'])}. "
            f"Órdenes: {r['ordenes']}; comisiones: \\${n(r['comisiones'])}; drawdown máximo: {f(r['drawdown_pct'])}\\%.\n\n"+
            'Los marcadores indican fills al precio de ejecución, no señales aplicadas al mismo precio que las generó. '
            'Cada imagen muestra precio y operaciones, patrimonio comparado y drawdown porcentual. '
            'Corresponde a simulación sobre datos conocidos, no a una medición de la placa.\n')
    (OUT/'graficos_series.tex').write_text('\n'.join(appendix),encoding='utf-8')
    print('PASS tablas y ocho figuras LaTeX generadas',OUT)

if __name__=='__main__':main()
