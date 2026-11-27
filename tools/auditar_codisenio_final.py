"""Coteja las 640000 filas archivadas contra modelo y precios originales."""
from pathlib import Path
import csv,gzip,hashlib,io,json,math,re,sys
import trader
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'proyecto4/alternativas/tendencia_lenta'))
from modelo_lento import run,load
OUT=ROOT/'docs/evidencia_codisenio_final'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    trader.verify()
    data=json.loads((OUT/'equivalencia_perfil.json').read_text());summary=json.loads((OUT/'resumen.json').read_text())
    assert len(data['series'])==32 and summary['bin_sha256']==sha(ROOT/'competition.bin')
    for path,h in data['fuentes'].items():assert sha(ROOT/path)==h,path
    for path,item in summary['archivos'].items():assert sha(ROOT/path)==item['sha256'],path
    expected={};total=0;seen=set()
    keys=['kernel_ciclos','kernel_ic','kernel_lecturas','kernel_escrituras','rx_ciclos','cartera_ciclos','decision_ciclos','alu_kernel']
    aggregate={}
    for case in data['series']:
        v=case['variante'];name=case['serie'];assert (v,name) not in seen;seen.add((v,name))
        path=ROOT/case['archivo'];assert sha(path)==case['sha256_gz']
        raw=gzip.decompress(path.read_bytes());assert hashlib.sha256(raw).hexdigest()==case['sha256_traza']
        rows=list(csv.DictReader(io.StringIO(raw.decode())))
        if name not in expected:expected[name]=run(load(ROOT/'proyecto4/alternativas/competitiva_definitiva/datos'/(name+'.csv')),trace=True)[1]
        ref=expected[name];assert len(rows)==len(ref)==case['ticks']==20000
        for a,b in zip(rows,ref,strict=True):
            for x,y in [('tick','tick'),('precio','precio'),('fill','cantidad_ejecutada'),('caja','caja'),('acciones','acciones'),('patrimonio','patrimonio'),('comisiones_acum','comisiones_acum')]:assert int(a[x])==b[y],(v,name,b['tick'],x)
            assert int(a['miso_hex'],16)==b['miso'] and int(a['decision_hex'],16)==b['decision']
            assert sum(int(a[k]) for k in ('rx_ciclos','cartera_ciclos','kernel_ciclos','decision_ciclos'))==int(a['ciclos'])
        for k in keys:assert math.isclose(sum(int(r[k]) for r in rows)/len(rows),case['regiones'][k])
        for k,out in [('ciclos','ciclos_media'),('ic','ic_media')]:assert math.isclose(sum(int(r[k]) for r in rows)/len(rows),case[out])
        assert max(int(r['ciclos']) for r in rows)==case['ciclos_max']
        assert math.isclose(sum(int(r['ciclos']) for r in rows)/sum(int(r['ic']) for r in rows),case['cpi'])
        aggregate.setdefault(v,[]).append(case);total+=len(rows)
    assert total==640000 and len(expected)==8 and all(len(x)==8 for x in aggregate.values())
    hw={r['variante']:r for r in json.loads((OUT/'hardware.json').read_text())}
    for r in summary['variantes']:
        v=r['variante'];assert math.isclose(r['ciclos'],sum(x['ciclos_media'] for x in aggregate[v])/8)
        assert math.isclose(r['speedup_medido'],summary['variantes'][0]['ciclos']/r['ciclos'])
        net=gzip.decompress((OUT/'implantacion'/v/'sintesis.json.gz').read_bytes())
        assert hashlib.sha256(net).hexdigest()==hw[v]['sintesis_sha256']
        cells=json.loads(net)['modules']['trade_spi_externo']['cells'].values()
        assert sum(c['type']=='SB_LUT4' for c in cells)==r['lut4']
        assert sum(c['type']=='SB_RAM40_4K' for c in cells)==r['bram']
        log=(OUT/'implantacion'/v/'nextpnr.log').read_text()
        assert int(re.search(r'ICESTORM_LC:\s*(\d+)',log)[1])==r['lc']
        if v=='custom0':assert r['lc']>1280 and r['ruta']=='FAIL' and r['fmax_soc_MHz'] is None
        else:
            assert r['lc']<=1280 and r['ruta']=='PASS' and r['fmax_soc_MHz']>=12.5
            timing=json.loads((OUT/'implantacion'/v/'timing.json').read_text())
            assert timing['fmax']['clk_soc']['achieved']==r['fmax_soc_MHz']
    for unit in json.loads((OUT/'unidades.json').read_text()):
        assert unit['estado']=='PASS'
        for path,h in unit.get('fuentes',{}).items():assert sha(ROOT/path)==h,path
    (OUT/'auditoria.json').write_text(json.dumps(dict(estado='PASS',ticks=total,series=32,variantes=4,modelo_y_precios=True,regiones=True,sintesis=True,bin_sin_cambios=True),indent=2)+'\n')
    print('PASS co-diseno final: 4 variantes, 32 series, 640000 ticks; custom0 no cabe en HX1K')
if __name__=='__main__':main()
