// UART RX 8N1, LSB first. 25 MHz / 115200 baud ~= 217 clocks per bit.
module uart_rx #(
  parameter integer CLKS_PER_BIT = 217
) (
  input wire clk_i,
  input wire serial_i,
  output reg data_valid_o = 1'b0,
  output reg [7:0] data_o = 8'h00
);
  localparam [1:0] IDLE=2'd0, START=2'd1, DATA=2'd2, STOP=2'd3;
  reg [1:0] state = IDLE;
  reg rx_meta = 1'b1, rx_sync = 1'b1;
  reg [15:0] clock_count = 16'd0;
  reg [2:0] bit_index = 3'd0;
  reg [7:0] shift = 8'h00;

  always @(posedge clk_i) begin
    rx_meta <= serial_i;
    rx_sync <= rx_meta;
    data_valid_o <= 1'b0;
    case (state)
      IDLE: if (!rx_sync) begin
        state <= START;
        clock_count <= 16'd0;
      end
      START: if (clock_count == (CLKS_PER_BIT/2)-1) begin
        clock_count <= 16'd0;
        if (!rx_sync) begin bit_index <= 3'd0; state <= DATA; end
        else state <= IDLE;
      end else clock_count <= clock_count + 1'b1;
      DATA: if (clock_count == CLKS_PER_BIT-1) begin
        clock_count <= 16'd0;
        shift[bit_index] <= rx_sync;
        if (bit_index == 3'd7) state <= STOP;
        else bit_index <= bit_index + 1'b1;
      end else clock_count <= clock_count + 1'b1;
      STOP: if (clock_count == CLKS_PER_BIT-1) begin
        clock_count <= 16'd0;
        state <= IDLE;
        if (rx_sync) begin data_o <= shift; data_valid_o <= 1'b1; end
      end else clock_count <= clock_count + 1'b1;
      default: state <= IDLE;
    endcase
  end
endmodule
