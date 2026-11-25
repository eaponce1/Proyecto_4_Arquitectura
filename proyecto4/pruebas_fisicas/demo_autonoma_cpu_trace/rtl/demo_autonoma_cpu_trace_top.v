module demo_autonoma_cpu_trace_top(input wire i_Clk,output reg [3:0] o_LED=0);
  localparam integer TICKS=16;
  wire rst_ni,sclk,mosi,cs_n,miso;
  wire [7:0] response;
  wire response_valid,master_done,frame_start,ack_accepted,sclk_rise;
  wire [4:0] sent_count;
  wire instr_req,commit_evt,core_stall,data_req,data_we;
  wire status_read,price_read,sum_read,ready_read,decision_write,spi_byte_done;
  wire [3:0] data_be;
  wire [31:0] instr_addr,core_pc,pc_id,data_addr,data_wdata,data_rdata,spi_rdata;
  wire [7:0] spi_price;
  reg [3:0] stage=0;
  reg [9:0] seen=0;
  reg price_ack_pending=0,status_req_pending=0;
  reg [7:0] last_decision=0;

  wire fetch_evt=instr_req;
  wire byte_evt=spi_byte_done;
  wire commit_evt_after_byte=(seen[1]||byte_evt)&&commit_evt;
  wire have_commit=seen[2]||commit_evt_after_byte;
  wire data_evt=have_commit&&data_req;
  wire status_req_evt=have_commit&&status_read;
  wire status_resp_evt=status_req_pending&&data_rdata[0];
  wire price_evt=(seen[5]||status_resp_evt)&&price_read;
  wire sumready_evt=(seen[6]||price_evt)&&(sum_read||ready_read);
  wire decision_evt=(seen[7]||sumready_evt)&&decision_write;
  wire miso_evt=(seen[8]||decision_evt)&&response_valid&&(sent_count>=2)&&
                (response==last_decision);

  price_spi_master_probe #(.TICKS(TICKS),.HALF_PERIOD(32),.MIN_GAP_CYCLES(6000)) u_master(
    .clk_i(i_Clk),.rst_ni(rst_ni),.enable_i(rst_ni),.price_consumed_i(price_ack_pending),
    .sclk_o(sclk),.mosi_o(mosi),.cs_n_o(cs_n),.miso_i(miso),
    .response_o(response),.response_valid_o(response_valid),.sent_o(sent_count),
    .done_o(master_done),.frame_start_o(frame_start),.ack_accepted_o(ack_accepted),
    .sclk_rise_o(sclk_rise));

  pochoco_soc_cpu_trace #(.NumWords(71),.MemFile("proyecto4/alternativas/mmio_sma10/sw/trade.hex")) u_soc(
    .i_Clk(i_Clk),.i_SPI_SCLK(sclk),.i_SPI_MOSI(mosi),.i_SPI_CS_n(cs_n),.o_SPI_MISO(miso),
    .dbg_reset_released(rst_ni),.dbg_instr_req(instr_req),.dbg_instr_addr(instr_addr),
    .dbg_commit(commit_evt),.dbg_core_stall(core_stall),.dbg_pc(core_pc),.dbg_pc_id(pc_id),
    .dbg_data_req(data_req),.dbg_data_we(data_we),.dbg_data_be(data_be),
    .dbg_data_addr(data_addr),.dbg_data_wdata(data_wdata),.dbg_data_rdata(data_rdata),
    .dbg_status_read(status_read),.dbg_price_read(price_read),.dbg_sum_read(sum_read),
    .dbg_ready_read(ready_read),.dbg_decision_write(decision_write),
    .dbg_spi_byte_done(spi_byte_done),.dbg_price(spi_price),.dbg_spi_rdata(spi_rdata));

  always @(posedge i_Clk) begin
    if(!rst_ni) begin
      stage<=0;seen<=0;price_ack_pending<=0;status_req_pending<=0;last_decision<=0;
    end else begin
      if(spi_byte_done) price_ack_pending<=0;
      if(price_read) price_ack_pending<=1;
      if(status_req_evt) status_req_pending<=1;
      if(status_resp_evt) status_req_pending<=0;
      if(decision_write) last_decision<=data_wdata[7:0];

      // Event bits are sticky: if several milestones share a clock, none is
      // discarded. The LED sequencer emits their numeric codes one per cycle.
      seen<=seen|{miso_evt,decision_evt,sumready_evt,price_evt,status_resp_evt,
                  status_req_evt,data_evt,commit_evt_after_byte,byte_evt,fetch_evt};
      case(stage)
        0: if(seen[0]||fetch_evt) stage<=1;
        1: if(seen[1]||byte_evt) stage<=2;
        2: if(seen[2]||commit_evt_after_byte) stage<=3;
        3: if(seen[3]||data_evt) stage<=4;
        4: if(seen[4]||status_req_evt) stage<=5;
        5: if(seen[5]||status_resp_evt) stage<=6;
        6: if(seen[6]||price_evt) stage<=7;
        7: if(seen[7]||sumready_evt) stage<=8;
        8: if(seen[8]||decision_evt) stage<=9;
        9: if(seen[9]||miso_evt) stage<=10;
        default: stage<=stage;
      endcase
      o_LED<=stage;
    end
  end
endmodule
