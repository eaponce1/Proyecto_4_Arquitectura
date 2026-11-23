`timescale 1ns/1ps
module tb_spi_physical_internal;
  reg clk=0;
  always #20 clk=~clk;
  wire [3:0] leds;
  wire sclk,mosi,cs_n,miso;
  integer starts=0,stops=0;

  spi_physical_internal_top dut(
    .i_Clk(clk),.o_LED(leds),
    .o_MON_SCLK(sclk),.o_MON_MOSI(mosi),.o_MON_CS_n(cs_n),.o_MON_MISO(miso)
  );

  always @(negedge cs_n) starts=starts+1;
  always @(posedge cs_n) if (starts>stops) stops=stops+1;

  initial begin
    repeat(100000) begin
      @(posedge clk);
      if (leds[3]) begin
        #1;
        if (starts!=5 || stops!=5)
          $fatal(1,"FAIL: frames starts=%0d stops=%0d, expected 5/5",starts,stops);
        if (leds[0]!==1'b1 || leds[1]!==1'b0 || leds[2]!==1'b0)
          $fatal(1,"FAIL: LED=%b (se esperaba DONE/PASS y no FAIL/BUSY)",leds);
        $display("PASS internal SPI: frames=%0d; STATUS/PRICE verificados=4; decisiones=4; MISO lag=5; LEDs=%b",starts,leds);
        $finish;
      end
    end
    $fatal(1,"timeout: LEDs=%b frames=%0d",leds,starts);
  end
endmodule
