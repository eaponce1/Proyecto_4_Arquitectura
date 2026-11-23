`timescale 1ns/1ps
module tb_agente_completo;
  reg clk=0; always #20 clk=~clk;
  wire [3:0] led;
  integer ticks=0, status_reads=0, price_reads=0, sum_reads=0, ready_reads=0;
  integer decision_writes=0, commits=0, fetches=0, miso_x=0;
  integer reset_low_seen=0, reset_high_seen=0;
  reg [7:0] expected_write [0:15];
  reg price_seen=0;
  agente_completo_top dut(.i_Clk(clk),.o_LED(led));
  initial $readmemh("proyecto4/pruebas_fisicas/agente_completo/data/expected_writes.hex", expected_write);
  always @(posedge clk) begin
    if(!dut.u_soc.dbg_reset_released) reset_low_seen=1; else reset_high_seen=1;
    if(dut.u_soc.dbg_instr_req) fetches=fetches+1;
    if(dut.u_soc.u_core.instr_valid_id && !dut.u_soc.u_core.stall) commits=commits+1;
    if(dut.u_soc.dbg_status_read) status_reads=status_reads+1;
    if(dut.u_soc.dbg_price_read) begin price_reads=price_reads+1; price_seen=1; end
    if(dut.u_soc.dbg_sum_read) sum_reads=sum_reads+1;
    if(dut.u_soc.dbg_ready_read) ready_reads=ready_reads+1;
    if(dut.u_soc.dbg_decision_write) begin
      if(!price_seen) $fatal(1,"DECISION antes de PRICE");
      if(decision_writes>=16 || dut.u_soc.dbg_data_wdata[7:0]!==expected_write[decision_writes])
        $fatal(1,"DECISION escrita distinta de Python: idx=%0d got=%02h expected=%02h",decision_writes,dut.u_soc.dbg_data_wdata[7:0],expected_write[decision_writes]);
      decision_writes=decision_writes+1; price_seen=0;
    end
    if(dut.u_generator.rx_valid_o) begin
      ticks=ticks+1;
      if(^dut.u_generator.rx_byte_o===1'bx) miso_x=miso_x+1;
    end
    if(dut.u_soc.u_spi.byte_done && dut.u_soc.u_spi.new_price_q && ticks>1)
      $fatal(1,"Precio previo no consumido: posible tick perdido");
  end
  initial begin
    wait(led[3]===1'b1);
    repeat(4) @(posedge clk);
    if(ticks!=16 || dut.u_verifier.checked_o!=16 || dut.u_verifier.error_o)
      $fatal(1,"MISO incorrecto ticks=%0d checked=%0d err=%b",ticks,dut.u_verifier.checked_o,dut.u_verifier.error_o);
    if(fetches==0 || commits==0) $fatal(1,"Espino no tuvo fetch/commit");
    if(!reset_low_seen || !reset_high_seen) $fatal(1,"No se observo asercion y liberacion de reset");
    if(status_reads<16 || price_reads<16 || decision_writes<16)
      $fatal(1,"Accesos incompletos STATUS=%0d PRICE=%0d DECISION=%0d",status_reads,price_reads,decision_writes);
    if(sum_reads<7 || ready_reads<7) $fatal(1,"Acelerador SMA10 insuficientemente consultado SUM=%0d READY=%0d",sum_reads,ready_reads);
    if(miso_x!=0) $fatal(1,"MISO contiene X");
    $display("PASS agente completo: reset_low=%0d reset_released=%0d ticks=%0d fetch=%0d commit=%0d STATUS=%0d PRICE=%0d SUM10=%0d READY=%0d DECISION=%0d MISO_check=%0d",reset_low_seen,reset_high_seen,ticks,fetches,commits,status_reads,price_reads,sum_reads,ready_reads,decision_writes,dut.u_verifier.checked_o);
    $finish;
  end
  initial begin #200000000; $fatal(1,"Timeout agente completo"); end
endmodule
