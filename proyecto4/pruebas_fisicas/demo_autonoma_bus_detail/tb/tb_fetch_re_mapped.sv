`timescale 1ns/1ps
module tb_fetch_re_mapped;
  reg clk=0;
  always #20 clk=~clk;
  wire [3:0] led;
  `ifdef AUTOTEST_UART
  wire tx;
  reg uart_ok=0;
  demo_autonoma_bus_detail_top dut(.i_Clk(clk), .o_LED(led), .debug_uart_tx(tx));
  reg [7:0] report;
  integer bit_number;
  initial begin
    @(negedge tx);
    #4340;
    if(tx!==0) $fatal(1,"UART start bit");
    for(bit_number=0;bit_number<8;bit_number=bit_number+1) begin
      #8680;
      report[bit_number]=tx;
    end
    #8680;
    if(tx!==1 || report!==8'haa) $fatal(1,"UART terminal report %02h",report);
    $display("PASS mapped UART returned AA for terminal LED 1010");
    uart_ok=1;
  end
  `else
  demo_autonoma_bus_detail_top dut(.i_Clk(clk), .o_LED(led));
  `endif
  integer cycle=0;
  always @(negedge clk) begin
    cycle=cycle+1;
    if(led>=4'hc) $fatal(1,"Mapped selftest fault: cycle=%0d LED=%b",cycle,led);
  end

  initial begin
    wait(led===4'ha);
    repeat(32) @(negedge clk);
    `ifdef AUTOTEST_UART
    wait(uart_ok);
    `endif
    if(led!==4'ha) $fatal(1,"Mapped selftest PASS did not remain stable");
    $display("PASS mapped selftest reached LED 1010 and remained stable through cycle %0d",cycle);
    $finish;
  end
  initial begin
    `ifdef AUTOTEST_UART
    #12000000;
    `else
    #5000000;
    `endif
    $fatal(1,"Mapped selftest failed to complete all 16 ticks. LED=%b",led);
  end
endmodule
