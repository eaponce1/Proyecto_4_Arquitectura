`timescale 1ns/1ps
module tb_demo_autonoma_trace;
  localparam integer NTICKS=16;
  reg clk=0; always #20 clk=~clk;
  wire [3:0] led;
  integer cycle=0,fetches=0,commits=0,status_reads=0,price_reads=0;
  integer sum_reads=0,ready_reads=0,decision_writes=0,spi_ticks=0,miso_checks=0,lost_ticks=0;
  integer buys=0,sells=0,stage_changes=0;
  reg price_seen=0;
  reg [3:0] prior_stage=0;
  reg [7:0] expected_miso[0:NTICKS-1],expected_write[0:NTICKS-1],expected_price[0:NTICKS-1];
  demo_autonoma_trace_top dut(.i_Clk(clk),.o_LED(led));
  initial begin
    $readmemh("proyecto4/pruebas_fisicas/demo_autonoma_trace/data/expected_decisions.hex",expected_miso);
    $readmemh("proyecto4/pruebas_fisicas/demo_autonoma_trace/data/expected_writes.hex",expected_write);
    $readmemh("proyecto4/pruebas_fisicas/demo_autonoma_trace/data/prices.hex",expected_price);
  end
  always @(posedge clk) begin
    cycle=cycle+1;
    #1;
    if(dut.progress!=prior_stage) begin
      stage_changes=stage_changes+1;
      $display("TRACE stage=%0d LED(D4..D1)=%04b at cycle=%0d",dut.progress,led,cycle);
      if(dut.progress!=prior_stage+1) $fatal(1,"Progress skipped/reversed: old=%0d new=%0d",prior_stage,dut.progress);
      prior_stage=dut.progress;
    end
  end
  always @(posedge clk) begin
    if(dut.instr_req) fetches=fetches+1;
    if(dut.u_soc.u_core.instr_valid_id && !dut.u_soc.u_core.stall) commits=commits+1;
    if(dut.status_read) status_reads=status_reads+1;
    if(dut.price_read) begin price_reads=price_reads+1;price_seen=1;end
    if(dut.sum_read) sum_reads=sum_reads+1;
    if(dut.ready_read) ready_reads=ready_reads+1;
    if(dut.decision_write) begin
      if(!price_seen) $fatal(1,"DECISION before PRICE read");
      if(decision_writes>=NTICKS || dut.data_wdata[7:0]!==expected_write[decision_writes])
        $fatal(1,"DECISION/Python mismatch idx=%0d actual=%02h expected=%02h",decision_writes,dut.data_wdata[7:0],expected_write[decision_writes]);
      if(dut.data_wdata[7:6]==2'b01) buys=buys+1;
      if(dut.data_wdata[7:6]==2'b10) sells=sells+1;
      decision_writes=decision_writes+1;price_seen=0;
    end
    if(dut.spi_byte_done) begin
      if(spi_ticks>0 && dut.price_pending) begin lost_ticks=lost_ticks+1;$fatal(1,"Previous PRICE pending at next frame");end
      if(spi_ticks>0 && (price_reads!=spi_ticks || decision_writes!=spi_ticks))
        $fatal(1,"Previous tick incomplete before next: ticks=%0d reads=%0d decisions=%0d",spi_ticks,price_reads,decision_writes);
      if(spi_ticks>=NTICKS || dut.u_soc.sma_price!==expected_price[spi_ticks])
        $fatal(1,"PRICE/Python mismatch idx=%0d",spi_ticks);
      spi_ticks=spi_ticks+1;
    end
    if(dut.u_master.response_valid_o) begin
      if(miso_checks>=NTICKS || dut.u_master.response_o!==expected_miso[miso_checks])
        $fatal(1,"MISO/Python mismatch idx=%0d actual=%02h expected=%02h",miso_checks,dut.u_master.response_o,expected_miso[miso_checks]);
      miso_checks=miso_checks+1;
    end
  end
  initial begin
    wait(dut.progress==9 && dut.master_done && dut.sent_count==NTICKS && dut.decision_count==NTICKS);
    repeat(3) @(posedge clk);
    if(stage_changes!=9 || led!==4'b1001) $fatal(1,"Trace did not reach expected final stage: changes=%0d LED=%b",stage_changes,led);
    if(fetches==0 || commits==0) $fatal(1,"Espino fetch/commit not observed");
    if(price_reads!=NTICKS || sum_reads!=NTICKS || ready_reads!=NTICKS || decision_writes!=NTICKS || spi_ticks!=NTICKS || miso_checks!=NTICKS || lost_ticks!=0)
      $fatal(1,"Counts PRICE=%0d SUM=%0d READY=%0d DECISION=%0d ticks=%0d MISO=%0d lost=%0d",price_reads,sum_reads,ready_reads,decision_writes,spi_ticks,miso_checks,lost_ticks);
    if(status_reads<NTICKS || buys==0 || sells==0) $fatal(1,"STATUS or strategy coverage incomplete");
    $display("PASS traced integration: 9/9 stages; 16 prices, decisions and MISO match Python; 0 lost ticks; fetch=%0d commit=%0d",fetches,commits);
    $finish;
  end
  initial begin #20000000;$fatal(1,"Trace timeout: progress=%0d sent=%0d decisions=%0d",dut.progress,dut.sent_count,dut.decision_count);end
endmodule
