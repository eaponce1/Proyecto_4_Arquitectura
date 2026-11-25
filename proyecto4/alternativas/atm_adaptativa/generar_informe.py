"""Informe auditable: no convierte un NO-GO financiero en aprobación de hardware."""
from pathlib import Path
import csv,gzip,json,os,statistics as st
from dataclasses import asdict
from estrategia_atm import population
from baselines import active,OLD
HERE=Path(__file__).resolve().parent;OUT=HERE/'resultados'
LABELS=['AMD enero','AMD mayo','Apple 2022','Apple 2023','Meta 2022','Netflix 2022','Netflix 2023','Tesla 2022']

def read(p):
    with p.open(encoding='utf-8',newline='') as f:return list(csv.DictReader(f))
def n(x):return f'{float(x):,.0f}'.replace(',','.')
def f(x):return f'{float(x):.2f}'.replace('.',',')
def table(rows):return '\n'.join(' | '.join(map(str,r)) for r in rows)

def main():
    d=json.loads((OUT/'decision.json').read_text());base=read(OUT/'referencia_estrategias.csv')
    final=read(OUT/'resultados_por_empresa.csv');combos=read(OUT/'combinaciones_tres_rondas.csv')
    global_rows=[]
    for label in ['No_operar','Mantener_teorico','Mantener_SPI','Momentum32','Tendencia_lenta','SMA10','Agresiva','Candidata_anterior','ATM']:
        rs=final if label=='ATM' else [r for r in base if r['estrategia']==label]
        global_rows.append([label,n(st.mean(float(r['patrimonio']) for r in rs)),sum(float(r['ventaja'])>0 for r in rs),
            n(min(float(r['patrimonio']) for r in rs)),f(max(float(r['drawdown_pct']) for r in rs)),n(st.mean(float(r['comisiones']) for r in rs))])
    bmap={r['serie']:r for r in base if r['estrategia']=='Momentum32'}
    byseries=[[label,n(bmap[r['serie']]['patrimonio']),n(r['patrimonio']),n(r['mantener_oficial']),n(r['ventaja']),r['compras'],r['ventas'],r['comisiones'],f(r['drawdown_pct'])] for label,r in zip(LABELS,final,strict=True)]
    triple=[]
    for label in ['Momentum32','ATM','Tendencia_lenta','SMA10','Mantener_SPI','No_operar','Mantener_teorico']:
        rs=[r for r in combos if r['tipo']=='distintas' and r['estrategia']==label]
        triple.append([label,sum(int(r['ventaja'])>0 for r in rs),n(min(int(r['patrimonio_total']) for r in rs)),n(min(int(r['ventaja']) for r in rs)),n(st.mean(int(r['ventaja']) for r in rs))])
    phases=[dict(fase='Python y contabilidad independiente',estado='PASS',evidencia='validacion_modelo.json: 160000 ticks'),
        dict(fase='Mejora financiera',estado=d['estado'],evidencia='decision.json, protocolo congelado'),
        *[dict(fase=phase,estado='NO_EJECUTADA_POR_NO_GO',evidencia='Puerta cuantitativa anterior no aprobada') for phase in
          ['Assembly ATM','Equivalencia Python/RV32E ATM','RTL ATM','Banco oficial ATM 4/4','Tres cadencias ATM',
           'Yosys ATM','Place and route ATM','Netlist ATM','BIN ATM','Prueba fisica ATM']],
        dict(fase='Referencia activa',estado='PASS_PRESERVADA',evidencia='referencia/pruebas_actuales.json y SHA activos'),
        dict(fase='Competencia oficial',estado='NO_APORTADA',evidencia='Sin patrimonios de tres rondas')]
    (OUT/'estado_fases.json').write_text(json.dumps(phases,indent=2))
    with (OUT/'matriz_aceptacion.csv').open('w',encoding='utf-8',newline='') as matrix_stream:
        w=csv.writer(matrix_stream)
        w.writerow(['criterio','resultado'])
        for key,value in d['puertas'].items():w.writerow([key,'PASS' if value else 'FAIL'])
        for row in phases:w.writerow([row['fase'],row['estado']])
    # Evidencia visual estándar: tres figuras, ocho series, sin precios futuros.
    os.environ.setdefault('MPLCONFIGDIR',str(HERE/'.matplotlib'))
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import numpy as np
    with gzip.open(OUT/'decisiones_tick.csv.gz','rt',encoding='utf-8',newline='') as stream:traces=list(csv.DictReader(stream))
    for kind in ('patrimonios','drawdowns','compras_ventas'):
        fig,axes=plt.subplots(4,2,figsize=(12,11),layout='constrained')
        for ax,label,r in zip(axes.flat,LABELS,final,strict=True):
            trace=[t for t in traces if t['serie']==r['serie']];prices=[int(t['precio']) for t in trace]
            actual,_trace=active.run(prices,active.frozen(),True)
            aw=np.array([t['patrimonio'] for t in _trace]);cw=np.array([int(t['patrimonio']) for t in trace])
            x=np.arange(len(prices))
            if kind=='patrimonios':
                q=9995//prices[0];bh=10000-5-q*prices[0]+q*np.array(prices)
                ax.plot(x,cw,label='ATM');ax.plot(x,aw,label='Momentum32',alpha=.8);ax.plot(x,bh,label='Mantener',alpha=.6)
            elif kind=='drawdowns':
                for wealth,name in [(cw,'ATM'),(aw,'Momentum32')]:
                    peaks=np.maximum.accumulate(np.r_[10000,wealth])[1:]
                    ax.plot(x,100*(peaks-wealth)/peaks,label=name)
                ax.set_ylabel('Drawdown (%)')
            else:
                ax.plot(x,prices,color='#666666',lw=.7,label='Precio')
                for action,color,marker,name in [(1,'#178855','^','Compra ATM'),(2,'#b63a48','v','Venta ATM')]:
                    idx=[i for i,t in enumerate(trace) if int(t['fill']) and int(t['miso'])>>6==action]
                    ax.scatter(idx,[prices[i] for i in idx],color=color,marker=marker,s=12,label=name,zorder=3)
            ax.set_title(label);ax.grid(alpha=.2);ax.legend(fontsize=6)
        fig.savefig(OUT/f'{kind}.png',dpi=140);plt.close(fig)
    md=f'''# ATM — informe cuantitativo

**Dictamen: {d['estado']}. No reemplazar la imagen activa.**

Se investigaron {len(population())} configuraciones, incluidas las perdedoras, y se
seleccionó la número {d['seleccion']} exclusivamente en los primeros 12.000 ticks
de cada serie. El protocolo se fijó antes de ejecutar la grilla. No se usaron
series secretas ni se descargaron datos externos. Los datos son de desarrollo
conocidos; LOCO, LOSO y walk-forward son validación interna.

## Diseño y criterios

ATM combina momentum rápido/lento, estados ALCISTA/LATERAL/BAJISTA, confirmación
de revisiones y gestión de exposición. La grilla compara señales de momentum,
medias, híbrida, persistencia, ruptura y pendiente; exposiciones 25/50/75/90/100 %
y dinámica; stops fijos/de volatilidad, permanencia, reserva, compras progresivas
y liquidación total/parcial. Todas las configuraciones están en PROTOCOLO.json.
Las variantes sin volatilidad son controles descriptivos; co-varían otros
parámetros del perfil y no permiten atribuir causalidad a un solo factor.

La elegida usa fast=16, slow=64, revisión=8, entrada delta rápido >=4 con delta
lento >=0 confirmado dos revisiones; salida delta rápido <=-4 y lento <=0, o
stop desde entrada/pico. Distancia de stop=min(40,max(12,4*max(1,volatilidad))).
Volatilidad es la media redondeada hacia arriba de 16 cambios absolutos de precio.
En lateralidad conserva la exposición anterior; en alcista busca 100 %, en
bajista 0 %. Mínimo 4 acciones por compra/rebalanceo y permanencia mínima de
16 ticks, salvo stop. El filtro de costo usa movimiento histórico por cantidad
>=10; es un proxy y no una estimación demostrada de rentabilidad esperada.

El ranking y las once puertas están congelados. Se exige >=6/8 ventajas,
mejor mediana monetaria y relativa, no empeorar la peor ventaja ni DD/comisiones,
LOCO>=5/8, LOSO>=6/8, WF>=14/24 y no empeorar victorias/peor ventaja de las 56
ternas. La elección no se repite mirando el test. Ninguna de las 155 variantes
elegibles cumplió simultáneamente las seis puertas descriptivas de serie completa;
ese cribado posterior se publica pero no se usa para seleccionar otra política.

## Contabilidad y referencias

Caja 10.000, inventario cero, comisión 5 por fill positivo, máximo 63, sin deuda
ni corto. Se ejecuta la orden anterior antes de decidir. La última decisión no
se liquida ficticiamente. Mantener teórico compra idealmente al inicio; mantener
SPI debe emitir y completar sus órdenes mediante el mismo protocolo. No son
referencias idénticas. La contabilidad ATM se cotejó con una implementación
anterior independiente en 160.000 ticks: cero discrepancias.

| Política | Patrimonio medio | Ventajas/8 | Peor final | DD máximo % | Comisión media |
|---|---:|---:|---:|---:|---:|
{table(global_rows)}

## Ocho series y operaciones ATM

| Serie | Momentum32 | ATM | Mantener | Ventaja ATM | Compras | Ventas | Comisión | DD % |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
{table(byseries)}

Los CSV incluyen caja, inventario, tiempo invertido y exposición por tick.
Hay 160.000 filas en decisiones_tick.csv.gz y todas las operaciones en operaciones.csv.

## Folds y tres rondas

| Procedimiento | Momentum32 histórico | ATM |
|---|---:|---:|
| LOCO | 5/8 | {d['loco']}/8 |
| LOSO | 6/8 | {d['loso']}/8 |
| Walk-forward | 14/24 | {d['walk']}/24 |

Las selecciones históricas LOCO/LOSO se comprobaron con su matriz completa;
las tres selecciones WF se recalcularon usando solo prefijos. Los resultados
históricos se reejecutaron, no se sustituyeron por los del entrenamiento.
En ATM, cada fold vuelve a elegir en su entrenamiento; LOCO excluye todas las
series de una empresa. WF reinicia cartera e indicadores en cada ventana test,
como en la referencia: no representa una única cartera continua por veinte mil ticks.

| Política | Ternas positivas/56 | Peor suma de patrimonios | Peor ventaja monetaria | Ventaja media |
|---|---:|---:|---:|---:|
{table(triple)}

Se publican además 120 ternas con repetición por política. Las permutaciones de
una terna no cambian la suma y no se cuentan como evidencia adicional. El objetivo
de suma de tres patrimonios sigue la instrucción de investigación del usuario;
estas combinaciones no son resultados oficiales de competencia ni determinan su nota.

## Por qué es NO-GO

ATM logra {d['atm']['ventajas']}/8 frente a 6/8; su mediana relativa es
{f(d['atm']['mediana_pct'])} % frente a {f(d['baseline']['mediana_pct'])} %.
Su peor ventaja es {f(d['atm']['peor_pct'])} % frente a
{f(d['baseline']['peor_pct'])} %. Reduce DD máximo a
{f(d['atm']['drawdown_max_pct'])} %, pero aumenta la comisión media a
{f(d['atm']['comisiones_media'])}. La mayor protección no compensa los fallos
de rentabilidad y consistencia exigidos. Los perdedores y el mejor caso están
identificados en resultados_por_empresa.csv. Los nueve estreses sintéticos se
publican por separado; no se atribuyen fechas o empresas a esas secuencias.

## Assembly, RTL, timing y BIN

**No ejecutados para ATM por NO-GO cuantitativo.** No se generaron trade.s,
trade.hex ni BIN de ATM; no se reutilizó el HEX anterior como si fuera nuevo.
No hay ciclos, CPI, LUT4, BRAM, Fmax ni 4/4 del profesor atribuibles a ATM.
Las pruebas originales de referencia Icarus se repitieron y permanecen en
resultados/referencia/; no son pruebas RTL de ATM. Los testbenches oficiales y
sus cuatro criterios permanecen intactos.

La versión activa conserva 1260/1280 LC, 9/16 BRAM, Fmax de 50,19 MHz y reloj
de procesamiento de 12,5 MHz. Su máximo observado de decisión es 321 ciclos,
25,68 us. Estas cifras son de la referencia, no mediciones de la candidata.
BIN activo SHA-256: 5e1579caef1f8de2813b6cf50bb17c505e77b3a534787447d27660eaad63a606.
No hay hash de BIN ATM porque no existe una imagen aprobada.

## Reproducción y programación

Desde la raíz del repositorio:

```powershell
python -X utf8 -B proyecto4/alternativas/atm_adaptativa/ejecutar_todo.py
```

El ejecutor reproduce la investigación, los controles y el informe. Conserva
el fallo financiero como NO-GO. Para programar manualmente la última versión
físicamente confirmada, seguir usando el programar.ps1 de la raíz; no programa ATM.
No se ejecutó iceprog en esta investigación. No se hereda a ATM la confirmación
de compras/ventas de la imagen activa. No se aportaron patrimonios oficiales
de tres rondas ni una nueva prueba física ATM.

## Conclusión

La familia y la grilla exploradas no justifican sustituir Momentum32. La mejora
aislada del drawdown y del fold LOCO no cumple el conjunto de puertas fijadas.
Este NO-GO no demuestra que toda estrategia adaptativa sea inferior; limita la
conclusión a estas configuraciones, reglas de selección y datos conocidos.
Se preservan los resultados fallidos para revisión y se mantiene el BIN funcional.
'''
    (HERE/'INFORME_CUANTITATIVO.md').write_text(md,encoding='utf-8')
    texrows=lambda rs:'\n'.join(' & '.join(str(x).replace('_',r'\_').replace('%',r'\%') for x in r)+r' \\' for r in rs)
    tex=r'''\documentclass[11pt,a4paper]{article}
\usepackage[T1]{fontenc}\usepackage[utf8]{inputenc}\usepackage[spanish,es-nodecimaldot]{babel}
\usepackage{lmodern,geometry,booktabs,graphicx,hyperref}
\geometry{margin=2cm}\setlength{\parindent}{0pt}\setlength{\parskip}{6pt}\setlength{\emergencystretch}{3em}
\begin{document}
\begin{center}{\LARGE ATM: investigación y decisión NO-GO}\par
Cristian Acevedo, Guillermo Arriaza y Eduardo Ponce\par 25 de noviembre de 2026\end{center}
\textbf{No sustituir el BIN activo.} Se evaluaron 191 configuraciones; la selección
usó solo ocho prefijos de 12000 ticks. No se reajustó tras ver el test.
El modelo tiene tres regímenes, momentum corto/largo, confirmación, exposición,
reserva y stops de volatilidad. La elegida usa 16/64 ticks, revisión 8, dos
confirmaciones, entrada +4, salida -4 y stop entre 12 y 40 puntos. La grilla
también incluye medias, persistencia, ruptura, pendiente y exposiciones de 25 a 100\%.

\begin{center}\small\begin{tabular}{lrrrrr}\toprule
Política & Media & Ventajas/8 & Peor final & DD máx.\% & Comisión media\\\midrule
@GLOBAL@
\bottomrule\end{tabular}\end{center}
\begin{center}\resizebox{\linewidth}{!}{\begin{tabular}{lrrrrrrrr}\toprule
Serie & Momentum32 & ATM & Mantener & Ventaja ATM & Compras & Ventas & Comisión & DD\%\\\midrule
@SERIES@
\bottomrule\end{tabular}}\end{center}

ATM gana en 5/8, frente a 6/8. La mediana relativa baja de 24,90\% a 16,50\%;
la peor ventaja pasa de -6,14\% a -15,85\%. El drawdown mejora de 61,11\% a
49,38\%, pero la comisión media sube de 270,63 a 411,88. Ninguna variante
elegible cumplió simultáneamente las seis puertas descriptivas de serie completa.
Esto no autoriza seleccionar retrospectivamente otra configuración por el test.

\textbf{Validación temporal.} LOCO: 6/8 frente a 5/8 histórico; LOSO: 5/8 frente
a 6/8; walk-forward: 14/24 frente a 14/24. Cada selección usa su entrenamiento,
sin su empresa/serie excluida o ventana futura. Son datos conocidos de desarrollo,
no una validación independiente en series secretas. WF reinicia la cartera y
los indicadores en cada ventana. Se reprodujeron las selecciones de referencia.

\begin{center}\small\begin{tabular}{lrrrr}\toprule
Política & Ternas +/56 & Peor suma & Peor ventaja & Ventaja media\\\midrule
@TRIPLES@
\bottomrule\end{tabular}\end{center}
Se evaluaron las 56 ternas distintas y, adicionalmente, 120 con repetición por
política. Se suman patrimonios de rondas independientes de 10000 iniciales.
No son resultados de la competencia oficial ni determinan una calificación.

\textbf{Contabilidad.} La orden se ejecuta al precio siguiente, máximo 63,
comisión 5 por fill positivo y sin deuda ni corto. Se cotejaron 160000 ticks de
decisiones y cartera con una implementación independiente; cero discrepancias.
El CSV completo está comprimido sin pérdida. Se conservaron las configuraciones
perdedoras, compras, ventas, exposición y nueve estreses sintéticos.

\textbf{Hardware: fase no habilitada.} Por NO-GO no se tradujo ATM a RV32E,
no se ejecutó RTL ATM ni el banco oficial con ATM, y no se sintetizó ni generó
un BIN nuevo. No se atribuyen a ATM ciclos, CPI o recursos de otra política.
La referencia activa sigue en 1260 LC, 9 BRAM, Fmax 50,19 MHz y 321 ciclos
máximos observados a 12,5 MHz (25,68 us). Sus pruebas Icarus se repitieron sin
modificar los archivos protegidos. No se programó físicamente la FPGA.

\textbf{Reproducción:}\par
\path{python -X utf8 -B proyecto4/alternativas/atm_adaptativa/ejecutar_todo.py}\par
Las reglas, el ranking y las puertas están en PROTOCOLO.json. El informe completo
en Markdown detalla las limitaciones; los CSV y firmas permiten revisar cada
resultado. La decisión corresponde a esta grilla, no a una imposibilidad general
de superar al baseline.

\clearpage\section*{Patrimonios: ATM, Momentum32 y mantener}
\includegraphics[width=\linewidth,height=.87\textheight,keepaspectratio]{resultados/patrimonios.png}
\clearpage\section*{Drawdown: comparación por serie}
\includegraphics[width=\linewidth,height=.87\textheight,keepaspectratio]{resultados/drawdowns.png}
\clearpage\section*{Compras y ventas ATM al precio de ejecución}
\includegraphics[width=\linewidth,height=.87\textheight,keepaspectratio]{resultados/compras_ventas.png}
\end{document}
'''.replace('@GLOBAL@',texrows(global_rows)).replace('@SERIES@',texrows(byseries)).replace('@TRIPLES@',texrows(triple))
    (HERE/'INFORME_CUANTITATIVO.tex').write_text(tex,encoding='utf-8')
    print('PASS informe, matriz y tres graficos; estado',d['estado'])

if __name__=='__main__':main()
