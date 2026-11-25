// UART TX 8N1, LSB first. Start requests are accepted while idle.
module uart_tx #(
  parameter integer CLKS_PER_BIT = 217
) (
  input wire clk_i,
  input wire start_i,
  input wire [7:0] data_i,
  output reg serial_o = 1'b1,
  output reg busy_o = 1'b0,
  output reg done_o = 1'b0
);
  localparam [1:0] IDLE=2'd0, START=2'd1, DATA=2'd2, STOP=2'd3;
  reg [1:0] state = IDLE;
  reg [15:0] clock_count = 16'd0;
  reg [2:0] bit_index = 3'd0;
  reg [7:0] shift = 8'h00;

  always @(posedge clk_i) begin
    done_o <= 1'b0;
    case (state)
      IDLE: begin
        serial_o <= 1'b1;
        busy_o <= 1'b0;
        if (start_i) begin
          shift <= data_i;
          clock_count <= 16'd0;
          bit_index <= 3'd0;
          busy_o <= 1'b1;
          serial_o <= 1'b0;
          state <= START;
        end
      end
      START: if (clock_count == CLKS_PER_BIT-1) begin
        clock_count <= 16'd0;
        serial_o <= shift[0];
        shift <= {1'b0, shift[7:1]};
        state <= DATA;
      end else clock_count <= clock_count + 1'b1;
      DATA: if (clock_count == CLKS_PER_BIT-1) begin
        clock_count <= 16'd0;
        if (bit_index == 3'd7) begin serial_o <= 1'b1; state <= STOP; end
        else begin
          bit_index <= bit_index + 1'b1;
          serial_o <= shift[0];
          shift <= {1'b0, shift[7:1]};
        end
      end else clock_count <= clock_count + 1'b1;
      STOP: if (clock_count == CLKS_PER_BIT-1) begin
        clock_count <= 16'd0;
        serial_o <= 1'b1;
        busy_o <= 1'b0;
        done_o <= 1'b1;
        state <= IDLE;
      end else clock_count <= clock_count + 1'b1;
      default: begin state <= IDLE; serial_o <= 1'b1; busy_o <= 1'b0; end
    endcase
  end
endmodule
