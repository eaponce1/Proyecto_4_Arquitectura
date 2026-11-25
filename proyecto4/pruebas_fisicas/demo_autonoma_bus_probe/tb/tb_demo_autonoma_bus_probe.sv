`timescale 1ns/1ps
module tb_demo_autonoma_bus_probe;
 localparam integer N=16;
 reg clk=0;always #20 clk=~clk;
 wire [3:0] led;
 integer cyc=0,bytes=0,status_n=0,price_n=0,sum_n=0,ready_n=0,dec_n=0,miso_n=0;
 integer first_status=0,first_response=0,first_pc_resume=0,first_byte_cycle=0,stalled=0;
 reg [7:0] prices[0:N-1],decisions[0:N-1],miso[0:N-1];
 reg after_req=0;reg [31:0] saved_pc;
 demo_autonoma_bus_probe_top dut(.i_Clk(clk),.o_LED(led));
 initial begin
  $readmemh("proyecto4/pruebas_fisicas/demo_autonoma_bus_probe/data/prices.hex",prices);
  $readmemh("proyecto4/pruebas_fisicas/demo_autonoma_bus_probe/data/expected_writes.hex",decisions);
  $readmemh("proyecto4/pruebas_fisicas/demo_autonoma_bus_probe/data/expected_decisions.hex",miso);
 end
 always @(posedge clk) begin
  cyc=cyc+1;
  if(dut.u_soc.dbg_data_req && dut.u_soc.dbg_instr_req===1'b0) stalled=stalled+1;
  if(dut.spi_byte_done) begin
   if(bytes>=N || dut.u_soc.dbg_price!==prices[bytes])$fatal(1,"PRICE mismatch idx=%0d got=%0d",bytes,dut.u_soc.dbg_price);
   bytes=bytes+1;
   if(bytes==1)begin first_byte_cycle=cyc;$display("BUS first byte_done cycle=%0d PRICE=%0d",cyc,dut.u_soc.dbg_price);end
  end
  if(cyc>=499 && cyc<530)
   $display("BUS trace cycle=%0d byte_done=%b status=%b req=%b we=%b addr=%08h rdata=%08h spi_rdata=%08h instr_req=%b pc=%08h",cyc,dut.spi_byte_done,dut.u_soc.dbg_status_read,dut.u_soc.dbg_data_req,dut.u_soc.dbg_data_we,dut.u_soc.dbg_data_addr,dut.u_soc.dbg_data_rdata,dut.u_soc.dbg_spi_rdata,dut.u_soc.dbg_instr_req,dut.u_soc.dbg_instr_addr);
  if(dut.u_soc.dbg_data_req) begin
   if(bytes>0 && first_status==0 && cyc>first_byte_cycle+1) begin
    if(dut.u_soc.dbg_data_we!==0 || dut.u_soc.dbg_data_addr!==32'h80010000)
      $fatal(1,"First post-price bus operation wrong: req=%b we=%b addr=%08h",dut.u_soc.dbg_data_req,dut.u_soc.dbg_data_we,dut.u_soc.dbg_data_addr);
    if(dut.u_soc.dbg_data_be!==4'b1111)$fatal(1,"Unexpected STATUS byte enables %b",dut.u_soc.dbg_data_be);
    if(dut.u_soc.dbg_instr_req!==0)$fatal(1,"Expected IF stall while STATUS load is outstanding");
    first_status=cyc;saved_pc=dut.u_soc.dbg_instr_addr;status_n=1;after_req=1;
    $display("BUS STATUS request cycle=%0d req=%b we=%b addr=%08h be=%b PC=%08h instr_req=%b",cyc,dut.u_soc.dbg_data_req,dut.u_soc.dbg_data_we,dut.u_soc.dbg_data_addr,dut.u_soc.dbg_data_be,saved_pc,dut.u_soc.dbg_instr_req);
   end
  end
  if(after_req) begin
   if(dut.u_soc.dbg_data_rdata[0]===1'b1 && dut.u_soc.dbg_spi_rdata[0]===1'b1) begin
    if(dut.u_soc.dbg_data_rdata!==32'h00000003)$fatal(1,"Unexpected STATUS word %08h",dut.u_soc.dbg_data_rdata);
    if(dut.u_soc.dbg_instr_req!==1 || dut.u_soc.dbg_instr_addr!==saved_pc)
      $fatal(1,"Core did not leave memory stall cleanly: instr_req=%b PC=%08h expected PC=%08h",dut.u_soc.dbg_instr_req,dut.u_soc.dbg_instr_addr,saved_pc);
    first_response=cyc;after_req=0;
    $display("BUS STATUS response cycle=%0d data_rdata=%08h spi_rdata=%08h",cyc,dut.u_soc.dbg_data_rdata,dut.u_soc.dbg_spi_rdata);
   end else if(cyc-first_status>4) after_req=0;
  end
  if(first_response && !first_pc_resume && dut.u_soc.dbg_instr_req && dut.u_soc.dbg_instr_addr!=saved_pc) begin
   first_pc_resume=cyc;
   $display("BUS PC resumed cycle=%0d old=%08h new=%08h",cyc,saved_pc,dut.u_soc.dbg_instr_addr);
  end
  if(dut.u_soc.dbg_status_read) status_n=status_n+1;
  if(dut.u_soc.dbg_price_read) price_n=price_n+1;
  if(dut.u_soc.dbg_sum_read) sum_n=sum_n+1;
  if(dut.u_soc.dbg_ready_read) ready_n=ready_n+1;
  if(dut.u_soc.dbg_decision_write) begin
   if(dec_n>=N || dut.u_soc.dbg_data_wdata[7:0]!==decisions[dec_n])$fatal(1,"DECISION mismatch idx=%0d data=%02h",dec_n,dut.u_soc.dbg_data_wdata[7:0]);
   dec_n=dec_n+1;
  end
  if(dut.response_valid) begin
   if(miso_n>=N || dut.response!==miso[miso_n])$fatal(1,"MISO mismatch idx=%0d got=%02h",miso_n,dut.response);
   miso_n=miso_n+1;
  end
 end
 initial begin
  wait(dut.master_done && dec_n==N && bytes==N);
  repeat(3) @(posedge clk);
  if(first_status==0 || first_response==0 || first_pc_resume==0)$fatal(1,"STATUS path incomplete request=%0d response=%0d pc=%0d",first_status,first_response,first_pc_resume);
  if(price_n!=N || sum_n!=N || ready_n!=N || miso_n!=N)$fatal(1,"Counts PRICE=%0d SUM=%0d READY=%0d MISO=%0d",price_n,sum_n,ready_n,miso_n);
  if(stalled==0 || dut.stage!=5)$fatal(1,"Expected memory stall and final PC-progress stage, stalls=%0d stage=%h",stalled,dut.stage);
  $display("PASS bus probe ticks=%0d STATUS req/response/PC=%0d/%0d/%0d cycles; STATUS reads=%0d; stalls=%0d; LED=%b",bytes,first_status,first_response,first_pc_resume,status_n,stalled,led);
  $finish;
 end
 initial begin #20000000;$fatal(1,"timeout bus probe LED=%b bytes=%0d status=%0d bus_req=%b addr=%08h data=%08h pc=%08h instr_req=%b",led,bytes,status_n,dut.u_soc.dbg_data_req,dut.u_soc.dbg_data_addr,dut.u_soc.dbg_data_rdata,dut.u_soc.dbg_instr_addr,dut.u_soc.dbg_instr_req);end
endmodule
