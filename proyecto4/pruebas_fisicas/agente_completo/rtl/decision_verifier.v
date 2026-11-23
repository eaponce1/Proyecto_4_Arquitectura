// Observa MISO y compara con vector externo; nunca conduce señales del SoC.
module decision_verifier #(
  parameter integer N=32,
  parameter EXPECTED_FILE="proyecto4/pruebas_fisicas/agente_completo/data/expected_decisions.hex"
) (
  input wire clk_i, input wire rst_ni, input wire valid_i,
  input wire [7:0] response_i, output reg error_o=0,
  output reg [15:0] checked_o=0
);
  reg [7:0] expected [0:N-1];
  initial $readmemh(EXPECTED_FILE,expected);
  always @(posedge clk_i or negedge rst_ni) begin
    if(!rst_ni) begin error_o<=0; checked_o<=0; end
    else if(valid_i) begin
      if(checked_o>=N || response_i!==expected[checked_o]) error_o<=1;
      checked_o<=checked_o+1'b1;
    end
  end
endmodule
