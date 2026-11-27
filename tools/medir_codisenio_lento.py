"""Linux/WSL: mide las cuatro implementaciones de la misma tendencia lenta."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor,as_completed
import argparse,csv,gzip,hashlib,json,os,re,shutil,statistics,subprocess,sys,time
import trader
from preparar_codisenio_lento import main as prepare
from banco_codisenio_lento import main as prepare_tb
from modelo_lento import load,run,synth,write_csv
ROOT=trader.ROOT;ALT=ROOT/'proyecto4/alternativas/codisenio_lento'
BUILD=ROOT/'build/codisenio_lento';OUT=ROOT/'docs/evidencia_codisenio_final'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def sources(variant):
    base={p.name:p for p in trader.sources()}
    if variant!='mmio':
        if variant in ('software','custom0'):base.pop('pochoco_sma10.v')
        for p in (ALT/variant/'rtl').glob('*.v'):base[p.name]=p
    return [base[p.name] for p in trader.sources() if p.name in base]
def command(args,log):
    log.parent.mkdir(parents=True,exist_ok=True);start=time.perf_counter()
    p=subprocess.run([str(a) for a in args],cwd=ROOT,capture_output=True,text=True)
    log.write_text(p.stdout+p.stderr+f'\nSalida={p.returncode}; segundos={time.perf_counter()-start:.3f}\n',encoding='utf-8')
    if p.returncode:raise RuntimeError(str(log)+'\n'+(p.stdout+p.stderr)[-2200:])
    return p.stdout+p.stderr
def cells():
    path=Path('/mnt/c/Tools/oss-cad-suite/share/yosys/ice40/cells_sim.v')
    return path if path.exists() else Path(shutil.which('yosys')).resolve().parents[1]/'share/yosys/ice40/cells_sim.v'
def compile_tb(variant,smoke):
    v=json.loads((ALT/'variantes.json').read_text())['variantes'][variant]
    ticks=396 if smoke else 20000
    obj=Path('/tmp')/f'pochoco_codisenio_{variant}_{ticks}'
    command([os.environ.get('POCH_VERILATOR','verilator'),'--binary','--timing','--assert',
        '--language','1800-2017','-DNO_ICE40_DEFAULT_ASSIGNMENTS','-Wno-fatal',
        '--top-module','tb_candidata','--Mdir',obj,'-j','2',f'-GTICKS={ticks}','-GPERIODO_NS=100000',
        f'-GPALABRAS_FIRMWARE={v["palabras"]}',f'-GK_START={v["kernel_start"]}',f'-GK_END={v["kernel_end"]}',
        f'-GES_MMIO={int(variant not in ("software","custom0"))}','-GREG_CAJA=15','-GREG_ACCIONES=5',
        '-GARCHIVO_FIRMWARE="'+(ALT/variant/'trade.hex').relative_to(ROOT).as_posix()+'"',
        ALT/'tb_codisenio.sv',*sources(variant),cells()],BUILD/variant/f'compilacion_{ticks}.log')
    return obj/'Vtb_candidata'
def one(variant,name,prices,exe):
    folder=BUILD/variant/name;folder.mkdir(parents=True,exist_ok=True)
    metrics,expected=run(prices,trace=True)
    for file,key in [('precios','precio'),('miso','miso'),('escrituras','decision')]:
        (folder/(file+'.hex')).write_text(''.join(f'{r[key]:02x}\n' for r in expected))
    trace=folder/'ticks.csv'
    output=command([exe,f'+vectores={folder.as_posix()}',f'+metricas={trace.as_posix()}','+progreso=5000'],folder/'simulacion.log')
    assert f'PASS {len(prices)} MISO frente a Python' in output
    with trace.open(newline='') as f:actual=list(csv.DictReader(f))
    assert len(actual)==len(prices)
    for a,b in zip(actual,expected,strict=True):
        for x,y in [('tick','tick'),('precio','precio'),('fill','cantidad_ejecutada'),('caja','caja'),
            ('acciones','acciones'),('patrimonio','patrimonio'),('comisiones_acum','comisiones_acum')]:assert int(a[x])==b[y],(variant,name,b['tick'],x)
        assert int(a['miso_hex'],16)==b['miso'] and int(a['decision_hex'],16)==b['decision']
        assert sum(int(a[x]) for x in ('rx_ciclos','cartera_ciclos','kernel_ciclos','decision_ciclos'))==int(a['ciclos'])
    numbers={k:[int(r[k]) for r in actual] for k in ('ic','ciclos','kernel_ciclos','kernel_ic','kernel_lecturas','kernel_escrituras','rx_ciclos','cartera_ciclos','decision_ciclos','alu_kernel')}
    summary=dict(variante=variant,serie=name,ticks=len(actual),discrepancias=0,**metrics,
        ciclos_media=statistics.mean(numbers['ciclos']),ciclos_max=max(numbers['ciclos']),
        ic_media=statistics.mean(numbers['ic']),ic_max=max(numbers['ic']),cpi=sum(numbers['ciclos'])/sum(numbers['ic']),
        cpi_max=max(int(a['ciclos'])/int(a['ic']) for a in actual),
        regiones={k:statistics.mean(v) for k,v in numbers.items() if k not in ('ic','ciclos')},
        traza=trace.relative_to(ROOT).as_posix(),sha256_traza=sha(trace))
    (folder/'resumen.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
    if len(prices)==20000:
        archive=OUT/'trazas'/variant/(name+'.csv.gz');archive.parent.mkdir(parents=True,exist_ok=True)
        archive.write_bytes(gzip.compress(trace.read_bytes(),mtime=0));summary['archivo']=archive.relative_to(ROOT).as_posix();summary['sha256_gz']=sha(archive)
    print('PASS',variant,name,len(actual),'ticks',summary['ciclos_max'],'ciclos max',flush=True)
    return summary
def simulate(variants,smoke,jobs):
    results=[]
    for v in variants:
        exe=compile_tb(v,smoke)
        data=[('integracion',synth()['integracion_cadencias'])] if smoke else [(p.stem,load(p)) for p in sorted((trader.OLD/'datos').glob('*.csv'))]
        with ThreadPoolExecutor(max_workers=jobs) as pool:
            fs=[pool.submit(one,v,n,p,exe) for n,p in data]
            for f in as_completed(fs):results.append(f.result())
    path=OUT/('smoke.json' if smoke else 'equivalencia_perfil.json');path.parent.mkdir(parents=True,exist_ok=True)
    previous=json.loads(path.read_text()) if path.exists() else dict(series=[],fuentes={})
    previous['series']=[r for r in previous['series'] if r['variante'] not in variants]+results
    previous.update(serie_politica='SUM10/128/5%',reloj_MHz=12.5)
    previous['fuentes'].update({p.relative_to(ROOT).as_posix():sha(p) for v in variants for p in [*sources(v),ALT/v/'trade.s',ALT/v/'trade.hex',ALT/'tb_codisenio.sv']})
    path.write_text(json.dumps(previous,indent=2),encoding='utf-8')
def hardware(variants):
    results=[]
    for v in variants:
        folder=BUILD/v;folder.mkdir(parents=True,exist_ok=True)
        js=folder/'sintesis.json';asc=folder/'ruta.asc';timing=folder/'timing.json'
        names=' '.join('"'+p.relative_to(ROOT).as_posix()+'"' for p in sources(v))
        command(['yosys','-p',f'read_verilog -sv {names}; synth_ice40 -dff -top trade_spi_externo; check -assert; stat; write_json {js.relative_to(ROOT).as_posix()}'],folder/'yosys.log')
        design=json.loads(js.read_text());counts={}
        for c in design['modules']['trade_spi_externo']['cells'].values():counts[c['type']]=counts.get(c['type'],0)+1
        args=['nextpnr-ice40','--hx1k','--package','vq100','--freq','25','--seed','1','--json',js.relative_to(ROOT),
            '--pcf','goboard_trader.pcf','--asc',asc.relative_to(ROOT),'--report',timing.relative_to(ROOT)]
        try:log=command(args,folder/'nextpnr.log');ok=True
        except RuntimeError:log=(folder/'nextpnr.log').read_text();ok=False
        lc=re.search(r'ICESTORM_LC:\s*(\d+)',log);bram=re.search(r'ICESTORM_RAM:\s*(\d+)',log)
        clocks=json.loads(timing.read_text())['fmax'] if ok else {}
        result=dict(variante=v,lut4=counts.get('SB_LUT4',0),bram_sintesis=counts.get('SB_RAM40_4K',0),
            lc=int(lc[1]) if lc else None,bram=int(bram[1]) if bram else None,ruta='PASS' if ok else 'FAIL',
            clocks=clocks,fmax_soc_MHz=clocks.get('clk_soc',{}).get('achieved'),
            sintesis_sha256=sha(js),yosys_log=(folder/'yosys.log').relative_to(ROOT).as_posix(),pnr_log=(folder/'nextpnr.log').relative_to(ROOT).as_posix())
        assert not ok or (result['lc']<=1280 and result['bram']<=16 and result['fmax_soc_MHz']>=12.5)
        results.append(result);print('HARDWARE',result,flush=True)
    OUT.mkdir(parents=True,exist_ok=True);path=OUT/'hardware.json'
    old=json.loads(path.read_text()) if path.exists() else []
    path.write_text(json.dumps([r for r in old if r['variante'] not in variants]+results,indent=2),encoding='utf-8')
def main():
    p=argparse.ArgumentParser();p.add_argument('--fase',choices=['smoke','simular','hardware'],required=True)
    p.add_argument('--variantes',nargs='+',default=['software','custom0','mmio','mmio_scan']);p.add_argument('--jobs',type=int,default=2)
    p.add_argument('--sin-preparar',action='store_true')
    args=p.parse_args();assert all(v in ('software','custom0','mmio','mmio_scan') for v in args.variantes)
    active=trader.verify()
    if not args.sin_preparar:prepare();prepare_tb()
    else:assert json.loads((ALT/'variantes.json').read_text())['bin_activo_sha256']==active['sha256_bin']
    BUILD.mkdir(parents=True,exist_ok=True)
    if args.fase=='hardware':hardware(args.variantes)
    else:simulate(args.variantes,args.fase=='smoke',args.jobs)
    assert sha(ROOT/'competition.bin')==active['sha256_bin'];trader.verify()
if __name__=='__main__':main()
