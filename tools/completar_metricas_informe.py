"""Resume las trazas ya ejecutadas del RTL activo; no corre nuevas simulaciones."""
from pathlib import Path
import csv, hashlib, json, statistics

ROOT=Path(__file__).resolve().parents[1]

def main():
    data=json.loads((ROOT/'build/trader/equivalencia_verilator.json').read_text())
    results=[]
    for s in data['series']:
        path=ROOT/'build/trader/verilator'/f"{s['serie']}.csv"
        raw=path.read_bytes()
        with path.open(newline='') as f:rows=list(csv.DictReader(f))
        assert len(rows)==s['ticks']==20000
        cycles=[int(r['ciclos']) for r in rows];ic=[int(r['ic']) for r in rows]
        assert all(v>0 for v in ic)
        assert abs(statistics.mean(cycles)-s['ciclos_media'])<1e-8
        assert max(cycles)==s['ciclos_max'] and max(ic)==s['ic_max']
        results.append(dict(serie=s['serie'],ticks=len(rows),cpi_global=sum(cycles)/sum(ic),
            cpi_max=max(c/i for c,i in zip(cycles,ic,strict=True)),
            tiempo_medio_us=statistics.mean(cycles)*.08,tiempo_max_us=max(cycles)*.08,
            sha256_traza=hashlib.sha256(raw).hexdigest(),ruta_traza=path.relative_to(ROOT).as_posix()))
    target=ROOT/'docs/evidencia_informe/metricas_finales.json';target.parent.mkdir(exist_ok=True)
    target.write_text(json.dumps(dict(reloj_MHz=12.5,ventana='byte_done hasta DECISION; excluye sondeo posterior',
        series=results),indent=2),encoding='utf-8')
    print('PASS CPI maximo y tiempos de 160000 ticks resumidos')

if __name__=='__main__':main()
