// SPI externo con el mismo fetch ROM y arranque que la demo fisica aprobada.
module trade_spi_externo #(
  parameter integer PALABRAS_FIRMWARE = 71,
  parameter ARCHIVO_FIRMWARE = "proyecto4/alternativas/mmio_sma10/sw/trade.hex"
) (
  input wire i_Clk, i_SPI_SCLK, i_SPI_MOSI, i_SPI_CS_n,
  output wire o_SPI_MISO,
  output reg [3:0] o_LED = 4'b0
);
  reg dividido = 1'b0;
  always @(posedge i_Clk) dividido <= ~dividido;
  wire clk_soc;
  SB_GB u_reloj(.USER_SIGNAL_TO_GLOBAL_BUFFER(dividido), .GLOBAL_BUFFER_OUTPUT(clk_soc));

  wire rst_ni, commit, byte_done, lee_price, lee_sum, lee_ready, escribe_decision;
  wire [31:0] bus_escritura;
  wire [7:0] precio_spi;
  pochoco_soc_cpu_trace #(
    .NumWords(PALABRAS_FIRMWARE), .MemFile(ARCHIVO_FIRMWARE), .FETCH_ROM(1), .WARMUP(1)
  ) u_soc (
    .i_Clk(clk_soc),
    .i_SPI_SCLK(i_SPI_SCLK), .i_SPI_MOSI(i_SPI_MOSI),
    .i_SPI_CS_n(i_SPI_CS_n), .o_SPI_MISO(o_SPI_MISO),
    .dbg_reset_released(rst_ni), .dbg_commit(commit),
    .dbg_spi_byte_done(byte_done), .dbg_price(precio_spi),
    .dbg_price_read(lee_price), .dbg_sum_read(lee_sum), .dbg_ready_read(lee_ready),
    .dbg_decision_write(escribe_decision), .dbg_data_wdata(bus_escritura)
  );

  // Los LED muestran hitos independientes desde el ultimo arranque.
  always @(posedge clk_soc) begin
    if (!rst_ni)
      o_LED <= 4'b0;
    else
      o_LED <= o_LED | {escribe_decision && (|bus_escritura[7:0]), lee_price, byte_done, commit};
  end
endmodule
