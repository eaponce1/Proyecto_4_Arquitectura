`timescale 1ns/1ps
module tb_error_monitor;
  reg clk=0; always #5 clk=~clk;
  reg rst_ni=0, e1=0, e2=0, e3=0;
  wire [1:0] code;
  error_monitor dut(.clk_i(clk),.rst_ni(rst_ni),.error_1_i(e1),.error_2_i(e2),.error_3_i(e3),.error_code_o(code));
  task reset_dut;
    begin
      rst_ni=0; e1=0; e2=0; e3=0; repeat(2) @(posedge clk);
      #1 rst_ni=1; @(posedge clk); #1;
      if(code!==0) $fatal(1,"Reset failed to clear error code");
    end
  endtask
  initial begin
    reset_dut(); e1=1; @(posedge clk); #1; e1=0;
    if(code!==2'b01) $fatal(1,"Error 1 code incorrect");
    e2=1; e3=1; @(posedge clk); #1; e2=0; e3=0;
    if(code!==2'b01) $fatal(1,"First error was overwritten");
    reset_dut(); e2=1; @(posedge clk); #1; e2=0;
    if(code!==2'b10) $fatal(1,"Error 2 code incorrect");
    e3=1; @(posedge clk); #1; e3=0;
    if(code!==2'b10) $fatal(1,"Second error overwrote first");
    reset_dut(); e3=1; @(posedge clk); #1; e3=0;
    if(code!==2'b11) $fatal(1,"Error 3 code incorrect");
    reset_dut(); repeat(3) @(posedge clk);
    if(code!==0) $fatal(1,"Unexpected error in idle case");
    $display("PASS error monitor: codes 1/2/3 isolated; sticky first error");
    $finish;
  end
endmodule
