"""SUM10 / 128 ticks / 5 %, igual al firmware de 130 palabras importado."""
from pathlib import Path
from dataclasses import dataclass,asdict
from collections import deque
import csv,json
HERE=Path(__file__).resolve().parent
DATA=HERE.parent/'competitiva_definitiva/datos'
@dataclass(frozen=True)
class Config:
    periodo:int=128
    umbral_pct:int=5
    lote_max:int=63
    min_adicional:int=8
    senal:str='SUM10'
def frozen():return Config()
def load(path):
    with Path(path).open(encoding='utf-8-sig',newline='') as f:r=list(csv.reader(f))
    assert len(r[0])==2 and [int(x[0]) for x in r[1:]]==list(range(len(r)-1))
    p=[int(x[1]) for x in r[1:]];assert all(1<=x<=255 for x in p);return p
def fill(cash,shares,order,p):
    action,q=order>>6,order&63
    if action==1:
        q=min(q,max(0,(cash-5)//p))
        if q:return cash-q*p-5,shares+q,q,5
    if action==2:
        q=min(q,shares)
        if q and cash+q*p>=5:return cash+q*p-5,shares-q,q,5
    return cash,shares,0,0
class Policy:
    def __init__(self,cfg=None):
        self.cfg=cfg or frozen();assert self.cfg==frozen(),'Firmware congelado 128/5 %'
        self.recent=deque(maxlen=10);self.anchor=0;self.inside=False;self.tick=0
    def decide(self,p,cash,shares):
        self.recent.append(p)
        if self.tick%128==0 and len(self.recent)==10:
            total=sum(self.recent)
            if self.anchor and 20*abs(total-self.anchor)>=self.anchor:self.inside=total>=self.anchor
            self.anchor=total
        self.tick+=1
        if self.inside:
            q=min(63,max(0,(cash-5)//p))
            return 64+q if q>=(8 if shares else 1) else 0
        return 128+min(63,shares) if shares else 0
def benchmark(p):
    q=9995//p[0];return 9995-q*p[0]+q*p[-1]
def run(prices,cfg=None,trace=False):
    policy=Policy(cfg);cash=peak=10000;shares=order=orders=fees=dd=buys=sells=invested=0;dd_pct=0.;rows=[]
    for t,p in enumerate(prices):
        miso=order;cash,shares,n,fee=fill(cash,shares,order,p)
        assert cash>=0 and shares>=0
        wealth=cash+shares*p;peak=max(peak,wealth);dd=max(dd,peak-wealth)
        dd_pct=max(dd_pct,100*(peak-wealth)/peak);orders+=n>0;fees+=fee
        buys+=bool(n and miso>>6==1);sells+=bool(n and miso>>6==2);invested+=shares>0
        order=policy.decide(p,cash,shares)
        if trace:rows.append(dict(tick=t,precio=p,miso=miso,decision=order,caja=cash,acciones=shares,
            patrimonio=wealth,cantidad_ejecutada=n,comision=fee,comisiones_acum=fees,
            regimen=int(policy.inside),sum10=sum(policy.recent),ready=int(len(policy.recent)==10),
            drawdown_actual=peak-wealth,drawdown_actual_pct=100*(peak-wealth)/peak))
    b=benchmark(prices)
    return dict(patrimonio=wealth,caja=cash,acciones=shares,ordenes=orders,compras=buys,ventas=sells,
        comisiones=fees,drawdown=dd,drawdown_pct=dd_pct,mantener_oficial=b,ventaja=wealth-b,
        ventaja_pct=100*(wealth-b)/b,ticks_caja=len(prices)-invested,ticks_exposicion_alta='',ticks_invertido=invested),rows
def write_csv(path,rows,fields=None):
    rows=list(rows);Path(path).parent.mkdir(parents=True,exist_ok=True)
    with Path(path).open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields or list(rows[0]));w.writeheader();w.writerows(rows)
def synth():
    return {'integracion_cadencias':[100]*128+[110]*128+[100]*140,
        'recuperacion':[220]*128+[100]*128+[100+t*120//511 for t in range(512)],
        'estres':[50]*128+[60]*128+[40]*140+[10]*116+[11]*128+[200]*128+[5]*128+[1]*40,
        'subida':[100+t*155//2047 for t in range(2048)],
        'caida_gradual':[255-t*155//2047 for t in range(2048)],
        'caida_brusca':[220]*256+[100]*256,'lateral':[170+(t%9==0)-(t%11==0) for t in range(1024)],
        'alternancia':[100,255]*512}
