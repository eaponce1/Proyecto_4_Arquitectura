"""Contabilidad independiente: primero llena el byte anterior, luego decide."""
import csv,statistics as st

def execute(cash,shares,byte,price):
    assert 1<=price<=255 and 0<=byte<=255 and cash>=0 and shares>=0
    action,q=byte>>6,byte&63
    if action==1:
        q=min(q,max(0,(cash-5)//price))
        if q:return cash-q*price-5,shares+q,q,5
    elif action==2:
        q=min(q,shares)
        if q and cash+q*price>=5:return cash+q*price-5,shares-q,q,5
    return cash,shares,0,0

def benchmark(prices):
    q=9995//prices[0]
    return 10000-5-q*prices[0]+q*prices[-1]

def run(prices,policy,trace=False):
    cash=peak=10000;shares=pending=orders=fees=dd=buys=sells=invested=0;ddpct=0.;rows=[]
    for tick,p in enumerate(prices):
        received=pending
        cash,shares,n,fee=execute(cash,shares,received,p)
        wealth=cash+shares*p;peak=max(peak,wealth);dd=max(dd,peak-wealth)
        ddpct=max(ddpct,100*(peak-wealth)/peak);orders+=n>0;fees+=fee
        buys+=bool(n and received>>6==1);sells+=bool(n and received>>6==2);invested+=shares>0
        pending=policy.decide(p,cash,shares)
        assert 0<=pending<=255 and cash>=0 and shares>=0
        if trace:rows.append(dict(tick=tick,precio=p,miso=received,decision=pending,caja=cash,
            acciones=shares,patrimonio=wealth,fill=n,comision=fee,comisiones_acum=fees,
            drawdown=peak-wealth,drawdown_pct=100*(peak-wealth)/peak,
            exposicion_pct=100*shares*p/wealth,regimen=getattr(policy,'regime_name','BASELINE')))
    bh=benchmark(prices)
    return dict(patrimonio=wealth,caja=cash,acciones=shares,ordenes=orders,compras=buys,ventas=sells,
        comisiones=fees,drawdown=dd,drawdown_pct=ddpct,mantener_oficial=bh,ventaja=wealth-bh,
        ventaja_pct=100*(wealth-bh)/bh,ticks_invertido=invested,ticks=len(prices)),rows

def rank(metrics):
    a=[m['ventaja_pct'] for m in metrics]
    # Congelado antes de medir: recompensa consistencia, penaliza cola negativa y riesgo.
    return (100*sum(x>0 for x in a)/len(a)+st.median(a)+.25*st.mean(a)+min(a)
            -.2*max(m['drawdown_pct'] for m in metrics)
            -st.mean(m['comisiones'] for m in metrics)/1000
            -10*sum(x<-10 for x in a)/len(a))

def write(path,rows,fields=None):
    rows=list(rows)
    with path.open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields or list(rows[0]));w.writeheader();w.writerows(rows)
