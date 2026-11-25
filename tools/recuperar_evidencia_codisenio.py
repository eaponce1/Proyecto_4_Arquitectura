"""Recupera evidencia histórica y coteja sus medias con las trazas Git originales."""
from pathlib import Path
import csv, hashlib, io, json, os, subprocess, statistics

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'docs/evidencia_codisenio'

def git_bytes(path):
    return subprocess.check_output(['git','show',f'66eede4:{path}'],cwd=ROOT)

def main():
    OUT.mkdir(parents=True,exist_ok=True)
    commit=subprocess.check_output(['git','rev-parse','66eede4'],cwd=ROOT,text=True).strip()
    origin={}
    for name in ['comparacion_codisenio.csv','informe_codisenio.md']:
        path='proyecto4/resultados/co_disenio/'+name;raw=git_bytes(path)
        (OUT/name).write_bytes(raw)
        origin[name]=dict(commit=commit,ruta_original=path,sha256=hashlib.sha256(raw).hexdigest())
    rows=list(csv.DictReader((OUT/'comparacion_codisenio.csv').open(encoding='utf-8-sig',newline='')))
    traces=['proyecto4/resultados/mediciones_software.csv',
            'proyecto4/resultados/co_disenio/custom0_ticks.csv',
            'proyecto4/resultados/co_disenio/mmio_sma10_ticks.csv']
    checks=[]
    for row,path in zip(rows,traces,strict=True):
        raw=git_bytes(path);ticks=list(csv.DictReader(io.StringIO(raw.decode('utf-8-sig'))))
        assert len(ticks)==int(row['ticks'])==20000
        for field,column in [('IC_avg','ic_total'),('cycles_avg','cycles_total')]:
            assert abs(statistics.mean(int(t[column]) for t in ticks)-float(row[field]))<1e-8
        assert max(int(t['cycles_total']) for t in ticks)==int(float(row['cycles_worst']))
        checks.append(dict(variante=row['version'],ticks=len(ticks),ruta_git=path,
                           sha256_traza=hashlib.sha256(raw).hexdigest(),medias_y_maximo_coinciden=True))
    (OUT/'procedencia.json').write_text(json.dumps(dict(commit=commit,archivos=origin,trazas=checks,
        nueva_simulacion=False,alcance='Estudio SMA10 historico; no es el perfil de Momentum32 final'),indent=2),encoding='utf-8')
    os.environ.setdefault('MPLCONFIGDIR',str(ROOT/'.matplotlib'))
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import numpy as np
    fig,ax=plt.subplots(figsize=(8,4.3),layout='constrained')
    intensities=np.logspace(-2,1,300)
    ax.loglog(intensities,np.minimum(25,50*intensities),color='#233b64',label='Techo: min(25, 50 I) Mops/s')
    for row,ops,bytes_,color in zip(rows,[14,6,6],[41,5,11],['#cf7428','#8d4eab','#26866a'],strict=True):
        x=ops/bytes_;y=ops*25/float(row['kernel_cycles_avg'])
        ax.scatter(x,y,s=55,color=color,zorder=3)
        ax.annotate(row['version'],(x,y),xytext=(5,-15),textcoords='offset points',fontsize=9)
    ax.set(xlabel='Intensidad aritmetica (operaciones/byte)',ylabel='Rendimiento del kernel (Mops/s)',
           title='Roofline simplificado: etapa SMA10 historica',xlim=(.01,10),ylim=(.2,40))
    ax.grid(True,which='both',alpha=.2);ax.legend(loc='upper left',fontsize=9)
    fig.savefig(ROOT/'docs/informe/figuras/roofline_historico.png',dpi=200)
    plt.close(fig)
    print('PASS evidencia historica: 60000 filas cotejadas; figura roofline generada')

if __name__=='__main__':main()
