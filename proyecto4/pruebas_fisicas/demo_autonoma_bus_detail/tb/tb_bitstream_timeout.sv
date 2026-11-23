`timescale 1ns/1ps
module tb_bitstream_timeout;
  reg clk=0;
  always #20 clk=~clk;
  wire [3:0] led;
  chip dut(.io_0_8_1(clk),
    .io_13_6_1(led[0]),.io_13_7_0(led[1]),.io_13_7_1(led[2]),.io_13_8_0(led[3]));
  integer cycle=0;
  reg [3:0] previous=0;
  initial $display("BITSTREAM model start");
  always @(posedge clk) begin
    cycle=cycle+1;
    #1;
    if (led!==previous || cycle==1 || cycle==100 || cycle==1000)
      $display("BITSTREAM cycle=%0d LED=%b",cycle,led);
    previous=led;
    if (led>=11 || (^led)===1'bx)
      $fatal(1,"BITSTREAM first error/unknown cycle=%0d LED=%b",cycle,led);
    if(cycle==110000) begin
      if(led!==10) $fatal(1,"BITSTREAM incomplete LED=%b",led);
      $display("PASS unpacked BIN model");
      $finish;
    end
  end
endmodule


