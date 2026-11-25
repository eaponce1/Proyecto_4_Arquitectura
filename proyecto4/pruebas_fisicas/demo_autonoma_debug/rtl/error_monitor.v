// Captures the first diagnostic event after reset; later events cannot replace it.
module error_monitor (
  input wire clk_i,
  input wire rst_ni,
  input wire error_1_i,
  input wire error_2_i,
  input wire error_3_i,
  output reg [1:0] error_code_o
);
  always @(posedge clk_i or negedge rst_ni) begin
    if (!rst_ni) error_code_o <= 2'b00;
    else if (error_code_o == 2'b00) begin
      if (error_1_i)      error_code_o <= 2'b01;
      else if (error_2_i) error_code_o <= 2'b10;
      else if (error_3_i) error_code_o <= 2'b11;
    end
  end
endmodule
