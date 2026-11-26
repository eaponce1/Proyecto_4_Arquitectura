"""Simula el RTL activo para todos los CSV de acciones aportados, sin tocar flash.

Linux/WSL: python3 tools/probar_todas_acciones.py
Los adicionales se leen del ZIP local, sin descargas. Dos escalas retrospectivas
son escenarios distintos sobre una misma muestra, no observaciones independientes.
"""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor,as_completed
import argparse,csv,hashlib,html,io,json,math,os,shutil,statistics,subprocess,sys,time,zipfile
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'proyecto4/alternativas/tendencia_lenta'))
from modelo_lento import load,run,write_csv
DATA=ROOT/'proyecto4/alternativas/competitiva_definitiva/datos'
BUILD=ROOT/'build/testbench_todas_acciones'
REPORT=ROOT/'resultados_simulacion/testbench_todas_acciones'
def sha(raw):return hashlib.sha256(raw).hexdigest()
def readcsv(raw):return list(csv.DictReader(io.StringIO(raw.decode('utf-8-sig'))))
def execute(args,log):
    start=time.perf_counter()
    p=subprocess.run([str(a) for a in args],cwd=ROOT,capture_output=True,text=True)
    log.write_text(p.stdout+p.stderr+f'\nSalida={p.returncode}; segundos={time.perf_counter()-start:.3f}\n',encoding='utf-8')
    if p.returncode:raise RuntimeError(f'{log.relative_to(ROOT)}: '+(p.stdout+p.stderr)[-1200:])
    return p.stdout
def inputs(zip_path):
    cases=[]
    for path in sorted(DATA.glob('*.csv')):
        p=load(path);assert len(p)==20000
        cases.append(dict(id=path.stem,grupo='practica',escala='original',precios=p,filas_originales=len(p),
            origen=path.relative_to(ROOT).as_posix(),sha256_original=sha(path.read_bytes())))
    assert len(cases)==8
    with zipfile.ZipFile(zip_path) as z:
        names=sorted(n for n in z.namelist() if n.endswith('.csv') and
            ('/momentum_lento/datos_reales/' in n or '/momentum_lento/datos_reservados/' in n))
        if not names:raise ValueError('ZIP sin los CSV adicionales de momentum_lento')
        for name in names:
            raw=z.read(name);rows=readcsv(raw)
            assert rows and 'close' in rows[0],name
            values=[float(r['close']) for r in rows[:20000]]
            assert all(math.isfinite(x) and x>0 for x in values),name
            lo,hi=min(values),max(values)
            for scale in ('prop','afin'):
                prices=[max(1,round(x*255/hi)) for x in values] if scale=='prop' else [
                    round(100+(x-lo)*155/(hi-lo)) if hi>lo else 100 for x in values]
                assert all(1<=p<=255 for p in prices)
                cases.append(dict(id=Path(name).stem+'_'+scale,grupo='adicional_zip',escala=scale,precios=prices,
                    filas_originales=len(rows),origen=name,sha256_original=sha(raw)))
    assert len({c['id'] for c in cases})==len(cases)
    return cases
def compile_tb(period,sources,ticks):
    cells=Path('/mnt/c/Tools/oss-cad-suite/share/yosys/ice40/cells_sim.v')
    if not cells.exists():cells=Path(shutil.which('yosys')).resolve().parents[1]/'share/yosys/ice40/cells_sim.v'
    tool=os.environ.get('POCH_VERILATOR','verilator')
    obj=Path('/tmp')/f'pochoco_todas_acciones_{period}_{ticks}'
    execute([tool,'--binary','--timing','--assert','--language','1800-2017','-DNO_ICE40_DEFAULT_ASSIGNMENTS',
        '-Wno-fatal','--top-module','tb_todas_acciones','--Mdir',obj,'-j','2',f'-GPERIODO_NS={period}',f'-GTICKS={ticks}',
        ROOT/'tb/tb_todas_acciones.sv',ROOT/'proyecto4/alternativas/candidata_final/tb/tb_candidata.sv',
        *sources,cells],BUILD/f'compilacion_{ticks}.log')
    return obj/'Vtb_todas_acciones'
def test(case,exe,period):
    folder=BUILD/case['id'];folder.mkdir(exist_ok=True)
    prices=case['precios'];metrics,expected=run(prices,trace=True)
    write_csv(folder/'entrada.csv',[dict(tick=i,precio=p) for i,p in enumerate(prices)])
    for filename,key in [('precios','precio'),('miso','miso'),('escrituras','decision')]:
        (folder/(filename+'.hex')).write_text(''.join(f'{r[key]:02x}\n' for r in expected))
    trace=folder/'rtl.csv';log=folder/'simulacion.log'
    result=dict(serie=case['id'],grupo=case['grupo'],escala=case['escala'],ticks=len(prices),periodo_ns=period,
        estado='FAIL',discrepancias=0,**metrics,primer_compra=-1,primer_venta=-1,ciclos_max=0,us_max=0.,
        margen_us=0.,origen=case['origen'],sha256_original=case['sha256_original'],
        sha256_precios=sha(bytes(prices)),filas_originales=case['filas_originales'],
        log=log.relative_to(ROOT).as_posix(),traza=trace.relative_to(ROOT).as_posix())
    discrepancies=[]
    try:
        # Sin cartera empaquetada de 8 bits: se comprueban registros de 32 bits
        # dentro del banco y contabilidad completa del CSV, incluso >255 acciones.
        output=execute([exe,f'+vectores={folder.as_posix()}',f'+metricas={trace.as_posix()}','+progreso=5000'],log)
        assert f'PASS {len(prices)} MISO frente a Python' in output,'Banco no completo'
        with trace.open(newline='') as f:actual=list(csv.DictReader(f))
        assert len(actual)==len(expected)==len(prices)
        for a,b in zip(actual,expected,strict=True):
            pairs=[('tick','tick'),('precio','precio'),('fill','cantidad_ejecutada'),('caja','caja'),
                ('acciones','acciones'),('patrimonio','patrimonio'),('comisiones_acum','comisiones_acum')]
            for field,key in pairs:
                if int(a[field])!=b[key]:discrepancies.append(dict(serie=case['id'],tick=b['tick'],campo=field,observado=a[field],esperado=b[key]))
            for field,key in [('miso_hex','miso'),('decision_hex','decision')]:
                if int(a[field],16)!=b[key]:discrepancies.append(dict(serie=case['id'],tick=b['tick'],campo=field,observado=a[field],esperado=b[key]))
        assert not discrepancies,'Diferencias RTL/modelo'
        result.update(estado='PASS',ciclos_max=max(int(r['ciclos']) for r in actual))
        result['us_max']=result['ciclos_max']*.08
        result['margen_us']=period/1000-9.5-.24-result['us_max']
        assert result['margen_us']>0,'Sin margen de respuesta'
        for action,field in [(1,'primer_compra'),(2,'primer_venta')]:
            result[field]=next((int(r['tick']) for r in actual if int(r['fill'])>0 and int(r['miso_hex'],16)>>6==action),-1)
        result['sha256_traza']=sha(trace.read_bytes())
        write_csv(folder/'operaciones.csv',[dict(tick=r['tick'],precio=r['precio'],
            tipo='compra' if r['miso']>>6==1 else 'venta',cantidad=r['cantidad_ejecutada'],caja=r['caja'],
            acciones=r['acciones'],patrimonio=r['patrimonio'],comision=r['comision']) for r in expected if r['cantidad_ejecutada']],
            fields=['tick','precio','tipo','cantidad','caja','acciones','patrimonio','comision'])
    except Exception as e:result.update(estado='FAIL',error=str(e))
    result['discrepancias']=len(discrepancies)
    write_csv(folder/'discrepancias.csv',discrepancies,fields=['serie','tick','campo','observado','esperado'])
    (folder/'resumen.json').write_text(json.dumps(result,indent=2,ensure_ascii=False),encoding='utf-8')
    print(f"{result['estado']} {case['id']}: ${metrics['patrimonio']} vs ${metrics['mantener_oficial']}; compras={metrics['compras']} ventas={metrics['ventas']}",flush=True)
    return result,discrepancies
def render(results,meta):
    REPORT.mkdir(parents=True,exist_ok=True)
    fields=['serie','grupo','escala','estado','ticks','patrimonio','mantener_oficial','ventaja','compras','ventas','comisiones',
        'drawdown_pct','primer_compra','primer_venta','ciclos_max','us_max','margen_us','discrepancias']
    write_csv(REPORT/'resumen.csv',[{k:r[k] for k in fields} for r in results])
    groups=[]
    for label,select in [('Ocho conocidas',lambda r:r['grupo']=='practica'),('ZIP proporcional',lambda r:r['escala']=='prop'),('ZIP afin',lambda r:r['escala']=='afin')]:
        rows=[r for r in results if select(r)]
        groups.append(dict(grupo=label,casos=len(rows),pass_rtl=sum(r['estado']=='PASS' for r in rows),
            ventajas=sum(r['ventaja']>0 for r in rows),con_ganancia=sum(r['patrimonio']>10000 for r in rows),
            sin_ordenes=sum(r['ordenes']==0 for r in rows),media=statistics.mean(r['patrimonio'] for r in rows),
            peor=min(r['patrimonio'] for r in rows),dd_max=max(r['drawdown_pct'] for r in rows)))
    meta.update(grupos=groups,resultados=results)
    (REPORT/'resumen.json').write_text(json.dumps(meta,indent=2,ensure_ascii=False),encoding='utf-8')
    lines=['# Testbench de todas las acciones','',
        f"RTL activo: {meta['sha256_bin']}. Periodo: {meta['periodo_ns']/1000:g} us. Reinicio independiente por escenario.",'',
        f"**{sum(r['estado']=='PASS' for r in results)}/{len(results)} PASS; {sum(r['ticks'] for r in results if r['estado']=='PASS'):,} ticks completos; {sum(r['discrepancias'] for r in results)} discrepancias registradas.**",'',
        'La prueba simula Espino, firmware y SPI; no lee la FPGA fisica. El usuario reporto haberla reprogramado, pero no aporto una traza de la maestra para cotejar esta sesion.','',
        '| Grupo | Casos | PASS | Supera mantener | Con ganancia | Sin ordenes | Media | Peor | DD maximo |',
        '|---|---:|---:|---:|---:|---:|---:|---:|---:|']
    for g in groups:lines.append(f"| {g['grupo']} | {g['casos']} | {g['pass_rtl']} | {g['ventajas']} | {g['con_ganancia']} | {g['sin_ordenes']} | ${g['media']:.2f} | ${g['peor']} | {g['dd_max']:.2f}% |")
    lines+=['','## Interpretacion','',
        'PASS acredita coincidencia tecnica y plazo de respuesta, no rentabilidad. No operar mantiene $10.000. Comprar y mantener es la referencia ideal del curso. Las comisiones se aplican solo a ejecuciones positivas.',
        'Las dos escalas de cada CSV adicional no son muestras independientes. Se utilizan hasta 20.000 precios; si un archivo tiene menos, se prueban todos sus datos sin rellenar ni repetir precios. GOOGL 2021 tiene 18.844 ticks y DIS 2022 tiene 19.966: no equivalen a rondas completas de 20.000. Las filas originales y utilizadas se documentan en resumen.json. La escala proporcional es round(precio*255/max), minimo 1; la afin lleva minimo a 100 y maximo a 255. Ambas usan extremos de la muestra como preprocesamiento retrospectivo; no acreditan una normalizacion causal en vivo. La procedencia de estos CSV del ZIP no se verifico externamente.',
        'Se comparan MISO, DECISION, caja, inventario, fills, comisiones y patrimonio por tick; el banco verifica una recepcion y decision por precio, SUM10, registros de CPU, reset y deadline. Verilator usa dos estados y complementa los chequeos Icarus previos.',
        '','## Todos los escenarios','',
        '| Serie | Escala | RTL | Trader | Mantener | Ventaja | Compras | Ventas | DD % | Primera compra |',
        '|---|---|---|---:|---:|---:|---:|---:|---:|---:|']
    for r in results:lines.append(f"| {r['serie']} | {r['escala']} | {r['estado']} | {r['patrimonio']} | {r['mantener_oficial']} | {r['ventaja']} | {r['compras']} | {r['ventas']} | {r['drawdown_pct']:.2f} | {r['primer_compra']} |")
    lines+=['','Los ticks empiezan en cero; -1 significa que no hubo ejecucion de ese tipo. CSV de resultados junto a este archivo. Trazas por tick, operaciones, vectores y logs en build/testbench_todas_acciones/. No se cambia ni se programa competition.bin.']
    (REPORT/'INFORME.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    headers=['Serie','Escala','RTL','Trader','Mantener','Ventaja','Compras','Ventas','DD %','Primer compra','Max us']
    body=[]
    for r in results:
        vals=[r['serie'],r['escala'],r['estado'],r['patrimonio'],r['mantener_oficial'],r['ventaja'],r['compras'],r['ventas'],f"{r['drawdown_pct']:.2f}",r['primer_compra'],f"{r['us_max']:.2f}"]
        body.append('<tr>'+''.join('<td>'+html.escape(str(v))+'</td>' for v in vals)+'</tr>')
    cards=''.join(f"<p><b>{html.escape(g['grupo'])}</b>: {g['pass_rtl']}/{g['casos']} PASS, supera mantener {g['ventajas']}/{g['casos']}; media ${g['media']:.2f}; peor ${g['peor']}; sin órdenes {g['sin_ordenes']}.</p>" for g in groups)
    page='''<!doctype html><html lang="es"><meta charset="utf-8"><title>Testbench de todas las acciones</title>
<style>body{font:16px system-ui;margin:30px;color:#182338}table{border-collapse:collapse;font-size:14px}td,th{padding:8px;border-bottom:1px solid #ddd;text-align:right}td:first-child{text-align:left}th{background:#e8eef6;position:sticky;top:0}input{padding:10px;width:320px}.note{background:#fff0cd;padding:16px}</style>
<h1>Testbench de todas las acciones</h1>'''+cards+'''
<p class="note">Simulación del RTL y firmware activos, a 100 µs por tick; no es medición de la placa. PASS indica coincidencia técnica, no ganancia. Las escalas adicionales comparten los mismos CSV y usan normalización retrospectiva. Consulta INFORME.md para el alcance y las limitaciones.</p>
<p><a href="resumen.csv">Abrir CSV</a> · <a href="INFORME.md">Informe completo</a></p>
<input id="buscar" placeholder="Filtrar por acción o escala" aria-label="Filtrar"><table><thead><tr>'''+''.join('<th>'+h+'</th>' for h in headers)+'</tr></thead><tbody>'+''.join(body)+'''</tbody></table>
<script>document.getElementById('buscar').addEventListener('input',e=>{const q=e.target.value.toLowerCase();document.querySelectorAll('tbody tr').forEach(r=>r.hidden=!r.textContent.toLowerCase().includes(q))})</script></html>'''
    (REPORT/'ABRIR_RESULTADOS.html').write_text(page,encoding='utf-8')
    print('\nINFORME:',REPORT/'ABRIR_RESULTADOS.html',flush=True)
def main():
    parser=argparse.ArgumentParser();parser.add_argument('--zip',type=Path,default=ROOT.parents[1]/'proyecto4.zip')
    parser.add_argument('--jobs',type=int,default=2);parser.add_argument('--periodo-ns',type=int,default=100000)
    args=parser.parse_args();assert args.jobs>=1 and args.periodo_ns>=40000
    sys.path.insert(0,str(ROOT/'tools'));import trader
    active=trader.verify();start=time.time()
    BUILD.mkdir(parents=True,exist_ok=True)
    sources=trader.sources();tb=[ROOT/'tb/tb_todas_acciones.sv',ROOT/'proyecto4/alternativas/candidata_final/tb/tb_candidata.sv']
    signature={p.relative_to(ROOT).as_posix():sha(p.read_bytes()) for p in [*sources,*tb,ROOT/'sw/trade.hex',ROOT/'tools/probar_todas_acciones.py']}
    cases=inputs(args.zip);print(f'ESCENARIOS {len(cases)}; {sum(len(c["precios"]) for c in cases)} ticks; {args.jobs} simulaciones concurrentes',flush=True)
    executables={n:compile_tb(args.periodo_ns,sources,n) for n in sorted({len(c['precios']) for c in cases})}
    results=[];discrepancies=[]
    with ThreadPoolExecutor(max_workers=args.jobs) as pool:
        futures=[pool.submit(test,c,executables[len(c['precios'])],args.periodo_ns) for c in cases]
        for future in as_completed(futures):
            r,d=future.result();results.append(r);discrepancies+=d
    results.sort(key=lambda r:(r['grupo']!='practica',r['escala'],r['serie']))
    for p,h in signature.items():assert sha((ROOT/p).read_bytes())==h,'Fuentes cambiaron durante la prueba'
    assert sha((ROOT/'competition.bin').read_bytes())==active['sha256_bin']
    write_csv(BUILD/'discrepancias.csv',discrepancies,fields=['serie','tick','campo','observado','esperado'])
    meta=dict(modo='SIMULACION_RTL_NO_TELEMETRIA',sha256_bin=active['sha256_bin'],sha256_hex=active['sha256_hex'],
        politica=active['politica'],periodo_ns=args.periodo_ns,fuentes=signature,sha256_zip=sha(args.zip.read_bytes()),
        segundos=time.time()-start,escenarios=len(cases),fuentes_csv=8+(len(cases)-8)//2)
    render(results,meta)
    assert all(r['estado']=='PASS' for r in results),'Revisar fallos en resumen y logs'
if __name__=='__main__':main()
