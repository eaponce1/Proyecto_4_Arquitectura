"""Banco multiserie independiente y adaptación explícita de bancos oficiales.

Sin mocks del procesador: instancia Espino, memorias y SPI reales. El banco
tb_candidata conserva sus aserciones de cartera, instrucciones, MMIO y latencia.
"""
from estrategia import *
import argparse
import subprocess
import sys
import hashlib
import shutil
import re
import statistics as st
import time
import difflib
from concurrent.futures import ThreadPoolExecutor

ROOT=HERE.parents[2]
BUILD=HERE/'build'
OUT=HERE/'resultados'
MMIO=HERE.parent/'mmio_sma10/rtl'
TRACE=ROOT/'proyecto4/pruebas_fisicas/demo_autonoma_bus_detail/rtl'
CELLS=Path(shutil.which('yosys')).resolve().parents[1]/'share/yosys/ice40/cells_sim.v'
TB=HERE.parent/'candidata_final/tb/tb_candidata.sv'

def sources():
    return [HERE/'rtl/trade_spi_externo.v',HERE/'rtl/pochoco_soc_cpu_trace.v',TRACE/'espino_core_cpu_trace.v',
      *(MMIO/f'{n}.v' for n in ('pochoco_ram','pochoco_spi_slave','pochoco_sma10')),
      *sorted((ROOT/'rtl/espino_core').glob('*.v'))]

def signature():
    return {p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest()
            for p in [*sources(),TB,HERE/'trade.hex']}

def command(cmd,log,cwd=ROOT):
    start=time.perf_counter()
    proc=subprocess.run([str(c) for c in cmd],cwd=cwd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,
        text=True,encoding='utf-8',errors='replace')
    Path(log).write_text(proc.stdout+f'\nSalida={proc.returncode}; segundos={time.perf_counter()-start:.6f}\n',encoding='utf-8')
    assert proc.returncode==0,(str(log),proc.stdout[-3000:])
    return proc.stdout

def simulate(name,n,period=100000,phase=0,netlist=None):
    initial_signature=signature()
    dest=BUILD/'rtl';dest.mkdir(exist_ok=True)
    label=f'{name}_{n}_{period}_{phase}'+('_puertas' if netlist else '')
    words=len((HERE/'trade.hex').read_text().split())
    vvp=dest/f'{label}.vvp';csvout=dest/f'{label}.csv'
    opts=['-DNETLIST'] if netlist else [f'-Ptb_candidata.PALABRAS_FIRMWARE={words}',
       f'-Ptb_candidata.ARCHIVO_FIRMWARE="{(HERE/"trade.hex").relative_to(ROOT).as_posix()}"',
       '-Ptb_candidata.REG_CAJA=15','-Ptb_candidata.REG_ACCIONES=5']
    cmd=['iverilog','-g2012','-s','tb_candidata',*opts,f'-Ptb_candidata.TICKS={n}',
       f'-Ptb_candidata.PERIODO_NS={period}',f'-Ptb_candidata.FASE_NS={phase}',
       '-o',vvp,TB,*([netlist] if netlist else sources()),CELLS]
    command(cmd,dest/f'{label}_compilacion.log')
    vec=BUILD/'vectores'/name
    log=command(['vvp','-n',vvp,f'+vectores={vec.as_posix()}',f'+cartera={(vec/"cartera.hex").as_posix()}',
        f'+metricas={csvout.as_posix()}'],dest/f'{label}.log')
    assert f'PASS {n} MISO frente a Python' in log
    prices=[int(x,16) for x in (vec/'precios.hex').read_text().split()][:n]
    _,expected=run(prices,frozen(),True)
    with csvout.open(newline='') as f:rows=list(csv.DictReader(f))
    assert len(rows)==n
    for actual,ex in zip(rows,expected,strict=True):
        for col,key in [('tick','tick'),('precio','precio'),('fill','cantidad_ejecutada'),('caja','caja'),
           ('acciones','acciones'),('patrimonio','patrimonio'),('comisiones_acum','comisiones_acum')]:
            assert int(actual[col])==ex[key],(name,col,ex['tick'],actual[col],ex[key])
        assert int(actual['miso_hex'],16)==ex['miso']
        if not netlist: assert int(actual['decision_hex'],16)==ex['decision']
    evidence=dict(nombre=name,ticks=n,periodo_ns=period,fase_ns=phase,puertas=bool(netlist),discrepancias=0,
        log=str((dest/f'{label}.log').relative_to(HERE)),csv=str(csvout.relative_to(HERE)),fuentes=initial_signature)
    assert initial_signature==signature(),'Fuentes modificadas durante la simulacion'
    if not netlist:
        cycles=[int(r['ciclos']) for r in rows];ic=[int(r['ic']) for r in rows]
        evidence.update(ciclos_max=max(cycles),ciclos_media=st.mean(cycles),ic_max=max(ic),ic_media=st.mean(ic),
           cpi=sum(cycles)/sum(ic),presupuesto=(period-9500)//80,us_max=max(cycles)*.08,
           margen_ciclos=(period-9500)//80-max(cycles),margen_us=(period-9500)/1000-max(cycles)*.08)
    (dest/f'{label}.json').write_text(json.dumps(evidence,indent=2))
    print('PASS RTL',label,evidence.get('ciclos_max','puertas'),flush=True)
    return evidence

def official():
    initial_signature=signature()
    dest=BUILD/'oficial';dest.mkdir(exist_ok=True)
    results=[]
    # Both independent bank sources run with explicit final-board wiring adapters.
    for label,source in [('profesor',ROOT/'proyecto4/resultados/validacion_oficial/tb_proyecto_4_profesor.sv'),
                         ('repositorio',ROOT/'tb/tb_proyecto_4.sv')]:
        original=source.read_text(encoding='utf-8');s=original
        s=s.replace('localparam string','localparam')
        s=re.sub(r'localparam\s+PROGRAMA\s*=\s*"[^"]*";',f'localparam PROGRAMA = "{(HERE/"trade.hex").relative_to(ROOT).as_posix()}";',s)
        s=re.sub(r'localparam\s+SERIE\s*=\s*"[^"]*";',f'localparam SERIE = "{(HERE/"datos/practica_meta_2022.csv").relative_to(ROOT).as_posix()}";',s)
        output=(dest/f'{label}_decisiones.csv').relative_to(ROOT).as_posix()
        s=s.replace('$fopen("decisiones.csv", "w")',f'$fopen("{output}", "w")')
        s=re.sub(r'localparam\s+SALIDA\s*=\s*"[^"]*";',f'localparam SALIDA = "{output}";',s)
        s=s.replace('string encabezado;', 'reg [8*128-1:0] encabezado;')
        start=s.index('  pochoco_soc #(');end=s.index('));',start)+3
        s=s[:start]+'''  trade_spi_externo #(.ARCHIVO_FIRMWARE(PROGRAMA)) dut (
    .i_Clk(clk), .o_LED(), .i_SPI_SCLK(sclk), .i_SPI_MOSI(mosi),
    .i_SPI_CS_n(cs_n), .o_SPI_MISO(miso));'''+s[end:]
        s=s.replace('always @(posedge clk)', 'always @(posedge dut.clk_soc)')
        s=s.replace('dut.u_spi.', 'dut.u_soc.u_spi.')
        s=s.replace('dut.data_addr', 'dut.u_soc.data_addr')
        s=s.replace('#4000;', '#120113;').replace('(PERIODO_NS - SPI_NS) / 40','(PERIODO_NS - SPI_NS) / 80')
        target=dest/f'{label}_adaptado.sv';target.write_text(s)
        (dest/f'{label}_adaptacion.diff').write_text(''.join(difflib.unified_diff(original.splitlines(True),s.splitlines(True),fromfile=str(source),tofile=str(target))))
        # Finance task and constants MUST remain literally identical.
        a=original[original.index('  task automatic ejecutar('):original.index('  endtask',original.index('  task automatic ejecutar('))+9]
        assert a in s
        vvp=dest/f'{label}.vvp'
        command(['iverilog','-g2012','-s','tb_proyecto_4','-o',vvp,target,*sources(),CELLS],dest/f'{label}_compilacion.log')
        log=command(['vvp','-n',vvp],dest/f'{label}.log')
        assert 'Testbenchs aprobados: 4/4' in log
        with (ROOT/output).open(newline='') as f:rows=list(csv.DictReader(f))
        _,expected=run(load(HERE/'datos/practica_meta_2022.csv')[:2000],frozen(),True)
        assert len(rows)==2000
        for real,ex in zip(rows,expected,strict=True):
            for col in ('tick','precio','caja','acciones','patrimonio'):assert int(real[col])==ex[col]
            assert int(real['decision'],16)==ex['miso']
        results.append(dict(banco=label,ticks=2000,tests='4/4',cartera_y_miso='PASS',
             adaptacion_explicita=True,sha256_original=hashlib.sha256(source.read_bytes()).hexdigest(),fuentes=initial_signature))
        print('PASS banco oficial adaptado',label,flush=True)
    assert initial_signature==signature()
    (OUT/'bancos_oficiales.json').write_text(json.dumps(results,indent=2))

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--rapido',action='store_true');parser.add_argument('--oficial',action='store_true')
    parser.add_argument('--solo-estres',action='store_true')
    args=parser.parse_args()
    if args.oficial:official();return
    jobs=[]
    if args.rapido:
        jobs=[('recuperacion',768,100000,27)]
    else:
        if not args.solo_estres:
            for path in sorted((HERE/'datos').glob('*.csv')):jobs.append((path.stem,20000,100000,0))
        from validar_estrategia import synth
        for name,p in synth().items():jobs.append((name,len(p),100000,27))
        # Exact official slower cadences verified on a complete deterministic series.
        jobs.extend([('integracion_cadencias',48,p,41) for p in (1000000,10000000)])
    with ThreadPoolExecutor(max_workers=2) as pool:
        futures=[pool.submit(simulate,*job) for job in jobs]
        results=[f.result() for f in futures]
    (OUT/('rtl_rapido.json' if args.rapido else 'equivalencia_rtl.json')).write_text(json.dumps(results,indent=2))

if __name__=='__main__':main()
