`timescale 1ns/1ps
module tb_uart_echo;
  localparam integer CLKS_PER_BIT=217;
  localparam integer BIT_NS=CLKS_PER_BIT*40;
  reg clk=0; always #20 clk=~clk;
  reg rx=1;
  wire tx;
  integer sent=0, received=0;
  reg [7:0] expected [0:4];
  uart_echo_top dut(.i_Clk(clk),.i_UART_RX(rx),.o_UART_TX(tx));

  task automatic send_byte(input [7:0] value);
    integer i;
    begin
      rx=0; #(BIT_NS);
      for(i=0;i<8;i=i+1) begin rx=value[i]; #(BIT_NS); end
      rx=1; #(BIT_NS);
      sent=sent+1;
    end
  endtask

  task automatic receive_byte(output [7:0] value);
    integer i;
    begin
      @(negedge tx);
      #(BIT_NS/2);
      if(tx!==1'b0) $fatal(1,"TX start bit invalido");
      value=0;
      for(i=0;i<8;i=i+1) begin
        #(BIT_NS); value[i]=tx;
      end
      #(BIT_NS);
      if(tx!==1'b1) $fatal(1,"TX stop bit invalido");
      received=received+1;
    end
  endtask

  reg [7:0] value;
  initial begin
    expected[0]=8'h41; expected[1]=8'h42; expected[2]=8'h43;
    expected[3]=8'h55; expected[4]=8'haa;
    repeat(10) @(posedge clk);
    for(integer n=0;n<5;n=n+1) begin
      fork
        send_byte(expected[n]);
        receive_byte(value);
      join
      if(value!==expected[n]) $fatal(1,"byte %0d: enviado=%02h recibido=%02h",n,expected[n],value);
    end
    if(sent!=5 || received!=5) $fatal(1,"conteos sent=%0d received=%0d",sent,received);
    $display("PASS UART echo: %0d bytes, 115200 8N1: 41 42 43 55 aa",received);
    $finish;
  end
  initial begin #6000000; $fatal(1,"timeout UART echo"); end
endmodule
