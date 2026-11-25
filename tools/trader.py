"""Build activo de Pochoco Trader. No programa la FPGA."""
from pathlib import Path
import argparse, csv, hashlib, json, re, shutil, subprocess, sys, time
ROOT=Path(__file__).resolve().parents[1]
ALT=ROOT/'proyecto4/alternativas/competitiva_definitiva'
OUT=ROOT/'build/trader'
sys.path.insert(0,str(ALT))
from estrategia import run, frozen
from validar_estrategia import synth

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def sources():
    return [ROOT/'rtl/trade_spi_externo.v',*sorted((ROOT/'rtl/trader').glob('*.v')),
            *sorted((ROOT/'rtl/espino_core').glob('*.v'))]
def signature():
    return {p.relative_to(ROOT).as_posix():sha(p) for p in
            [*sources(),ROOT/'sw/trade.s',ROOT/'sw/trade.hex',ROOT/'goboard_trader.pcf']}
def command(cmd,name):
    OUT.mkdir(parents=True,exist_ok=True);start=time.perf_counter()
    result=subprocess.run([str(x) for x in cmd],cwd=ROOT,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,
                          encoding='utf-8',errors='replace')
    (OUT/f'{name}.log').write_text(result.stdout+f'\nSalida={result.returncode}; segundos={time.perf_counter()-start:.3f}\n',encoding='utf-8')
    if result.returncode:raise RuntimeError(f'{name}: revisar build/trader/{name}.log\n'+result.stdout[-1500:])
    return result.stdout
def check_sources():
    reference=json.loads((ALT/'resultados/equivalencia_verilator.json').read_text())['fuentes']
    for name,h in reference.items():assert sha(ROOT/name)==h,f'Cambio en referencia validada: {name}'
    for name in ['trade.s','trade.hex']:assert sha(ROOT/'sw'/name)==sha(ALT/name),f'{name} distinto del validado'
    top=(ALT/'rtl/trade_spi_externo.v').read_text().replace('PALABRAS_FIRMWARE = 153','PALABRAS_FIRMWARE = 150').replace(
        'proyecto4/alternativas/competitiva_definitiva/trade.hex','sw/trade.hex')
    assert (ROOT/'rtl/trade_spi_externo.v').read_text()==top
    pairs=[(ROOT/'rtl/trader/pochoco_soc_cpu_trace.v',ALT/'rtl/pochoco_soc_cpu_trace.v'),
           (ROOT/'rtl/trader/espino_core_cpu_trace.v',ROOT/'proyecto4/pruebas_fisicas/demo_autonoma_bus_detail/rtl/espino_core_cpu_trace.v')]
    pairs += [(ROOT/'rtl/trader'/f'{n}.v',ROOT/'proyecto4/alternativas/mmio_sma10/rtl'/f'{n}.v') for n in
              ['pochoco_ram','pochoco_sma10']]
    assert all(sha(a)==sha(b) for a,b in pairs),'RTL activo distinto de la referencia'
    assert sha(ROOT/'goboard_trader.pcf')==sha(ROOT/'proyecto4/pruebas_fisicas/spi_externo_robusto/goboard_spi_externo.pcf')
def simulate(name,prices,phase=0,netlist=None):
    folder=OUT/name;folder.mkdir(parents=True,exist_ok=True);_,rows=run(prices,frozen(),True)
    for file,key in [('precios','precio'),('miso','miso'),('escrituras','decision')]:
        (folder/f'{file}.hex').write_text(''.join(f'{r[key]:02x}\n' for r in rows))
    (folder/'cartera.hex').write_text(''.join(f"{(r['caja']<<32)|(r['patrimonio']<<8)|r['acciones']:016x}\n" for r in rows))
    cells=Path(shutil.which('yosys')).resolve().parents[1]/'share/yosys/ice40/cells_sim.v'
    opts=['-DNETLIST'] if netlist else ['-Ptb_candidata.PALABRAS_FIRMWARE=150',
         '-Ptb_candidata.ARCHIVO_FIRMWARE="sw/trade.hex"','-Ptb_candidata.REG_CAJA=15','-Ptb_candidata.REG_ACCIONES=5']
    vvp=folder/'test.vvp';trace=folder/'decisiones.csv'
    command(['iverilog','-g2012','-s','tb_candidata',*opts,f'-Ptb_candidata.TICKS={len(prices)}',
             '-Ptb_candidata.PERIODO_NS=100000',f'-Ptb_candidata.FASE_NS={phase}','-o',vvp,
             ROOT/'proyecto4/alternativas/candidata_final/tb/tb_candidata.sv',
             *([netlist] if netlist else sources()),cells],name+'_compilacion')
    log=command(['vvp','-n',vvp,f'+vectores={folder.as_posix()}',f'+cartera={(folder/"cartera.hex").as_posix()}',
                 f'+metricas={trace.as_posix()}'],name)
    assert f'PASS {len(prices)} MISO frente a Python' in log
    with trace.open(newline='') as f:actual=list(csv.DictReader(f))
    assert len(actual)==len(rows)
    for a,b in zip(actual,rows,strict=True):
        for field,key in [('tick','tick'),('precio','precio'),('fill','cantidad_ejecutada'),('caja','caja'),
                          ('acciones','acciones'),('patrimonio','patrimonio'),('comisiones_acum','comisiones_acum')]:
            assert int(a[field])==b[key],(name,b['tick'],field)
        assert int(a['miso_hex'],16)==b['miso']
        if not netlist:assert int(a['decision_hex'],16)==b['decision']
    result=dict(nombre=name,ticks=len(rows),discrepancias=0,netlist=bool(netlist))
    if not netlist:result['ciclos_max']=max(int(r['ciclos']) for r in actual)
    print('PASS',name,len(rows),'ticks',flush=True);return result
def spi_margin(netlist=None, packed=False):
    """Ejercita CS corto, todas las fases de sincronizacion y ambos tipos de orden."""
    evidence=[]
    cases=[(20,p) for p in (0,19,20,39,40,59,60,79)]+[(40,0),(1000,0)]
    if netlist:cases=[(20,0),(40,0),(1000,0)]
    cells=Path(shutil.which('yosys')).resolve().parents[1]/'share/yosys/ice40/cells_sim.v'
    kind='bin' if packed else ('netlist' if netlist else 'rtl')
    for setup,phase in cases:
        name=f'spi_{kind}_cs{setup}_fase{phase}';exe=OUT/f'{name}.vvp'
        command(['iverilog','-g2012','-s','tb_spi_margen',*(['-DNETLIST'] if netlist else []),
                 f'-Ptb_spi_margen.SETUP_NS={setup}',f'-Ptb_spi_margen.FASE_NS={phase}',
                 '-o',exe,ROOT/'tb/tb_spi_margen.sv',*([netlist] if netlist else sources()),cells],name+'_compilacion')
        log=command(['vvp','-n',exe,'+vectores=build/trader/rtl_compra_venta'],name)
        assert 'PASS SPI CS corto 48 ticks' in log
        evidence.append(dict(nombre=name,ticks=48,discrepancias=0,setup_ns=setup,fase_ns=phase))
        print('PASS',name,flush=True)
    return evidence

def test():
    check_sources()
    return [simulate('rtl_recuperacion',synth()['recuperacion'],27),
            simulate('rtl_compra_venta',synth()['integracion_cadencias'],41),*spi_margin()]
def verify():
    check_sources();record=json.loads((OUT/'validacion.json').read_text())
    assert record['fuentes']==signature(),'Fuentes distintas de la sintesis validada'
    assert sha(ROOT/'competition.bin')==record['sha256_bin'],'BIN distinto del validado'
    assert (ROOT/'competition.bin').stat().st_size==32220
    print('PASS competition.bin',record['sha256_bin'],flush=True);return record
def build():
    if (OUT/'validacion.json').exists() and (ROOT/'competition.bin').exists():
        try:verify();return
        except AssertionError:pass
    command([sys.executable,'-B','sw/assembler.py','sw/trade.s','-o','sw/trade.hex'],'ensamblado')
    tests=test();initial=signature()
    names=' '.join('"'+p.relative_to(ROOT).as_posix()+'"' for p in sources())
    command(['yosys','-p',f'read_verilog -sv {names}; synth_ice40 -dff -top trade_spi_externo; '
             'check -assert; stat; write_json build/trader/trade.json'],'yosys')
    log=command(['nextpnr-ice40','--hx1k','--package','vq100','--freq','25','--seed','1',
                 '--json','build/trader/trade.json','--pcf','goboard_trader.pcf',
                 '--asc','build/trader/trade.asc','--report','build/trader/timing.json'],'nextpnr')
    lc=int(re.search(r'ICESTORM_LC:\s*(\d+)',log)[1]);bram=int(re.search(r'ICESTORM_RAM:\s*(\d+)',log)[1])
    clocks=json.loads((OUT/'timing.json').read_text())['fmax']
    assert lc<=1280 and bram<=16 and all(c['achieved']>=25 for c in clocks.values())
    command(['yosys','-Q','-q','-p','read_json build/trader/trade.json; write_verilog -noattr build/trader/netlist.v'],'netlist')
    for phase in (0,41):tests.append(simulate(f'netlist_fase_{phase}',synth()['integracion_cadencias'],phase,OUT/'netlist.v'))
    tests.extend(spi_margin(OUT/'netlist.v'))
    package(tests,initial,lc,bram,clocks)

def package(tests,initial,lc,bram,clocks):
    assert initial==signature(),'Las fuentes cambiaron durante el build'
    tmp=OUT/'competition.tmp';command(['icepack','build/trader/trade.asc',tmp],'icepack');assert tmp.stat().st_size==32220
    # Comprobar tambien la configuracion realmente empaquetada, antes de publicarla.
    command(['icepack','-u',tmp,OUT/'bin_desempaquetado.asc'],'desempaquetado')
    decoded=command(['icebox_vlog','-d','vq100','-p','goboard_trader.pcf','-c','-n',
                     'trade_spi_externo',OUT/'bin_desempaquetado.asc'],'decodificado')
    # Retardo funcional uniforme de 1 ps para resolver redes combinacionales de puertas.
    reconstructed=OUT/'bin_desempaquetado.v'
    reconstructed.write_text(decoded.replace('assign ','assign #1 '),encoding='utf-8')
    tests.extend(spi_margin(reconstructed,packed=True))
    target=ROOT/'competition.bin'
    if target.exists():
        backup=ROOT/'respaldos'/('competition_'+sha(target)+'.bin')
        backup.parent.mkdir(exist_ok=True)
        if not backup.exists():shutil.copy2(target,backup)
    tmp.replace(target)
    record=dict(fuentes=initial,sha256_bin=sha(target),sha256_hex=sha(ROOT/'sw/trade.hex'),lc=lc,bram=bram,
                clocks=clocks,tests=tests,prueba_fisica='PENDIENTE')
    (OUT/'validacion.json').write_text(json.dumps(record,indent=2))
    (ROOT/'competition.sha256').write_text(record['sha256_bin']+'  competition.bin\n');verify()
if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('accion',choices=['build','test','verify','spi'])
    action=parser.parse_args().accion
    if action=='build':build()
    elif action=='test':test()
    elif action=='spi':
        check_sources();simulate('rtl_compra_venta',synth()['integracion_cadencias'],41);spi_margin()
    else:verify()
