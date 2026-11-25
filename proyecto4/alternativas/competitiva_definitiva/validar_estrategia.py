"""Investigación reproducible: grilla declarada, folds separados y datos auditados.

Todos los CSV son datos de desarrollo ya conocidos; los folds son validación
interna y NO una nueva evaluación independiente sobre series secretas.
"""
from estrategia import *
from dataclasses import replace
import statistics as st
import hashlib
import sys
import time
import itertools
import importlib.util

ROOT=HERE.parents[2]
OUT=HERE/'resultados'

def population():
    # Grilla pequeña y publicada antes de medir. Sin reglas por empresa.
    cfg=[Config()]
    for fast,ext,entry in itertools.product((16,32,64),(12,16,20),(4,6,8)):
        cfg.append(Config(fast=fast,exit=ext,entry=entry))
    for slow,g in itertools.product((64,128,256),(6,12,20)):
        cfg.append(Config(family='dual',slow=slow,gradual=g))
    for f in ('breakout','trailing','adaptive','hybrid'):
        for s in (12,20,32):
            cfg.append(Config(family=f,stop=s,gradual=12))
    for f,g in (('persistence',6),('persistence',12),('lowerhigh',4),('lowerhigh',8),('negative',70),('negative',90)):
        cfg.append(Config(family=f,gradual=g))
    for exp,neutral in ((0,0),(25,0),(50,0),(75,0),(100,25),(100,50),(100,75)):
        cfg.append(Config(family='dual',gradual=12,exposure=exp,neutral=neutral))
    return list(dict.fromkeys(cfg))

def rank(ms):
    # Aucun seuil dépendant d'une entreprise. Adversité et dispersion sont pénalisées.
    advantages=[r['ventaja_pct'] for r in ms]
    return (sum(x>0 for x in advantages)/len(ms),st.median(advantages)+0.25*st.mean(advantages)
            +0.5*min(advantages)-0.05*max(r['drawdown_pct'] for r in ms),
            min(r['patrimonio'] for r in ms),-st.mean(r['comisiones'] for r in ms))

ELIGIBLE=None

def select(table,idx):
    return max(ELIGIBLE if ELIGIBLE is not None else range(len(table)),
               key=lambda c:rank([table[c][i] for i in idx]))

def synth():
    return {
      'subida':[100+t*155//1023 for t in range(1024)],
      'caida_gradual':[255-t*155//2047 for t in range(2048)],
      'caida_brusca':[220]*200+[100]*200,
      'lateral':[170+(t%9==0)-(t%11==0) for t in range(1024)],
      'recuperacion':[220]*128+[100]*128+[100+t*120//511 for t in range(512)],
      'limites_inventario':[100]*128+[255]*64+[100]*128+[255]*128,
      'alternancia':[100,255]*256,
      'integracion_cadencias':[100]*8+[220]*24+[100]*16,
    }

def baselines(data):
    # Use original policy sources but route every fill through the same official model.
    sys.path.insert(0,str(ROOT/'proyecto4/python'))
    # Local estrategia.py intentionally has a different API; load originals under
    # their own module names only while importing legacy policies.
    current=sys.modules['estrategia']
    def module(name,path):
        spec=importlib.util.spec_from_file_location(name,path); m=importlib.util.module_from_spec(spec)
        sys.modules[name]=m;spec.loader.exec_module(m);return m
    original=module('estrategia',ROOT/'proyecto4/python/estrategia.py')
    sma=module('enfoques_finales',ROOT/'proyecto4/python/enfoques_finales.py')
    cand=module('estrategia_referencia',HERE.parent/'candidata_final/estrategia_referencia.py')
    agg=module('estrategia_agresiva',HERE.parent/'agresiva/estrategia_agresiva.py')
    sys.modules['estrategia']=current
    rows=[]
    for name,p in data.items():
        for label,policy in [('Conservar',lambda h,s,t:original.MANTENER),
             ('SMA10',sma.estrategia_reversion_media),('candidata_final',cand.crear_politica()),
             ('agresiva',agg.crear_politica(agg.Parametros('momentum',100,False,16,8)))]:
            cash=peak=wealth=10000; shares=order=orders=fees=dd=0;h=[]
            for t,price in enumerate(p):
                cash,shares,n,fee=fill(cash,shares,order,price);orders+=n>0;fees+=fee
                wealth=cash+shares*price;peak=max(peak,wealth);dd=max(dd,peak-wealth)
                h.append(price); d=policy(h,shares,t);order=int(d.accion)<<6 | d.cantidad
            rows.append(dict(serie=name,estrategia=label,patrimonio=wealth,mantener=benchmark(p),
                 ventaja=wealth-benchmark(p),ordenes=orders,comisiones=fees,drawdown=dd))
        m,_=run(p)
        rows.append(dict(serie=name,estrategia='Momentum32',patrimonio=m['patrimonio'],mantener=benchmark(p),
            ventaja=m['ventaja'],ordenes=m['ordenes'],comisiones=m['comisiones'],drawdown=m['drawdown']))
        # SPI feasible buy and hold: first decision after tick 0, up to 63/tick.
        m,_=run(p,Config(fast=1000000))
        rows.append(dict(serie=name,estrategia='Mantener_SPI',patrimonio=m['patrimonio'],mantener=benchmark(p),
            ventaja=m['ventaja'],ordenes=m['ordenes'],comisiones=m['comisiones'],drawdown=m['drawdown']))
    write_csv(OUT/'comparacion_existentes.csv',rows)

def describe(data):
    rows=[]; horizons=[]
    for name,p in data.items():
        dif=[b-a for a,b in zip(p,p[1:])]
        peak=p[0]; dd=0; last_peak=0; durations=[]; draw_durations=[];signs=[]
        for i,x in enumerate(p):
            if x>=peak:
                if i>last_peak: draw_durations.append(i-last_peak)
                peak=x;last_peak=i
            dd=max(dd,peak-x)
        if last_peak<len(p)-1:draw_durations.append(len(p)-1-last_peak)
        for horizon in (4,8,16,32,64,128,256):
            ds=[p[i]-p[i-horizon] for i in range(horizon,len(p))]
            # Nonoverlapping horizon blocks classify trend with a fixed +/-2 point deadband.
            labels=[1 if p[i]-p[i-horizon]>=2 else -1 if p[i]-p[i-horizon]<=-2 else 0
                    for i in range(horizon,len(p),horizon)]
            runs=[(k,len(list(g))*horizon) for k,g in itertools.groupby(labels)]
            declines=[v for k,v in runs if k<0]; up=[v for k,v in runs if k>0]; side=[v for k,v in runs if k==0]
            horizons.append(dict(serie=name,horizonte=horizon,delta_media=st.mean(ds),delta_mediana=st.median(ds),
              volatilidad=st.pstdev(ds),positivos=sum(x>0 for x in ds),negativos=sum(x<0 for x in ds),
              cambios_regimen=max(0,len(runs)-1),duracion_alcista_media=st.mean(up) if up else 0,
              duracion_bajista_media=st.mean(declines) if declines else 0,
              duracion_lateral_media=st.mean(side) if side else 0,retroceso_max=max(0,-min(ds))))
        rows.append(dict(serie=name,ticks=len(p),inicial=p[0],final=p[-1],minimo=min(p),maximo=max(p),
          mantener=benchmark(p),retorno_activo_pct=100*(p[-1]/p[0]-1),variacion_media=st.mean(dif),
          variacion_mediana=st.median(dif),repetidos_pct=100*dif.count(0)/len(dif),volatilidad=st.pstdev(dif),
          cambios_significativos_2=sum(abs(d)>=2 for d in dif),drawdown_precio=dd,
          duracion_drawdown_max=max(draw_durations,default=0),sha256=hashlib.sha256(bytes(p)).hexdigest()))
    write_csv(OUT/'estadisticas_series.csv',rows);write_csv(OUT/'estadisticas_horizontes.csv',horizons)

def main():
    global ELIGIBLE
    start=time.perf_counter();OUT.mkdir(exist_ok=True)
    data={p.stem:load(p) for p in sorted((HERE/'datos').glob('*.csv'))}
    assert len(data)==8 and all(len(p)==20000 for p in data.values())
    describe(data); baselines(data)
    configs=population();names=list(data);prices=list(data.values())
    # Revision de desarrollo V2, tras observar fallo de V1 en caida gradual.
    # El filtro se aplica identico en TODOS los folds, sin observar su empresa test.
    # Exige reducir al menos a la mitad el DD de mantener en el descenso sintético.
    adversarial=synth()['caida_gradual']
    risk=[]
    for i,c in enumerate(configs):
        m,_=run(adversarial,c)
        risk.append(dict(config=i,admisible=int(m['drawdown']<=3025),**m))
    ELIGIBLE=[r['config'] for r in risk if r['admisible']]
    write_csv(OUT/'filtro_adverso_desarrollo.csv',risk)
    (OUT/'grilla_declarada.json').write_text(json.dumps([asdict(c) for c in configs],indent=2))
    table=[[run(p,c)[0] for p in prices] for c in configs]
    write_csv(OUT/'grilla_completa_desarrollo.csv',[
       dict(config=i,serie=names[j],**asdict(c),**m) for i,c in enumerate(configs) for j,m in enumerate(table[i])])
    folds=[]
    for method in ('leave_one_company_out','leave_one_series_out'):
        groups=sorted(set(n.split('_')[1] for n in names)) if method.endswith('company_out') else names
        for group in groups:
            test=[j for j,n in enumerate(names) if (n.split('_')[1] if method.endswith('company_out') else n)==group]
            train=[j for j in range(8) if j not in test]; winner=select(table,train)
            for j in test:
                folds.append(dict(metodo=method,excluido=group,serie=names[j],config=winner,
                    entrenamiento=','.join(names[k] for k in train),**table[winner][j]))
    write_csv(OUT/'validacion_por_grupos.csv',folds)
    # Freeze policy on first 12000 ticks of ALL series, before measuring later windows.
    train=[[run(p[:12000],c)[0] for p in prices] for c in configs]
    winner=select(train,list(range(8)));cfg=configs[winner]
    selection=dict(config=asdict(cfg),indice=winner,criterio='rank: fraccion ventajas, mediana+0.25media+0.5peor-0.05DD, minimo patrimonio, comisiones',
       revision='V2: filtro DD<=3025 en caida gradual sintetica; V1 descartada. Umbral de desarrollo, no evaluacion independiente.',
       origen='primeros 12000 ticks de ocho series conocidas; validacion interna, no OOS independiente',
       grilla_sha256=hashlib.sha256((OUT/'grilla_declarada.json').read_bytes()).hexdigest())
    (OUT/'seleccion.json').write_text(json.dumps(selection,indent=2))
    print('CONGELADA',cfg,flush=True)
    walk=[]
    for end in (8000,12000,16000):
        train=[[run(p[:end],c)[0] for p in prices] for c in configs]
        win=select(train,list(range(8)))
        for j,p in enumerate(prices):
            m,_=run(p[end:end+4000],configs[win])
            walk.append(dict(serie=names[j],fin_ajuste=end,fin_prueba=end+4000,config=win,**m))
    write_csv(OUT/'walk_forward.csv',walk)
    final=[]; segments=[]
    for name,p in data.items():
        m,rows=run(p,cfg,True);final.append(dict(serie=name,**m))
        write_csv(OUT/f'{name}_ticks.csv',rows)
        for a,b in ((0,12000),(12000,16000),(16000,20000)):
            # Restart portfolio and indicators explicitly: independent window test.
            met,_=run(p[a:b],cfg)
            segments.append(dict(serie=name,inicio=a,fin=b,rol='ajuste' if a==0 else 'validacion_conocida',
              mercado='alcista' if p[b-1]-p[a]>2 else 'bajista' if p[b-1]-p[a]<-2 else 'lateral',**met))
    write_csv(OUT/'comparacion_final.csv',final);write_csv(OUT/'tramos.csv',segments)
    synthetic=[]
    for name,p in synth().items():
        m,rows=run(p,cfg,True);synthetic.append(dict(escenario=name,**m))
        write_csv(OUT/f'sintetico_{name}_ticks.csv',rows)
    write_csv(OUT/'sinteticos.csv',synthetic)
    sensitivity=[]
    for f in ('entry','exit','stop'):
        for offset in (-2,0,2):
            c=replace(cfg,**{f:max(1,getattr(cfg,f)+offset)})
            for name,p in data.items():
                m,_=run(p,c);sensitivity.append(dict(campo=f,offset=offset,serie=name,**m))
    write_csv(OUT/'sensibilidad.csv',sensitivity)
    (OUT/'tiempo_python.json').write_text(json.dumps(dict(segundos=time.perf_counter()-start)))
    # Standalone scientific plot; optional dependency errors must be visible.
    try:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        fig,axes=plt.subplots(4,2,figsize=(13,12))
        for ax,(name,p) in zip(axes.flat,data.items()):
            _,r=run(p,cfg,True);q=9995//p[0]
            ax.plot([x['patrimonio'] for x in r],label='Candidata congelada')
            ax.plot([9995-q*p[0]+q*x for x in p],label='Mantener oficial',alpha=.8)
            ax.set_title(name);ax.grid(alpha=.2);ax.legend(fontsize=7)
        fig.tight_layout();fig.savefig(OUT/'patrimonios.png',dpi=150);plt.close(fig)
    except ImportError as e:
        (OUT/'graficos_pendientes.txt').write_text(str(e))
    print(json.dumps(final,indent=2),flush=True)

if __name__=='__main__':main()
