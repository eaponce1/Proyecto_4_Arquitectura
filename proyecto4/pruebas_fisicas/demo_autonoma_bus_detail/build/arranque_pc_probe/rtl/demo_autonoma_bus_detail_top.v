module demo_autonoma_bus_detail_top(
  input  wire       i_Clk,
  output wire [3:0] o_LED
);
  localparam integer TICKS=16;

  wire rst_ni,sclk,mosi,cs_n,miso;
  wire [7:0] response;
  wire response_valid,master_done,frame_start,ack_accepted,sclk_rise;
  wire [4:0] sent_count;

  wire instr_req,instr_valid_id,core_stall,lsu_busy,data_req,data_we;
  wire commit_evt;
  wire status_read,price_read,sum_read,ready_read,decision_write,spi_byte_done;
  wire [3:0] data_be;
  wire [31:0] instr_addr,pc_id,instr_id,data_addr,data_wdata,data_rdata,spi_rdata;
  wire [31:0] pc_unused;
  wire [7:0] spi_price;
  reg price_ack_pending=1'b0;

  // Simulation-only snapshots are intentionally not routed to board pins.
  // The one-shot PC probe drives only the four existing user LEDs.
  wire [3:0] pc_probe_led;
  wire pc_probe_valid;
  wire [31:0] pc_probe_pc,pc_probe_instr;
  assign o_LED = pc_probe_led;

  assign commit_evt = instr_valid_id && !core_stall;

  price_spi_master_probe #(
    .TICKS(TICKS),
    .HALF_PERIOD(32),
    .MIN_GAP_CYCLES(6000)
  ) u_master (
    .clk_i(i_Clk),
    .rst_ni(rst_ni),
    .enable_i(rst_ni),
    .price_consumed_i(price_ack_pending),
    .sclk_o(sclk),
    .mosi_o(mosi),
    .cs_n_o(cs_n),
    .miso_i(miso),
    .response_o(response),
    .response_valid_o(response_valid),
    .sent_o(sent_count),
    .done_o(master_done),
    .frame_start_o(frame_start),
    .ack_accepted_o(ack_accepted),
    .sclk_rise_o(sclk_rise)
  );

  pochoco_soc_cpu_trace #(
    .NumWords(71),
    .MemFile("proyecto4/alternativas/mmio_sma10/sw/trade.hex")
  ) u_soc (
    .i_Clk(i_Clk),
    .i_SPI_SCLK(sclk),
    .i_SPI_MOSI(mosi),
    .i_SPI_CS_n(cs_n),
    .o_SPI_MISO(miso),
    .dbg_reset_released(rst_ni),
    .dbg_instr_req(instr_req),
    .dbg_instr_addr(instr_addr),
    .dbg_commit(),
    .dbg_core_stall(core_stall),
    .dbg_instr_valid(instr_valid_id),
    .dbg_lsu_busy(lsu_busy),
    .dbg_instr_id(instr_id),
    .dbg_pc(pc_unused),
    .dbg_pc_id(pc_id),
    .dbg_data_req(data_req),
    .dbg_data_we(data_we),
    .dbg_data_be(data_be),
    .dbg_data_addr(data_addr),
    .dbg_data_wdata(data_wdata),
    .dbg_data_rdata(data_rdata),
    .dbg_status_read(status_read),
    .dbg_price_read(price_read),
    .dbg_sum_read(sum_read),
    .dbg_ready_read(ready_read),
    .dbg_decision_write(decision_write),
    .dbg_spi_byte_done(spi_byte_done),
    .dbg_price(spi_price),
    .dbg_spi_rdata(spi_rdata)
  );

  first_post_byte_pc_probe u_pc_probe (
    .clk_i(i_Clk),
    .rst_ni(rst_ni),
    .byte_done_i(spi_byte_done),
    .instr_valid_id_i(instr_valid_id),
    .stall_i(core_stall),
    .pc_id_i(pc_id),
    .instr_id_i(instr_id),
    .led_o(pc_probe_led),
    .snapshot_valid_o(pc_probe_valid),
    .snapshot_pc_o(pc_probe_pc),
    .snapshot_instr_o(pc_probe_instr)
  );

  // Stop-and-wait: the SPI master sends the next price only after Espino
  // reads PRICE for the current one. Last tick needs no following ACK.
  always @(posedge i_Clk) begin
    if (!rst_ni) begin
      price_ack_pending <= 1'b0;
    end else begin
      if (price_read)
        price_ack_pending <= 1'b1;
      if (spi_byte_done)
        price_ack_pending <= 1'b0;
    end
  end
endmodule
