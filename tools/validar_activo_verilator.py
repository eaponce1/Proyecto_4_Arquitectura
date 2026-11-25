"""Ejecutor Linux/WSL de las ocho series contra el RTL ACTIVO.

Complementa Icarus (cuatro estados): Verilator simula en dos estados y no
sustituye sus comprobaciones de X. Requiere Verilator >=5 y g++/make.
"""
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
HERE=ROOT/"proyecto4/alternativas/competitiva_definitiva"
sys.path.insert(0,str(HERE))
from estrategia import *
import os
import shutil
import subprocess
import time
import hashlib
import statistics as st

BUILD=ROOT/'build/trader/verilator'

def cmd(args,log):
    start=time.perf_counter()
    with log.open('w') as f:
        p=subprocess.run([str(x) for x in args],cwd=ROOT,stdout=f,stderr=subprocess.STDOUT)
        f.write(f'\nSalida={p.returncode}; segundos={time.perf_counter()-start:.6f}\n')
    assert p.returncode==0,(log,log.read_text()[-2500:])

def main():
    BUILD.mkdir(parents=True,exist_ok=True)
    tool=os.environ.get('POCH_VERILATOR','verilator')
    words=len((ROOT/'sw/trade.hex').read_text().split())
    src=[ROOT/'rtl/trade_spi_externo.v',*sorted((ROOT/'rtl/trader').glob('*.v')),
         *sorted((ROOT/'rtl/espino_core').glob('*.v'))]
    tb=HERE.parent/'candidata_final/tb/tb_candidata.sv'
    initial_signature={p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest()
                       for p in [*src,tb,ROOT/'sw/trade.hex']}
    cells=Path('/mnt/c/Tools/oss-cad-suite/share/yosys/ice40/cells_sim.v')
    if not cells.exists():
        cells=Path(shutil.which('yosys')).resolve().parents[1]/'share/yosys/ice40/cells_sim.v'
    # Local temporary compilation avoids slow C++ builds over the Windows mount.
    obj=Path('/tmp/pochoco_activo_spi_obj')
    base=[tool,'--binary','--timing','--assert','--language','1800-2017','-DNO_ICE40_DEFAULT_ASSIGNMENTS','-Wno-fatal','--top-module','tb_candidata','-j','2',
       '--Mdir',obj,'-GTICKS=20000','-GPERIODO_NS=100000',f'-GPALABRAS_FIRMWARE={words}',
       '-GREG_CAJA=15','-GREG_ACCIONES=5',f'-GARCHIVO_FIRMWARE="{(ROOT/"sw/trade.hex").relative_to(ROOT).as_posix()}"',
       tb,*src,cells]
    cmd(base,BUILD/'compilacion.log')
    executable=obj/'Vtb_candidata'
    evidence=[]
    for path in sorted((HERE/'datos').glob('*.csv')):
        name=path.stem;vec=HERE/'build/vectores'/name;csvout=BUILD/f'{name}.csv'
        cmd([executable,f'+vectores={vec.as_posix()}',f'+cartera={(vec/"cartera.hex").as_posix()}',
           f'+metricas={csvout.as_posix()}'],BUILD/f'{name}.log')
        log=(BUILD/f'{name}.log').read_text();assert 'PASS 20000 MISO frente a Python' in log
        _,expected=run(load(path),frozen(),True)
        with csvout.open(newline='') as f:rows=list(csv.DictReader(f))
        assert len(rows)==20000
        for real,ex in zip(rows,expected,strict=True):
            for a,b in [('tick','tick'),('precio','precio'),('caja','caja'),('acciones','acciones'),
                ('fill','cantidad_ejecutada'),('patrimonio','patrimonio'),('comisiones_acum','comisiones_acum')]:
                assert int(real[a])==ex[b],(name,ex['tick'],a,real[a],ex[b])
            assert int(real['miso_hex'],16)==ex['miso'] and int(real['decision_hex'],16)==ex['decision']
        cycles=[int(r['ciclos']) for r in rows];ic=[int(r['ic']) for r in rows]
        evidence.append(dict(serie=name,ticks=20000,discrepancias=0,periodo_ns=100000,
           ciclos_max=max(cycles),ciclos_media=st.mean(cycles),ic_max=max(ic),ic_media=st.mean(ic),
           cpi=sum(cycles)/sum(ic),us_max=max(cycles)*.08,
           log=str((BUILD/f'{name}.log').relative_to(ROOT)),dos_estados=True))
        print('PASS Verilator',name,'20000 ticks',max(cycles),'ciclos',flush=True)
    assert all(hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==h for p,h in initial_signature.items())
    (ROOT/'build/trader/equivalencia_verilator.json').write_text(json.dumps(dict(
        sha256_hex=hashlib.sha256((ROOT/'sw/trade.hex').read_bytes()).hexdigest(),series=evidence,
        fuentes=initial_signature),indent=2))

if __name__=='__main__':main()
