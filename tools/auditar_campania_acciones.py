"""Archiva/audita los 78 CSV RTL; funciona en clones sin el ZIP de entrada."""
from pathlib import Path
import argparse,csv,gzip,hashlib,io,json,sys
import trader
ROOT=trader.ROOT
REPORT=ROOT/'resultados_simulacion/testbench_todas_acciones'
ARCHIVE=ROOT/'docs/evidencia_todas_acciones'
sys.path.insert(0,str(trader.ALT))
from modelo_lento import run
def sha(raw):return hashlib.sha256(raw).hexdigest()
def main():
    p=argparse.ArgumentParser();p.add_argument('--archivar',action='store_true');args=p.parse_args()
    active=trader.verify();data=json.loads((REPORT/'resumen.json').read_text(encoding='utf-8'))
    assert data['sha256_bin']==active['sha256_bin'] and data['sha256_hex']==active['sha256_hex']
    for path,h in data['fuentes'].items():assert sha((ROOT/path).read_bytes())==h,path
    assert len(data['resultados'])==78 and len({r['serie'] for r in data['resultados']})==78
    total=orders=0;entries=[]
    for r in data['resultados']:
        assert r['estado']=='PASS' and r['discrepancias']==0 and r['periodo_ns']==100000
        target=ARCHIVE/'trazas_rtl'/(r['serie']+'.csv.gz')
        if args.archivar:
            raw=(ROOT/r['traza']).read_bytes()
            assert sha(raw)==r['sha256_traza']
            target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(gzip.compress(raw,mtime=0))
        raw=gzip.decompress(target.read_bytes());assert sha(raw)==r['sha256_traza']
        rows=list(csv.DictReader(io.StringIO(raw.decode())))
        prices=[int(x['precio']) for x in rows]
        assert len(rows)==r['ticks'] and sha(bytes(prices))==r['sha256_precios']
        metrics,expected=run(prices,trace=True)
        for key in ('patrimonio','mantener_oficial','compras','ventas','comisiones','ordenes','drawdown'):
            assert metrics[key]==r[key],(r['serie'],key)
        for a,b in zip(rows,expected,strict=True):
            for x,y in [('tick','tick'),('caja','caja'),('acciones','acciones'),('fill','cantidad_ejecutada'),
                ('patrimonio','patrimonio'),('comisiones_acum','comisiones_acum')]:assert int(a[x])==b[y],(r['serie'],b['tick'],x)
            assert int(a['miso_hex'],16)==b['miso'] and int(a['decision_hex'],16)==b['decision']
        assert max(int(a['ciclos']) for a in rows)==r['ciclos_max']
        total+=len(rows);orders+=metrics['ordenes']
        entries.append(dict(serie=r['serie'],ruta=target.relative_to(ROOT).as_posix(),sha256_gz=sha(target.read_bytes()),sha256_csv=sha(raw),ticks=len(rows)))
    assert total==1557620 and orders==792
    assert [g['casos'] for g in data['grupos']]==[8,35,35]
    if args.archivar:
        manifest=dict(sha256_bin=active['sha256_bin'],sha256_hex=active['sha256_hex'],
            sha256_resumen=sha((REPORT/'resumen.json').read_bytes()),ticks=total,ordenes=orders,
            procedencia='CSV generados por el testbench RTL; entradas de los 43 CSV documentados en resumen.json',
            limites='Simulacion a 100 us. Dos escalas retrospectivas de los mismos 35 CSV adicionales; no son muestras independientes.',trazas=entries)
        (ARCHIVE/'manifest.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False),encoding='utf-8')
    manifest=json.loads((ARCHIVE/'manifest.json').read_text(encoding='utf-8'))
    assert manifest['trazas']==entries and manifest['sha256_resumen']==sha((REPORT/'resumen.json').read_bytes())
    print('PASS 78/78 trazas archivadas; 1557620 ticks, 428 compras, 364 ventas; modelo/RTL/firmware vigentes')
if __name__=='__main__':main()
