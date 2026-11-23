`timescale 1ns/1ps
module tb_arranque_netlist;
  reg clk=0;
  always #20 clk=~clk;
  wire [3:0] led;
  demo_autonoma_bus_detail_top dut(clk,led);
  integer c=0;
  reg [3:0] last=0;
  always @(posedge clk) begin
    c=c+1;
    #1;
    if(led!==last || c==1 || c==15 || c==16 || c==100)
      $display("NET cycle=%0d POR=%h LED=%b error=%b",c,dut.\u_soc.por_cnt ,led,dut.monitor_error);
    if(led===15 || dut.monitor_error===1 || (^led)===1'bx)
      $fatal(1,"First netlist fault/X cycle=%0d",c);
    last=led;
    if(c==100000) begin
      if(led!==10)$fatal(1,"Netlist did not reach PASS");
      $display("PASS netlist at cycle=%0d LED=%b",c,led);
      $finish;
    end
  end
endmodule
