"""Genera el banco aislado de equivalencia y perfil regional por cada tick."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'proyecto4/alternativas/codisenio_lento'
def main():
    tb=(ROOT/'proyecto4/alternativas/candidata_final/tb/tb_candidata.sv').read_text(encoding='utf-8')
    tb=tb.replace('  parameter integer REG_CAJA = -1, REG_ACCIONES = -1;','  parameter integer REG_CAJA = -1, REG_ACCIONES = -1;\n  parameter integer K_START=0, K_END=0, ES_MMIO=1;')
    tb=tb.replace('  integer cargas_mantenidas = 0;','''  integer cargas_mantenidas = 0;
  longint prof_price=-1, prof_start=-1, prof_end=-1;
  integer prof_ic=0, prof_reads=0, prof_writes=0, prof_alu=0;
''')
    marker='      if (dut.commit && (dut.u_soc.dbg_pc_id >= 4 * PALABRAS_FIRMWARE'
    assert marker in tb
    profile='''      if (dut.byte_done) begin
        prof_price=-1; prof_start=-1; prof_end=-1;
        prof_ic=0; prof_reads=0; prof_writes=0; prof_alu=0;
      end
      if (activo && !dut.byte_done) begin
        if (dut.lee_price) prof_price=ciclo;
        if (dut.u_soc.dbg_instr_valid && dut.u_soc.dbg_pc_id==K_START && prof_start<0)
          prof_start=ciclo;
        if (dut.u_soc.dbg_instr_valid && dut.u_soc.dbg_pc_id==K_END && prof_end<0)
          prof_end=ciclo;
        if (dut.commit && dut.u_soc.dbg_pc_id>=K_START && dut.u_soc.dbg_pc_id<K_END) begin
          prof_ic++;
          if (dut.u_soc.dbg_instr_id[6:0]==7'h0b) prof_alu+=2;
          else if ((dut.u_soc.dbg_instr_id[6:0]==7'h13 || dut.u_soc.dbg_instr_id[6:0]==7'h33)
                   && dut.u_soc.dbg_instr_id[14:12]==0) prof_alu++;
        end
        if (dut.u_soc.dbg_data_req && dut.u_soc.dbg_pc_id>=K_START && dut.u_soc.dbg_pc_id<K_END) begin
          if (dut.u_soc.dbg_data_we) prof_writes++; else prof_reads++;
        end
        if (dut.commit && dut.u_soc.dbg_pc_id==K_END) begin
          if (registros[10] !== suma_esperada || registros[13] !== (tick>=9 ? 32'd1 : 32'd0))
            $fatal(1,"Kernel distinto tick=%0d SUM=%0d/%0d READY=%0d",tick,registros[10],suma_esperada,registros[13]);
        end
        if (dut.escribe_decision && (prof_price<llegada || prof_start<prof_price || prof_end<=prof_start || ciclo<prof_end))
          $fatal(1,"Perfil fuera de orden tick=%0d precio=%0d inicio=%0d fin=%0d",tick,prof_price,prof_start,prof_end);
      end
'''
    tb=tb.replace(marker,profile+marker)
    tb=tb.replace('!vio_sum || !vio_ready','(ES_MMIO && (!vio_sum || !vio_ready))')
    tb=tb.replace('ic,ciclos,cpi");','ic,ciclos,cpi,kernel_ciclos,kernel_ic,kernel_lecturas,kernel_escrituras,rx_ciclos,cartera_ciclos,decision_ciclos,alu_kernel");')
    old='"%0d,%0d,%0d,%02h,%02h,%0d,%0d,%0d,%0d,%0d,%0d,%0d,%0d,%0d,%0d,%.6f",'
    assert old in tb
    tb=tb.replace(old,'"%0d,%0d,%0d,%02h,%02h,%0d,%0d,%0d,%0d,%0d,%0d,%0d,%0d,%0d,%0d,%.6f,%0d,%0d,%0d,%0d,%0d,%0d,%0d,%0d",')
    old='suma_esperada, status_leidos, ic, latencia, real\'(latencia) / ic);'
    assert old in tb
    tb=tb.replace(old,"suma_esperada, status_leidos, ic, latencia, real'(latencia) / ic,\n                            prof_end-prof_start,prof_ic,prof_reads,prof_writes,prof_price-llegada,\n                            prof_start-prof_price,latencia+llegada-prof_end,prof_alu);")
    OUT.mkdir(parents=True,exist_ok=True)
    (OUT/'tb_codisenio.sv').write_text(tb,encoding='utf-8')
    print('PASS banco con equivalencia CPU/SPI/cartera y perfil de regiones')
if __name__=='__main__':main()
