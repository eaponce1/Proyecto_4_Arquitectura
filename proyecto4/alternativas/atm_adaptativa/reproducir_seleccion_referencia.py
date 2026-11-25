"""Verifica selección histórica LOCO/LOSO y vuelve a seleccionar prefijos WF."""
from concurrent.futures import ProcessPoolExecutor
import json,statistics as st
from pathlib import Path
from baselines import active,OLD
from backtest import read
HERE=Path(__file__).resolve().parent

def rank(rows):
    a=[float(r['ventaja_pct']) for r in rows]
    return (sum(x>0 for x in a)/len(a),st.median(a)+.25*st.mean(a)+.5*min(a)-.05*max(float(r['drawdown_pct']) for r in rows),
            min(int(r['patrimonio']) for r in rows),-st.mean(float(r['comisiones']) for r in rows))

def wf(end):
    data=[active.load(p) for p in sorted((OLD/'datos').glob('*.csv'))]
    configs=[active.Config(**r) for r in json.loads((OLD/'resultados/grilla_declarada.json').read_text())]
    eligible=[int(r['config']) for r in read(OLD/'resultados/filtro_adverso_desarrollo.csv') if int(r['admisible'])]
    winner=max(eligible,key=lambda i:rank([active.run(p[:end],configs[i])[0] for p in data]))
    return dict(fin_ajuste=end,config=winner)

def main():
    full=read(OLD/'resultados/grilla_completa_desarrollo.csv')
    table={}
    for r in full:table.setdefault(int(r['config']),{})[r['serie']]=r
    eligible=[int(r['config']) for r in read(OLD/'resultados/filtro_adverso_desarrollo.csv') if int(r['admisible'])]
    folds=read(OLD/'resultados/validacion_por_grupos.csv');checked=0
    for r in folds:
        train=r['entrenamiento'].split(',')
        assert r['serie'] not in train
        if r['metodo']=='leave_one_company_out':assert all(n.split('_')[1]!=r['excluido'] for n in train)
        winner=max(eligible,key=lambda i:rank([table[i][n] for n in train]))
        assert winner==int(r['config']);checked+=1
    with ProcessPoolExecutor(max_workers=3) as pool:walk=list(pool.map(wf,[8000,12000,16000]))
    saved=read(OLD/'resultados/walk_forward.csv')
    for r in walk:assert all(int(s['config'])==r['config'] for s in saved if int(s['fin_ajuste'])==r['fin_ajuste'])
    (HERE/'resultados/referencia/selecciones_historicas_reproducidas.json').write_text(json.dumps(dict(
        folds_comprobados=checked,seleccion_loco_loso='Matriz historica completa, solo empresas/series de ajuste',
        walk_forward=walk,walk_seleccion='Prefijos historicos reejecutados sin ventanas de prueba'),indent=2))
    print('PASS seleccion historica: LOCO/LOSO desde matriz y WF desde prefijos reejecutados',flush=True)

if __name__=='__main__':main()
