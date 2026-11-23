module demo_autonoma_bus_detail_top #(parameter TIMEOUT_DIAG=0)(
  input  wire       i_Clk,
  output wire [3:0] o_LED
);
  localparam integer TICKS=16;

  wire rst_ni,sclk,mosi,cs_n,miso;
  wire [7:0] response;
  wire response_valid,master_done,frame_start,ack_accepted,sclk_rise;
  wire [4:0] sent_count;
  wire [3:0] frame_index;
  wire master_timeout,response_ok,final_complete,first_byte_seen;

  wire instr_req,instr_valid_id,core_stall,lsu_busy,data_req,data_we;
  wire commit_evt;
  wire status_read,price_read,sum_read,ready_read,decision_write,spi_byte_done;
  wire [3:0] data_be;
  wire [31:0] instr_addr,pc_id,instr_id,data_addr,data_wdata,data_rdata,spi_rdata;
  wire [31:0] pc_unused;
  wire [7:0] spi_price;
  reg price_ack_pending=1'b0;

  // Preserve the approved probe as the first-commit qualifier.
  // The integral monitor owns the physical LEDs.
  wire [3:0] pc_probe_led;
  wire pc_probe_valid;
  wire [31:0] pc_probe_pc,pc_probe_instr;
  reg status_pending=0;
  always @(posedge i_Clk)
    status_pending <= rst_ni && status_read;
  wire monitor_error;
  wire [2:0] debug_master_state;
  wire debug_in_tick,debug_price_read,debug_decision_written;
  wire [3:0] timeout_code;
  demo_integral_monitor #(.TIMEOUT_DIAG(TIMEOUT_DIAG)) u_monitor(
    .timeout_code(timeout_code),.debug_in_tick(debug_in_tick),
    .debug_price_read(debug_price_read),.debug_decision_written(debug_decision_written),
    .clk(i_Clk),.rst(!rst_ni),.byte_done(spi_byte_done),
    .first_commit(!pc_probe_valid && commit_evt && pc_id==32'h14 && (spi_byte_done || first_byte_seen)),
    .status_valid(status_pending && data_rdata[0]),
    .access({decision_write,ready_read,sum_read,price_read}),
    .frame_index(frame_index),.transport_timeout(master_timeout),.frame_start(frame_start),.response_ok(response_ok),
    .price(spi_price),.decision(data_wdata[7:0]),
    .response_valid(response_valid),.master_done(master_done),
    .led(o_LED),.error(monitor_error),.final_complete(final_complete),.first_byte_seen(first_byte_seen));

  assign commit_evt = instr_valid_id && !core_stall;

  price_spi_master_probe #(
    .TICKS(TICKS),
    .HALF_PERIOD(32),
    .MIN_GAP_CYCLES(6000)
  ) u_master (
    .clk_i(i_Clk),
    .rst_ni(rst_ni),
    .enable_i(rst_ni),
    .price_consumed_i(price_ack_pending),.final_complete_i(final_complete),
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
    .sclk_rise_o(sclk_rise),.debug_state_o(debug_master_state),.frame_index_o(frame_index),.timeout_o(master_timeout),.response_ok_o(response_ok)
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

  generate if(TIMEOUT_DIAG) begin : g_timeout_diag
    // Read-only shadow of the slave's new_price_q with the same priority.
    reg price_pending=0;
    reg status_poll_after_byte=0,status_ready_after_byte=0;
    always @(posedge i_Clk) begin
      if(!rst_ni || frame_start) begin
        status_poll_after_byte<=0;
        status_ready_after_byte<=0;
      end else if(debug_in_tick) begin
        if(status_read) status_poll_after_byte<=1;
        if(status_pending && data_rdata[0]) status_ready_after_byte<=1;
      end
    end
    always @(posedge i_Clk) begin
      if(!rst_ni) price_pending<=0;
      else if(spi_byte_done) price_pending<=1;
      else if(price_read) price_pending<=0;
    end

    // Each field samples the pre-edge state of the same first timeout.
    // Its enable additionally implies gap_count=8191, timeout_enable=1,
    // and rst_ni=1. Keep that information in the valid bit.
    wire capture=rst_ni && !monitor_error && master_timeout;
    (* keep *) reg snapshot_valid=0;
    (* keep *) reg snapshot_done_state=0;
    (* keep *) reg [3:0] snapshot_index=0;

    (* keep *) reg [7:0] snapshot_flags=0;
    always @(posedge i_Clk) begin
      if(!rst_ni) snapshot_valid<=0;
      else if(capture) begin
        snapshot_valid<=1;
        snapshot_done_state<=debug_master_state[1];
        snapshot_index<=frame_index;

        snapshot_flags<={price_ack_pending,ack_accepted,frame_start,spi_byte_done,
                          price_pending,debug_decision_written,master_done,final_complete};
      end
    end
    // During normal execution each prior frame has one validated DECISION.
    // Record the count as its two inputs instead of duplicating an adder.
    // At timeout only WAIT_ACK (101) and DONE (111) are reachable.
    wire [2:0] snapshot_state={1'b1,snapshot_done_state,1'b1};
    // At either state FINISH has already emitted the current frame.
    wire [4:0] snapshot_sent={1'b0,snapshot_index}+5'd1;
    wire [4:0] snapshot_decision_count=snapshot_sent-!snapshot_flags[2];
    wire [12:0] snapshot_gap_count=snapshot_valid ? 13'h1fff : 13'd0;
    wire snapshot_timeout_enable=snapshot_valid;
    wire snapshot_rst_ni=snapshot_valid;

    assign timeout_code=master_done ? (debug_decision_written ? 4'h2 : 4'h5) :
                        !debug_in_tick ? 4'h4 :
                        debug_price_read ? 4'h3 :
                        status_ready_after_byte ? 4'h7 :
                        status_poll_after_byte ? 4'h6 : 4'h1;
  end else begin : g_no_timeout_diag
    assign timeout_code=4'hf;
  end endgenerate

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










