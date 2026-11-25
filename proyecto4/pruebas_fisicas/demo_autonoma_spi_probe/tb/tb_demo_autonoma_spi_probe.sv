`timescale 1ns/1ps
module tb_demo_autonoma_spi_probe;
  localparam integer NTICKS=16;
  reg clk=0; always #20 clk=~clk;
  wire [3:0] led;
  integer cycle=0,master_edges=0,shadow_edges=0,byte_dones=0;
  integer status_reads=0,post_price_status=0,price_reads=0,ack_accepts=0;
  integer sum_reads=0,ready_reads=0,decision_writes=0,miso_checks=0,lost_ticks=0;
  integer master_rises_first=0,shadow_rises_first=0,decision_count=0,spi_ticks=0;
  integer first_byte_cycle=0;
  reg [7:0] expected_miso[0:NTICKS-1],expected_write[0:NTICKS-1],expected_price[0:NTICKS-1];
  reg first_price_pending=0;
  demo_autonoma_spi_probe_top dut(.i_Clk(clk),.o_LED(led));
  initial begin
    $readmemh("proyecto4/pruebas_fisicas/demo_autonoma_spi_probe/data/expected_decisions.hex",expected_miso);
    $readmemh("proyecto4/pruebas_fisicas/demo_autonoma_spi_probe/data/expected_writes.hex",expected_write);
    $readmemh("proyecto4/pruebas_fisicas/demo_autonoma_spi_probe/data/prices.hex",expected_price);
  end
  always @(posedge clk) begin
    cycle=cycle+1;
    if(dut.frame_start && dut.sent_count==0) begin
      $display("PROBE master frame start cycle=%0d rst=%b",cycle,dut.rst_ni);
      if(dut.rst_ni!==1'b1) $fatal(1,"Master started while reset asserted");
    end
    if(dut.sclk_rise) begin
      master_edges=master_edges+1;
      if(dut.sent_count==0) master_rises_first=master_rises_first+1;
    end
    if(dut.shadow_sclk_r && dut.shadow_cs_active && !dut.shadow_cs_assert) begin
      shadow_edges=shadow_edges+1;
      if(dut.sent_count==0) shadow_rises_first=shadow_rises_first+1;
    end
    if(dut.status_read) begin
      status_reads=status_reads+1;
      if(byte_dones>0) begin
        post_price_status=post_price_status+1;
        if(post_price_status==1) $display("PROBE first STATUS after price cycle=%0d",cycle);
      end
    end
    if(dut.spi_byte_done) begin
      if(byte_dones>0 && (price_reads!=spi_ticks || decision_writes!=spi_ticks))
        begin lost_ticks=lost_ticks+1;$fatal(1,"New price before prior PRICE/DECISION: reads=%0d decisions=%0d ticks=%0d",price_reads,decision_writes,spi_ticks);end
      if(spi_ticks>=NTICKS || dut.u_soc.sma_price!==expected_price[spi_ticks])
        $fatal(1,"Slave PRICE mismatch tick=%0d actual=%0d expected=%0d",spi_ticks,dut.u_soc.sma_price,expected_price[spi_ticks]);
      if(byte_dones==0) begin
        if(master_rises_first!=8) $fatal(1,"Master had %0d rising edges before first byte_done",master_rises_first);
        if(shadow_rises_first!=8) $fatal(1,"Shadow sync had %0d rising edges at byte_done, expected eight",shadow_rises_first);
        first_byte_cycle=cycle;
        $display("PROBE slave byte_done cycle=%0d; master rises=%0d synchronized shadow rises=%0d",cycle,master_rises_first,shadow_rises_first);
        first_price_pending=1;
      end
      byte_dones=byte_dones+1;spi_ticks=spi_ticks+1;
    end
    if(dut.price_read) begin
      price_reads=price_reads+1;
      if(first_price_pending) begin $display("PROBE PRICE read cycle=%0d latency=%0d cycles",cycle,cycle-first_byte_cycle);first_price_pending=0;end
    end
    if(dut.ack_accepted) begin
      ack_accepts=ack_accepts+1;
      if(ack_accepts==1)$display("PROBE ACK accepted cycle=%0d",cycle);
    end
    if(dut.sum_read) sum_reads=sum_reads+1;
    if(dut.ready_read) ready_reads=ready_reads+1;
    if(dut.decision_write) begin
      if(decision_writes>=NTICKS || dut.data_wdata[7:0]!==expected_write[decision_writes])
        $fatal(1,"DECISION/Python mismatch idx=%0d actual=%02h expected=%02h",decision_writes,dut.data_wdata[7:0],expected_write[decision_writes]);
      decision_writes=decision_writes+1;
    end
    if(dut.response_valid) begin
      if(miso_checks>=NTICKS || dut.response!==expected_miso[miso_checks])
        $fatal(1,"MISO/Python mismatch idx=%0d actual=%02h expected=%02h",miso_checks,dut.response,expected_miso[miso_checks]);
      miso_checks=miso_checks+1;
    end
  end
  always @(posedge clk) begin
    #1;
    if(dut.o_LED!==dut.expected_led) $fatal(1,"LED probe status disagrees with captured events");
  end
  initial begin
    wait(dut.master_done && dut.sent_count==NTICKS && dut.decision_count==NTICKS);
    repeat(3) @(posedge clk);
    if(led!==4'b1100) $fatal(1,"Final diagnostic pattern should be D3+D4, got %b",led);
    if(byte_dones!=NTICKS || master_rises_first!=8 || shadow_rises_first!=8 || price_reads!=NTICKS || ack_accepts!=NTICKS-1)
      $fatal(1,"SPI/handshake counts byte=%0d master8=%0d shadow8=%0d price=%0d ack=%0d",byte_dones,master_rises_first,shadow_rises_first,price_reads,ack_accepts);
    if(decision_writes!=NTICKS || miso_checks!=NTICKS || lost_ticks!=0 || sum_reads!=NTICKS || ready_reads!=NTICKS)
      $fatal(1,"Integration counts DECISION=%0d MISO=%0d lost=%0d SUM=%0d READY=%0d",decision_writes,miso_checks,lost_ticks,sum_reads,ready_reads);
    $display("PASS probe: ticks=%0d; first master/shadow edges=8/8; byte_done=%0d; PRICE=%0d ACK=%0d DECISION=%0d MISO=%0d lost=%0d",spi_ticks,byte_dones,price_reads,ack_accepts,decision_writes,miso_checks,lost_ticks);
    $finish;
  end
  initial begin #20000000;$fatal(1,"Probe timeout LED=%b byte_done=%0d PRICE=%0d ACK=%0d",led,byte_dones,price_reads,ack_accepts);end
endmodule
