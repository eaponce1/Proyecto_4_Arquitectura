"""Pruebas de las unidades reales usadas por las variantes de co-diseno."""
import json
from medir_codisenio_lento import ROOT,ALT,BUILD,OUT,command,cells,sha
from preparar_codisenio_lento import assemble
def main():
    records=[];folder=BUILD/'unidades';folder.mkdir(parents=True,exist_ok=True)
    custom=[ALT/'tb_custom0_unit.sv',ALT/'custom0/rtl/espino_alu.v',ALT/'custom0/rtl/espino_decoder.v']
    for name,top,src in [('custom0','tb_custom0_unit',custom),
        ('mmio_incremental','tb_sma10_unit',[ALT/'tb_sma10_unit.sv',ROOT/'rtl/trader/pochoco_sma10.v',cells()]),
        ('mmio_scan','tb_sma10_unit',[ALT/'tb_sma10_unit.sv',ALT/'mmio_scan/rtl/pochoco_sma10.v',cells()])]:
        exe=folder/(name+'.vvp')
        command(['iverilog','-g2012','-s',top,'-o',exe,*src],folder/(name+'_compile.log'))
        output=command(['vvp','-n',exe],folder/(name+'.log'));assert 'PASS' in output
        records.append(dict(unidad=name,estado='PASS',salida=output.splitlines()[0],
            fuentes={p.relative_to(ROOT).as_posix():sha(p) for p in src if p.is_relative_to(ROOT)},
            log=(folder/(name+'.log')).relative_to(ROOT).as_posix()))
        print(records[-1]['salida'])
    _,words=assemble('smaupd x10, x12, x3\n');assert words==[(3<<20)|(12<<15)|(10<<7)|0x0b]
    for line in ('smaupd x16,x12,x3','smaupd x10,x16,x3','smaupd x10,x12,x16','slli x10,x10,1'):
        try:assemble(line)
        except ValueError:continue
        raise AssertionError('Ensamblador acepto: '+line)
    records.append(dict(unidad='assembler_custom0',estado='PASS',salida='Codificacion de campos, RV32E y rechazo de shifts'))
    OUT.mkdir(parents=True,exist_ok=True);(OUT/'unidades.json').write_text(json.dumps(records,indent=2),encoding='utf-8')
if __name__=='__main__':main()
