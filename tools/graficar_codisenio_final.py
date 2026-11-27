"""Figura del co-diseno: mediciones por tick y roofline arquitectonico declarado."""
from pathlib import Path
import json,os
ROOT=Path(__file__).resolve().parents[1]
cache=ROOT/'build/codisenio_lento/matplotlib';cache.mkdir(parents=True,exist_ok=True)
os.environ.setdefault('MPLCONFIGDIR',str(cache))
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
def main():
    rows=json.loads((ROOT/'docs/evidencia_codisenio_final/resumen.json').read_text())['variantes']
    names=['Software','Custom-0 (no cabe)','MMIO incremental','MMIO barrido']
    colors=['#52616b','#b66a35','#216e55','#386cb0']
    fig,(a,b)=plt.subplots(1,2,figsize=(12,4.5),layout='constrained')
    bars=a.barh(names,[r['ciclos'] for r in rows],color=colors)
    a.invert_yaxis();a.set(xlabel='Ciclos medios por precio hasta DECISION',xlim=(0,155),title='Misma política, 160.000 ticks por variante')
    for bar,r in zip(bars,rows):a.text(bar.get_width()+2,bar.get_y()+bar.get_height()/2,f"{r['ciclos']:.2f}",va='center',fontsize=9)
    intensities=[2/28,2/28,2/8,9/18];peaks=[6.25,12.5,25,12.5];bandwidths=[50,50,50,25];ops=[2,2,2,9]
    xs=[10**(-1.7+i*2.2/200) for i in range(201)]
    for r,name,c,i,peak,bw,n in zip(rows,names,colors,intensities,peaks,bandwidths,ops):
        b.plot(xs,[min(peak,bw*x) for x in xs],color=c,linestyle='--',alpha=.65)
        b.scatter([i],[r['ticks_s']*n/1e6],color=c,s=48,label=name)
    b.set(xscale='log',yscale='log',xlabel='Intensidad del recurso limitante (op/B)',ylabel='Operaciones SUM10 / segundo (millones)',title='Techos ideales y tasa de extremo a extremo',ylim=(.1,40))
    b.legend(fontsize=8,loc='lower right');b.grid(alpha=.2,which='both')
    fig.savefig(ROOT/'docs/informe/figuras/codisenio_final.png',dpi=180)
    fig.savefig(ROOT/'docs/evidencia_codisenio_final/codisenio_final.svg')
    plt.close(fig)
if __name__=='__main__':main()
