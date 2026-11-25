`timescale 1ns/1ps
module tb_uart_netlist;
reg clk=0;
always #20 clk=~clk;
wire [3:0] led;
wire tx;
reg [7:0] packet[0:8];
integer i,j;
demo_autonoma_bus_detail_top dut(.i_Clk(clk),.o_LED(led),.debug_uart_tx(tx));
initial begin
  #5000000;
  $display("GATE 5ms LEDs=%h TX=%b",led,tx);
  if (led !== 4'h0) $fatal(1,"unexpected diagnostic fault");
  $finish;
end
initial begin
  for (i=0;i<9;i=i+1) begin
    @(negedge tx);
    #8680;
    for(j=0;j<8;j=j+1) begin
      #4340; packet[i][j]=tx; #4340;
    end
    $display("GATE UART byte %0d = %02h",i,packet[i]);
  end
end
endmodule
