"""Reejecución independiente de la cartera y decisiones ATM: no simula Assembly/RTL."""
from pathlib import Path
import csv,gzip,json
from estrategia_atm import Config,Policy
from simulador_atm import execute,run,write
from baselines import active
HERE=Path(__file__).resolve().parent
OUT=HERE/'resultados'

def main():
    chosen=json.loads((HERE/'parametros_congelados.json').read_text())
    cfg=Config(**chosen['config']);last=None;bad=[];count=0;policy=None;cash=10000;shares=pending=0;fees=0
    with gzip.open(OUT/'decisiones_tick.csv.gz','rt',encoding='utf-8',newline='') as f:
        for r in csv.DictReader(f):
            if r['serie']!=last:
                last=r['serie'];policy=Policy(cfg);cash=10000;shares=pending=fees=0
            p=int(r['precio'])
            # Implementación conservada anterior, independiente del broker del estudio.
            cash,shares,n,fee=active.fill(cash,shares,pending,p);fees+=fee
            decision=policy.decide(p,cash,shares)
            real=(pending,decision,cash,shares,cash+shares*p,fees)
            expected=tuple(int(r[k]) for k in ('miso','decision','caja','acciones','patrimonio','comisiones_acum'))
            if real!=expected:bad.append(dict(serie=last,tick=r['tick'],real=str(real),esperado=str(expected)))
            pending=decision;count+=1
    write(OUT/'discrepancias_contabilidad.csv',bad,fields=['serie','tick','real','esperado'])
    assert count==160000 and not bad
    stress={
      'subida_prolongada':[100+t*155//19999 for t in range(20000)],
      'caida_gradual':[255-t*155//2047 for t in range(2048)],
      'caida_brusca':[220]*200+[100]*200,
      'lateral':[170+(t%9==0)-(t%11==0) for t in range(1024)],
      'recuperacion':[220]*128+[100]*128+[100+t*120//511 for t in range(512)],
      'alternancia':[100,255]*256,
      'limites_inventario':[1]*128+[255]*128+[1]*128+[255]*128,
      'integracion_compra_venta':[100]*80+[220]*80+[100]*80,
      'falsas_senales':([160]*64+[170]*8+[160]*64+[150]*8)*8,
    }
    rows=[]
    for name,p in stress.items():
        for label,policy in [('ATM',Policy(cfg)),('Momentum32',active.Policy(active.frozen()))]:
            m,_=run(p,policy);rows.append(dict(escenario=name,estrategia=label,sintetico=True,**m))
    write(OUT/'pruebas_estres.csv',rows)
    (OUT/'validacion_modelo.json').write_text(json.dumps(dict(ticks=count,discrepancias=0,
        capa='Python y cartera independiente; NO RV32E ni RTL ATM',estres=len(stress)),indent=2))
    print('PASS 160000 ticks de contabilidad/decisiones ATM; 9 escenarios sinteticos; no implica RV32E ni RTL')

if __name__=='__main__':main()
