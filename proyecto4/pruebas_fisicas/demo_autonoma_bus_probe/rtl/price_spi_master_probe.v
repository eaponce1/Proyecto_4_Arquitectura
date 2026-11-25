// Local copy of the diagnostic master; transmits prices only.
module price_spi_master_probe #(parameter integer TICKS=16,HALF_PERIOD=32,MIN_GAP_CYCLES=6000)(
 input wire clk_i,rst_ni,enable_i,price_consumed_i,
 output reg sclk_o,mosi_o,cs_n_o,input wire miso_i,
 output reg [7:0] response_o,output reg response_valid_o,
 output reg [4:0] sent_o,output reg done_o,
 output reg frame_start_o,ack_accepted_o,sclk_rise_o);
 localparam [2:0] IDLE=0,SELECT=1,LOW=2,HIGH=3,FINISH=4,WAIT_ACK=5,GAP=6,DONE=7;
 reg [2:0] state=IDLE;
 reg [4:0] price_index=0;
 reg [2:0] bit_index=7;
 reg [5:0] half_count=0;
 reg [12:0] gap_count=0;
 reg [7:0] rx_shift=0;
 wire [7:0] current_price=(price_index<10)?8'd200:(price_index<13)?8'd90:8'd220;
 always @(posedge clk_i or negedge rst_ni) begin
  if(!rst_ni) begin
   state<=IDLE;sclk_o<=0;mosi_o<=0;cs_n_o<=1;response_o<=0;response_valid_o<=0;
   sent_o<=0;done_o<=0;frame_start_o<=0;ack_accepted_o<=0;sclk_rise_o<=0;
   price_index<=0;bit_index<=7;half_count<=0;gap_count<=0;rx_shift<=0;
  end else begin
   response_valid_o<=0;frame_start_o<=0;ack_accepted_o<=0;sclk_rise_o<=0;
   case(state)
    IDLE: if(enable_i) begin price_index<=0;sent_o<=0;done_o<=0;state<=SELECT;end
    SELECT: begin cs_n_o<=0;sclk_o<=0;mosi_o<=current_price[7];bit_index<=7;half_count<=0;rx_shift<=0;frame_start_o<=1;state<=LOW;end
    LOW: if(half_count==HALF_PERIOD-1) begin half_count<=0;sclk_o<=1;sclk_rise_o<=1;rx_shift<={rx_shift[6:0],miso_i};state<=HIGH;end else half_count<=half_count+1'b1;
    HIGH: if(half_count==HALF_PERIOD-1) begin
     half_count<=0;sclk_o<=0;
     if(bit_index==0) state<=FINISH;
     else begin bit_index<=bit_index-1'b1;mosi_o<=current_price[bit_index-1'b1];state<=LOW;end
    end else half_count<=half_count+1'b1;
    FINISH: begin cs_n_o<=1;response_o<=rx_shift;response_valid_o<=1;sent_o<=price_index+1'b1;if(price_index==TICKS-1)begin done_o<=1;state<=DONE;end else state<=WAIT_ACK;end
    WAIT_ACK: if(price_consumed_i) begin ack_accepted_o<=1;gap_count<=0;state<=GAP;end
    GAP: if(gap_count==MIN_GAP_CYCLES-1)begin price_index<=price_index+1'b1;state<=SELECT;end else gap_count<=gap_count+1'b1;
    DONE: begin cs_n_o<=1;sclk_o<=0;end
    default:state<=IDLE;
   endcase
  end
 end
endmodule
