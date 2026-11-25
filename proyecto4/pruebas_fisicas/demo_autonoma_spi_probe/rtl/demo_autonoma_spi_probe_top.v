module demo_autonoma_spi_probe_top (
  input wire i_Clk,
  output wire [3:0] o_LED
);
  localparam integer TICKS=16;
  wire rst_ni,sclk,mosi,cs_n,miso;
  wire [7:0] response;
  wire response_valid,master_done,frame_start,ack_accepted,sclk_rise;
  wire [4:0] sent_count;
  wire instr_req,status_read,price_read,sum_read,ready_read,decision_write,spi_byte_done;
  wire [31:0] data_wdata;

  reg master_started=0,cs_seen=0,master_eight=0,slave_done=0;
  reg status_after_price=0,price_read_seen=0,ack_seen=0,price_ack_pending=0;
  reg price_read_since_tick=0;
  reg [4:0] decision_count=0;
  reg [3:0] master_rise_count=0;

  // Mirror the unmodified slave input synchronizers/edge equations so we can
  // see whether the physical SCLK edges reach a clock-domain detector.
  reg [2:0] sclk_sync=0,cs_sync=3'b111;
  wire shadow_sclk_r=sclk_sync[1]&~sclk_sync[2];
  wire shadow_cs_active=~cs_sync[1];
  wire shadow_cs_assert=~cs_sync[1]&cs_sync[2];
  reg [3:0] shadow_rise_count=0;
  always @(posedge i_Clk or negedge rst_ni) begin
    if(!rst_ni) begin sclk_sync<=0;cs_sync<=3'b111;shadow_rise_count<=0;end
    else begin
      sclk_sync<={sclk_sync[1:0],sclk};
      cs_sync<={cs_sync[1:0],cs_n};
      if(shadow_cs_assert) shadow_rise_count<=0;
      else if(shadow_cs_active && shadow_sclk_r && shadow_rise_count<8)
        shadow_rise_count<=shadow_rise_count+1'b1;
    end
  end

  price_spi_master_probe #(.TICKS(TICKS),.HALF_PERIOD(32),.MIN_GAP_CYCLES(6000)) u_master(
    .clk_i(i_Clk),.rst_ni(rst_ni),.enable_i(rst_ni),.price_consumed_i(price_ack_pending),
    .sclk_o(sclk),.mosi_o(mosi),.cs_n_o(cs_n),.miso_i(miso),
    .response_o(response),.response_valid_o(response_valid),.sent_o(sent_count),.done_o(master_done),
    .frame_start_o(frame_start),.ack_accepted_o(ack_accepted),.sclk_rise_o(sclk_rise)
  );

  pochoco_soc_demo #(.NumWords(71),.MemFile("proyecto4/alternativas/mmio_sma10/sw/trade.hex")) u_soc(
    .i_Clk(i_Clk),.i_SPI_SCLK(sclk),.i_SPI_MOSI(mosi),.i_SPI_CS_n(cs_n),.o_SPI_MISO(miso),
    .dbg_reset_released(rst_ni),.dbg_instr_req(instr_req),.dbg_status_read(status_read),
    .dbg_price_read(price_read),.dbg_sum_read(sum_read),.dbg_ready_read(ready_read),
    .dbg_decision_write(decision_write),.dbg_spi_byte_done(spi_byte_done),.dbg_data_wdata(data_wdata)
  );

  always @(posedge i_Clk or negedge rst_ni) begin
    if(!rst_ni) begin
      master_started<=0;cs_seen<=0;master_eight<=0;slave_done<=0;
      status_after_price<=0;price_read_seen<=0;ack_seen<=0;price_ack_pending<=0;master_rise_count<=0;
      price_read_since_tick<=0;decision_count<=0;
    end else begin
      if(frame_start && !master_started) master_started<=1;
      if(!cs_n && !cs_seen) cs_seen<=1;
      if(frame_start && !master_eight) master_rise_count<=0;
      else if(sclk_rise && master_rise_count<8) begin
        master_rise_count<=master_rise_count+1'b1;
        if(master_rise_count==7) master_eight<=1;
      end
      if(spi_byte_done && !slave_done) slave_done<=1;
      if(spi_byte_done) begin price_ack_pending<=0;price_read_since_tick<=0;end
      if(slave_done && status_read && !status_after_price) status_after_price<=1;
      if(slave_done && price_read) begin
        price_ack_pending<=1;
        price_read_since_tick<=1;
        if(!price_read_seen) price_read_seen<=1;
      end
      if(decision_write && price_read_since_tick && decision_count<TICKS) begin
        decision_count<=decision_count+1'b1;
        price_read_since_tick<=0;
      end
      if(ack_accepted && !ack_seen) ack_seen<=1;
    end
  end

  // Before byte_done, LEDs are sticky event bits: D1=start, D2=CS,
  // D3=eight master rising edges, D4=actual slave byte_done.
  // Afterwards D1/D2 progress through STATUS, PRICE and ACK respectively.
  wire [3:0] expected_led = !slave_done ? {slave_done,master_eight,cs_seen,master_started} :
                            !status_after_price ? 4'b1111 :
                            !price_read_seen ? 4'b1110 :
                            !ack_seen ? 4'b1101 : 4'b1100;
  assign o_LED=expected_led;
endmodule
