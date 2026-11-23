// SPI master interno de solo precios. No conoce decisiones ni las calcula.
module price_generator #(
  parameter integer N = 32,
  parameter integer HALF_PERIOD = 32,
  parameter integer GAP_CYCLES = 12000,
  parameter PRICE_FILE = "proyecto4/pruebas_fisicas/agente_completo/data/prices.hex"
) (
  input wire clk_i, input wire rst_ni, input wire enable_i,
  output reg sclk_o = 1'b0, output reg mosi_o = 1'b0,
  output reg cs_n_o = 1'b1, input wire miso_i,
  output reg [7:0] rx_byte_o = 0, output reg rx_valid_o = 0,
  output reg [15:0] tick_o = 0, output reg done_o = 0
);
  reg [7:0] prices [0:N-1];
  initial $readmemh(PRICE_FILE, prices);
  localparam IDLE=0, SELECT=1, LOW=2, HIGH=3, FINISH=4, GAP=5, DONE=6;
  reg [2:0] state=IDLE;
  integer count=0, bit_index=7, timer=0, gap_timer=0;
  reg [7:0] rx_shift=0;
  always @(posedge clk_i or negedge rst_ni) begin
    if (!rst_ni) begin
      state<=IDLE; sclk_o<=0; mosi_o<=0; cs_n_o<=1;
      rx_byte_o<=0; rx_valid_o<=0; tick_o<=0; done_o<=0;
      count<=0; bit_index<=7; timer<=0; gap_timer<=0; rx_shift<=0;
    end else begin
      rx_valid_o<=0;
      case(state)
        IDLE: if(enable_i) begin count<=0; tick_o<=0; done_o<=0; state<=SELECT; end
        SELECT: begin cs_n_o<=0; sclk_o<=0; mosi_o<=prices[count][7]; bit_index<=7; timer<=0; rx_shift<=0; state<=LOW; end
        LOW: if(timer==HALF_PERIOD-1) begin timer<=0; sclk_o<=1; rx_shift<={rx_shift[6:0],miso_i}; state<=HIGH; end else timer<=timer+1;
        HIGH: if(timer==HALF_PERIOD-1) begin
          timer<=0; sclk_o<=0;
          if(bit_index==0) state<=FINISH;
          else begin bit_index<=bit_index-1; mosi_o<=prices[count][bit_index-1]; state<=LOW; end
        end else timer<=timer+1;
        FINISH: begin
          cs_n_o<=1; rx_byte_o<=rx_shift; rx_valid_o<=1; tick_o<=count+1;
          if(count==N-1) begin done_o<=1; state<=DONE; end
          else begin count<=count+1; gap_timer<=0; state<=GAP; end
        end
        GAP: if(gap_timer==GAP_CYCLES-1) state<=SELECT; else gap_timer<=gap_timer+1;
        DONE: begin cs_n_o<=1; sclk_o<=0; end
        default: state<=IDLE;
      endcase
    end
  end
endmodule
