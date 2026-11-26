"""Reproduccion visual y exportacion de Pochoco Trader; no accede a la FPGA."""
from pathlib import Path
import argparse
import csv
import hashlib
import json
import os
import shutil
import sys
from datetime import datetime

ROOT=Path(__file__).resolve().parent
ALT=ROOT/'proyecto4/alternativas/tendencia_lenta'
DATA=ROOT/'proyecto4/alternativas/competitiva_definitiva/datos'
sys.path.insert(0,str(ALT))
from modelo_lento import load, run, frozen, write_csv

SERIES={
 'amd_enero':('AMD enero 2022','practica_amd_2022_ene.csv'),
 'amd_mayo':('AMD mayo 2022','practica_amd_2022_may.csv'),
 'apple_2022':('Apple 2022','practica_apple_2022.csv'),
 'apple_2023':('Apple 2023','practica_apple_2023.csv'),
 'meta_2022':('Meta 2022','practica_meta_2022.csv'),
 'netflix_2022':('Netflix 2022','practica_netflix_2022.csv'),
 'netflix_2023':('Netflix 2023','practica_netflix_2023.csv'),
 'tesla_2022':('Tesla 2022','practica_tesla_2022.csv'),
}

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def simulate(key):
    label,filename=SERIES[key];path=DATA/filename;prices=load(path)
    metrics,rows=run(prices,frozen(),True)
    q=9995//prices[0];n=buys=sells=0;peak=10000
    for r in rows:
        n+=r['cantidad_ejecutada']>0
        buys+=r['cantidad_ejecutada']>0 and r['miso']>>6==1
        sells+=r['cantidad_ejecutada']>0 and r['miso']>>6==2
        peak=max(peak,r['patrimonio'])
        r.update(mantener=9995-q*prices[0]+q*r['precio'],ordenes_acum=n,compras_acum=buys,ventas_acum=sells,
                 drawdown_actual_pct=100*(peak-r['patrimonio'])/peak,
                 miso_hex=f"0x{r['miso']:02X}",decision_hex=f"0x{r['decision']:02X}")
    # La visualizacion debe reproducir la entrega congelada, no reoptimizarla.
    with (ALT/'resultados/comparacion_final.csv').open(newline='') as f:
        ref=next(r for r in csv.DictReader(f) if r['serie']==path.stem)
    for field in ('patrimonio','ordenes','comisiones','drawdown'):
        assert metrics[field]==int(ref[field]),f'Diferencia respecto de entrega validada: {key}/{field}'
    rtl=ROOT/'build/trader/verilator'/f'{path.stem}.csv'
    if rtl.exists():
        with rtl.open(newline='') as f:actual=list(csv.DictReader(f))
        assert len(actual)==len(rows),'Traza RTL incompleta'
        for a,b in zip(actual,rows,strict=True):
            for field,key_ in [('tick','tick'),('precio','precio'),('caja','caja'),('acciones','acciones'),
                               ('fill','cantidad_ejecutada'),('patrimonio','patrimonio'),('comisiones_acum','comisiones_acum')]:
                assert int(a[field])==b[key_],(label,b['tick'],field)
            assert int(a['miso_hex'],16)==b['miso'] and int(a['decision_hex'],16)==b['decision']
    return dict(key=key,label=label,prices=prices,metrics=metrics,rows=rows,csv=path,rtl=rtl if rtl.exists() else None)

def export(data,dest):
    dest.mkdir(parents=True,exist_ok=True);m=data['metrics'];rows=data['rows']
    write_csv(dest/'ticks.csv',rows)
    trades=[dict(tick=r['tick'],precio=r['precio'],tipo='comprar' if r['miso']>>6==1 else 'vender',
                 miso=r['miso_hex'],cantidad=r['cantidad_ejecutada'],caja=r['caja'],acciones=r['acciones'],
                 patrimonio=r['patrimonio'],comision=r['comision']) for r in rows if r['cantidad_ejecutada']]
    write_csv(dest/'operaciones.csv',trades)
    provenance=dict(serie=data['label'],ticks=len(rows),modo='SIMULACION_PYTHON_REPRODUCCION_VISUAL',
        prueba_fisica='NO_REALIZADA_POR_ESTE_SIMULADOR',parametros=frozen().__dict__,
        csv_sha256=sha(data['csv']),hex_sha256=sha(ALT/'trade.hex'),
        bin_disponible_sha256=sha(ROOT/'competition.bin') if (ROOT/'competition.bin').exists() else None,
        bin_nota='Hash del archivo local; no es una lectura de la flash.',metricas=m)
    if data['rtl']:
        shutil.copy2(data['rtl'],dest/'referencia_RTL.csv')
        provenance['rtl_archivada_cotejada']=dict(ticks=len(rows),discrepancias=0,sha256=sha(data['rtl']),
            nota='Traza RTL de la validacion anterior; este comando NO ejecuta un testbench nuevo.')
    (dest/'resumen.json').write_text(json.dumps(provenance,indent=2,ensure_ascii=False),encoding='utf-8')
    os.environ.setdefault('MPLCONFIGDIR',str(ROOT/'resultados_simulacion/.matplotlib'))
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    fig,axes=plt.subplots(3,1,figsize=(12,10),sharex=True)
    ticks=[r['tick'] for r in rows]
    axes[0].plot(ticks,data['prices'],color='#334155',lw=.8,label='Precio normalizado')
    for action,color,marker in [(1,'#15803d','^'),(2,'#dc2626','v')]:
        points=[r for r in rows if r['cantidad_ejecutada'] and r['miso']>>6==action]
        axes[0].scatter([r['tick'] for r in points],[r['precio'] for r in points],
                         color=color,marker=marker,s=25,label='Compra ejecutada' if action==1 else 'Venta ejecutada',zorder=3)
    axes[1].plot(ticks,[r['patrimonio'] for r in rows],label='Trader',color='#2563eb')
    axes[1].plot(ticks,[r['mantener'] for r in rows],label='Comprar y mantener oficial',color='#d97706')
    axes[1].axhline(10000,color='#64748b',ls=':',label='Capital inicial')
    axes[2].fill_between(ticks,[r['drawdown_actual_pct'] for r in rows],color='#dc2626',alpha=.25)
    for ax in axes:ax.grid(alpha=.2)
    axes[0].legend();axes[1].legend();axes[0].set_ylabel('Precio');axes[1].set_ylabel('Patrimonio ($)')
    axes[2].set_ylabel('Drawdown actual (%)');axes[2].set_xlabel('Tick')
    fig.suptitle(data['label']+' | Simulacion de la politica congelada; no es una medicion fisica')
    fig.tight_layout();fig.savefig(dest/'grafico.png',dpi=160);fig.savefig(dest/'grafico.svg');plt.close(fig)
    text=f'''# Simulacion — {data['label']}

Se reprodujeron {len(rows):,} ticks de una serie conocida de practica con la politica congelada.
La estrategia usa solo los precios recibidos hasta cada decision; el visor reproduce una traza
precalculada a velocidad humana. No se consulto ni midio una FPGA fisica.

| Medida | Resultado |
|---|---:|
| Capital inicial | $10.000 |
| Patrimonio final Trader | ${m['patrimonio']:,} |
| Comprar y mantener oficial | ${m['mantener_oficial']:,} |
| Ventaja absoluta | ${m['ventaja']:,} |
| Ventaja relativa | {m['ventaja_pct']:.2f}% |
| Caja final | ${m['caja']:,} |
| Acciones finales | {m['acciones']} |
| Ordenes ejecutadas | {m['ordenes']} |
| Comisiones | ${m['comisiones']:,} |
| Drawdown maximo absoluto | ${m['drawdown']:,} |
| Drawdown maximo porcentual | {m['drawdown_pct']:.2f}% |

![Precio, operaciones, patrimonio y drawdown](grafico.png)

`ticks.csv` contiene todos los precios y estados. `operaciones.csv` contiene solo fills
reales del modelo. `resumen.json` conserva parametros y hashes de procedencia.
MISO en el tick n ejecuta la decision calculada en n-1 al precio de n. La decision
calculada despues del ultimo precio no se ejecuta. Cada orden ejecutada paga $5;
la cantidad se recorta a caja/inventario y a 63 acciones por byte.

El benchmark oficial compra idealmente en tick 0 con una sola comision y puede superar
63 acciones; tiene esa ventaja respecto del SPI real. El firmware comienza con MISO=0.
Estos datos ya se usaron durante desarrollo: este resultado no es validacion independiente
ni demuestra el resultado de la competencia secreta. La velocidad de animacion no mide
el deadline del procesador; para eso se usan los testbenches RTL.

La traza RTL archivada, cuando esta disponible, se copia a `referencia_RTL.csv` y se
coteja en todos los ticks contra el modelo antes de exportar. Esto permite distinguir
evidencia RTL previa de una simulacion RTL nueva y de la prueba fisica pendiente.
'''
    (dest/'INFORME.md').write_text(text,encoding='utf-8')
    print(f"{data['label']}: Trader=${m['patrimonio']} | Mantener=${m['mantener_oficial']} | "
          f"Ordenes={m['ordenes']} | Comisiones=${m['comisiones']} | DD={m['drawdown_pct']:.2f}%",flush=True)
    return dict(serie=data['label'],**m)

class Viewer:
    def __init__(self,root,key,out):
        import tkinter as tk
        from tkinter import ttk
        self.root=root;self.out=out;self.playing=False;self.index=0;self.shown=-1
        root.title('Pochoco Trader | Simulacion de practica');root.geometry('1140x840')
        self.key=tk.StringVar(value=key);self.speed=tk.StringVar(value='32');self.status=tk.StringVar()
        top=ttk.Frame(root,padding=8);top.pack(fill='x')
        ttk.Label(top,text='Serie:').pack(side='left')
        select=ttk.Combobox(top,textvariable=self.key,values=list(SERIES),state='readonly',width=18);select.pack(side='left',padx=6)
        select.bind('<<ComboboxSelected>>',lambda e:self.load())
        ttk.Button(top,text='Iniciar / Pausar',command=self.toggle).pack(side='left',padx=4)
        ttk.Button(top,text='Un tick',command=self.step).pack(side='left',padx=4)
        ttk.Button(top,text='Reiniciar',command=self.reset).pack(side='left',padx=4)
        ttk.Label(top,text='Ticks por paso:').pack(side='left',padx=6)
        ttk.Combobox(top,textvariable=self.speed,values=['1','8','32','128'],state='readonly',width=5).pack(side='left')
        ttk.Button(top,text='Exportar informe',command=self.save).pack(side='right')
        ttk.Label(root,text='Reproduccion del modelo validado. No es telemetria de la placa ni datos bursatiles en vivo.',padding=5).pack()
        ttk.Label(root,textvariable=self.status,font=('Consolas',11),padding=7).pack(fill='x')
        self.canvas=tk.Canvas(root,height=395,bg='white',highlightthickness=0);self.canvas.pack(fill='both',expand=True,padx=12)
        columns=('tick','precio','tipo','cantidad','miso','caja','acciones','patrimonio')
        self.trades=ttk.Treeview(root,columns=columns,show='headings',height=7)
        for c in columns:self.trades.heading(c,text=c);self.trades.column(c,width=100,anchor='center')
        self.trades.pack(fill='x',padx=12,pady=8)
        ttk.Label(root,text='Azul: Trader | Naranja: mantener | Verde: compra ejecutada | Rojo: venta ejecutada',padding=5).pack()
        self.canvas.bind('<Configure>',lambda e:self.draw())
        self.load();root.after(40,self.pulse)

    def load(self):
        self.playing=False;self.data=simulate(self.key.get());self.reset()
    def reset(self):
        self.playing=False;self.index=0;self.shown=-1
        for item in self.trades.get_children():self.trades.delete(item)
        self.draw()
    def toggle(self):
        if self.index==len(self.data['rows'])-1:self.reset()
        self.playing=not self.playing
    def step(self):
        self.playing=False;self.index=min(self.index+1,len(self.data['rows'])-1);self.draw()
    def pulse(self):
        if self.playing:
            self.index=min(self.index+int(self.speed.get()),len(self.data['rows'])-1)
            if self.index==len(self.data['rows'])-1:self.playing=False
            self.draw()
        self.root.after(40,self.pulse)
    def draw(self):
        if not hasattr(self,'data'):return
        rows=self.data['rows'];r=rows[self.index]
        self.status.set(f"{self.data['label']} | Tick {self.index}/{len(rows)-1} | Precio ${r['precio']} | MISO {r['miso_hex']} | Decision nueva {r['decision_hex']}\n"
                        f"Caja ${r['caja']} | Acciones {r['acciones']} | Trader ${r['patrimonio']} | Mantener ${r['mantener']} | Ordenes {r['ordenes_acum']} | Comisiones ${r['comisiones_acum']}")
        for row in rows[self.shown+1:self.index+1]:
            if row['cantidad_ejecutada']:
                self.trades.insert('', 'end',values=(row['tick'],row['precio'],'COMPRA' if row['miso']>>6==1 else 'VENTA',
                    row['cantidad_ejecutada'],row['miso_hex'],row['caja'],row['acciones'],row['patrimonio']))
        self.shown=self.index;items=self.trades.get_children()
        if items:self.trades.see(items[-1])
        c=self.canvas;c.delete('all');w=max(200,c.winfo_width());h=max(200,c.winfo_height());left=75;right=w-20
        end=max(1,self.index);stride=max(1,(self.index+1)//700);idx=list(range(0,self.index+1,stride))
        if idx[-1]!=self.index:idx.append(self.index)
        for panel,fields,title in [(0,[('precio','#334155')],'Precio y operaciones'),
                                   (1,[('patrimonio','#2563eb'),('mantener','#d97706')],'Patrimonio: Trader / mantener')]:
            top=panel*h/2+30;bottom=(panel+1)*h/2-25
            values=[rows[i][field] for field,_ in fields for i in range(self.index+1)]
            lo=min(values);hi=max(values);padding=max(1,(hi-lo)*.08);lo-=padding;hi+=padding
            x=lambda i:left+(right-left)*i/end
            y=lambda value:bottom-(bottom-top)*(value-lo)/(hi-lo)
            c.create_text(left,top-16,text=title,anchor='w',font=('Arial',10,'bold'))
            c.create_rectangle(left,top,right,bottom,outline='#cbd5e1')
            c.create_text(left-8,top,text=f'{hi:,.0f}',anchor='e');c.create_text(left-8,bottom,text=f'{lo:,.0f}',anchor='e')
            c.create_text(left,bottom+12,text='0');c.create_text(right,bottom+12,text=str(self.index))
            for field,color in fields:
                points=[v for i in idx for v in (x(i),y(rows[i][field]))]
                if len(points)>=4:c.create_line(*points,fill=color,width=1.5)
            if panel==0:
                for row in rows[:self.index+1]:
                    if row['cantidad_ejecutada']:
                        px=x(row['tick']);py=y(row['precio']);color='#15803d' if row['miso']>>6==1 else '#dc2626'
                        c.create_oval(px-3,py-3,px+3,py+3,fill=color,outline=color)
    def save(self):
        from tkinter import messagebox
        try:
            folder=self.out/self.key.get();export(self.data,folder)
            messagebox.showinfo('Informe exportado',f'Serie completa exportada (no solo el tick visible):\n{folder}\n\nINFORME.md, grafico.png/svg, ticks.csv, operaciones.csv y resumen.json')
        except Exception as e:messagebox.showerror('Error al exportar',str(e))

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--serie',choices=list(SERIES),default='meta_2022')
    parser.add_argument('--todas',action='store_true',help='Exportar las ocho series')
    parser.add_argument('--sin-ventana',action='store_true',help='Solo generar archivos')
    parser.add_argument('--listar',action='store_true')
    args=parser.parse_args()
    if args.listar:
        for key,(label,_) in SERIES.items():print(key,':',label)
        return
    # Nunca sobrescribir evidencia: cada ejecucion tiene su propio directorio.
    output=ROOT/'resultados_simulacion'/datetime.now().strftime('%Y%m%d_%H%M%S_%f')
    keys=list(SERIES) if args.todas else [args.serie]
    summaries=[export(simulate(key),output/key) for key in keys]
    write_csv(output/'comparacion.csv',summaries)
    table='| Serie | Trader | Mantener | Ventaja | Ordenes | Comisiones | DD max. % |\n|---|---:|---:|---:|---:|---:|---:|\n'
    table+='\n'.join(f"| {r['serie']} | {r['patrimonio']} | {r['mantener_oficial']} | {r['ventaja']} | {r['ordenes']} | {r['comisiones']} | {r['drawdown_pct']:.2f} |" for r in summaries)
    links='\n'.join(f"- [{SERIES[k][0]}: informe y grafico]({k}/INFORME.md)" for k in keys)
    (output/'INFORME_COMPARATIVO.md').write_text('# Resultados de simulacion de Pochoco Trader\n\n'+table+'\n\n'+
        f"Ventaja frente a mantener en {sum(r['ventaja']>0 for r in summaries)}/{len(summaries)} series ejecutadas.\n\n"+
        'Politica activa: SUM10, revision cada 128 ticks, entrada/salida relativa del 5 %, inicio en caja. '+
        'Capital $10.000, comision $5 por orden ejecutada, maximo 63 acciones por orden, ejecucion al tick siguiente.\n\n'+
        links+'\n\nSon series conocidas de desarrollo. No se afirma superioridad fuera de muestra ni aprobacion fisica. '+
        'Los graficos son exportables a un informe y las trazas RTL previas se cotejan con el modelo cuando estan disponibles.\n',encoding='utf-8')
    (output/'LEEME.md').write_text('Resultados de simulacion sobre series conocidas, no medicion fisica.\n'
        'Cada carpeta contiene INFORME.md, grafico.png/svg, ticks.csv, operaciones.csv y resumen.json.\n'
        'comparacion.csv resume las series ejecutadas. La interfaz reproduce la traza precalculada; no mide el reloj de la FPGA.\n',encoding='utf-8')
    print('ARCHIVOS PARA EL INFORME:',output,flush=True)
    if not args.sin_ventana:
        import tkinter as tk
        root=tk.Tk();Viewer(root,args.serie,output);root.mainloop()

if __name__=='__main__':main()
