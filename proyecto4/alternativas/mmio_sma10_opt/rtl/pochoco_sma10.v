// Rolling SMA10 fed by completed SPI price bytes. Sum range: 0..2550 (12 bits).
module pochoco_sma10 (
  input  wire        clk_i,
  input  wire        rst_ni,
  input  wire        price_valid_i,
  input  wire [7:0]  price_i,
  output wire [11:0] sum_o,
  output wire        ready_o
);
  reg [3:0] pointer_q;
  reg       ready_q;
  reg [11:0] sum_q;
  wire [15:0] history_rdata;
  wire [10:0] history_addr = {7'b0, pointer_q};
  assign sum_o = sum_q;
  assign ready_o = ready_q;

  // Un bloque BRAM conserva las diez muestras; lectura continua para que el
  // precio saliente ya esté disponible cuando llega el siguiente byte SPI.
  SB_RAM40_4K #(.READ_MODE(0),.WRITE_MODE(0),.INIT_0(256'h0)) u_history (
    .RDATA(history_rdata), .RADDR(history_addr), .RCLK(clk_i), .RCLKE(1'b1), .RE(1'b1),
    .WDATA({8'b0,price_i}), .WADDR(history_addr), .WCLK(clk_i), .WCLKE(1'b1),
    .WE(price_valid_i), .MASK(16'hff00)
  );

  always @(posedge clk_i or negedge rst_ni) begin
    if (!rst_ni) begin
      pointer_q <= 4'd0;
      ready_q <= 1'b0;
      sum_q <= 12'd0;
    end else if (price_valid_i) begin
      pointer_q <= (pointer_q == 4'd9) ? 4'd0 : pointer_q + 4'd1;
      if (!ready_q) begin
        // The pointer reaches slot 9 on the tenth sample. This replaces the
        // separate saturating 4-bit sample counter and its equality decode.
        if (pointer_q == 4'd9) ready_q <= 1'b1;
        sum_q <= sum_q + {4'b0, price_i};
      end else begin
        sum_q <= sum_q - {4'b0, history_rdata[7:0]} + {4'b0, price_i};
      end
    end
  end

  // MMIO map within SPI window: word offset 3=SUM10, 4=READY.
endmodule
