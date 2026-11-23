module demo_autonoma_bus_detail_top #(
  parameter TIMEOUT_DIAG=0, FETCH_ROM=0, SLOW_CLOCK=0
)(
  input  wire       i_Clk,
  output wire [3:0] o_LED
);
  localparam integer TICKS=16;
  wire system_clk;
  generate if(SLOW_CLOCK) begin : g_clock_divider
    reg divided=0;
    always @(posedge i_Clk) divided<=!divided;
    SB_GB u_clock(.USER_SIGNAL_TO_GLOBAL_BUFFER(divided),.GLOBAL_BUFFER_OUTPUT(system_clk));
  end else begin : g_direct_clock
    assign system_clk=i_Clk;
  end endgenerate

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
  wire [31:0] operand_a,operand_b;
  wire branch_taken,pc_set;
  wire [31:0] pc_unused;
  wire [7:0] spi_price;
  reg price_ack_pending=1'b0;

  // Preserve the approved probe as the first-commit qualifier.
  // The integral monitor owns the physical LEDs.
  wire [3:0] pc_probe_led;
  wire pc_probe_valid;
  wire [31:0] pc_probe_pc,pc_probe_instr;
  reg status_pending=0;
  always @(posedge system_clk)
    status_pending <= rst_ni && status_read;
  wire monitor_error;
  wire [3:0] monitor_led;
  wire [3:0] uart_led;
  localparam UART_DIAG = TIMEOUT_DIAG>=2;
  assign o_LED=UART_DIAG ? uart_led : monitor_led;
  wire [2:0] debug_master_state;
  wire debug_in_tick,debug_price_read,debug_decision_written;
  wire [3:0] timeout_code;
  demo_integral_monitor #(.TIMEOUT_DIAG(TIMEOUT_DIAG),.TERMINAL_ONLY(SLOW_CLOCK)) u_monitor(
    .timeout_code(timeout_code),.debug_in_tick(debug_in_tick),
    .debug_price_read(debug_price_read),.debug_decision_written(debug_decision_written),
    .clk(system_clk),.rst(!rst_ni),.byte_done(spi_byte_done),
    .first_commit(!pc_probe_valid && commit_evt && pc_id==32'h14 && (spi_byte_done || first_byte_seen)),
    .status_valid(status_pending && data_rdata[0]),
    .access({decision_write,ready_read,sum_read,price_read}),
    .frame_index(frame_index),.transport_timeout(master_timeout),.frame_start(frame_start),.response_ok(response_ok),
    .price(spi_price),.decision(data_wdata[7:0]),
    .response_valid(response_valid),.master_done(master_done),
    .led(monitor_led),.error(monitor_error),.final_complete(final_complete),.first_byte_seen(first_byte_seen));

  assign commit_evt = instr_valid_id && !core_stall;

  price_spi_master_probe #(
    .TICKS(TICKS),
    .HALF_PERIOD(32),
    .MIN_GAP_CYCLES(6000)
  ) u_master (
    .clk_i(system_clk),
    .rst_ni(rst_ni),
    .enable_i(rst_ni),
    .price_consumed_i(price_ack_pending),.final_complete_i(UART_DIAG ? debug_decision_written : final_complete),
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
    .NumWords(71),.FETCH_ROM(FETCH_ROM),.WARMUP(SLOW_CLOCK),
    .MemFile("proyecto4/alternativas/mmio_sma10/sw/trade.hex")
  ) u_soc (
    .i_Clk(system_clk),
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
    .dbg_spi_rdata(spi_rdata),
    .dbg_operand_a(operand_a),.dbg_operand_b(operand_b),
    .dbg_branch_taken(branch_taken),.dbg_pc_set(pc_set)
  );

  first_post_byte_pc_probe u_pc_probe (
    .clk_i(system_clk),
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

  wire debug_uart_tx;
  generate if(TIMEOUT_DIAG==1) begin : g_timeout_diag
    assign debug_uart_tx=1'b1;
    assign uart_led=4'd0;
    // Read-only shadow of the slave's new_price_q with the same priority.
    reg price_pending=0;
    reg commit_after_byte=0, request_after_byte=0;
    reg [1:0] last_commit_tag=0;
    wire poll_pc_aligned=(pc_id[31:4]==28'd1) && (pc_id[1:0]==0);
    always @(posedge system_clk) begin
      if(!rst_ni || frame_start) begin
        commit_after_byte<=0;
        request_after_byte<=0;
        last_commit_tag<=0;
      end else if(debug_in_tick || spi_byte_done) begin
        if(commit_evt) begin
          commit_after_byte<=1;
          last_commit_tag<=poll_pc_aligned ? pc_id[3:2] : 2'd0;
        end
        // Ignore the request coincident with byte_done. It can sample the
        // old STATUS. The issue in hardware is the missing next request.
        if(debug_in_tick && data_req) request_after_byte<=1;
      end
    end
    always @(posedge system_clk) begin
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

    (* keep *) reg [4:0] snapshot_payload=0;
    always @(posedge system_clk) begin
      if(!rst_ni) snapshot_valid<=0;
      else if(capture) begin
        snapshot_valid<=1;
        snapshot_done_state<=debug_master_state[1];
        snapshot_index<=frame_index;

        snapshot_payload<={price_ack_pending,spi_byte_done,price_pending,
                           debug_decision_written,final_complete};
      end
    end
    // During normal execution each prior frame has one validated DECISION.
    // Record the count as its two inputs instead of duplicating an adder.
    // At timeout only WAIT_ACK (101) and DONE (111) are reachable.
    wire [2:0] snapshot_state={1'b1,snapshot_done_state,1'b1};
    // Neither pulse can be active in WAIT_ACK or DONE: ACK acceptance
    // moves to GAP, and frame_start moves to LOW. DONE sets master_done.
    wire [7:0] snapshot_flags={snapshot_payload[4],2'b00,snapshot_payload[3:1],
                              snapshot_done_state,snapshot_payload[0]};
    // At either state FINISH has already emitted the current frame.
    wire [4:0] snapshot_sent={1'b0,snapshot_index}+5'd1;
    wire [4:0] snapshot_decision_count=snapshot_sent-!snapshot_flags[2];
    wire [12:0] snapshot_gap_count=snapshot_valid ? 13'h1fff : 13'd0;
    wire snapshot_timeout_enable=snapshot_valid;
    wire snapshot_rst_ni=snapshot_valid;

    wire [3:0] commit_code=(last_commit_tag==0) ? 4'h8 : {2'b01,last_commit_tag};
    assign timeout_code=master_done ? 4'h2 :
                        !debug_in_tick ? 4'h4 :
                        debug_price_read ? 4'h3 :
                        request_after_byte ? 4'h9 :
                        commit_after_byte ? commit_code : 4'h1;
  end else if(UART_DIAG) begin : g_timeout_uart
    reg uart_timeout=0, uart_miso_error=0;
    wire captured_commit,observe_commit;
    wire [31:0] captured_pc,captured_word;
    wire [7:0] packet_header;
    always @(posedge system_clk) begin
      if(!rst_ni) begin
        uart_timeout<=0;
        uart_miso_error<=0;
      end else begin
        if(master_timeout) uart_timeout<=1;
        if(response_valid && !response_ok) uart_miso_error<=1;
      end
    end
    assign uart_led=uart_miso_error ? 4'hd : uart_timeout ? 4'h8 : 4'h0;
    if(TIMEOUT_DIAG>=4) begin : g_boot_poll
      reg poll_seen=0,next_pending=0,next_is_poll=0,left_poll=0;
      reg status_one=0;
      reg [4:0] poll_flags=0;
      wire before_first_byte=!first_byte_seen && !spi_byte_done;
      // Track polling before the first byte. Freeze at the first unexpected
      // exit even if earlier iterations returned to STATUS correctly.
      assign observe_commit=commit_evt && before_first_byte &&
                            !left_poll && !next_pending && pc_id==32'h1c;
      assign captured_commit=poll_seen;
      assign captured_pc=instr_id;
      assign captured_word=0;
      assign packet_header=TIMEOUT_DIAG==5 ?
        {7'h5a,left_poll} :
        {1'b1,status_one,poll_flags,next_is_poll};
      always @(posedge system_clk) begin
        if(!rst_ni) begin
          poll_seen<=0; next_pending<=0; next_is_poll<=0; left_poll<=0;
          status_one<=0; poll_flags<=0;
        end else begin
          if(before_first_byte && !left_poll && status_pending && data_rdata[0])
            status_one<=1;
          if(observe_commit) begin
            poll_seen<=1;
            next_pending<=1;
            next_is_poll<=0;
            poll_flags<={operand_a==0,operand_b==0,
                         instr_id==32'hfe010ce3,branch_taken,pc_set};
          end
          if(next_pending && commit_evt) begin
            next_pending<=0;
            next_is_poll<=(pc_id==32'h14);
            if(before_first_byte && pc_id!=32'h14)
              left_poll<=1;
          end
        end
      end
    end else begin : g_last_commit
      reg seen=0;
      assign observe_commit=commit_evt && (debug_in_tick || spi_byte_done);
      assign captured_commit=seen;
      always @(posedge system_clk)
        if(!rst_ni || frame_start) seen<=0;
        else if(observe_commit) seen<=1;
      // Bit zero of the aligned PC carries the branch outcome in context mode.
      assign captured_pc=TIMEOUT_DIAG==3 ? {pc_id[31:1],branch_taken} : pc_id;
      assign captured_word=TIMEOUT_DIAG==3 ? operand_a : instr_id;
      assign packet_header=TIMEOUT_DIAG==3 ? {3'b110,master_done,frame_index} : 8'ha5;
    end
    timeout_pc_uart #(.PAYLOAD_BYTES(TIMEOUT_DIAG==4 ? 0 : TIMEOUT_DIAG==5 ? 4 : 8)) u_uart(
      .clk(system_clk),.rst_n(rst_ni),
      .write_capture(observe_commit && !master_timeout && !uart_timeout),
      .trigger(master_timeout && !uart_timeout && captured_commit),
      .header(packet_header),.pc(captured_pc),.insn(captured_word),.tx(debug_uart_tx));
    assign timeout_code=master_done ? 4'h2 : captured_commit ? 4'h8 : 4'h1;
  end else if(SLOW_CLOCK) begin : g_integral_uart
    // The terminal code is held by the monitor. Synchronize its validity
    // before sending the code once at 115200 from the original board clock.
    reg [1:0] terminal_sync=0;
    reg reported=0;
    always @(posedge i_Clk) begin
      terminal_sync<={terminal_sync[0],monitor_led[3]};
      if(terminal_sync[1]) reported<=1;
    end
    terminal_status_uart u_uart(
      .clk(i_Clk),
      .trigger(terminal_sync[1] && !reported),
      .value({4'ha,monitor_led}),.tx(debug_uart_tx));
    assign uart_led=4'd0;
    assign timeout_code=4'hf;
  end else begin : g_no_timeout_diag
    assign debug_uart_tx=1'b1;
    assign uart_led=4'd0;
    assign timeout_code=4'hf;
  end endgenerate

  // Stop-and-wait: the SPI master sends the next price only after Espino
  // reads PRICE for the current one. Last tick needs no following ACK.
  always @(posedge system_clk) begin
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



















