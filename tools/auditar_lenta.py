"""Audita la imagen lenta y archiva trazas RTL verificables sin acceso a FPGA."""
from pathlib import Path
import argparse,csv,gzip,hashlib,io,json,sys
import trader as t
from modelo_lento import load,run,frozen
ROOT=t.ROOT;DEST=ROOT/'docs/evidencia_tendencia_lenta'
def sha(raw):return hashlib.sha256(raw).hexdigest()
def check_sources(record):
    for path,h in record['fuentes'].items():assert t.sha(ROOT/path)==h,path
def main():
    parser=argparse.ArgumentParser();parser.add_argument('--archivar',action='store_true');args=parser.parse_args()
    active=t.verify();assert active['politica']=='tendencia_lenta_128_5pct'
    assert active['prueba_fisica'] in ('PENDIENTE_NUEVA_IMAGEN','REPROGRAMACION_REPORTADA_POR_USUARIO')
    if active['prueba_fisica']=='REPROGRAMACION_REPORTADA_POR_USUARIO':
        physical=json.loads((ROOT/'docs/evidencia_fisica/reprogramacion_tendencia_lenta.json').read_text(encoding='utf-8'))
        assert physical['estado']==active['prueba_fisica'] and physical['sha256_bin_local']==active['sha256_bin']
    full=json.loads((t.OUT/'equivalencia_verilator.json').read_text());check_sources(full)
    assert sum(r['ticks'] for r in full['series'])==160000 and all(r['discrepancias']==0 for r in full['series'])
    official=json.loads((t.OUT/'bancos_oficiales.json').read_text())
    assert any(s['nombre']=='rtl_estres' and s['ticks']==936 and s['discrepancias']==0 for s in active['tests'])
    assert len(official)==2
    for r in official:
        assert r['fuentes']==t.signature() and r['criterios']=='4/4' and r['discrepancias']==0
    long=[]
    for period in (1000000,10000000):
        record=json.loads((t.OUT/f'equivalencia_396_{period}.json').read_text());check_sources(record)
        assert len(record['series'])==1 and record['series'][0]['ticks']==396 and record['series'][0]['discrepancias']==0
        long+=record['series']
    rv=json.loads((t.ALT/'resultados/equivalencia_rv32e.json').read_text())
    assert rv['sha256_hex']==active['sha256_hex'] and rv['ticks_practica']==160000 and rv['discrepancias']==0
    tests=[]
    for kind in ('netlist','bin'):
        r=json.loads((t.OUT/f'validacion_{kind}.json').read_text())
        if kind=='netlist':assert r['sha256_netlist']==t.sha(t.OUT/'netlist.v')
        else:
            decoded=t.OUT/'bin_desempaquetado.v'
            if decoded.exists():assert r['sha256_netlist']==t.sha(decoded)
        assert {s['setup_ns'] for s in r['tests'] if 'setup_ns' in s}=={20,40,1000}
        for s in r['tests']:
            assert s['ticks']==396 and s['discrepancias']==0
            if 'log' in s:
                text=(ROOT/s['log']).read_text()
                assert 'PASS' in text and 'Salida=0' in text
        tests+=r['tests']
    traces=[]
    for series in full['series']:
        name=series['serie'];target=DEST/'trazas_rtl'/f'{name}.csv.gz'
        if args.archivar:
            raw=(t.OUT/'verilator'/f'{name}.csv').read_bytes()
            target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(gzip.compress(raw,mtime=0))
        raw=gzip.decompress(target.read_bytes())
        rows=list(csv.DictReader(io.StringIO(raw.decode())))
        _,expected=run(load(t.OLD/'datos'/f'{name}.csv'),frozen(),True)
        assert len(rows)==len(expected)==20000
        for a,b in zip(rows,expected,strict=True):
            for field,key in [('tick','tick'),('precio','precio'),('fill','cantidad_ejecutada'),('caja','caja'),
                ('acciones','acciones'),('patrimonio','patrimonio'),('comisiones_acum','comisiones_acum')]:assert int(a[field])==b[key]
            assert int(a['miso_hex'],16)==b['miso'] and int(a['decision_hex'],16)==b['decision']
        traces.append(dict(serie=name,ticks=len(rows),ruta=target.relative_to(ROOT).as_posix(),sha256_gz=t.sha(target),sha256_csv=sha(raw)))
    if args.archivar:
        docs=[*t.sources(),ROOT/'sw/trade.s',ROOT/'sw/trade.hex',ROOT/'tb/tb_spi_margen.sv',
            ROOT/'proyecto4/alternativas/candidata_final/tb/tb_candidata.sv',
            ROOT/'tools/validar_puertas.py',ROOT/'tools/validar_activo_verilator.py',ROOT/'tools/validar_oficial.py']
        report=dict(politica=active['politica'],sha256_bin=active['sha256_bin'],sha256_hex=active['sha256_hex'],
            prueba_fisica=active['prueba_fisica'],fuentes={p.relative_to(ROOT).as_posix():t.sha(p) for p in docs},
            rtl=traces,rtl_integracion=active['tests'],integracion_cadencias_largas=long,puertas=tests,
            area=dict(lc=active['lc'],bram=active['bram']),
            limites=['Cadencias largas: integracion de 396 ticks por periodo, no ocho series completas',
                'BIN reconstruido: retardo funcional uniforme de 1 ns; no simulacion de timing fisico',
                'La prueba fisica anterior corresponde solo al respaldo Momentum32 5e1579ca',
                'Rentabilidad secreta y resultados oficiales no demostrados'])
        (DEST/'validacion_integral.json').write_text(json.dumps(report,indent=2,ensure_ascii=False),encoding='utf-8')
    report=json.loads((DEST/'validacion_integral.json').read_text(encoding='utf-8'));check_sources(report)
    assert report['sha256_bin']==active['sha256_bin'] and report['rtl']==traces
    assert report['rtl_integracion']==active['tests']
    print('PASS auditoria lenta: 160000 ticks archivados, 4/4 por banco, tres cadencias de integracion y puertas;',active['prueba_fisica'])
if __name__=='__main__':main()
