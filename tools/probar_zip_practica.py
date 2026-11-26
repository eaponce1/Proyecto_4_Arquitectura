"""Ejecuta SPI/CPU/RTL actual leyendo directamente el ZIP de practica aportado."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor,as_completed
from datetime import datetime,timezone
import argparse,csv,gzip,hashlib,html,io,json,time,zipfile
import probar_todas_acciones as bank
import trader
ROOT=bank.ROOT
OUT=ROOT/'resultados_simulacion/testbench_zip_practica'
def sha(raw):return hashlib.sha256(raw).hexdigest()
def main():
    p=argparse.ArgumentParser();p.add_argument('--zip',type=Path,required=True)
    p.add_argument('--jobs',type=int,default=2);p.add_argument('--periodo-ns',type=int,default=100000)
    args=p.parse_args();assert args.jobs>0 and args.periodo_ns>=40000
    active=trader.verify();started=datetime.now(timezone.utc).isoformat();start=time.perf_counter()
    bank.BUILD=ROOT/'build/testbench_zip_practica';bank.BUILD.mkdir(parents=True,exist_ok=True)
    OUT.mkdir(parents=True,exist_ok=True)
    sources=trader.sources()
    files=[*sources,ROOT/'sw/trade.s',ROOT/'sw/trade.hex',ROOT/'proyecto4/alternativas/tendencia_lenta/modelo_lento.py',
        ROOT/'tb/tb_todas_acciones.sv',ROOT/'proyecto4/alternativas/candidata_final/tb/tb_candidata.sv',
        ROOT/'tools/probar_todas_acciones.py',ROOT/'tools/probar_zip_practica.py']
    signature={f.relative_to(ROOT).as_posix():sha(f.read_bytes()) for f in files}
    rawzip=args.zip.read_bytes();cases=[];origins=[]
    with zipfile.ZipFile(io.BytesIO(rawzip)) as z:
        names=sorted(n for n in z.namelist() if n.lower().endswith('.csv') and not n.startswith('__MACOSX/'))
        assert names,'El ZIP no contiene CSV'
        for name in names:
            raw=z.read(name);rows=list(csv.reader(io.StringIO(raw.decode('utf-8-sig'))))
            assert len(rows[0])==2,name
            assert [int(r[0]) for r in rows[1:]]==list(range(len(rows)-1)),name
            prices=[int(r[1]) for r in rows[1:]]
            assert prices and all(1<=v<=255 for v in prices),name
            canonical=bank.DATA/Path(name).name
            origins.append(dict(archivo=name,sha256_csv=sha(raw),ticks=len(prices),
                identico_a_canonico=canonical.exists() and canonical.read_bytes()==raw))
            cases.append(dict(id=Path(name).stem,grupo='zip_practica',escala='original_sin_transformacion',
                precios=prices,filas_originales=len(prices),origen=name,sha256_original=sha(raw)))
    assert len({c['id'] for c in cases})==len(cases),'Nombres CSV duplicados'
    print(f'ZIP {args.zip.name}: {len(cases)} series, {sum(len(c["precios"]) for c in cases)} ticks, sin normalizar',flush=True)
    executables={n:bank.compile_tb(args.periodo_ns,sources,n) for n in sorted({len(c['precios']) for c in cases})}
    results=[];differences=[]
    with ThreadPoolExecutor(max_workers=args.jobs) as pool:
        futures=[pool.submit(bank.test,c,executables[len(c['precios'])],args.periodo_ns) for c in cases]
        for future in as_completed(futures):
            r,d=future.result();results.append(r);differences+=d
    results.sort(key=lambda r:r['serie'])
    for path,h in signature.items():assert sha((ROOT/path).read_bytes())==h,'Fuentes modificadas durante el test'
    assert sha((ROOT/'competition.bin').read_bytes())==active['sha256_bin']
    archive=OUT/'trazas_rtl';archive.mkdir(exist_ok=True)
    for r in results:
        if r['estado']=='PASS':
            raw=(ROOT/r['traza']).read_bytes();assert sha(raw)==r['sha256_traza']
            target=archive/(r['serie']+'.csv.gz');target.write_bytes(gzip.compress(raw,mtime=0))
            r['traza_archivada']=target.relative_to(ROOT).as_posix();r['sha256_gz']=sha(target.read_bytes())
    meta=dict(inicio_utc=started,fin_utc=datetime.now(timezone.utc).isoformat(),segundos=time.perf_counter()-start,
        tipo='NUEVA_EJECUCION_RTL_DESDE_ZIP',zip_nombre=args.zip.name,zip_sha256=sha(rawzip),
        sha256_bin=active['sha256_bin'],sha256_hex=active['sha256_hex'],politica=active['politica'],
        periodo_ns=args.periodo_ns,fuentes=signature,archivos=origins,resultados=results,
        medicion='Simulacion del procesador, SPI y firmware actuales; no telemetria fisica',
        ticks=sum(r['ticks'] for r in results if r['estado']=='PASS'),discrepancias=len(differences),
        compras=sum(r['compras'] for r in results),ventas=sum(r['ventas'] for r in results),
        ventajas=sum(r['ventaja']>0 for r in results))
    (OUT/'resumen.json').write_text(json.dumps(meta,indent=2,ensure_ascii=False),encoding='utf-8')
    fields=['serie','estado','ticks','patrimonio','mantener_oficial','ventaja','compras','ventas','comisiones',
        'drawdown_pct','primer_compra','primer_venta','us_max','margen_us','discrepancias']
    bank.write_csv(OUT/'resumen.csv',[{k:r[k] for k in fields} for r in results])
    bank.write_csv(OUT/'discrepancias.csv',differences,fields=['serie','tick','campo','observado','esperado'])
    lines=['# Testbench del ZIP de practica','',f"Entrada: `{args.zip.name}`. SHA-256: `{meta['zip_sha256']}`.",
        f"BIN: `{active['sha256_bin']}`; firmware: tendencia lenta SUM10/128/5%.",
        f"{sum(r['estado']=='PASS' for r in results)}/{len(results)} PASS; {meta['ticks']:,} ticks a {args.periodo_ns/1000:g} us; {len(differences)} discrepancias.",
        '', 'Nueva ejecucion del RTL desde los precios exactos del ZIP, sin normalizar. Cada serie reinicia caja en $10.000 e inventario cero. Comision $5 por orden ejecutada.',
        'El banco comprueba MISO, DECISION, caja, inventario, fills, comisiones, patrimonio, MMIO, SUM10, registros CPU, reset y plazo. Verilator usa dos estados; los chequeos Icarus previos son complementarios.',
        'Los CSV coinciden con los datos de practica existentes segun la comparacion byte por byte en resumen.json. Esta repeticion no constituye datos nuevos ni una prueba fuera de muestra. No es una lectura de la flash ni una traza de la maestra fisica.',
        '', '| Serie | RTL | Trader | Mantener | Ventaja | Compras | Ventas | Comisiones | DD % | Primera compra |',
        '|---|---|---:|---:|---:|---:|---:|---:|---:|---:|']
    for r in results:lines.append(f"| {r['serie']} | {r['estado']} | {r['patrimonio']} | {r['mantener_oficial']} | {r['ventaja']} | {r['compras']} | {r['ventas']} | {r['comisiones']} | {r['drawdown_pct']:.2f} | {r['primer_compra']} |")
    lines+=['', 'Los ticks empiezan en cero; -1 indica ausencia de ejecucion. Una señal se ejecuta al precio de la siguiente trama. D4 registra orden no nula; los demas LED confirman CPU, recepcion y lectura.',
        'Las trazas comprimidas se guardan junto al informe. Vectores, operaciones y logs completos estan en build/testbench_zip_practica/. PASS tecnico no garantiza beneficio financiero.']
    (OUT/'INFORME.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    print('RESULTADOS:',OUT,flush=True)
    assert all(r['estado']=='PASS' for r in results),'Revisar fallos y logs'
if __name__=='__main__':main()
