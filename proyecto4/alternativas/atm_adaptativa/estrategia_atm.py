"""ATM: régimen causal, exposición configurable y stop entero según volatilidad.

Solo decide; la ejecución del byte pendiente pertenece al simulador independiente.
Los deltas son puntos del precio normalizado; ninguna señal recibe datos futuros.
"""
from dataclasses import dataclass, asdict, replace
from collections import deque

@dataclass(frozen=True)
class Config:
    signal: str = 'hybrid'
    fast: int = 16
    slow: int = 64
    review: int = 8
    entry: int = 4
    exit: int = 4
    stop: int = 12
    vol_mult: int = 4
    confirm: int = 2
    exposure: int = 100       # 0 = dinámica, no caja permanente
    neutral: int = -1        # -1 conserva exposición anterior en lateralidad
    bear: int = 0
    reserve: int = 0
    min_order: int = 4
    min_hold: int = 16
    progressive: int = 63
    initial: int = 0

def population():
    profiles=[Config(),Config(fast=32,slow=128,review=16,entry=6,exit=8,stop=20,
        vol_mult=2,neutral=25,bear=25,reserve=1000,min_order=8,min_hold=64,progressive=16),
        Config(review=4,entry=2,stop=8,vol_mult=8,confirm=3,reserve=500,min_hold=0,progressive=16),
        Config(fast=32,review=8,exit=6,stop=20,vol_mult=0,confirm=1,neutral=0,min_order=1,min_hold=0,initial=100)]
    configs=[]
    for p in profiles:
        for signal in ('momentum','ma','hybrid','persistence','breakout','slope'):
            for exposure in (25,50,75,90,100,0):
                configs.append(replace(p,signal=signal,exposure=exposure))
    for fast in (16,32):
        for slow in (64,128):
            for stop in (12,20,28):
                for review in (8,16):
                    for confirm in (1,2):
                        configs.append(replace(Config(),fast=fast,slow=slow,stop=stop,
                            review=review,confirm=confirm,exposure=0))
    return list(dict.fromkeys(configs))

class Policy:
    def __init__(self,cfg):
        self.c=cfg;self.history=[];self.prefix=[0];self.abs_prefix=[0]
        self.regime=0;self.exposure=cfg.initial;self.confirmations=0
        self.peak=0;self.entry_price=0;self.entry_tick=0;self.last_shares=0
        self.regime_name='LATERAL';self.volatility=0;self.stop_distance=cfg.stop

    def decide(self,p,cash,shares):
        c=self.c;t=len(self.history);h=self.history
        if shares and not self.last_shares:
            self.entry_tick=t;self.entry_price=p;self.peak=p
        self.peak=max(self.peak,p) if shares else p
        self.last_shares=shares
        self.prefix.append(self.prefix[-1]+p)
        self.abs_prefix.append(self.abs_prefix[-1]+(abs(p-h[-1]) if h else 0))
        if t%c.review==0 and t>=c.slow:
            fast=p-h[t-c.fast];slow=p-h[t-c.slow]
            sf=self.prefix[-1]-self.prefix[-1-c.fast]
            ss=self.prefix[-1]-self.prefix[-1-c.slow]
            spread=sf*c.slow-ss*c.fast
            volatility=(self.abs_prefix[-1]-self.abs_prefix[-17]+15)//16
            self.volatility=volatility
            distance=min(40,max(c.stop,c.vol_mult*max(1,volatility)))
            self.stop_distance=distance
            up=fast>=c.entry and slow>=0
            down=fast<=-c.exit and slow<=0
            if c.signal=='ma':
                up=spread>=c.entry*c.fast*c.slow and slow>=0
                down=spread<=-c.exit*c.fast*c.slow
            elif c.signal=='hybrid':
                up=up and spread>=0
                down=down or spread<=-c.exit*c.fast*c.slow
            elif c.signal=='persistence':
                signs=sum(h[i]>h[i-c.review] for i in range(t-3*c.review,t,c.review) if i>=c.review)
                up=up and signs>=2
                down=down or (fast<0 and signs==0)
            elif c.signal=='breakout':
                up=up and p>=max(h[-c.slow:])
                down=down or p<min(h[-c.fast:])
            elif c.signal=='slope':
                previous=h[t-c.review]-h[max(0,t-c.review-c.fast)]
                up=up and fast>=previous
                down=down or (slow<0 and fast<previous)
            stop=bool(shares and (self.peak-p>=distance or self.entry_price-p>=distance))
            self.confirmations=self.confirmations+1 if up else 0
            holding=shares and t-self.entry_tick<c.min_hold
            if stop or (down and not holding):
                self.regime=-1;self.exposure=c.bear;self.regime_name='BAJISTA'
            elif self.confirmations>=c.confirm:
                self.regime=1;self.regime_name='ALCISTA'
                self.exposure=c.exposure or (100 if fast>=2*c.entry and slow>=c.entry and volatility<=2 else 75 if volatility<=3 else 25)
            else:
                self.regime=0;self.regime_name='LATERAL'
                if c.neutral>=0 and not holding:self.exposure=c.neutral
        self.history.append(p)
        wealth=cash+shares*p
        budget=max(0,wealth-c.reserve)
        target=(budget*self.exposure)//(100*p)
        if shares>target:
            q=min(63,shares-target)
            return 128+q if q and (target==0 or q>=c.min_order) else 0
        if shares<target:
            q=min(63,c.progressive,target-shares,max(0,(cash-c.reserve-5)//p))
            # Movimiento pasado como filtro de costo; no es una ganancia esperada garantizada.
            edge=abs(p-self.history[max(0,t-c.fast)])
            return 64+q if q>=c.min_order and edge*q>=10 else 0
        return 0
