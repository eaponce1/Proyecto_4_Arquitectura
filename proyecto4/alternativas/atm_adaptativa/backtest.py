"""Un comando: auditoría cuantitativa, selección sin test, folds y puertas GO/NO-GO."""
from pathlib import Path
from dataclasses import asdict
from concurrent.futures import ProcessPoolExecutor,as_completed
import argparse,csv,gzip,hashlib,itertools,json,statistics as st,time
from estrategia_atm import Config,Policy,population
from simulador_atm import run,rank,write
from baselines import policies,active,ROOT,OLD

HERE=Path(__file__).resolve().parent
OUT=HERE/'resultados'
ENDS=(8000,12000,16000,20000)

def read(path):
    with path.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))

def task(name,prices,end,configs):
    return name,end,[run(prices[:end],Policy(c))[0] for c in configs]

def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def selection(table,names,eligible):
    return max(eligible,key=lambda i:(rank([table[name][i] for name in names]),-i))

def summarized(rows):
    return dict(ventajas=sum(r['ventaja']>0 for r in rows),n=len(rows),
        mediana_dolares=st.median(r['ventaja'] for r in rows),mediana_pct=st.median(r['ventaja_pct'] for r in rows),
        media_dolares=st.mean(r['ventaja'] for r in rows),media_pct=st.mean(r['ventaja_pct'] for r in rows),
        peor_pct=min(r['ventaja_pct'] for r in rows),minimo=min(r['patrimonio'] for r in rows),
        drawdown_max_pct=max(r['drawdown_pct'] for r in rows),comisiones_media=st.mean(r['comisiones'] for r in rows))

def baseline_audit(data):
    makers=policies();records=[]
    for name,p in data.items():
        for label,maker in makers.items():records.append(dict(serie=name,estrategia=label,**run(p,maker())[0]))
        b=active.benchmark(p)
        q=9995//p[0];cash=9995-q*p[0];peak=10000;dd=0;ddpct=0.
        for price in p:
            wealth=cash+q*price;peak=max(peak,wealth)
            dd=max(dd,peak-wealth);ddpct=max(ddpct,100*(peak-wealth)/peak)
        records.append(dict(serie=name,estrategia='Mantener_teorico',patrimonio=b,caja=10000-5-(9995//p[0])*p[0],
            acciones=q,ordenes=1,compras=1,ventas=0,comisiones=5,drawdown=dd,drawdown_pct=ddpct,
            mantener_oficial=b,ventaja=0,ventaja_pct=0,ticks_invertido=len(p),ticks=len(p)))
    write(OUT/'referencia_estrategias.csv',records)
    saved={r['serie']:r for r in read(OLD/'resultados/comparacion_final.csv')}
    base=[r for r in records if r['estrategia']=='Momentum32']
    for r in base:
        for k in ('patrimonio','ordenes','comisiones','drawdown'):assert r[k]==int(saved[r['serie']][k]),(r['serie'],k)
    # Los estados por tick se reejecutan; no se toma un resultado de entrenamiento como test.
    oldfold=read(OLD/'resultados/validacion_por_grupos.csv')
    configs=json.loads((OLD/'resultados/grilla_declarada.json').read_text())
    foldreport=[]
    for r in oldfold:
        cfg=active.Config(**configs[int(r['config'])]);m,_=run(data[r['serie']],active.Policy(cfg))
        assert m['patrimonio']==int(r['patrimonio'])
        foldreport.append(dict(metodo=r['metodo'],serie=r['serie'],**m))
    walks=[]
    for r in read(OLD/'resultados/walk_forward.csv'):
        cfg=active.Config(**configs[int(r['config'])]);a,b=int(r['fin_ajuste']),int(r['fin_prueba'])
        m,_=run(data[r['serie']][a:b],active.Policy(cfg));assert m['patrimonio']==int(r['patrimonio'])
        walks.append(dict(serie=r['serie'],fin_ajuste=a,**m))
    write(OUT/'referencia_folds_reproducidos.csv',foldreport);write(OUT/'referencia_walk_reproducido.csv',walks)
    assert sum(r['ventaja']>0 for r in walks)==14
    assert sum(r['ventaja']>0 for r in foldreport if r['metodo']=='leave_one_company_out')==5
    assert sum(r['ventaja']>0 for r in foldreport if r['metodo']=='leave_one_series_out')==6
    assert summarized(base)['ventajas']==6 and min(r['patrimonio'] for r in base)==8615
    return records,base

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--workers',type=int,default=3)
    args=parser.parse_args();start=time.perf_counter();OUT.mkdir(exist_ok=True)
    data={p.stem:active.load(p) for p in sorted((OLD/'datos').glob('*.csv'))};names=list(data)
    configs=population()
    protocol=dict(version=1,base_commit='07d0dd95d491f7b7f08a6f1b813d998e53a8c123',
        selection='Solo prefijos [0:12000]; rank congelado en simulador.py; desempate indice menor',
        score='100*fraccion_ventajas + mediana_pct + .25*media_pct + peor_pct - .2*maxDD - comision_media/1000 - 10*fraccion_perdidas_relativas_menores_-10pct',
        eligible='vol_mult>0; otras configuraciones solo ablation',
        folds='LOCO excluye empresa completa; LOSO serie completa; WF ajuste 8000/12000/16000, test siguiente 4000; reinicio de cartera e indicadores',
        acceptance=dict(ventajas_min=6,mediana_dolares='> baseline',mediana_pct='> baseline',peor_pct='>= baseline',
            loco_min=5,loso_min=6,walk_min=14,drawdown_max='<= baseline',comision_media='<= baseline',
            triples_ventajas='>= baseline',triples_peor_ventaja='>= baseline'),
        no_reselection='Si el elegido falla test, NO-GO; no se escoge retrospectivamente otro',
        combinaciones='56 ternas distintas y 120 multiconjuntos con repeticion; las permutaciones no cambian la suma',
        externos='No se descargan datos ni se usan CSV adicionales para seleccionar',
        grilla=[asdict(c) for c in configs],datos={n:digest(OLD/'datos'/f'{n}.csv') for n in names})
    plan=HERE/'PROTOCOLO.json'
    if plan.exists():assert json.loads(plan.read_text())==protocol,'El protocolo cambio; no sobreescribir un experimento congelado'
    else:plan.write_text(json.dumps(protocol,indent=2),encoding='utf-8')
    print('PROTOCOLO CONGELADO',digest(plan),len(configs),'configuraciones',flush=True)
    baseline,base=baseline_audit(data)
    print('PASS referencias 8 series, LOCO 5/8, LOSO 6/8, WF 14/24',flush=True)
    eligible=[i for i,c in enumerate(configs) if c.vol_mult>0]
    tables={e:{} for e in ENDS}
    cache=HERE/'build/cache';cache.mkdir(parents=True,exist_ok=True)
    tasks=[]
    with ProcessPoolExecutor(max_workers=args.workers) as pool:
        for end in ENDS:
            for name,p in data.items():
                path=cache/f'{name}_{end}.json'
                stamp=hashlib.sha256((digest(plan)+digest(HERE/'estrategia_atm.py')+digest(HERE/'simulador.py')).encode()).hexdigest()
                if path.exists():
                    saved=json.loads(path.read_text())
                    if saved.get('stamp')==stamp:tables[end][name]=saved['metrics'];continue
                tasks.append((pool.submit(task,name,p,end,configs),path,stamp))
        future_map={f:(path,stamp) for f,path,stamp in tasks}
        for future in as_completed(future_map):
            name,end,metrics=future.result();path,stamp=future_map[future]
            path.write_text(json.dumps(dict(stamp=stamp,metrics=metrics)))
            tables[end][name]=metrics;print('MEDIDO',name,end,flush=True)
    # Escritura explicita del ajuste y congelacion ANTES de consumir las tablas de test.
    winner=selection(tables[12000],names,eligible);chosen=configs[winner]
    (HERE/'parametros_congelados.json').write_text(json.dumps(dict(indice=winner,config=asdict(chosen),
        sha256_protocolo=digest(plan),seleccion='prefijos 12000, sin evaluacion posterior'),indent=2))
    grid=[]
    for end in ENDS:
        for name in names:
            grid.extend(dict(config=i,serie=name,fin=end,rol='ajuste' if end<20000 else 'evaluacion_descriptiva',
                elegible=int(i in eligible),**m) for i,m in enumerate(tables[end][name]))
    write(OUT/'grilla_completa.csv',grid)
    final=[];operations=[];ticks=[]
    for name,p in data.items():
        m,trace=run(p,Policy(chosen),True);final.append(dict(serie=name,estrategia='ATM',**m))
        assert m==tables[20000][name][winner]
        ticks.extend(dict(serie=name,**r) for r in trace)
        operations.extend(dict(serie=name,**r) for r in trace if r['fill'])
    write(OUT/'decisiones_tick.csv',ticks);write(OUT/'operaciones.csv',operations,fields=list(ticks[0]))
    (OUT/'decisiones_tick.csv.gz').write_bytes(gzip.compress((OUT/'decisiones_tick.csv').read_bytes(),mtime=0))
    write(OUT/'resultados_por_empresa.csv',final);write(OUT/'comparacion_estrategias.csv',baseline+final)
    folds=[]
    for method in ('LOCO','LOSO'):
        groups=sorted({n.split('_')[1] for n in names}) if method=='LOCO' else names
        for group in groups:
            test=[n for n in names if (n.split('_')[1] if method=='LOCO' else n)==group]
            train=[n for n in names if n not in test];win=selection(tables[20000],train,eligible)
            for name in test:folds.append(dict(metodo=method,excluido=group,serie=name,config=win,
                entrenamiento=','.join(train),**tables[20000][name][win]))
    write(OUT/'resultados_leave_one_out.csv',folds)
    walk=[]
    for end in (8000,12000,16000):
        win=selection(tables[end],names,eligible)
        for name,p in data.items():
            m,_=run(p[end:end+4000],Policy(configs[win]))
            walk.append(dict(serie=name,fin_ajuste=end,fin_prueba=end+4000,config=win,**m))
    write(OUT/'resultados_walk_forward.csv',walk)
    combinations=[]
    for mode,triples in [('distintas',itertools.combinations(names,3)),('con_repeticion',itertools.combinations_with_replacement(names,3))]:
        for triple in triples:
            for label,rs in [('Momentum32',base),('ATM',final),('Tendencia_lenta',[r for r in baseline if r['estrategia']=='Tendencia_lenta']),
                            ('SMA10',[r for r in baseline if r['estrategia']=='SMA10']),('No_operar',[r for r in baseline if r['estrategia']=='No_operar']),
                            ('Mantener_SPI',[r for r in baseline if r['estrategia']=='Mantener_SPI']),('Mantener_teorico',[r for r in baseline if r['estrategia']=='Mantener_teorico'])]:
                ms={r['serie']:r for r in rs};wealth=sum(ms[n]['patrimonio'] for n in triple);bh=sum(ms[n]['mantener_oficial'] for n in triple)
                combinations.append(dict(tipo=mode,series='+'.join(triple),estrategia=label,patrimonio_total=wealth,mantener_total=bh,ventaja=wealth-bh))
    write(OUT/'combinaciones_tres_rondas.csv',combinations)
    def combo(label):return [r for r in combinations if r['tipo']=='distintas' and r['estrategia']==label]
    bm,am=summarized(base),summarized(final)
    gates=dict(ventajas=am['ventajas']>=6,mediana_dolares=am['mediana_dolares']>bm['mediana_dolares'],
        mediana_pct=am['mediana_pct']>bm['mediana_pct'],peor_relativo=am['peor_pct']>=bm['peor_pct'],
        drawdown=am['drawdown_max_pct']<=bm['drawdown_max_pct'],comisiones=am['comisiones_media']<=bm['comisiones_media'],
        loco=sum(r['ventaja']>0 for r in folds if r['metodo']=='LOCO')>=5,
        loso=sum(r['ventaja']>0 for r in folds if r['metodo']=='LOSO')>=6,
        walk=sum(r['ventaja']>0 for r in walk)>=14,
        ternas_ventajas=sum(r['ventaja']>0 for r in combo('ATM'))>=sum(r['ventaja']>0 for r in combo('Momentum32')),
        ternas_peor=min(r['ventaja'] for r in combo('ATM'))>=min(r['ventaja'] for r in combo('Momentum32')))
    decision=dict(estado='GO_CUANTITATIVO' if all(gates.values()) else 'NO-GO',seleccion=winner,config=asdict(chosen),
        puertas=gates,baseline=bm,atm=am,loco=sum(r['ventaja']>0 for r in folds if r['metodo']=='LOCO'),
        loso=sum(r['ventaja']>0 for r in folds if r['metodo']=='LOSO'),walk=sum(r['ventaja']>0 for r in walk),
        segundos=time.perf_counter()-start,protocolo_sha256=digest(plan),
        siguientes_fases='No aprobadas; solo se habilitan con GO cuantitativo')
    descriptive=[]
    for i in eligible:
        m=summarized([tables[20000][name][i] for name in names])
        if (m['ventajas']>=6 and m['mediana_dolares']>bm['mediana_dolares'] and m['mediana_pct']>bm['mediana_pct']
            and m['peor_pct']>=bm['peor_pct'] and m['drawdown_max_pct']<=bm['drawdown_max_pct']
            and m['comisiones_media']<=bm['comisiones_media']):descriptive.append(i)
    (OUT/'cribado_descriptivo.json').write_text(json.dumps(dict(configuraciones_que_pasan=descriptive,
        solo_descriptivo=True,no_utilizado_para_reseleccionar=True),indent=2))
    (OUT/'decision.json').write_text(json.dumps(decision,indent=2))
    write(OUT/'matriz_aceptacion.csv',[dict(criterio=k,resultado='PASS' if v else 'FAIL') for k,v in gates.items()])
    print(json.dumps(decision,indent=2),flush=True)

if __name__=='__main__':main()
