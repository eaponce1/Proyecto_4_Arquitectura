"""Linux/WSL: simula netlist/BIN reconstruido con bancos estrictos, sin acceder a FPGA."""
from pathlib import Path
import hashlib,json,os,shutil,subprocess,sys,time
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'build/trader'
def cmd(args,path):
    start=time.perf_counter()
    p=subprocess.run([str(x) for x in args],cwd=ROOT,capture_output=True,text=True)
    path.write_text(p.stdout+p.stderr+f'\nSalida={p.returncode}; segundos={time.perf_counter()-start:.3f}\n')
    assert p.returncode==0,(path,(p.stdout+p.stderr)[-2500:])
    return p.stdout
def main():
    netlist=ROOT/sys.argv[1];kind=sys.argv[2]
    sourcehash=hashlib.sha256(netlist.read_bytes()).hexdigest()
    folder=OUT/f'puertas_{kind}';folder.mkdir(exist_ok=True)
    tool=os.environ.get('POCH_VERILATOR','verilator')
    cells=Path('/mnt/c/Tools/oss-cad-suite/share/yosys/ice40/cells_sim.v')
    if not cells.exists():cells=Path(shutil.which('yosys')).resolve().parents[1]/'share/yosys/ice40/cells_sim.v'
    common=[tool,'--binary','--timing','--assert','--language','1800-2017','-DNO_ICE40_DEFAULT_ASSIGNMENTS',
        '-DNETLIST','-Wno-fatal','-j','2']
    if kind=='bin':
        # El modelo de rutas con retardos converge mucho mejor en Icarus.
        # Ademas verifica cuatro estados, a diferencia de Verilator.
        exe=folder/'bin.vvp'
        cmd(['iverilog','-g2012','-DNETLIST','-s','tb_spi_margen','-o',exe,
             ROOT/'tb/tb_spi_margen.sv',netlist,cells],folder/'compilacion_icarus.log')
        tests=[]
        for setup in (20,40,1000):
            label=f'spi_bin_cs{setup}'
            log=cmd(['vvp','-n',exe,'+vectores=build/trader/rtl_compra_venta',f'+setup_ns={setup}'],folder/f'{label}.log')
            assert 'PASS SPI CS corto 396 ticks' in log
            tests.append(dict(nombre=label,ticks=396,setup_ns=setup,periodo_ns=40000,discrepancias=0,
                simulador='Icarus cuatro estados',retardo_funcional_uniforme_ns=1,
                log=(folder/f'{label}.log').relative_to(ROOT).as_posix()))
            print('PASS BIN cuatro estados',label,flush=True)
        assert hashlib.sha256(netlist.read_bytes()).hexdigest()==sourcehash
        (OUT/'validacion_bin.json').write_text(json.dumps(dict(sha256_netlist=sourcehash,tests=tests),indent=2))
        return
    obj=Path('/tmp')/('pochoco_lenta_puertas_'+kind)
    cmd([*common,'--top-module','tb_spi_margen','--Mdir',obj,
        ROOT/'tb/tb_spi_margen.sv',netlist,cells],folder/'compilacion_spi.log')
    tests=[]
    for setup in (20,40,1000):
        label=f'spi_{kind}_cs{setup}'
        log=cmd([obj/'Vtb_spi_margen','+vectores=build/trader/rtl_compra_venta',f'+setup_ns={setup}'],folder/f'{label}.log')
        assert 'PASS SPI CS corto 396 ticks' in log
        tests.append(dict(nombre=label,ticks=396,setup_ns=setup,periodo_ns=40000,discrepancias=0,
            simulador='Verilator dos estados',log=(folder/f'{label}.log').relative_to(ROOT).as_posix()))
        print('PASS puertas',label,flush=True)
    if kind=='netlist':
        obj2=Path('/tmp/pochoco_lenta_puertas_contabilidad')
        cmd([*common,'--top-module','tb_candidata','--Mdir',obj2,'-GTICKS=396','-GPERIODO_NS=40000',
            ROOT/'proyecto4/alternativas/candidata_final/tb/tb_candidata.sv',netlist,cells],folder/'compilacion_cartera.log')
        log=cmd([obj2/'Vtb_candidata','+vectores=build/trader/rtl_compra_venta',
            '+metricas=build/trader/puertas_netlist/decisiones.csv'],folder/'cartera.log')
        assert 'PASS 396 MISO frente a Python' in log
        tests.append(dict(nombre='netlist_contabilidad',ticks=396,periodo_ns=40000,discrepancias=0))
    assert hashlib.sha256(netlist.read_bytes()).hexdigest()==sourcehash
    (OUT/f'validacion_{kind}.json').write_text(json.dumps(dict(sha256_netlist=sourcehash,tests=tests),indent=2))
if __name__=='__main__':main()
