`timescale 1ns/1ps
module tb_demo_integral_monitor;
  reg clk=0;
  always #5 clk=~clk;
  reg rst=1, byte_done=0, response_valid=0;
  reg [3:0] access=0;
  reg timeout=0, frame_start=0;
  reg [3:0] frame_index=0;
  integer cycle=0;
  always @(posedge clk) cycle=cycle+1;
  reg [7:0] response=0;
  wire [3:0] led;
  wire error;
  demo_integral_monitor dut(
    .clk(clk),.rst(rst),.byte_done(byte_done),.first_commit(byte_done),
    .status_valid(byte_done),.access(access),.frame_index(frame_index),
    .transport_timeout(timeout),.frame_start(frame_start),.response_ok(response==0),
    .price(8'd200),.decision(8'd0),.response_valid(response_valid),.master_done(1'b0),
    .led(led),.error(error));
  task step;
    begin @(posedge clk); #1; end
  endtask
  task reset;
    begin rst=1; access=0; timeout=0; frame_start=0; frame_index=0; response=0; response_valid=0; byte_done=0;
      step; rst=0; end
  endtask
  task price;
    begin byte_done=1; step; byte_done=0; end
  endtask
  initial begin
    reset;
    price;
    // Simultaneous sticky accesses and a held PRICE request.
    access=5'b00111; repeat(4) step;
    if(error || dut.n_read!=1 || dut.n_sum!=1 || dut.n_ready!=1)
      $fatal(1,"simultaneous or held accesses counted incorrectly");
    access=8; response_valid=1; step;
    access=0; response_valid=0; step;
    if(error || dut.n_write!=1 || dut.n_response!=1)
      $fatal(1,"simultaneous DECISION/MISO lost");
    access=8; step;
    if(!error || led!=12) $fatal(1,"duplicate DECISION missed");
    $display("FAULT cycle=%0d LED=%b DECISION duplicate",cycle,led);
    access=0; step;
    if(!error) $fatal(1,"error did not latch");
    reset; price; price;
    if(!error || led!=11) $fatal(1,"overwritten price missed");
    $display("FAULT cycle=%0d LED=%b price overwrite",cycle,led);
    reset; price; response=8'hff; response_valid=1; step;
    if(!error || led!=13) $fatal(1,"wrong MISO missed");
    $display("FAULT cycle=%0d LED=%b MISO mismatch",cycle,led);
    reset; price;
    timeout=1; step;
    if(!error || led!=15) $fatal(1,"timeout missed");
    $display("FAULT cycle=%0d LED=%b timeout",cycle,led);
    reset; access=1; step;
    if(!error || led!=14) $fatal(1,"out-of-tick PRICE missed");
    $display("FAULT cycle=%0d LED=%b out-of-tick PRICE",cycle,led);
    reset; price; access=2; step;
    if(!error || led!=14) $fatal(1,"SMA without PRICE missed");
    $display("FAULT cycle=%0d LED=%b SMA without PRICE",cycle,led);
    reset; price; frame_index=1; frame_start=1; step;
    if(!error || led!=14) $fatal(1,"Lost tick missed");
    $display("FAULT cycle=%0d LED=%b incomplete prior tick",cycle,led);
    reset; price; access=8; step;
    if(!error || led!=12) $fatal(1,"Premature DECISION missed");
    $display("FAULT cycle=%0d LED=%b premature DECISION",cycle,led);
    $display("PASS integral monitor: simultaneous, held request, duplicate, overwrite, MISO and timeout");
    $finish;
  end
endmodule







