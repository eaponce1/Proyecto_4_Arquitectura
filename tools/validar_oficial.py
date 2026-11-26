"""Adaptaciones de instancia/rutas/reloj; conserva tarea financiera y cuatro criterios."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import csv,difflib,hashlib,json,re
import trader as t
from modelo_lento import load
ROOT=t.ROOT;OUT=t.OUT/'oficial';DATA=t.OLD/'datos'

def one(label,source):
    raw=source.read_bytes();original=raw.decode('utf-8');s=original
    s=s.replace('localparam string','localparam')
    s=re.sub(r'localparam\s+PROGRAMA\s*=\s*"[^"]*";','localparam PROGRAMA = "sw/trade.hex";',s)
    s=re.sub(r'localparam\s+SERIE\s*=\s*"[^"]*";',f'localparam SERIE = "{(DATA/"practica_meta_2022.csv").relative_to(ROOT).as_posix()}";',s)
    output=(OUT/f'{label}_decisiones.csv').relative_to(ROOT).as_posix()
    s=s.replace('$fopen("decisiones.csv", "w")',f'$fopen("{output}", "w")')
    s=re.sub(r'localparam\s+SALIDA\s*=\s*"[^"]*";',f'localparam SALIDA = "{output}";',s)
    s=s.replace('string encabezado;','reg [8*128-1:0] encabezado;')
    a=s.index('  pochoco_soc #(');b=s.index('));',a)+3
    s=s[:a]+'''  trade_spi_externo #(.ARCHIVO_FIRMWARE(PROGRAMA)) dut (
    .i_Clk(clk),.o_LED(),.i_SPI_SCLK(sclk),.i_SPI_MOSI(mosi),
    .i_SPI_CS_n(cs_n),.o_SPI_MISO(miso));'''+s[b:]
    s=s.replace('always @(posedge clk)','always @(posedge dut.clk_soc)')
    s=s.replace('dut.u_spi.','dut.u_soc.u_spi.').replace('dut.data_addr','dut.u_soc.data_addr')
    s=s.replace('#4000;','#120113;').replace('(PERIODO_NS - SPI_NS) / 40','(PERIODO_NS - SPI_NS) / 80')
    finance=original[original.index('  task automatic ejecutar('):original.index('  endtask',original.index('  task automatic ejecutar('))+9]
    assert finance in s
    criteria=re.findall(r'^\s+chequear\([^;]+;',original,re.M)
    assert len(criteria)==4 and all(c in s for c in criteria)
    target=OUT/f'{label}_adaptado.sv';target.write_text(s,encoding='utf-8')
    (OUT/f'{label}.diff').write_text(''.join(difflib.unified_diff(original.splitlines(True),s.splitlines(True),fromfile=str(source),tofile=str(target))),encoding='utf-8')
    cells=Path(t.shutil.which('yosys')).resolve().parents[1]/'share/yosys/ice40/cells_sim.v'
    exe=OUT/f'{label}.vvp'
    t.command(['iverilog','-g2012','-s','tb_proyecto_4','-o',exe,target,*t.sources(),cells],'oficial_'+label+'_compilacion')
    log=t.command(['vvp','-n',exe],'oficial_'+label)
    assert 'Testbenchs aprobados: 4/4' in log
    rows=list(csv.DictReader((ROOT/output).open(newline='')))
    _,expected=t.run(load(DATA/'practica_meta_2022.csv')[:2000],t.frozen(),True)
    assert len(rows)==2000
    for a,b in zip(rows,expected,strict=True):
        for key in ('tick','precio','caja','acciones','patrimonio'):assert int(a[key])==b[key],(label,key)
        assert int(a['decision'],16)==b['miso']
    assert source.read_bytes()==raw
    print('PASS banco oficial adaptado',label,'2000 ticks 4/4',flush=True)
    return dict(banco=label,ticks=2000,periodo_ns=100000,criterios='4/4',
        tarea_financiera_y_criterios_preservados=True,discrepancias=0,sha256_original=hashlib.sha256(raw).hexdigest(),fuentes=t.signature())

def main():
    OUT.mkdir(parents=True,exist_ok=True)
    with ThreadPoolExecutor(max_workers=2) as pool:
        futures=[pool.submit(one,*job) for job in [('profesor',ROOT/'proyecto4/resultados/validacion_oficial/tb_proyecto_4_profesor.sv'),
                                                  ('repositorio',ROOT/'tb/tb_proyecto_4.sv')]]
        result=[f.result() for f in futures]
    (t.OUT/'bancos_oficiales.json').write_text(json.dumps(result,indent=2))
if __name__=='__main__':main()
