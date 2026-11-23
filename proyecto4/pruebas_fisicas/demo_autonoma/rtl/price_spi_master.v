// SPI mode 0 master: deterministic price-only sequence.
// 10x 200, 3x 90, 3x 220. Bounded counters keep FPGA cost small.
module price_spi_master #(
  parameter integer TICKS=16,
  parameter integer HALF_PERIOD=32,
  parameter integer GAP_CYCLES=6000
) (
  input wire clk_i,input wire rst_ni,input wire enable_i,
  output reg sclk_o=0,output reg mosi_o=0,output reg cs_n_o=1,input wire miso_i,
  output reg [7:0] response_o=0,output reg response_valid_o=0,
  output reg [4:0] sent_o=0,output reg done_o=0
);
  localparam [2:0] IDLE=0,SELECT=1,LOW=2,HIGH=3,FINISH=4,GAP=5,DONE=6;
  reg [2:0] state=IDLE;
  reg [4:0] price_index=0;
  reg [2:0] bit_index=7;
  reg [5:0] half_count=0;
  reg [12:0] gap_count=0;
  reg [7:0] rx_shift=0;
  wire [7:0] current_price = (price_index<10) ? 8'd200 :
                             (price_index<13) ? 8'd90 : 8'd220;

  always @(posedge clk_i or negedge rst_ni) begin
    if(!rst_ni) begin
      state<=IDLE;sclk_o<=0;mosi_o<=0;cs_n_o<=1;response_o<=0;
      response_valid_o<=0;sent_o<=0;done_o<=0;price_index<=0;
      bit_index<=7;half_count<=0;gap_count<=0;rx_shift<=0;
    end else begin
      response_valid_o<=0;
      case(state)
        IDLE: if(enable_i) begin price_index<=0;sent_o<=0;done_o<=0;state<=SELECT;end
        SELECT: begin
          cs_n_o<=0;sclk_o<=0;mosi_o<=current_price[7];bit_index<=7;
          half_count<=0;rx_shift<=0;state<=LOW;
        end
        LOW: if(half_count==HALF_PERIOD-1) begin
          half_count<=0;sclk_o<=1;rx_shift<={rx_shift[6:0],miso_i};state<=HIGH;
        end else half_count<=half_count+1'b1;
        HIGH: if(half_count==HALF_PERIOD-1) begin
          half_count<=0;sclk_o<=0;
          if(bit_index==0) state<=FINISH;
          else begin bit_index<=bit_index-1'b1;mosi_o<=current_price[bit_index-1'b1];state<=LOW;end
        end else half_count<=half_count+1'b1;
        FINISH: begin
          cs_n_o<=1;response_o<=rx_shift;response_valid_o<=1;
          sent_o<=price_index+1'b1;
          if(price_index==TICKS-1) begin done_o<=1;state<=DONE;end
          else begin price_index<=price_index+1'b1;gap_count<=0;state<=GAP;end
        end
        GAP: if(gap_count==GAP_CYCLES-1) state<=SELECT;
             else gap_count<=gap_count+1'b1;
        DONE: begin cs_n_o<=1;sclk_o<=0;end
        default: state<=IDLE;
      endcase
    end
  end
endmodule
