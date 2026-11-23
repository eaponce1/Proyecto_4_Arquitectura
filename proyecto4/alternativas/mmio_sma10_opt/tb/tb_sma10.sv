`timescale 1ns/1ps
module tb_sma10;
  reg clk=0; always #20 clk=~clk;
  reg rst_n=0, price_valid=0;
  reg [7:0] price=0;
  wire [11:0] sum;
  wire ready;
  integer i, expected=0;
  reg [7:0] model[0:9];
  reg [3:0] ptr=0, count=0;
  pochoco_sma10 dut(.clk_i(clk),.rst_ni(rst_n),.price_valid_i(price_valid),
    .price_i(price),.sum_o(sum),.ready_o(ready));
  task send(input [7:0] p);
    begin
      @(negedge clk); price=p; price_valid=1;
      @(negedge clk); price_valid=0;
      if (count<10) begin expected=expected+p; count=count+1; end
      else begin expected=expected-model[ptr]+p; end
      model[ptr]=p; ptr=(ptr==9)?0:ptr+1;
      repeat(2) @(posedge clk); #1;
      if (sum !== expected) $fatal(1,"SUM tick %0d got %0d expected %0d",i,sum,expected);
      if (ready !== (count==10)) $fatal(1,"READY tick %0d mismatch",i);
    end
  endtask
  initial begin
    for (i=0;i<10;i=i+1) model[i]=0;
    repeat(3) @(negedge clk); rst_n=1;
    for(i=0;i<20000;i=i+1) send(((i*37+19)%255)+1);
    $display("PASS SMA10 peripheral: 20000 prices, sum and ready checked every tick");
    $finish;
  end
endmodule
