`timescale 1ns/1ps
module tb_demo_autonoma_handshake;
  localparam integer NTICKS=16;
  reg clk=0; always #20 clk=~clk;
  wire [3:0] led;
  integer cycles=0,fetches=0,commits=0,status_reads=0,price_reads=0;
  integer sum_reads=0,ready_reads=0,decision_writes=0,spi_ticks=0,miso_checks=0;
  integer lost_ticks=0,buys=0,sells=0,max_price_latency=0,latency_sum=0;
  integer min_read_to_next_price=32'h7fffffff;
  integer byte_cycle=0,price_read_cycle=0;
  reg price_seen=0;
  reg [7:0] expected_miso[0:NTICKS-1];
  reg [7:0] expected_write[0:NTICKS-1];
  reg [7:0] expected_price[0:NTICKS-1];
  demo_autonoma_handshake_top dut(.i_Clk(clk),.o_LED(led));
  initial begin
    $readmemh("proyecto4/pruebas_fisicas/demo_autonoma_handshake/data/expected_decisions.hex",expected_miso);
    $readmemh("proyecto4/pruebas_fisicas/demo_autonoma_handshake/data/expected_writes.hex",expected_write);
    $readmemh("proyecto4/pruebas_fisicas/demo_autonoma_handshake/data/prices.hex",expected_price);
  end
  always @(posedge clk) begin
    cycles=cycles+1;
    if(dut.instr_req) fetches=fetches+1;
    if(dut.u_soc.u_core.instr_valid_id && !dut.u_soc.u_core.stall) commits=commits+1;
    if(dut.status_read) status_reads=status_reads+1;
    if(dut.price_read) begin
      price_reads=price_reads+1; price_seen=1;
      price_read_cycle=cycles;
      if(cycles-byte_cycle>max_price_latency) max_price_latency=cycles-byte_cycle;
      latency_sum=latency_sum+(cycles-byte_cycle);
    end
    if(dut.sum_read) sum_reads=sum_reads+1;
    if(dut.ready_read) ready_reads=ready_reads+1;
    if(dut.decision_write) begin
      if(!price_seen) $fatal(1,"DECISION without current PRICE read");
      if(decision_writes>=NTICKS || dut.data_wdata[7:0]!==expected_write[decision_writes])
        $fatal(1,"DECISION differs from Python idx=%0d actual=%02h expected=%02h",decision_writes,dut.data_wdata[7:0],expected_write[decision_writes]);
      if(dut.data_wdata[7:6]==2'b01) buys=buys+1;
      if(dut.data_wdata[7:6]==2'b10) sells=sells+1;
      decision_writes=decision_writes+1; price_seen=0;
    end
    if(dut.spi_byte_done) begin
      if(spi_ticks>0 && dut.price_pending) begin lost_ticks=lost_ticks+1;$fatal(1,"price_pending remained set at next byte");end
      if(spi_ticks>0 && (price_reads!=spi_ticks || decision_writes!=spi_ticks))
        $fatal(1,"Previous price not fully handled before next tick: ticks=%0d reads=%0d decisions=%0d",spi_ticks,price_reads,decision_writes);
      if(spi_ticks>0 && cycles-price_read_cycle<min_read_to_next_price)
        min_read_to_next_price=cycles-price_read_cycle;
      if(spi_ticks>0 && cycles-price_read_cycle<6000)
        $fatal(1,"Next frame violated post-ack minimum gap: %0d cycles",cycles-price_read_cycle);
      if(spi_ticks>=NTICKS || dut.u_soc.sma_price!==expected_price[spi_ticks])
        $fatal(1,"Received PRICE differs idx=%0d actual=%0d expected=%0d",spi_ticks,dut.u_soc.sma_price,expected_price[spi_ticks]);
      spi_ticks=spi_ticks+1; byte_cycle=cycles;
    end
    if(dut.u_master.response_valid_o) begin
      if(miso_checks>=NTICKS || dut.u_master.response_o!==expected_miso[miso_checks])
        $fatal(1,"MISO differs idx=%0d actual=%02h expected=%02h",miso_checks,dut.u_master.response_o,expected_miso[miso_checks]);
      miso_checks=miso_checks+1;
    end
  end
  initial begin
    wait(dut.master_done && dut.sent_count==NTICKS && dut.decision_count==NTICKS);
    repeat(3) @(posedge clk);
    if(dut.error_code!==0 || led!==4'b0001) $fatal(1,"Success LEDs/code incorrect: code=%b LED=%b",dut.error_code,led);
    if(fetches==0 || commits==0) $fatal(1,"Espino did not fetch/commit");
    if(status_reads<NTICKS || price_reads!=NTICKS || sum_reads!=NTICKS || ready_reads!=NTICKS)
      $fatal(1,"MMIO incomplete STATUS=%0d PRICE=%0d SUM=%0d READY=%0d",status_reads,price_reads,sum_reads,ready_reads);
    if(spi_ticks!=NTICKS || decision_writes!=NTICKS || miso_checks!=NTICKS || lost_ticks!=0)
      $fatal(1,"Counts ticks=%0d decisions=%0d miso=%0d lost=%0d",spi_ticks,decision_writes,miso_checks,lost_ticks);
    if(buys==0 || sells==0) $fatal(1,"Expected sequence did not exercise buy and sell");
    $display("PASS handshake integration: ticks=%0d reads=%0d decisions=%0d MISO=%0d max_PRICE_latency=%0d cycles (%.2f us) mean=%.2f cycles min_read_to_next_price=%0d cycles fetch=%0d commit=%0d",
      spi_ticks,price_reads,decision_writes,miso_checks,max_price_latency,max_price_latency*0.04,latency_sum/16.0,min_read_to_next_price,fetches,commits);
    $finish;
  end
  initial begin #20000000;$fatal(1,"Timeout: sent=%0d decisions=%0d code=%b",dut.sent_count,dut.decision_count,dut.error_code);end
endmodule
