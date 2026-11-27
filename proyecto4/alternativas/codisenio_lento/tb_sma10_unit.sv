`timescale 1ns/1ps
module tb_sma10_unit;
  reg clk=0,rst=0,valid=0;
  reg [7:0] price=0;
  wire [11:0] total;
  wire ready;
  always #40 clk=~clk;
  pochoco_sma10 dut(.clk_i(clk),.rst_ni(rst),.price_valid_i(valid),.price_i(price),.sum_o(total),.ready_o(ready));
  integer history[0:9];integer index=0,count=0,expected=0;
  integer seed=711;
  task sample(input integer value);
    begin
      @(negedge clk);price=value;valid=1;
      expected=expected-history[index]+value;history[index]=value;
      index=(index+1)%10;if(count<10)count++;
      @(negedge clk);valid=0;
      repeat(12)@(negedge clk);
      if(total!==expected || ready!==(count==10))$fatal(1,"SUM10/READY p=%0d sum=%0d/%0d count=%0d ready=%b",value,total,expected,count,ready);
    end
  endtask
  task reset_model;
    begin
      @(negedge clk);rst=0;valid=0;
      for(integer j=0;j<10;j++)history[j]=0;
      index=0;count=0;expected=0;
      repeat(3)@(negedge clk);rst=1;
    end
  endtask
  initial begin
    reset_model();
    for(integer k=0;k<20000;k++)sample(1+($unsigned($random(seed))%255));
    reset_model();
    for(integer k=0;k<40;k++)sample(k%2?255:1);
    $display("PASS SMA10 20040 precios, suma, READY y reinicio con BRAM no borrada");$finish;
  end
endmodule
