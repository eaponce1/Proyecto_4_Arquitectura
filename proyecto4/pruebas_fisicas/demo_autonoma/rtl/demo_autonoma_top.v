module demo_autonoma_top(
  input wire i_Clk,output wire [3:0] o_LED
);
  localparam integer TICKS=16;
  wire rst_ni;
  wire sclk,mosi,cs_n,miso;
  wire [7:0] response;
  wire response_valid,master_done;
  wire [4:0] sent_count;
  wire instr_req,status_read,price_read,sum_read,ready_read,decision_write;
  wire spi_byte_done;
  wire [31:0] data_wdata;
  reg cpu_seen=0,sma_seen=0,error_seen=0;
  reg price_pending=0,price_read_since_tick=0;
  reg [4:0] decision_count=0;

  price_spi_master #(.TICKS(TICKS),.HALF_PERIOD(32),.GAP_CYCLES(6000)) u_master(
    .clk_i(i_Clk),.rst_ni(rst_ni),.enable_i(rst_ni),
    .sclk_o(sclk),.mosi_o(mosi),.cs_n_o(cs_n),.miso_i(miso),
    .response_o(response),.response_valid_o(response_valid),
    .sent_o(sent_count),.done_o(master_done)
  );
  pochoco_soc_demo #(.NumWords(71),.MemFile("proyecto4/alternativas/mmio_sma10/sw/trade.hex")) u_soc(
    .i_Clk(i_Clk),.i_SPI_SCLK(sclk),.i_SPI_MOSI(mosi),.i_SPI_CS_n(cs_n),.o_SPI_MISO(miso),
    .dbg_reset_released(rst_ni),.dbg_instr_req(instr_req),
    .dbg_status_read(status_read),.dbg_price_read(price_read),.dbg_sum_read(sum_read),
    .dbg_ready_read(ready_read),.dbg_decision_write(decision_write),
    .dbg_spi_byte_done(spi_byte_done),
    .dbg_data_wdata(data_wdata)
  );
  always @(posedge i_Clk or negedge rst_ni) begin
    if(!rst_ni) begin
      cpu_seen<=0;sma_seen<=0;error_seen<=0;price_pending<=0;
      price_read_since_tick<=0;decision_count<=0;
    end else begin
      if(instr_req) cpu_seen<=1;
      if(sum_read || ready_read) sma_seen<=1;
      if(spi_byte_done) begin
        if(price_pending) error_seen<=1;
        price_pending<=1;
        price_read_since_tick<=0;
      end
      if(price_read) begin price_pending<=0;price_read_since_tick<=1;end
      if(decision_write) begin
        if(!price_read_since_tick || decision_count>=TICKS) error_seen<=1;
        else begin decision_count<=decision_count+1'b1;price_read_since_tick<=0;end
      end
    end
  end
  assign o_LED={master_done && decision_count==TICKS && sent_count==TICKS,
                error_seen,sma_seen,cpu_seen};
endmodule
