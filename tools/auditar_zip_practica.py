"""Audita ZIP publicado, firmas y las ocho trazas de su nueva ejecucion RTL."""
from pathlib import Path
import csv,gzip,hashlib,io,json,zipfile
import trader
from modelo_lento import run
ROOT=trader.ROOT
OUT=ROOT/'resultados_simulacion/testbench_zip_practica'
def sha(raw):return hashlib.sha256(raw).hexdigest()
def main():
    active=trader.verify();d=json.loads((OUT/'resumen.json').read_text(encoding='utf-8'))
    assert d['sha256_bin']==active['sha256_bin'] and d['sha256_hex']==active['sha256_hex']
    assert len(d['resultados'])==len(d['archivos'])==8 and d['ticks']==160000 and d['discrepancias']==0
    assert d['compras']==98 and d['ventas']==92 and d['ventajas']==5 and d['periodo_ns']==100000
    for name,h in d['fuentes'].items():assert sha((ROOT/name).read_bytes())==h,name
    zipraw=(ROOT/'docs/referencia/Proyecto_4_Series_Practica_export.zip').read_bytes()
    assert sha(zipraw)==d['zip_sha256']
    files={f['archivo']:f for f in d['archivos']}
    with zipfile.ZipFile(io.BytesIO(zipraw)) as z:
        assert sorted(n for n in z.namelist() if n.endswith('.csv'))==sorted(files)
        for r in d['resultados']:
            name=r['origen'];raw=z.read(name)
            assert r['estado']=='PASS' and r['ticks']==20000 and r['discrepancias']==0
            assert sha(raw)==files[name]['sha256_csv']==r['sha256_original']
            assert raw==(trader.OLD/'datos'/Path(name).name).read_bytes() and files[name]['identico_a_canonico']
            source=list(csv.reader(io.StringIO(raw.decode('utf-8-sig'))))[1:]
            assert [int(row[0]) for row in source]==list(range(20000))
            prices=[int(row[1]) for row in source]
            assert sha(bytes(prices))==r['sha256_precios']
            archive=(ROOT/r['traza_archivada']).read_bytes();assert sha(archive)==r['sha256_gz']
            actual=gzip.decompress(archive);assert sha(actual)==r['sha256_traza']
            actual=list(csv.DictReader(io.StringIO(actual.decode())))
            metrics,expected=run(prices,trace=True);assert len(actual)==20000
            for a,b in zip(actual,expected,strict=True):
                for x,y in [('tick','tick'),('precio','precio'),('caja','caja'),('acciones','acciones'),
                    ('fill','cantidad_ejecutada'),('patrimonio','patrimonio'),('comisiones_acum','comisiones_acum')]:assert int(a[x])==b[y],(r['serie'],b['tick'],x)
                assert int(a['miso_hex'],16)==b['miso'] and int(a['decision_hex'],16)==b['decision']
            for key in ('patrimonio','mantener_oficial','compras','ventas','ordenes','comisiones','drawdown'):
                assert metrics[key]==r[key],(r['serie'],key)
            assert max(int(a['ciclos']) for a in actual)==r['ciclos_max']
    print('PASS ZIP exacto, 8/8 CSV identicos al corpus, 160000 ticks, 98 compras y 92 ventas; fuentes y BIN vigentes')
if __name__=='__main__':main()
