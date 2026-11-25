module demo_autonoma_trace_top (
  input wire i_Clk,
  output wire [3:0] o_LED
);
  localparam integer TICKS=16;
  wire rst_ni,sclk,mosi,cs_n,miso;
  wire [7:0] response;
  wire response_valid,master_done,frame_start,ack_accepted;
  wire [4:0] sent_count;
  wire instr_req,status_read,price_read,sum_read,ready_read,decision_write,spi_byte_done;
  wire [31:0] data_wdata;
  reg [3:0] progress=0;
  reg price_pending=0,price_read_since_tick=0,price_ack=0;
  reg [4:0] decision_count=0;
  reg first_price_seen=0,sum_seen=0,ready_seen=0;

  price_spi_master_trace #(.TICKS(TICKS),.HALF_PERIOD(32),.MIN_GAP_CYCLES(6000)) u_master(
    .clk_i(i_Clk),.rst_ni(rst_ni),.enable_i(rst_ni),.price_consumed_i(price_ack),
    .sclk_o(sclk),.mosi_o(mosi),.cs_n_o(cs_n),.miso_i(miso),
    .response_o(response),.response_valid_o(response_valid),.sent_o(sent_count),
    .done_o(master_done),.frame_start_o(frame_start),.ack_accepted_o(ack_accepted)
  );

  pochoco_soc_demo #(.NumWords(71),.MemFile("proyecto4/alternativas/mmio_sma10/sw/trade.hex")) u_soc(
    .i_Clk(i_Clk),.i_SPI_SCLK(sclk),.i_SPI_MOSI(mosi),.i_SPI_CS_n(cs_n),.o_SPI_MISO(miso),
    .dbg_reset_released(rst_ni),.dbg_instr_req(instr_req),.dbg_status_read(status_read),
    .dbg_price_read(price_read),.dbg_sum_read(sum_read),.dbg_ready_read(ready_read),
    .dbg_decision_write(decision_write),.dbg_spi_byte_done(spi_byte_done),.dbg_data_wdata(data_wdata)
  );

  always @(posedge i_Clk or negedge rst_ni) begin
    if(!rst_ni) begin
      progress<=0;price_pending<=0;price_read_since_tick<=0;price_ack<=0;
      decision_count<=0;first_price_seen<=0;sum_seen<=0;ready_seen<=0;
    end else begin
      // Stage encoding is monotonic. STATUS before the first received price is
      // intentionally ignored because firmware polls STATUS while waiting.
      if(progress==0 && instr_req) progress<=1;
      else if(progress==1 && frame_start) progress<=2;
      else if(progress==2 && spi_byte_done) begin progress<=3;first_price_seen<=1;end
      else if(progress==3 && first_price_seen && status_read) progress<=4;
      else if(progress==4 && price_read) progress<=5;
      else if(progress==5 && ack_accepted) progress<=6;
      else if(progress==6 && (sum_seen||sum_read) && (ready_seen||ready_read)) progress<=7;
      else if(progress==7 && decision_write) progress<=8;
      else if(progress==8 && response_valid && sent_count>=2) progress<=9;

      if(sum_read) sum_seen<=1;
      if(ready_read) ready_seen<=1;
      if(spi_byte_done) begin price_pending<=1;price_read_since_tick<=0;price_ack<=0;end
      if(price_read) begin price_pending<=0;price_read_since_tick<=1;price_ack<=1;end
      if(decision_write && price_read_since_tick && decision_count<TICKS) begin
        decision_count<=decision_count+1'b1;
        price_read_since_tick<=0;
      end
    end
  end

  // Binary progress code, D1 is bit 0 and D4 is bit 3.
  assign o_LED=progress;
endmodule
