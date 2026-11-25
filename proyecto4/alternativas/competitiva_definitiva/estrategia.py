"""Modelo causal entero. La orden pendiente se ejecuta ANTES de decidir.

Benchmark oficial (compra ideal en tick 0) y benchmark SPI ejecutable son distintos.
No hay información de empresa, fechas ni precios futuros en Policy.
"""
from dataclasses import dataclass, asdict
from pathlib import Path
import csv
import json

HERE = Path(__file__).resolve().parent

@dataclass(frozen=True)
class Config:
    family: str = 'momentum'
    fast: int = 32
    slow: int = 128
    exit: int = 16
    entry: int = 6
    gradual: int = 0
    stop: int = 0
    exposure: int = 100
    neutral: int = 0
    review: int = 8

def load(path):
    with Path(path).open(encoding='utf-8-sig', newline='') as f:
        rows = list(csv.reader(f))
    assert len(rows[0]) == 2, rows[0]
    prices = [int(r[1]) for r in rows[1:] if r]
    assert all(100 <= p <= 255 for p in prices)
    assert [int(r[0]) for r in rows[1:] if r] == list(range(len(prices)))
    return prices

def fill(cash, shares, order, price):
    """SV division truncates toward zero; negative buying capacity never fills."""
    q, act = order & 63, order >> 6
    n = fee = 0
    if act == 1:
        n = min(q, max(0, (cash-5)//price))
        if n:
            cash -= n*price+5
            shares += n
            fee = 5
    elif act == 2:
        n = min(q, shares)
        if n and cash+n*price >= 5:
            cash += n*price-5
            shares -= n
            fee = 5
        else:
            n = 0
    assert cash >= 0 and shares >= 0
    return cash, shares, n, fee

class Policy:
    def __init__(self, cfg=Config()):
        self.cfg=cfg
        self.history=[]
        self.regime=1
        self.peak=0
        self.fast=self.slow=0
        self.target=0

    def decide(self, p, cash, shares):
        c=self.cfg
        t=len(self.history)
        h=self.history
        self.fast=p-h[t-c.fast] if t>=c.fast else 0
        self.slow=p-h[t-c.slow] if t>=c.slow else 0
        self.peak=max(self.peak,p) if shares else p
        if t%c.review == 0 and t>=c.fast:
            leave=self.fast<=-c.exit
            enter=self.fast>=c.entry
            if c.family in ('dual','hybrid'):
                leave |= t>=c.slow and self.slow<=-c.gradual
                enter &= self.slow>=0
            elif c.family=='persistence':
                leave |= t>=c.slow and p*c.slow < sum(h[-c.slow:])-c.gradual*c.slow
            elif c.family=='lowerhigh':
                leave |= t>=c.slow and max(h[-c.fast:]) < max(h[-c.slow:-c.fast])-c.gradual
            elif c.family=='negative':
                leave |= t>=c.slow and sum(b<a for a,b in zip(h[-c.slow:],h[-c.slow+1:]+[p]))>=c.gradual
            if c.family=='breakout':
                enter &= p>=max(h[-c.fast:]) and self.slow>=0
            if c.family in ('trailing','adaptive','hybrid'):
                distance=c.stop
                if c.family=='adaptive':
                    distance=max(c.stop, 4*sum(abs(b-a) for a,b in zip(h[-c.fast:], h[-c.fast+1:]+[p]))//c.fast)
                leave |= self.peak-p>=distance
            if leave: self.regime=0
            elif enter: self.regime=1
        exposure=c.exposure if self.regime else c.neutral
        self.target=shares+max(0,(cash-5)//p) if exposure==100 else exposure*(cash+shares*p)//(100*p)
        self.history.append(p)
        if shares>self.target:
            return 128+min(63,shares-self.target)
        if self.target>shares:
            q=min(63,self.target-shares,max(0,(cash-5)//p))
            return 64+q if q else 0
        return 0

def benchmark(prices):
    q=(10000-5)//prices[0]
    return 10000-5-q*prices[0]+q*prices[-1]

def run(prices,cfg=Config(),trace=False):
    policy=Policy(cfg)
    cash=peak=wealth=10000
    shares=order=orders=fees=dd=0
    dd_pct=0.0
    cash_ticks=high_ticks=0
    rows=[]
    for t,p in enumerate(prices):
        miso=order
        cash,shares,n,fee=fill(cash,shares,order,p)
        orders+=int(n>0); fees+=fee
        wealth=cash+shares*p
        peak=max(peak,wealth); dd=max(dd,peak-wealth)
        dd_pct=max(dd_pct,100*(peak-wealth)/peak)
        cash_ticks+=shares==0
        high_ticks+=shares*p*4>=wealth*3
        order=policy.decide(p,cash,shares)
        assert order>>6 in (0,1,2) and 0<=order&63<=63
        if trace:
            rows.append(dict(tick=t,precio=p,decision=order,miso=miso,fast=policy.fast,slow=policy.slow,
                regimen=policy.regime,posicion_objetivo=policy.target,cantidad_solicitada=miso&63,
                cantidad_ejecutada=n,caja=cash,acciones=shares,patrimonio=wealth,comision=fee,
                orden_pendiente=order,comisiones_acum=fees,drawdown_max=dd))
    bh=benchmark(prices)
    return dict(patrimonio=wealth,caja=cash,acciones=shares,ordenes=orders,comisiones=fees,drawdown=dd,
        drawdown_pct=dd_pct,mantener_oficial=bh,ventaja=wealth-bh,ventaja_pct=100*(wealth/bh-1),
        ticks_caja=cash_ticks,ticks_exposicion_alta=high_ticks),rows

def frozen():
    return Config(**json.loads((HERE/'resultados/seleccion.json').read_text())['config'])

def write_csv(path, rows):
    rows=list(rows)
    assert rows
    Path(path).parent.mkdir(parents=True,exist_ok=True)
    with Path(path).open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
