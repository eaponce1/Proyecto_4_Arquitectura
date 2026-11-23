`timescale 1ns/1ps
module tb_timeout_fetch_word #(parameter TIMEOUT_DIAG=5);
  localparam integer BIT_NS=8680;
  localparam [31:0] BEQ_STATUS=32'hfe010ce3, LW_PRICE=32'h0040a183;
  reg clk=0;
  always #20 clk=~clk;
  wire [3:0] led;
  demo_autonoma_bus_detail_top #(.TIMEOUT_DIAG(TIMEOUT_DIAG)) dut(clk,led);
  wire tx=dut.debug_uart_tx;
  wire zero_word=$test$plusargs("zero_word");
  wire bad_word=$test$plusargs("bad_word") || zero_word;
  wire [31:0] injected_word=zero_word ? 32'b0 : LW_PRICE;
  wire [31:0] cpu_word=(dut.pc_id==32'h1c && !dut.first_byte_seen) ?
                       injected_word : dut.u_soc.u_ram.a_rdata_o;
  initial begin
    #1;
    force dut.u_master.price_consumed_i=0;
    if(bad_word) force dut.u_soc.u_core.instr_rdata_i=cpu_word;
  end

  task read_byte(output reg [7:0] value);
    integer bit_num;
    begin
      @(negedge tx);
      #(BIT_NS/2);
      if(tx!==0) $fatal(1,"UART start");
      for(bit_num=0;bit_num<8;bit_num=bit_num+1) begin
        #BIT_NS;
        value[bit_num]=tx;
      end
      #BIT_NS;
      if(tx!==1) $fatal(1,"UART stop");
    end
  endtask

  reg [7:0] header,b;
  reg [31:0] word;
  integer i;
  initial begin
    read_byte(header);
    for(i=0;i<4;i=i+1) begin
      read_byte(b);
      word[8*i+:8]=b;
    end
    if(led!==4'h8 || header!==(bad_word ? 8'hb5 : 8'hb4) ||
       word!==(bad_word ? injected_word : BEQ_STATUS))
      $fatal(1,"incorrect fetch report: led=%h header=%h word=%h",led,header,word);
    $display("PASS fetch capture PC_ID=0000001C WORD=%08h FLAGS=%02h",word,header);
    $finish;
  end
  initial begin #1500000; $fatal(1,"fetch capture timeout"); end
endmodule
