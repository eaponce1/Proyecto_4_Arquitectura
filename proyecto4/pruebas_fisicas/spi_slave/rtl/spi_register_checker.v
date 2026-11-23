module spi_register_checker (
  input  wire        clk_i,
  input  wire        rst_ni,
  input  wire        price_valid_i,
  input  wire [7:0]  price_i,
  input  wire [31:0] rdata_i,
  output reg         sel_o,
  output reg         req_o,
  output reg         we_o,
  output reg  [7:0]  addr_o,
  output reg  [31:0] wdata_o,
  output wire [3:0]  be_o,
  output reg         bus_done_o,
  output reg         fail_o
);
  localparam [2:0] WAIT_PRICE=0, ISSUE_STATUS=1, CHECK_STATUS=2,
                   ISSUE_PRICE=3, CHECK_PRICE=4, WRITE_DECISION=5, FINISHED=6;
  reg [2:0] state_q;
  reg [1:0] sample_q;
  assign be_o = 4'b0001;

  function [7:0] known_price;
    input [1:0] sample;
    begin
      case (sample)
        2'd0: known_price=8'h35;
        2'd1: known_price=8'h56;
        2'd2: known_price=8'h2c;
        default: known_price=8'h7a;
      endcase
    end
  endfunction

  function [7:0] known_decision;
    input [1:0] sample;
    begin
      case (sample)
        2'd0: known_decision=8'h41;
        2'd1: known_decision=8'h42;
        2'd2: known_decision=8'h43;
        default: known_decision=8'h44;
      endcase
    end
  endfunction

  always @* begin
    sel_o=1'b0; req_o=1'b0; we_o=1'b0; addr_o=8'h00; wdata_o=32'h0;
    case (state_q)
      ISSUE_STATUS: begin sel_o=1; req_o=1; addr_o=8'h00; end
      ISSUE_PRICE: begin sel_o=1; req_o=1; addr_o=8'h04; end
      WRITE_DECISION: begin
        sel_o=1; req_o=1; we_o=1; addr_o=8'h08;
        wdata_o={24'b0,known_decision(sample_q)};
      end
      default: ;
    endcase
  end

  always @(posedge clk_i or negedge rst_ni) begin
    if (!rst_ni) begin
      state_q <= WAIT_PRICE;
      sample_q <= 0;
      bus_done_o <= 0;
      fail_o <= 0;
    end else begin
      case (state_q)
        WAIT_PRICE: if (price_valid_i && sample_q < 4) state_q <= ISSUE_STATUS;
        ISSUE_STATUS: state_q <= CHECK_STATUS;
        CHECK_STATUS: begin
          if (rdata_i[0] !== 1'b1) fail_o <= 1'b1;
          state_q <= ISSUE_PRICE;
        end
        ISSUE_PRICE: state_q <= CHECK_PRICE;
        CHECK_PRICE: begin
          if (rdata_i[7:0] !== known_price(sample_q)) fail_o <= 1'b1;
          state_q <= WRITE_DECISION;
        end
        WRITE_DECISION: begin
          if (sample_q == 3) begin
            bus_done_o <= 1'b1;
            state_q <= FINISHED;
          end else begin
            sample_q <= sample_q + 1'b1;
            state_q <= WAIT_PRICE;
          end
        end
        FINISHED: state_q <= FINISHED;
        default: state_q <= WAIT_PRICE;
      endcase
    end
  end
endmodule
