// Copyright 2026 Universidad de los Andes.
// Licensed under the Solderpad Hardware License, Version 0.51 (the "License");
// you may not use this file except in compliance with the License.
// SPDX-License-Identifier: SHL-0.51
//
// Course: Arquitectura de Computadores (2026)
// 
// Authors:
// - Nicolás Villegas <navillegas@miuandes.cl>



// lo volvemos opcional para que no gaste memoria
module pochoco_soc_observable #(
  parameter NumWords   = 512,
  parameter MemFile    = "sw/game.hex",
  parameter EnableSpi  = 0   // 0 = quita el SPI slave (no usado por game.s) para ahorrar LUTs/FFs
) (
  input  wire       i_Clk,

  output wire [3:0] o_LED,
  input  wire [3:0] i_Switch,

  output wire       o_Segment1_A, o_Segment1_B, o_Segment1_C, o_Segment1_D,
  output wire       o_Segment1_E, o_Segment1_F, o_Segment1_G,
  output wire       o_Segment2_A, o_Segment2_B, o_Segment2_C, o_Segment2_D,
  output wire       o_Segment2_E, o_Segment2_F, o_Segment2_G,

  input  wire       i_SPI_SCLK,
  input  wire       i_SPI_MOSI,
  input  wire       i_SPI_CS_n,
  output wire       o_SPI_MISO,
  output wire       dbg_instr_req, dbg_data_req, dbg_data_we,
  output wire [31:0] dbg_data_addr, dbg_data_wdata,
  output wire       dbg_reset_released,
  output wire       dbg_status_read, dbg_price_read, dbg_sum_read,
  output wire       dbg_ready_read, dbg_decision_write
);

  wire clk;
  assign clk = i_Clk;

  // Power-on reset
  reg  [3:0] por_cnt = 4'b0;
  wire       rst_ni;
  always @(posedge clk) begin
    if (por_cnt != 4'hF) por_cnt <= por_cnt + 4'd1;
  end
  assign rst_ni = (por_cnt == 4'hF);
  assign dbg_reset_released = rst_ni;

  // Core-memory wiring
  wire        instr_req;
  wire [31:0] instr_addr, instr_rdata;

  wire        data_req, data_we;
  wire [3:0]  data_be;
  wire [31:0] data_addr, data_wdata, data_rdata;

  espino_core #(.BootAddr(32'h0000_0000)) u_core (
    .clk_i         (clk),
    .rst_ni        (rst_ni),
    .instr_req_o   (instr_req),
    .instr_addr_o  (instr_addr),
    .instr_rdata_i (instr_rdata),
    .data_req_o    (data_req),
    .data_we_o     (data_we),
    .data_be_o     (data_be),
    .data_addr_o   (data_addr),
    .data_wdata_o  (data_wdata),
    .data_rdata_i  (data_rdata)
  );
  assign dbg_instr_req = instr_req;
  assign dbg_data_req = data_req;
  assign dbg_data_we = data_we;
  assign dbg_data_addr = data_addr;
  assign dbg_data_wdata = data_wdata;

  wire is_mmio, spi_sel, per_sel;
  assign is_mmio = data_addr[31];
  assign per_sel = is_mmio & ~data_addr[16];
  assign spi_sel = is_mmio &  data_addr[16];

  wire ram_b_req, per_req, spi_req;
  assign ram_b_req = data_req & ~is_mmio;
  assign per_req   = data_req &  per_sel;
  assign spi_req   = data_req &  spi_sel;
  assign dbg_status_read = spi_req & ~data_we & (data_addr[7:2] == 0);
  assign dbg_price_read = spi_req & ~data_we & (data_addr[7:2] == 1);
  assign dbg_decision_write = spi_req & data_we & data_be[0] & (data_addr[7:2] == 2);
  assign dbg_sum_read = spi_req & ~data_we & (data_addr[7:2] == 3);
  assign dbg_ready_read = spi_req & ~data_we & (data_addr[7:2] == 4);

  wire [31:0] ram_b_rdata, per_rdata, spi_rdata;
  wire [7:0] sma_price;
  wire sma_price_valid;
  wire [11:0] sma_sum;
  wire sma_ready;

  reg rd_is_per, rd_is_spi;
  always @(posedge clk or negedge rst_ni) begin
    if (!rst_ni) begin
      rd_is_per <= 1'b0;
      rd_is_spi <= 1'b0;
    end else if (data_req & ~data_we) begin
      rd_is_per <= per_sel;
      rd_is_spi <= EnableSpi ? spi_sel : 1'b0;
    end
  end
  assign data_rdata = rd_is_per ? per_rdata :
                      rd_is_spi ? spi_rdata : ram_b_rdata;

  pochoco_ram #(.NumWords(NumWords), .MemFile(MemFile)) u_ram (
    .clk_i     (clk),
    .a_req_i   (instr_req),
    .a_addr_i  (instr_addr),
    .a_rdata_o (instr_rdata),
    .b_req_i   (ram_b_req),
    .b_we_i    (data_we),
    .b_be_i    (data_be),
    .b_addr_i  (data_addr),
    .b_wdata_i (data_wdata),
    .b_rdata_o (ram_b_rdata)
  );

  // Peripherals
  wire [6:0] seg1, seg2;

  pochoco_periph u_periph (
    .clk_i     (clk),
    .rst_ni    (rst_ni),
    .sel_i     (per_sel),
    .req_i     (per_req),
    .we_i      (data_we),
    .addr_i    (data_addr[7:0]),
    .wdata_i   (data_wdata),
    .be_i      (data_be),
    .rdata_o   (per_rdata),
    .leds_o    (o_LED),
    .btn_i     (i_Switch),
    .seg1_o    (seg1),
    .seg2_o    (seg2)
  );

  // SPI Slave
  pochoco_spi_slave u_spi (
    .clk_i      (clk),
    .rst_ni     (rst_ni),
    .sel_i      (spi_sel),
    .req_i      (spi_req),
    .we_i       (data_we),
    .addr_i     (data_addr[7:0]),
    .wdata_i    (data_wdata),
    .be_i       (data_be),
    .rdata_o    (spi_rdata),
    .spi_sclk_i (i_SPI_SCLK),
    .spi_mosi_i (i_SPI_MOSI),
    .spi_cs_n_i (i_SPI_CS_n),
    .spi_miso_o (o_SPI_MISO),
    .price_o (sma_price),
    .price_valid_o (sma_price_valid),
    .sma_sum_i(sma_sum), .sma_ready_i(sma_ready)
  );

  pochoco_sma10 u_sma10 (
    .clk_i(clk), .rst_ni(rst_ni), .price_valid_i(EnableSpi ? sma_price_valid : 1'b0),
    .price_i(sma_price), .sum_o(sma_sum), .ready_o(sma_ready)
  );

  // 7-seg is active-low on the board
  assign {o_Segment1_G, o_Segment1_F, o_Segment1_E, o_Segment1_D,
          o_Segment1_C, o_Segment1_B, o_Segment1_A} = ~seg1;
  assign {o_Segment2_G, o_Segment2_F, o_Segment2_E, o_Segment2_D,
          o_Segment2_C, o_Segment2_B, o_Segment2_A} = ~seg2;

endmodule
