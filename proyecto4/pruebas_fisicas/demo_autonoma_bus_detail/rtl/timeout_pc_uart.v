module timeout_pc_uart #(parameter PAYLOAD_BYTES=8)(
  input wire clk, rst_n, write_capture, trigger,
  input wire [7:0] header,
  input wire [31:0] pc, insn,
  output wire tx
);
  reg active=0;
  reg [7:0] baud_count=0;
  reg [3:0] bit_index=0;
  reg [(PAYLOAD_BYTES<=4 ? 2 : 3):0] byte_index=0;
  reg [9:0] shift=10'h3ff;
  wire [63:0] capture_data={insn,pc};
  wire [63:0] frozen_data;
  wire [7:0] next_byte;

  // EBRs preserve the captured record without a bank of fabric flip-flops.
  // The transmitter starts with a header byte,
  // allowing the registered BRAM outputs to settle before the payload.
  genvar word_index;
  generate if(PAYLOAD_BYTES==0) begin : no_payload
    assign next_byte=8'd0;
  end else if(PAYLOAD_BYTES==4) begin : one_word
    assign next_byte=frozen_data[8*byte_index[1:0] +: 8];
  end else begin : two_words
    assign next_byte=frozen_data[8*byte_index[2:0] +: 8];
  end endgenerate
  generate for(word_index=0;word_index<PAYLOAD_BYTES/2;word_index=word_index+1) begin : snapshot
    SB_RAM40_4K #(.READ_MODE(0),.WRITE_MODE(0),.INIT_0(256'h0)) u_word(
      .RDATA(frozen_data[16*word_index +: 16]),
      .RADDR(11'd0),.RCLK(clk),.RCLKE(1'b1),.RE(1'b1),
      .WDATA(capture_data[16*word_index +: 16]),
      .WADDR(11'd0),.WCLK(clk),.WCLKE(1'b1),
      .WE(rst_n && write_capture),.MASK(16'd0));
  end endgenerate

  assign tx=shift[0];
  // 25 MHz / 217 = 115207 baud, 8N1.
  always @(posedge clk) begin
    if(!rst_n) begin
      active<=0; baud_count<=0;
      bit_index<=0; byte_index<=0; shift<=10'h3ff;
    end else if(!active) begin
      if(trigger) begin
        active<=1;
        baud_count<=0; bit_index<=0; byte_index<=0;
        shift<={1'b1,header,1'b0};
      end
    end else if(baud_count==216) begin
      baud_count<=0;
      if(bit_index!=9) begin
        bit_index<=bit_index+1'b1;
        shift<={1'b1,shift[9:1]};
      end else if(byte_index==PAYLOAD_BYTES) begin
        active<=0;
      end else begin
        bit_index<=0;
        byte_index<=byte_index+1'b1;
        shift<={1'b1,next_byte,1'b0};
      end
    end else baud_count<=baud_count+1'b1;
  end
endmodule

// Single status byte, 115200 8N1 with the board's 25 MHz clock.
module terminal_status_uart(
  input wire clk, trigger,
  input wire [7:0] value,
  output wire tx
);
  reg [10:0] frame=0;
  reg [7:0] baud_count=0;
  wire busy=|frame;
  assign tx=!busy || frame[0];

  always @(posedge clk) begin
    if(!busy) begin
      if(trigger) frame<={2'b11,value,1'b0};
    end else if(baud_count==216) begin
      baud_count<=0;
      frame<={1'b0,frame[10:1]};
    end else baud_count<=baud_count+1'b1;
  end
endmodule



