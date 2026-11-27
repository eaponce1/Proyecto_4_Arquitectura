"""Resume mediciones reales; archiva resultados de sintesis sin modificar el BIN."""
from pathlib import Path
import csv,gzip,hashlib,json,shutil,statistics as st
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'docs/evidencia_codisenio_final'
VAR=['software','custom0','mmio','mmio_scan']
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    data=json.loads((OUT/'equivalencia_perfil.json').read_text());hw={r['variante']:r for r in json.loads((OUT/'hardware.json').read_text())}
    assert len(data['series'])==32 and sum(r['ticks'] for r in data['series'])==640000
    rows=[]
    for v in VAR:
        cases=[r for r in data['series'] if r['variante']==v];assert len(cases)==8
        avg=lambda k:st.mean(r[k] for r in cases)
        regions={k:st.mean(r['regiones'][k] for r in cases) for k in cases[0]['regiones']}
        rows.append(dict(variante=v,ticks=sum(r['ticks'] for r in cases),ciclos=avg('ciclos_media'),ciclos_max=max(r['ciclos_max'] for r in cases),ic=avg('ic_media'),cpi=avg('ciclos_media')/avg('ic_media'),tiempo_us=avg('ciclos_media')*.08,tiempo_max_us=max(r['ciclos_max'] for r in cases)*.08,ticks_s=12500000/avg('ciclos_media'),**regions,**{k:hw[v][k] for k in ('lut4','lc','bram','fmax_soc_MHz','ruta')}))
    base=rows[0]
    for r in rows:
        r['fraccion_kernel']=base['kernel_ciclos']/base['ciclos'];r['speedup_kernel']=base['kernel_ciclos']/r['kernel_ciclos']
        r['speedup_amdahl']=1/(1-r['fraccion_kernel']+r['fraccion_kernel']/r['speedup_kernel'])
        r['speedup_medido']=base['ciclos']/r['ciclos'];r['residuo_ciclos']=r['ciclos']-(base['ciclos']-base['kernel_ciclos']+r['kernel_ciclos'])
    manifest={}
    for v in VAR:
        dest=OUT/'implantacion'/v;dest.mkdir(parents=True,exist_ok=True)
        for name in ['yosys.log','nextpnr.log','sintesis.json','timing.json','ruta.asc']:
            src=ROOT/'build/codisenio_lento'/v/name
            if not src.exists() or (hw[v]['ruta']=='FAIL' and name in ('timing.json','ruta.asc')):continue
            target=dest/(name+'.gz' if name in ('sintesis.json','ruta.asc') else name)
            target.write_bytes(gzip.compress(src.read_bytes(),mtime=0) if target.suffix=='.gz' else src.read_bytes())
            manifest[target.relative_to(ROOT).as_posix()]=dict(sha256=sha(target),sha256_original=sha(src))
    dest=OUT/'unidades';dest.mkdir(exist_ok=True)
    for src in (ROOT/'build/codisenio_lento/unidades').glob('*.log'):
        target=dest/src.name;shutil.copyfile(src,target);manifest[target.relative_to(ROOT).as_posix()]=dict(sha256=sha(target))
    result=dict(politica='SUM10/128/5%; misma cartera causal en cuatro variantes',ticks=640000,variantes=rows,frecuencia_MHz=12.5,periodo_us=100,ops_definicion='Una operacion util es un tick completo con DECISION; ticks_s es capacidad de servicio, no tasa de entradas ni operaciones de compra.',archivos=manifest,bin_sha256=sha(ROOT/'competition.bin'))
    (OUT/'resumen.json').write_text(json.dumps(result,indent=2,ensure_ascii=False),encoding='utf-8')
    with (OUT/'comparacion.csv').open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    def table(items):return '\n'.join(' & '.join(str(x) for x in r)+r' \\' for r in items)
    def num(x):return '--' if x is None else f'{x:.2f}'.replace('.',',')
    names={'software':'Software','custom0':'Custom-0','mmio':'MMIO incremental','mmio_scan':'MMIO barrido'}
    tex='% Generado por tools/resumir_codisenio_lento.py\n'
    for key,items in [('Recursos',[[names[r['variante']],r['lut4'],r['lc'],r['bram'],num(r['fmax_soc_MHz']),r['ruta']] for r in rows]),('Rendimiento',[[names[r['variante']],num(r['ciclos']),r['ciclos_max'],num(r['ic']),num(r['cpi']),num(r['tiempo_max_us']),num(r['ticks_s'])] for r in rows]),('Regiones',[[names[r['variante']],num(r['rx_ciclos']),num(r['cartera_ciclos']),num(r['kernel_ciclos']),num(r['decision_ciclos']),num(r['kernel_ic'])] for r in rows]),('Amdahl',[[names[r['variante']],num(r['speedup_kernel']),num(r['speedup_amdahl']),num(r['speedup_medido']),num(r['residuo_ciclos'])] for r in rows])]:
        tex+='\\newcommand{\\TablaFinal'+key+'}{'+table(items)+'}\n'
    tex+='\\newcommand{\\FraccionKernel}{'+num(base['fraccion_kernel']*100)+'}\n'
    (ROOT/'docs/informe/codisenio_datos.tex').write_text(tex,encoding='utf-8')
    print(json.dumps(rows,indent=2))
if __name__=='__main__':main()
