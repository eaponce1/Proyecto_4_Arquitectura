"""Equivalencia exacta, incluyendo todas las órdenes y estados de cartera."""
from estrategia import *
import importlib.util
import sys
import time
import subprocess
import hashlib

ROOT=HERE.parents[2]

def machine_class():
    current=sys.modules['estrategia']
    spec=importlib.util.spec_from_file_location('estrategia',ROOT/'proyecto4/python/estrategia.py')
    m=importlib.util.module_from_spec(spec);sys.modules['estrategia']=m;spec.loader.exec_module(m)
    sys.path.insert(0,str(ROOT/'proyecto4/python'))
    from test_trade_equivalencia import TradeMachine
    sys.modules['estrategia']=current
    return TradeMachine

def main():
    start=time.perf_counter()
    assembled=HERE/'build/trade_reensamblado.hex'
    proc=subprocess.run([sys.executable,'-B','sw/assembler.py',str(HERE/'trade.s'),'-o',str(assembled)],cwd=ROOT,capture_output=True,text=True)
    (HERE/'build/ensamblado.log').write_text(proc.stdout+proc.stderr+f'\nSalida={proc.returncode}\n')
    assert proc.returncode==0
    words=[int(x,16) for x in assembled.read_text().split()]
    assert words==[int(x,16) for x in (HERE/'trade.hex').read_text().split()], 'Ensamblado distinto del HEX validado'
    assert len(words)<256
    Machine=machine_class()
    from validar_estrategia import synth
    data={p.stem:load(p) for p in sorted((HERE/'datos').glob('*.csv'))}
    data.update(synth())
    reports=[];cfg=frozen()
    for name,p in data.items():
        met,rows=run(p,cfg,True);cpu=Machine(words);maxic=0
        for row in rows:
            miso,ic=cpu.one_tick(row['precio']);maxic=max(maxic,ic)
            real=(miso,cpu.tx_hold,cpu.reg[15],cpu.reg[5])
            expected=(row['miso'],row['decision'],row['caja'],row['acciones'])
            assert real==expected,(name,row['tick'],real,expected)
            assert cpu.reg[7]==row['regimen']
        dest=HERE/'build/vectores'/name;dest.mkdir(parents=True,exist_ok=True)
        for label,key in [('precios','precio'),('miso','miso'),('escrituras','decision')]:
            (dest/f'{label}.hex').write_text(''.join(f'{r[key]:02x}\n' for r in rows))
        (dest/'cartera.hex').write_text(''.join(f"{(r['caja']<<32)|(r['patrimonio']<<8)|r['acciones']:016x}\n" for r in rows))
        assert max(r['acciones'] for r in rows)<=255, 'Cambiar empaquetado antes de usar estos vectores RTL'
        reports.append(dict(serie=name,ticks=len(p),discrepancias=0,ic_max=maxic,**met))
        print('PASS Python/RV32E',name,len(p),maxic,flush=True)
    out=dict(hex_sha256=hashlib.sha256((HERE/'trade.hex').read_bytes()).hexdigest(),
        asm_sha256=hashlib.sha256((HERE/'trade.s').read_bytes()).hexdigest(),
        words=len(words),series=reports,segundos=time.perf_counter()-start)
    (HERE/'resultados/equivalencia_rv32e.json').write_text(json.dumps(out,indent=2))

if __name__=='__main__':main()
