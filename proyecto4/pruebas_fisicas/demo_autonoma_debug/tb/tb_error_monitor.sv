`timescale 1ns/1ps
module tb_error_monitor;
  reg clk = 1'b0;
  always #5 clk = ~clk;
  reg rst_ni = 1'b0;
  reg e1 = 1'b0, e2 = 1'b0, e3 = 1'b0;
  wire [1:0] code;

  error_monitor dut(.clk_i(clk), .rst_ni(rst_ni),
                    .error_1_i(e1), .error_2_i(e2), .error_3_i(e3),
                    .error_code_o(code));

  task reset_dut;
    begin
      rst_ni = 1'b0; e1 = 0; e2 = 0; e3 = 0;
      repeat (2) @(posedge clk);
      #1 rst_ni = 1'b1;
      @(posedge clk); #1;
      if (code !== 2'b00) $fatal(1, "Reset did not clear error_code");
    end
  endtask

  initial begin
    reset_dut();
    e1 = 1; @(posedge clk); #1; e1 = 0;
    if (code !== 2'b01) $fatal(1, "Condition 1 did not latch code 1");
    e2 = 1; e3 = 1; @(posedge clk); #1; e2 = 0; e3 = 0;
    if (code !== 2'b01) $fatal(1, "First error was overwritten after condition 1");

    reset_dut();
    e2 = 1; @(posedge clk); #1; e2 = 0;
    if (code !== 2'b10) $fatal(1, "Condition 2 did not latch code 2");
    e3 = 1; @(posedge clk); #1; e3 = 0;
    if (code !== 2'b10) $fatal(1, "First error was overwritten after condition 2");

    reset_dut();
    e3 = 1; @(posedge clk); #1; e3 = 0;
    if (code !== 2'b11) $fatal(1, "Condition 3 did not latch code 3");

    reset_dut();
    repeat (3) @(posedge clk);
    if (code !== 2'b00) $fatal(1, "Normal sequence unexpectedly raised an error");
    $display("PASS error monitor: codes 1/2/3 isolated; first error sticky; normal code=0");
    $finish;
  end
endmodule
