module spi_test_master #(
  parameter HALF_CLKS = 32,
  parameter GAP_CLKS = 6000,
  parameter BOOT_CLKS = 1000
) (
  input  wire       clk_i,
  input  wire       rst_ni,
  input  wire       miso_i,
  output reg        sclk_o,
  output reg        mosi_o,
  output reg        cs_n_o,
  output reg        busy_o,
  output reg        done_o,
  output reg        fail_o
);
  localparam [2:0] IDLE=0, LOW=1, HIGH=2, GAP=3, FINISHED=4;
  reg [2:0] state_q;
  reg [12:0] timer_q;
  reg [10:0] boot_q;
  reg [2:0] frame_q;
  reg [2:0] bit_q;
  reg [7:0] tx_q, rx_q;
  wire [7:0] current_price = price_for_frame(frame_q);
  wire [7:0] received_byte = {rx_q[6:0], miso_i};

  function [7:0] price_for_frame;
    input [2:0] frame;
    begin
      case (frame)
        3'd0: price_for_frame=8'h35;
        3'd1: price_for_frame=8'h56;
        3'd2: price_for_frame=8'h2c;
        3'd3: price_for_frame=8'h7a;
        default: price_for_frame=8'h12;
      endcase
    end
  endfunction

  function [7:0] previous_decision;
    input [2:0] frame;
    begin
      case (frame)
        3'd0: previous_decision=8'h00;
        3'd1: previous_decision=8'h41;
        3'd2: previous_decision=8'h42;
        3'd3: previous_decision=8'h43;
        default: previous_decision=8'h44;
      endcase
    end
  endfunction

  task start_frame;
    begin
      cs_n_o <= 1'b0;
      sclk_o <= 1'b0;
      tx_q <= current_price;
      rx_q <= 8'h00;
      mosi_o <= current_price[7];
      bit_q <= 3'd0;
      timer_q <= HALF_CLKS-1;
      state_q <= LOW;
    end
  endtask

  always @(posedge clk_i or negedge rst_ni) begin
    if (!rst_ni) begin
      state_q <= IDLE;
      timer_q <= 0;
      boot_q <= 0;
      frame_q <= 0;
      bit_q <= 0;
      tx_q <= 0;
      rx_q <= 0;
      sclk_o <= 0;
      mosi_o <= 0;
      cs_n_o <= 1;
      busy_o <= 0;
      done_o <= 0;
      fail_o <= 0;
    end else begin
      case (state_q)
        IDLE: begin
          if (boot_q < BOOT_CLKS) boot_q <= boot_q + 1'b1;
          else begin
            busy_o <= 1'b1;
            start_frame();
          end
        end
        LOW: begin
          if (timer_q == 0) begin
            sclk_o <= 1'b1;
            timer_q <= HALF_CLKS-1;
            state_q <= HIGH;
          end else timer_q <= timer_q - 1'b1;
        end
        HIGH: begin
          if (timer_q == 0) begin
            rx_q <= received_byte;
            sclk_o <= 1'b0;
            if (bit_q == 3'd7) begin
              if (received_byte !== previous_decision(frame_q)) fail_o <= 1'b1;
              cs_n_o <= 1'b1;
              if (frame_q == 3'd4) begin
                busy_o <= 1'b0;
                done_o <= 1'b1;
                state_q <= FINISHED;
              end else begin
                frame_q <= frame_q + 1'b1;
                timer_q <= GAP_CLKS-1;
                state_q <= GAP;
              end
            end else begin
              bit_q <= bit_q + 1'b1;
              tx_q <= {tx_q[6:0],1'b0};
              mosi_o <= tx_q[6];
              timer_q <= HALF_CLKS-1;
              state_q <= LOW;
            end
          end else timer_q <= timer_q - 1'b1;
        end
        GAP: begin
          if (timer_q == 0) start_frame();
          else timer_q <= timer_q - 1'b1;
        end
        FINISHED: begin
          cs_n_o <= 1'b1;
          sclk_o <= 1'b0;
        end
        default: state_q <= IDLE;
      endcase
    end
  end
endmodule
