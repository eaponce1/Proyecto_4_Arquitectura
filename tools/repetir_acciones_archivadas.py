"""Repite SPI/RTL desde los precios de las trazas publicadas, sin ZIP externo.

Linux/WSL con Verilator >=5 y g++/make. --serie permite repetir un solo caso.
La salida se separa de la campaña original, que no se sobrescribe.
"""
from pathlib import Path
import argparse,csv,gzip,hashlib,io,json,os,shutil
from concurrent.futures import ThreadPoolExecutor,as_completed
import probar_todas_acciones as bank
import trader
def main():
    p=argparse.ArgumentParser();p.add_argument('--serie');p.add_argument('--jobs',type=int,default=2)
    p.add_argument('--listar',action='store_true');args=p.parse_args();assert args.jobs>0
    report=json.loads((bank.REPORT/'resumen.json').read_text(encoding='utf-8'))
    if args.listar:
        print('\n'.join(r['serie'] for r in report['resultados']));return
    active=trader.verify();assert report['sha256_bin']==active['sha256_bin']
    selected=[r for r in report['resultados'] if args.serie is None or r['serie']==args.serie]
    if not selected:raise ValueError('Serie desconocida; consulta --listar')
    native=shutil.which('verilator')
    if 'POCH_VERILATOR' not in os.environ and native and not str(native).startswith('/mnt/'):
        os.environ['POCH_VERILATOR']=native
    if 'POCH_VERILATOR' not in os.environ:
        cache=Path('/tmp/pochoco_verilator_20261125/extracted/usr')
        assert (cache/'bin/verilator_bin').exists(),'Instala Verilator nativo >=5, g++ y make'
        os.environ['POCH_VERILATOR']=str(cache/'bin/verilator_bin')
        os.environ['VERILATOR_ROOT']=str(cache/'share/verilator')
    bank.BUILD=bank.ROOT/'build/repeticion_acciones_archivadas';bank.BUILD.mkdir(parents=True,exist_ok=True)
    cases=[]
    for r in selected:
        raw=gzip.decompress((bank.ROOT/'docs/evidencia_todas_acciones/trazas_rtl'/(r['serie']+'.csv.gz')).read_bytes())
        assert hashlib.sha256(raw).hexdigest()==r['sha256_traza']
        prices=[int(a['precio']) for a in csv.DictReader(io.StringIO(raw.decode()))]
        assert hashlib.sha256(bytes(prices)).hexdigest()==r['sha256_precios'] and len(prices)==r['ticks']
        cases.append(dict(id=r['serie'],precios=prices,**{k:r[k] for k in ('grupo','escala','filas_originales','origen','sha256_original')}))
    period=report['periodo_ns'];sources=trader.sources()
    executables={n:bank.compile_tb(period,sources,n) for n in sorted({len(c['precios']) for c in cases})}
    results=[]
    with ThreadPoolExecutor(max_workers=args.jobs) as pool:
        futures=[pool.submit(bank.test,c,executables[len(c['precios'])],period) for c in cases]
        for future in as_completed(futures):results.append(future.result()[0])
    path=bank.BUILD/'resumen_repeticion.json'
    path.write_text(json.dumps(dict(sha256_bin=active['sha256_bin'],resultados=results),indent=2),encoding='utf-8')
    assert all(r['estado']=='PASS' for r in results),path
    print('PASS repeticion',len(results),'casos;',sum(r['ticks'] for r in results),'ticks;',path)
if __name__=='__main__':main()
