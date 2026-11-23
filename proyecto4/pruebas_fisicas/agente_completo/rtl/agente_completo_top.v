// Top independiente: el agente real permanece en pochoco_soc MMIO SMA10.
module agente_completo_top (
  input wire i_Clk,
  output wire [3:0] o_LED
);
  wire [3:0] soc_led;
  wire sclk, mosi, cs_n;
  wire [7:0] rx_byte;
  wire rx_valid;
  wire [15:0] tick;
  wire generator_done;
  wire [31:0] dbg_addr, dbg_wdata;
  wire dbg_instr_req, dbg_data_req, dbg_data_we, dbg_reset_released;
  wire dbg_status_read, dbg_price_read, dbg_sum_read, dbg_ready_read, dbg_decision_write;
  wire miso;
  reg mmio_seen=0;
  reg [5:0] decision_count=0;
  wire verify_error;
  wire [15:0] verified_count;
  price_generator #(.N(16)) u_generator (
    .clk_i(i_Clk), .rst_ni(dbg_reset_released), .enable_i(dbg_reset_released),
    .sclk_o(sclk), .mosi_o(mosi), .cs_n_o(cs_n), .miso_i(miso),
    .rx_byte_o(rx_byte), .rx_valid_o(rx_valid), .tick_o(tick), .done_o(generator_done)
  );
  pochoco_soc_observable #(.MemFile("proyecto4/alternativas/mmio_sma10/sw/trade.hex"),.EnableSpi(1)) u_soc (
    .i_Clk(i_Clk), .o_LED(soc_led), .i_Switch(4'b0),
    .o_Segment1_A(),.o_Segment1_B(),.o_Segment1_C(),.o_Segment1_D(),.o_Segment1_E(),.o_Segment1_F(),.o_Segment1_G(),
    .o_Segment2_A(),.o_Segment2_B(),.o_Segment2_C(),.o_Segment2_D(),.o_Segment2_E(),.o_Segment2_F(),.o_Segment2_G(),
    .i_SPI_SCLK(sclk), .i_SPI_MOSI(mosi), .i_SPI_CS_n(cs_n), .o_SPI_MISO(miso),
    .dbg_instr_req(dbg_instr_req), .dbg_data_req(dbg_data_req), .dbg_data_we(dbg_data_we), .dbg_data_addr(dbg_addr), .dbg_data_wdata(dbg_wdata), .dbg_reset_released(dbg_reset_released),
    .dbg_status_read(dbg_status_read),.dbg_price_read(dbg_price_read),.dbg_sum_read(dbg_sum_read),.dbg_ready_read(dbg_ready_read),.dbg_decision_write(dbg_decision_write)
  );
  decision_verifier #(.N(16)) u_verifier (
    .clk_i(i_Clk), .rst_ni(dbg_reset_released), .valid_i(rx_valid),
    .response_i(rx_byte), .error_o(verify_error), .checked_o(verified_count)
  );
  always @(posedge i_Clk) begin
    if (!dbg_reset_released) begin mmio_seen<=0; decision_count<=0; end
    else begin
      if (dbg_sum_read || dbg_ready_read) mmio_seen<=1;
      if (dbg_decision_write && decision_count<16) decision_count<=decision_count+1'b1;
    end
  end
  // LED0=Espino con fetch, LED1=lectura MMIO SMA, LED2=error MISO, LED3=fin verificado.
  assign o_LED={generator_done && (verified_count==16) && (decision_count==16) && !verify_error,verify_error,mmio_seen,dbg_instr_req};
endmodule
