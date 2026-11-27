// SMA10 alternativa: nueve lecturas de historia + precio entrante.
// Latencia de actualización: nueve ciclos; CPU consulta después del fin.
module pochoco_sma10 (
  input wire clk_i,rst_ni,price_valid_i,
  input wire [7:0] price_i,
  output wire [11:0] sum_o,
  output wire ready_o
);
  reg [3:0] pointer_q=0,count_q=0,scan_q=0,remaining_q=0;
  reg busy_q=0;
  reg [11:0] accumulator_q=0;
  wire [15:0] old_word;
  wire [3:0] next_pointer=(pointer_q==9)?0:pointer_q+1'b1;
  wire [3:0] first=(count_q<9)?0:next_pointer;
  wire [3:0] read_pointer=price_valid_i?first:scan_q;
  wire read_enable=(price_valid_i && count_q!=0) || (busy_q && remaining_q>1);
  assign sum_o=accumulator_q;
  assign ready_o=(count_q==10) && !busy_q;
  SB_RAM40_4K #(.READ_MODE(0),.WRITE_MODE(0),.INIT_0(256'h0)) history (
    .RDATA(old_word),.RADDR({7'b0,read_pointer}),.RCLK(clk_i),.RCLKE(read_enable),.RE(1'b1),
    .WDATA({8'b0,price_i}),.WADDR({7'b0,pointer_q}),.WCLK(clk_i),.WCLKE(1'b1),
    .WE(price_valid_i),.MASK(16'hff00)
  );
  always @(posedge clk_i or negedge rst_ni) begin
    if(!rst_ni) begin
      pointer_q<=0;count_q<=0;scan_q<=0;remaining_q<=0;busy_q<=0;accumulator_q<=0;
    end else if(price_valid_i) begin
      pointer_q<=next_pointer;
      if(count_q<10)count_q<=count_q+1'b1;
      scan_q<=(first==9)?0:first+1'b1;
      accumulator_q<={4'b0,price_i};remaining_q<=(count_q<9)?count_q:9;busy_q<=(count_q!=0);
    end else if(busy_q) begin
      accumulator_q<=accumulator_q+{4'b0,old_word[7:0]};
      remaining_q<=remaining_q-1'b1;
      scan_q<=(scan_q==9)?0:scan_q+1'b1;
      if(remaining_q==1)busy_q<=0;
    end
  end
endmodule
