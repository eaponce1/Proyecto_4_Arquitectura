"""Políticas anteriores, todas ejecutadas por simulador.execute del estudio ATM."""
from pathlib import Path
import importlib.util,sys
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
OLD=HERE.parent/'competitiva_definitiva'

def module(name,path):
    spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec)
    sys.modules[name]=m;spec.loader.exec_module(m);return m

active=module('atm_baseline_momentum',OLD/'estrategia.py')

class Slow:
    def __init__(self):self.h=[];self.anchor=0;self.inside=False;self.tick=0
    def decide(self,p,cash,shares):
        self.h=(self.h+[p])[-10:]
        if self.tick%128==0 and len(self.h)==10:
            total=sum(self.h)
            if self.anchor and 20*abs(total-self.anchor)>=self.anchor:self.inside=total>=self.anchor
            self.anchor=total
        self.tick+=1
        if self.inside:
            q=min(63,max(0,(cash-5)//p))
            return 64+q if q>=(8 if shares else 1) else 0
        return 128+min(63,shares) if shares else 0

class Cash:
    def decide(self,p,cash,shares):return 0

class HoldSPI:
    def decide(self,p,cash,shares):
        q=min(63,max(0,(cash-5)//p));return 64+q if q else 0

class Legacy:
    def __init__(self,policy):self.policy=policy;self.h=[]
    def decide(self,p,cash,shares):
        self.h.append(p);return self.policy(self.h,shares,len(self.h)-1).byte

def policies():
    # Importar la API histórica en su propio entorno; no usar el modelo activo con ese nombre.
    sys.path.insert(0,str(ROOT/'proyecto4/python'))
    original=sys.modules.get('estrategia')
    current_simulator=sys.modules.get('simulador')
    module('estrategia',ROOT/'proyecto4/python/estrategia.py')
    module('simulador',ROOT/'proyecto4/python/simulador.py')
    sma=module('atm_legacy_sma',ROOT/'proyecto4/python/enfoques_finales.py')
    candidate=module('atm_legacy_candidate',HERE.parent/'candidata_final/estrategia_referencia.py')
    aggressive=module('atm_legacy_aggressive',HERE.parent/'agresiva/estrategia_agresiva.py')
    if original is not None:sys.modules['estrategia']=original
    if current_simulator is None:sys.modules.pop('simulador',None)
    else:sys.modules['simulador']=current_simulator
    return {'Momentum32':lambda:active.Policy(active.frozen()),'Tendencia_lenta':Slow,
        'SMA10':lambda:Legacy(sma.estrategia_reversion_media),
        'Agresiva':lambda:Legacy(aggressive.crear_politica(aggressive.Parametros('momentum',100,False,16,8))),
        'Candidata_anterior':lambda:Legacy(candidate.crear_politica()),
        'Mantener_SPI':HoldSPI,'No_operar':Cash}
