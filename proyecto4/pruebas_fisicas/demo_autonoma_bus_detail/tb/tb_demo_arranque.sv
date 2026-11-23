`timescale 1ns/1ps
module tb_demo_arranque;
  reg clk=0;
  always #20 clk=~clk;
  wire [3:0] led;
  demo_autonoma_bus_detail_top dut(.i_Clk(clk),.o_LED(led));
  integer c=0, start_cycle=0, byte_cycle=0, response_cycle=0;
  reg [6:0] causes;
`ifndef PREVIOUS
  initial if($test$plusargs("bad_miso")) begin
    wait(dut.frame_start);
    force dut.miso=1'b1;
    wait(dut.response_valid);
    release dut.miso;
  end
`endif
  always @(posedge clk) begin
    c=c+1;
    if(dut.frame_start && !start_cycle) start_cycle=c;
    if(dut.spi_byte_done && !byte_cycle) byte_cycle=c;
    if(dut.response_valid && !response_cycle) response_cycle=c;
    if(c<=17 || dut.frame_start || dut.spi_byte_done || dut.response_valid || c==100)
      $display("PRE cycle=%0d reset_n=%b CS_n=%b start=%b byte=%b response=%b LED=%b",
               c,dut.rst_ni,dut.cs_n,dut.frame_start,dut.spi_byte_done,dut.response_valid,led);
    if(dut.rst_ni !== (c>=16)) $fatal(1,"POR cycle=%0d",c);
    if(c>1 && c<16 && (dut.cs_n!==1 || dut.sclk!==0 || led!==0))
      $fatal(1,"Reset outputs cycle=%0d",c);
`ifndef PREVIOUS
    causes={
      dut.response_valid && !dut.response_ok,
      dut.u_monitor.write_decision && (!(dut.u_monitor.tick_seen[1] || dut.u_monitor.sum_read) ||
        !(dut.u_monitor.tick_seen[2] || dut.u_monitor.ready_read) ||
        dut.data_wdata[7:0]!=dut.u_monitor.decisions[dut.frame_index]),
      (dut.u_monitor.sum_read || dut.u_monitor.ready_read) &&
        !(dut.u_monitor.tick_seen[0] || dut.u_monitor.price_read),
      (|dut.u_monitor.tick_events) && (!dut.u_monitor.in_tick || dut.frame_start ||
        |(dut.u_monitor.tick_seen & dut.u_monitor.tick_events)),
      dut.spi_byte_done && (dut.u_monitor.in_tick ||
        dut.spi_price!=dut.u_monitor.prices[dut.frame_index]),
      dut.frame_start && dut.frame_index!=0 && (!dut.u_monitor.in_tick || !dut.u_monitor.drained),
      dut.master_timeout
    };
    if($test$plusargs("bad_miso") && c==531) begin
      if(causes!==7'b1000000 || dut.u_monitor.fault!==1)
        $fatal(1,"Injected MISO was not the unique cause: %b",causes);
      #1;
      if(led!==13 || dut.monitor_error!==1)
        $fatal(1,"MISO fault did not latch");
      $display("PASS injected MISO: unique fault and LED=1101 at edge %0d",c);
      $finish;
    end
    if(c>=16 && (causes!==0 || dut.u_monitor.fault!==0 ||
                 dut.monitor_error!==0 || dut.master_timeout!==0))
      $fatal(1,"First fault/X cycle=%0d causes MISO/DECISION/SMA/event/byte/frame/timeout=%b fault=%b",
             c,causes,dut.u_monitor.fault);
`endif
    if(c<500 && (byte_cycle || response_cycle)) $fatal(1,"Premature SPI byte or response");
    #1;
    if(c<=15 && led!==0) $fatal(1,"LED not reset at edge %0d",c);
    if(led===4'hf || (^led)===1'bx) $fatal(1,"First bad LED at edge %0d",c);
    if(c==550) begin
      if(start_cycle!=18 || byte_cycle!=500 || response_cycle!=531)
        $fatal(1,"Unexpected startup start=%0d byte=%0d MISO=%0d",start_cycle,byte_cycle,response_cycle);
      $display("PASS startup first 550 edges start=%0d byte=%0d MISO=%0d",start_cycle,byte_cycle,response_cycle);
      $finish;
    end
  end
endmodule



