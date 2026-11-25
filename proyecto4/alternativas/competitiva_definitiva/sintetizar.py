"""Entrega un solo BIN después de las puertas digitales, área, timing y netlist."""
from estrategia import *
from validar_rtl import sources, signature, command, simulate, BUILD, OUT, ROOT
import hashlib
import re
import shutil

def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def main():
    target=BUILD/'competition.bin'
    assert not target.exists(),'BIN existente: usar otra copia limpia para repetir la sintesis'
    interp=json.loads((OUT/'equivalencia_rv32e.json').read_text())
    full=json.loads((OUT/'equivalencia_verilator.json').read_text())
    stress=json.loads((OUT/'equivalencia_rtl.json').read_text())
    banks=json.loads((OUT/'bancos_oficiales.json').read_text())
    assert interp['hex_sha256']==full['sha256_hex']==sha(HERE/'trade.hex')
    assert interp['asm_sha256']==sha(HERE/'trade.s')
    assert len([r for r in interp['series'] if r['ticks']==20000 and r['discrepancias']==0])==8
    assert len(full['series'])==8 and all(r['ticks']==20000 and r['discrepancias']==0 for r in full['series'])
    assert len(banks)==2 and all(r['tests']=='4/4' for r in banks)
    assert {r['periodo_ns'] for r in stress} >= {100000,1000000,10000000}
    assert all(r['discrepancias']==0 and r['margen_ciclos']>0 for r in stress)
    # Reject stale evidence from any different source or firmware revision.
    current_signature=signature()
    assert full['fuentes']==current_signature
    assert all(r['fuentes']==current_signature for r in stress+banks)
    fw=(HERE/'trade.hex').relative_to(ROOT).as_posix();words=interp['words']
    # Explicit manifest binds every synthesised source to the validated run.
    src=sources();manifest={str(p.relative_to(ROOT)):sha(p) for p in src}
    manifest[str((HERE/'trade.hex').relative_to(ROOT))]=sha(HERE/'trade.hex')
    pcf=ROOT/'proyecto4/pruebas_fisicas/spi_externo_robusto/goboard_spi_externo.pcf'
    base=dict(re.findall(r'^set_io (\S+) (\d+)$',(ROOT/'goboard.pcf').read_text(),re.M))
    pins=re.findall(r'^set_io (\S+) (\d+)$',pcf.read_text(),re.M)
    assert len(pins)==9 and len(set(p for _,p in pins))==9 and all(base[s]==p for s,p in pins)
    manifest[str(pcf.relative_to(ROOT))]=sha(pcf)
    (BUILD/'fuentes_validadas.json').write_text(json.dumps(manifest,indent=2))
    net=BUILD/'trade.json';asc=BUILD/'trade.asc';report=BUILD/'timing.json'
    names=' '.join('"'+p.relative_to(ROOT).as_posix()+'"' for p in src)
    y=command(['yosys','-p',f'read_verilog -sv {names}; '
        f'chparam -set PALABRAS_FIRMWARE {words} -set ARCHIVO_FIRMWARE "{fw}" trade_spi_externo; '
        f'synth_ice40 -dff -top trade_spi_externo; check -assert; stat; write_json "{net.as_posix()}"'],BUILD/'yosys.log')
    pn=command(['nextpnr-ice40','--hx1k','--package','vq100','--freq','25','--seed','1','--json',net,
        '--pcf',pcf,'--asc',asc,'--report',report],BUILD/'nextpnr.log')
    lc=int(re.search(r'ICESTORM_LC:\s*(\d+)',pn)[1]);bram=int(re.search(r'ICESTORM_RAM:\s*(\d+)',pn)[1])
    clocks=json.loads(report.read_text())['fmax']
    assert lc<=1280 and bram<=16 and min(c['achieved'] for c in clocks.values())>=25
    mapped=BUILD/'trade_netlist.v'
    command(['yosys','-Q','-q','-p',f'read_json "{net.as_posix()}"; write_verilog -noattr "{mapped.as_posix()}"'],BUILD/'netlist.log')
    gates=[]
    for phase in (0,41):gates.append(simulate('integracion_cadencias',48,100000,phase,mapped))
    for p,h in manifest.items():assert sha(ROOT/p)==h,'La fuente cambio durante la sintesis'
    tmp=BUILD/'competition.tmp'
    command(['icepack',asc,tmp],BUILD/'icepack.log');assert tmp.stat().st_size==32220
    tmp.rename(target)
    result=dict(lc=lc,bram=bram,clocks=clocks,netlist=gates,sha256_bin=sha(target),sha256_hex=sha(HERE/'trade.hex'),
       physical_test='PENDIENTE',top='trade_spi_externo',soc_mhz=12.5,input_mhz=25)
    (BUILD/'resultados.json').write_text(json.dumps(result,indent=2))
    (HERE/'SHA256_entrega.txt').write_text('\n'.join(sha(p)+'  '+str(p.relative_to(HERE)) for p in
        [target,HERE/'trade.hex',HERE/'trade.s',BUILD/'trade.json',BUILD/'trade.asc',BUILD/'trade_netlist.v'])+'\n')
    print('PASS BIN',result,flush=True)

if __name__=='__main__':main()
