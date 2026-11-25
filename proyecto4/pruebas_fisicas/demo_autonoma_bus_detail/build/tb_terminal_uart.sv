`timescale 1ns/1ps
module tb_terminal_uart;
reg clk=0;
always #20 clk=~clk;
reg start=0;
reg [7:0] value=0;
wire tx;
terminal_status_uart dut(clk,start,value,tx);
task check_byte(input [7:0] expected);
  integer n;
  reg [7:0] got;
  begin
    @(negedge clk);
    value=expected;
    start=1;
    @(negedge tx);
    #4340;
    if(tx!==0) $fatal(1,"start bit");
    start=0;
    for(n=0;n<8;n=n+1) begin
      #8680;
      got[n]=tx;
    end
    #8680;
    if(tx!==1 || got!==expected) $fatal(1,"UART got %h expected %h",got,expected);
    #17360;
    if(tx!==1) $fatal(1,"idle line");
  end
endtask
initial begin
  check_byte(8'haa);
  check_byte(8'haf);
  $display("PASS terminal UART frames AA (PASS), AF (watchdog)");
  $finish;
end
initial begin #300000; $fatal(1,"timeout"); end
endmodule
