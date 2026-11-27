"""Genera variantes aisladas de la politica vigente; no modifica el BIN activo."""
from pathlib import Path
import hashlib,importlib.util,json,subprocess
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'proyecto4/alternativas/codisenio_lento'
CUSTOM_ORIGIN='proyecto4/alternativas/custom0/rtl/espino_core/'
INIT='''    addi x8, x0, 1024
    sw x0, 0(x8)
    sw x0, 4(x8)
    sw x0, 8(x8)
    addi x8, x0, 1040
    addi x9, x0, 10
LIMPIAR_HISTORIA:
    sw x0, 0(x8)
    addi x8, x8, 4
    addi x9, x9, -1
    bne x9, x0, LIMPIAR_HISTORIA
'''
KERNEL='''    addi x8, x0, 1024
    lw x9, 0(x8)
    addi x11, x0, 1040
    add x11, x11, x9
    lw x12, 0(x11)
    sw x3, 0(x11)
    lw x10, 8(x8)
{update}
    sw x10, 8(x8)
    addi x9, x9, 4
    addi x11, x0, 40
    bne x9, x11, GUARDAR_PUNTERO
    addi x9, x0, 0
GUARDAR_PUNTERO:
    sw x9, 0(x8)
    lw x13, 4(x8)
    addi x11, x0, 10
    bge x13, x11, HISTORIA_LLENA
    addi x13, x13, 1
    sw x13, 4(x8)
HISTORIA_LLENA:
    addi x11, x0, 10
    blt x13, x11, HISTORIA_INCOMPLETA
    addi x13, x0, 1
    jal x0, KERNEL_END
HISTORIA_INCOMPLETA:
    addi x13, x0, 0
'''
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def assembler():
    spec=importlib.util.spec_from_file_location('base_assembler',ROOT/'sw/assembler.py')
    mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod);return mod
def assemble(text):
    asm=assembler();labels,instructions=asm.analizar_programa(text.splitlines());words=[]
    for pc,line in instructions:
        a=line.replace(',',' ').split()
        if a[0]=='smaupd':
            assert len(a)==4
            rd,rs1,rs2=map(asm.registro,a[1:]);words.append((rs2<<20)|(rs1<<15)|(rd<<7)|0x0b)
        else:words.append(asm.codificar_instruccion(line,pc,labels))
    assert len(words)<256
    return labels,words
def main():
    original=(ROOT/'sw/trade.s').read_text(encoding='utf-8')
    old='    lw    x10, 12(x1)         # SUM10\n    lw    x13, 16(x1)         # READY'
    assert old in original
    variants={}
    for variant in ('software','custom0','mmio'):
        folder=OUT/variant;folder.mkdir(parents=True,exist_ok=True)
        if variant=='mmio':text=original.replace(old,'KERNEL_START:\n'+old+'\nKERNEL_END:')
        else:
            update='    smaupd x10, x12, x3' if variant=='custom0' else '    sub x10, x10, x12\n    add x10, x10, x3'
            text=original.replace('POLL_STATUS:\n',INIT+'\nPOLL_STATUS:\n',1).replace(old,'KERNEL_START:\n'+KERNEL.format(update=update)+'KERNEL_END:')
        labels,words=assemble(text)
        (folder/'trade.s').write_text(text,encoding='utf-8')
        if variant=='mmio':
            assert words==[int(w,16) for w in (ROOT/'sw/trade.hex').read_text().split()]
            (folder/'trade.hex').write_bytes((ROOT/'sw/trade.hex').read_bytes())
        else:(folder/'trade.hex').write_text(''.join(f'{w:08x}\n' for w in words),encoding='ascii')
        variants[variant]=dict(palabras=len(words),kernel_start=labels['KERNEL_START'],kernel_end=labels['KERNEL_END'],
            sha256_s=sha(folder/'trade.s'),sha256_hex=sha(folder/'trade.hex'),etiquetas=labels)
        if variant=='mmio':continue
        rtl=folder/'rtl';rtl.mkdir(exist_ok=True)
        top=(ROOT/'rtl/trade_spi_externo.v').read_text().replace('PALABRAS_FIRMWARE = 130',f'PALABRAS_FIRMWARE = {len(words)}').replace('sw/trade.hex',(folder/'trade.hex').relative_to(ROOT).as_posix())
        (rtl/'trade_spi_externo.v').write_text(top,encoding='utf-8')
        soc=(ROOT/'rtl/trader/pochoco_soc_cpu_trace.v').read_text()
        a=soc.index('  pochoco_sma10 u_sma10(');b=soc.index('  assign dbg_spi_byte_done',a)
        soc=soc[:a]+"  assign sma_sum=12'b0;\n  assign sma_ready=1'b0;\n"+soc[b:]
        (rtl/'pochoco_soc_cpu_trace.v').write_text(soc,encoding='utf-8')
    origin=[];custom=OUT/'custom0/rtl'
    for name in ('espino_alu.v','espino_decoder.v','espino_id_stage.v','espino_register_file.v','espino_core.v'):
        raw=subprocess.check_output(['git','show','66eede4:'+CUSTOM_ORIGIN+name],cwd=ROOT)
        (custom/name).write_bytes(raw);origin.append(dict(ruta=CUSTOM_ORIGIN+name,commit='66eede4',sha256=hashlib.sha256(raw).hexdigest()))
    core=(ROOT/'rtl/trader/espino_core_cpu_trace.v').read_text()
    changes=[('rf_raddr_a, rf_raddr_b, rf_waddr','rf_raddr_a, rf_raddr_b, rf_raddr_c, rf_waddr'),
        ('rf_rdata_a, rf_rdata_b, rf_wdata','rf_rdata_a, rf_rdata_b, rf_rdata_c, rf_wdata'),
        ('.rf_raddr_b_o   (rf_raddr_b),','.rf_raddr_b_o   (rf_raddr_b),\n    .rf_raddr_c_o   (rf_raddr_c),'),
        ('.rf_rdata_b_i   (rf_rdata_b),','.rf_rdata_b_i   (rf_rdata_b),\n    .rf_rdata_c_i   (rf_rdata_c),'),
        ('.raddr_b_i (rf_raddr_b),','.raddr_b_i (rf_raddr_b),\n    .raddr_c_i (rf_raddr_c),'),
        ('.rdata_b_o (rf_rdata_b),','.rdata_b_o (rf_rdata_b),\n    .rdata_c_o (rf_rdata_c),')]
    for a,b in changes:assert core.count(a)==1,a;core=core.replace(a,b)
    (custom/'espino_core_cpu_trace.v').write_text(core,encoding='utf-8')
    (OUT/'variantes.json').write_text(json.dumps(dict(reloj_MHz=12.5,politica='SUM10/128/5%',
        bin_activo_sha256=sha(ROOT/'competition.bin'),origen_custom0=origin,variantes=variants),indent=2),encoding='utf-8')
    print('PASS variantes aisladas:',[(k,v['palabras']) for k,v in variants.items()])
    from preparar_mmio_scan import main as scan
    scan()
if __name__=='__main__':main()
