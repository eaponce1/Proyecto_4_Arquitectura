module spi_physical_test_top (
  input wire i_Clk,
  output wire [3:0] o_LED,
  input wire i_SPI_SCLK,
  input wire i_SPI_MOSI,
  input wire i_SPI_CS_n,
  output wire o_SPI_MISO,
  output wire o_TEST_SCLK,
  output wire o_TEST_MOSI,
  output wire o_TEST_CS_n,
  input wire i_TEST_MISO
);
  reg [4:0] por_q = 5'b0;
  wire rst_ni = por_q[4];
  always @(posedge i_Clk) if (!por_q[4]) por_q <= por_q + 1'b1;

  wire busy, master_done, master_fail, bus_done, bus_fail;
  wire [7:0] price;
  wire price_valid;
  wire [31:0] bus_rdata;
  wire bus_sel,bus_req,bus_we;
  wire [7:0] bus_addr;
  wire [31:0] bus_wdata;
  wire [3:0] bus_be;

  spi_test_master u_master (
    .clk_i(i_Clk), .rst_ni(rst_ni), .miso_i(i_TEST_MISO),
    .sclk_o(o_TEST_SCLK), .mosi_o(o_TEST_MOSI), .cs_n_o(o_TEST_CS_n),
    .busy_o(busy), .done_o(master_done), .fail_o(master_fail)
  );

  pochoco_spi_slave u_spi_slave (
    .clk_i(i_Clk), .rst_ni(rst_ni),
    .sel_i(bus_sel), .req_i(bus_req), .we_i(bus_we),
    .addr_i(bus_addr), .wdata_i(bus_wdata), .be_i(bus_be), .rdata_o(bus_rdata),
    .spi_sclk_i(i_SPI_SCLK), .spi_mosi_i(i_SPI_MOSI), .spi_cs_n_i(i_SPI_CS_n),
    .spi_miso_o(o_SPI_MISO), .price_o(price), .price_valid_o(price_valid),
    .sma_sum_i(12'b0), .sma_ready_i(1'b0)
  );

  spi_register_checker u_register_checker (
    .clk_i(i_Clk), .rst_ni(rst_ni), .price_valid_i(price_valid), .price_i(price),
    .rdata_i(bus_rdata), .sel_o(bus_sel), .req_o(bus_req), .we_o(bus_we),
    .addr_o(bus_addr), .wdata_o(bus_wdata), .be_o(bus_be),
    .bus_done_o(bus_done), .fail_o(bus_fail)
  );

  assign o_LED[0] = master_done & bus_done & ~master_fail & ~bus_fail;
  assign o_LED[1] = master_fail | bus_fail;
  assign o_LED[2] = busy;
  assign o_LED[3] = master_done;
endmodule
