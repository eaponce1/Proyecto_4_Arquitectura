`timescale 1ns/1ps

// Integracion RTL del programa trade.hex con una secuencia y decisiones
// esperadas generadas por estrategia_reversion_media en Python.
module tb_trade_equivalencia;
  localparam integer MAX_TICKS = 64;
  localparam integer PERIODO_NS = 100000;
  localparam integer SPI_NS = 9500;

  reg clk = 0;
  always #20 clk = ~clk;
  reg sclk = 0, mosi = 0, cs_n = 1;
  wire miso;
  integer precios [0:MAX_TICKS-1];
  integer esperadas [0:MAX_TICKS-1];
  integer nticks = 0;
  integer lecturas_status = 0, lecturas_price = 0, escrituras_decision = 0;
  integer bit_x = 0;

  pochoco_soc #(
    .MemFile("proyecto4/sw/trade.hex"),
    .EnableSpi(1)
  ) dut (
    .i_Clk(clk), .o_LED(), .i_Switch(4'b0000),
    .o_Segment1_A(), .o_Segment1_B(), .o_Segment1_C(), .o_Segment1_D(),
    .o_Segment1_E(), .o_Segment1_F(), .o_Segment1_G(),
    .o_Segment2_A(), .o_Segment2_B(), .o_Segment2_C(), .o_Segment2_D(),
    .o_Segment2_E(), .o_Segment2_F(), .o_Segment2_G(),
    .i_SPI_SCLK(sclk), .i_SPI_MOSI(mosi), .i_SPI_CS_n(cs_n), .o_SPI_MISO(miso)
  );

  always @(posedge clk) begin
    if (dut.u_spi.rd && dut.u_spi.off == 0) lecturas_status = lecturas_status + 1;
    if (dut.u_spi.rd && dut.u_spi.off == 1) lecturas_price = lecturas_price + 1;
    if (dut.u_spi.wr && dut.u_spi.off == 2) escrituras_decision = escrituras_decision + 1;
  end

  task automatic transaccion(input reg [7:0] precio, output reg [7:0] decision);
    integer bit_idx;
    begin
      decision = 0;
      cs_n = 0;
      #1000;
      for (bit_idx = 7; bit_idx >= 0; bit_idx = bit_idx - 1) begin
        mosi = precio[bit_idx];
        #500 sclk = 1;
        if (miso !== 1'b0 && miso !== 1'b1) bit_x = bit_x + 1;
        decision[bit_idx] = (miso === 1'b1);
        #500 sclk = 0;
      end
      #500 cs_n = 1;
    end
  endtask

  reg [7:0] decision;
  integer idx;
  reg [1023:0] ruta_precios, ruta_esperadas;

  initial begin
    if (!$value$plusargs("TICKS=%d", nticks)) $fatal(1, "Falta +TICKS");
    if (!$value$plusargs("PRICE_FILE=%s", ruta_precios)) $fatal(1, "Falta +PRICE_FILE");
    if (!$value$plusargs("EXPECTED_FILE=%s", ruta_esperadas)) $fatal(1, "Falta +EXPECTED_FILE");
    if (nticks < 1 || nticks > MAX_TICKS) $fatal(1, "TICKS fuera de rango");
    $readmemh(ruta_precios, precios);
    $readmemh(ruta_esperadas, esperadas);
    #4000;

    for (idx = 0; idx < nticks; idx = idx + 1) begin
      transaccion(precios[idx][7:0], decision);
      if (decision !== esperadas[idx][7:0])
        $fatal(1, "Tick %0d: MISO=%02h, Python esperaba=%02h", idx, decision, esperadas[idx]);
      #(PERIODO_NS - SPI_NS);
    end
    repeat (20) @(posedge clk);
    if (lecturas_status == 0 || lecturas_price < nticks || escrituras_decision < nticks)
      $fatal(1, "Accesos MMIO incompletos: STATUS=%0d PRICE=%0d DECISION=%0d",
             lecturas_status, lecturas_price, escrituras_decision);
    if (bit_x != 0) $fatal(1, "MISO tuvo %0d bits desconocidos", bit_x);
    $display("PASS trade RTL/Python: %0d ticks; STATUS=%0d PRICE=%0d DECISION=%0d",
             nticks, lecturas_status, lecturas_price, escrituras_decision);
    $finish;
  end
endmodule
