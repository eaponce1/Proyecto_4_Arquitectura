`timescale 1ns/1ps
module tb_spi_physical_test;
  reg clk=0;
  always #20 clk=~clk;
  wire [3:0] leds;
  wire test_sclk,test_mosi,test_cs_n,spi_miso;
  spi_physical_test_top dut (
    .i_Clk(clk), .o_LED(leds),
    .i_SPI_SCLK(test_sclk), .i_SPI_MOSI(test_mosi), .i_SPI_CS_n(test_cs_n),
    .o_SPI_MISO(spi_miso),
    .o_TEST_SCLK(test_sclk), .o_TEST_MOSI(test_mosi), .o_TEST_CS_n(test_cs_n),
    .i_TEST_MISO(spi_miso)
  );
  initial begin
    repeat (100000) begin
      @(posedge clk);
      if (leds[3]) begin
        #1;
        if (leds[0] !== 1'b1 || leds[1] !== 1'b0)
          $fatal(1,"FAIL LEDs=%b: esperado PASS=1 FAIL=0",leds);
        $display("PASS SPI slave: STATUS/PRICE verificados en 4 bytes; 5 respuestas MISO correctas con lag de un tick; LEDs=%b",leds);
        $finish;
      end
    end
    $fatal(1,"timeout esperando fin del test; LEDs=%b",leds);
  end
endmodule
