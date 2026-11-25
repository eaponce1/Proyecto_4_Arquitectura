module uart_echo_top (
  input wire i_Clk,
  input wire i_UART_RX,
  output wire o_UART_TX
);
  wire rx_valid;
  wire [7:0] rx_data;
  wire tx_busy, tx_done;
  reg tx_start = 1'b0;
  reg [7:0] tx_data = 8'h00;

  uart_rx #(.CLKS_PER_BIT(217)) u_rx (
    .clk_i(i_Clk), .serial_i(i_UART_RX),
    .data_valid_o(rx_valid), .data_o(rx_data)
  );
  uart_tx #(.CLKS_PER_BIT(217)) u_tx (
    .clk_i(i_Clk), .start_i(tx_start), .data_i(tx_data),
    .serial_o(o_UART_TX), .busy_o(tx_busy), .done_o(tx_done)
  );

  // Echo one byte after its stop bit. Host waits for each echo before sending next.
  always @(posedge i_Clk) begin
    tx_start <= 1'b0;
    if (rx_valid && !tx_busy) begin
      tx_data <= rx_data;
      tx_start <= 1'b1;
    end
  end
endmodule
