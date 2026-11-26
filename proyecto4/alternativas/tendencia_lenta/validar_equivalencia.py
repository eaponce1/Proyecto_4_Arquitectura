"""Reensambla y coteja todas las decisiones, MISO y cartera contra RV32E real."""
from pathlib import Path
import sys,hashlib,json,subprocess,gzip
from modelo_lento import *
ROOT=HERE.parents[2];OUT=HERE/'resultados';BUILD=HERE/'build'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    OUT.mkdir(exist_ok=True);BUILD.mkdir(exist_ok=True)
    assembled=BUILD/'reensamblado.hex'
    p=subprocess.run([sys.executable,'-B',ROOT/'sw/assembler.py',HERE/'trade.s','-o',assembled],cwd=ROOT,capture_output=True,text=True)
    (OUT/'ensamblado.log').write_text(p.stdout+p.stderr+f'\nSalida={p.returncode}\n')
    assert p.returncode==0,p.stderr
    assert assembled.read_text().split()==(HERE/'trade.hex').read_text().split()
    sys.path.insert(0,str(ROOT/'proyecto4/python'))
    from test_capital_protegido import MaquinaMMIO,words_from_hex
    words=words_from_hex(HERE/'trade.hex');assert len(words)==130
    data={p.stem:load(p) for p in sorted(DATA.glob('*.csv'))};data.update(synth())
    reports=[];bad=[]
    for name,prices in data.items():
        m,rows=run(prices,frozen(),True);cpu=MaquinaMMIO(words);maxic=0
        for r in rows:
            miso,ic=cpu.one_tick(r['precio']);maxic=max(maxic,ic)
            actual=(miso,cpu.tx_hold,cpu.reg[15],cpu.reg[5]);expected=(r['miso'],r['decision'],r['caja'],r['acciones'])
            if actual!=expected:bad.append(dict(serie=name,tick=r['tick'],observado=str(actual),esperado=str(expected)))
            assert actual==expected,(name,r['tick'],actual,expected)
            assert bool(cpu.reg[6]&128)==bool(r['regimen'])
        folder=BUILD/'vectores'/name;folder.mkdir(parents=True,exist_ok=True)
        for f,k in [('precios','precio'),('miso','miso'),('escrituras','decision')]:
            (folder/(f+'.hex')).write_text(''.join(f'{r[k]:02x}\n' for r in rows))
        if max(r['acciones'] for r in rows)<=255:
            (folder/'cartera.hex').write_text(''.join(f"{(r['caja']<<32)|(r['patrimonio']<<8)|r['acciones']:016x}\n" for r in rows))
        write_csv(BUILD/f'{name}_ticks.csv',rows)
        reports.append(dict(serie=name,ticks=len(rows),ic_max=maxic,discrepancias=0,**m))
        print('PASS Python/RV32E',name,len(rows),'IC max',maxic,flush=True)
    write_csv(OUT/'discrepancias_python_rv32e.csv',bad,fields=['serie','tick','observado','esperado'])
    write_csv(OUT/'comparacion_final.csv',[{k:v for k,v in r.items() if k not in ('ic_max','discrepancias','ticks')} for r in reports[:8]])
    (OUT/'equivalencia_rv32e.json').write_text(json.dumps(dict(sha256_s=sha(HERE/'trade.s'),sha256_hex=sha(HERE/'trade.hex'),
        palabras=130,series=reports,ticks_practica=sum(r['ticks'] for r in reports[:8]),discrepancias=0),indent=2))
if __name__=='__main__':main()
