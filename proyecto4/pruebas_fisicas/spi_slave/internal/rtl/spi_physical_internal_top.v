module spi_physical_internal_top (
  input  wire       i_Clk,
  output wire [3:0] o_LED,
  output wire       o_MON_SCLK,
  output wire       o_MON_MOSI,
  output wire       o_MON_CS_n,
  output wire       o_MON_MISO
);
  reg [4:0] por_q = 5'b0;
  wire rst_ni = por_q[4];
  always @(posedge i_Clk) if (!por_q[4]) por_q <= por_q + 1'b1;

  wire busy, master_done, master_fail, bus_done, bus_fail;
  wire master_sclk, master_mosi, master_cs_n, slave_miso;
  wire [7:0] price;
  wire price_valid;
  wire [31:0] bus_rdata;
  wire bus_sel,bus_req,bus_we;
  wire [7:0] bus_addr;
  wire [31:0] bus_wdata;
  wire [3:0] bus_be;

  // Probe outputs are observation only. The protocol path is entirely internal.
  assign o_MON_SCLK = master_sclk;
  assign o_MON_MOSI = master_mosi;
  assign o_MON_CS_n = master_cs_n;
  assign o_MON_MISO = slave_miso;

  spi_test_master u_master (
    .clk_i(i_Clk), .rst_ni(rst_ni), .miso_i(slave_miso),
    .sclk_o(master_sclk), .mosi_o(master_mosi), .cs_n_o(master_cs_n),
    .busy_o(busy), .done_o(master_done), .fail_o(master_fail)
  );

  pochoco_spi_slave u_spi_slave (
    .clk_i(i_Clk), .rst_ni(rst_ni),
    .sel_i(bus_sel), .req_i(bus_req), .we_i(bus_we),
    .addr_i(bus_addr), .wdata_i(bus_wdata), .be_i(bus_be), .rdata_o(bus_rdata),
    .spi_sclk_i(master_sclk), .spi_mosi_i(master_mosi), .spi_cs_n_i(master_cs_n),
    .spi_miso_o(slave_miso), .price_o(price), .price_valid_o(price_valid),
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
