module demo_autonoma_bus_probe_top(input wire i_Clk,output reg [3:0] o_LED=0);
  localparam integer TICKS=16;
  wire rst_ni,sclk,mosi,cs_n,miso;
  wire [7:0] response;
  wire response_valid,master_done,frame_start,ack_accepted,sclk_rise;
  wire [4:0] sent_count;
  wire instr_req,data_req,data_we,status_read,price_read,sum_read,ready_read;
  wire decision_write,spi_byte_done;
  wire [3:0] data_be;
  wire [31:0] instr_addr,data_addr,data_wdata,data_rdata,spi_rdata;
  wire [7:0] spi_price;
  reg [3:0] master_rises=0;
  reg price_ack_pending=0;
  reg status_req_q=0;
  reg [31:0] pc_at_status=0;
  reg [3:0] stage=0;
  reg saw_fetch=0,saw_byte=0,saw_status_req=0,saw_status_data=0,saw_pc_advance=0;

  price_spi_master_probe #(.TICKS(TICKS),.HALF_PERIOD(32),.MIN_GAP_CYCLES(6000)) u_master(
    .clk_i(i_Clk),.rst_ni(rst_ni),.enable_i(rst_ni),.price_consumed_i(price_ack_pending),
    .sclk_o(sclk),.mosi_o(mosi),.cs_n_o(cs_n),.miso_i(miso),
    .response_o(response),.response_valid_o(response_valid),.sent_o(sent_count),
    .done_o(master_done),.frame_start_o(frame_start),.ack_accepted_o(ack_accepted),
    .sclk_rise_o(sclk_rise));

  pochoco_soc_bus_probe #(.NumWords(71),.MemFile("proyecto4/alternativas/mmio_sma10/sw/trade.hex")) u_soc(
    .i_Clk(i_Clk),.i_SPI_SCLK(sclk),.i_SPI_MOSI(mosi),.i_SPI_CS_n(cs_n),.o_SPI_MISO(miso),
    .dbg_reset_released(rst_ni),.dbg_instr_req(instr_req),.dbg_instr_addr(instr_addr),
    .dbg_data_req(data_req),.dbg_data_we(data_we),.dbg_data_be(data_be),
    .dbg_data_addr(data_addr),.dbg_data_wdata(data_wdata),.dbg_data_rdata(data_rdata),
    .dbg_status_read(status_read),.dbg_price_read(price_read),.dbg_sum_read(sum_read),
    .dbg_ready_read(ready_read),.dbg_decision_write(decision_write),
    .dbg_spi_byte_done(spi_byte_done),.dbg_price(spi_price),.dbg_spi_rdata(spi_rdata));

  // LED stage codes are sticky and identify the STATUS load path.
  // 1=fetch, 2=byte_done, 3=correct STATUS bus request, 4=valid STATUS data,
  // 5=PC/fetch resumes, 6=STATUS response invalid, A=unexpected bus request.
  always @(posedge i_Clk) begin
    if(!rst_ni) begin
      stage<=0;status_req_q<=0;pc_at_status<=0;
      saw_fetch<=0;saw_byte<=0;saw_status_req<=0;saw_status_data<=0;saw_pc_advance<=0;
      master_rises<=0;price_ack_pending<=0;
    end else begin
      status_req_q<=0;
      if(spi_byte_done)price_ack_pending<=0;
      if(price_read)price_ack_pending<=1;
      if(instr_req && !saw_fetch) begin saw_fetch<=1;if(stage==0)stage<=1;end
      if(frame_start && sent_count==0) master_rises<=0;
      else if(sclk_rise && master_rises<8) master_rises<=master_rises+1'b1;
      if(spi_byte_done && !saw_byte) begin saw_byte<=1;stage<=2;end
      status_req_q<=0;
      if(saw_byte && !saw_status_req && data_req) begin
        if(!data_we && data_addr==32'h80010000) begin
          saw_status_req<=1;status_req_q<=1;pc_at_status<=instr_addr;stage<=3;
        end else if(stage<3) stage<=4'ha;
      end
      if(status_req_q && !saw_status_data) begin
        if(data_rdata[0] && spi_rdata[0]) begin saw_status_data<=1;stage<=4;end
        else stage<=6;
      end
      if(saw_status_data && !saw_pc_advance && instr_req && instr_addr!=pc_at_status) begin
        saw_pc_advance<=1;stage<=5;
      end
      o_LED<=stage;
    end
  end
endmodule
