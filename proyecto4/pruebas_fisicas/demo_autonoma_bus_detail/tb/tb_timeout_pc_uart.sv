`timescale 1ns/1ps
module tb_timeout_pc_uart #(parameter TIMEOUT_DIAG=2);
  localparam integer BIT_NS=8680;
  reg clk=0;
  always #20 clk=~clk;
  wire [3:0] led;
  demo_autonoma_bus_detail_top #(.TIMEOUT_DIAG(TIMEOUT_DIAG)) dut(clk,led);
  wire tx=dut.debug_uart_tx;

  task read_byte(output reg [7:0] value);
    integer bit_num;
    begin
      @(negedge tx);
      #(BIT_NS/2);
      if(tx!==0)$fatal(1,"bad UART start");
      for(bit_num=0;bit_num<8;bit_num=bit_num+1) begin
        #BIT_NS;
        value[bit_num]=tx;
      end
      #BIT_NS;
      if(tx!==1)$fatal(1,"bad UART stop bit");
    end
  endtask

  integer n;
  reg [7:0] b;
  reg [63:0] packet;
  wire test_done;
  assign test_done = TIMEOUT_DIAG==3 && $test$plusargs("done");
  initial begin
    #1;
    if(test_done) begin
      wait(dut.frame_index==15);
      @(negedge clk);
      force dut.decision_write=1'b0;
    end else begin
      force dut.u_soc.data_req=1'b0;
      wait(dut.debug_in_tick);
      @(negedge clk);
      force dut.commit_evt=1'b1;
      force dut.pc_id=32'h00000018;
      force dut.instr_id=32'h00117113;
      repeat(4) @(negedge clk);
      force dut.pc_id=32'h00004120;
      force dut.instr_id=32'hdeadbeef;
      force dut.operand_a=32'h97531000;
      force dut.branch_taken=1'b1;
      force dut.frame_index=4'd14;
    end
    wait(dut.master_timeout);
    @(posedge clk);
    if(dut.master_done!==test_done) $fatal(1,"unexpected state for timeout");
    $display("Timeout at %0t state=%0d sent=%0d", $time, dut.debug_master_state, dut.sent_count);
    @(negedge clk);
    // The diagnostic must freeze the captured commit after the timeout.
    force dut.pc_id=32'hffffffff;
    force dut.instr_id=32'hffffffff;
    force dut.operand_a=32'hffffffff;
    force dut.branch_taken=1'b0;
    force dut.frame_index=4'd6;
  end

  initial begin
    read_byte(b);
    if(b!==(test_done ? 8'hdf : TIMEOUT_DIAG==3 ? 8'hce : 8'ha5))
      $fatal(1,"bad UART header %h",b);
    packet=0;
    for(n=0;n<8;n=n+1) begin
      read_byte(b);
      packet[8*n +: 8]=b;
    end
    if((!test_done &&
        packet!==(TIMEOUT_DIAG==3 ? 64'h9753100000004121 : 64'hdeadbeef00004120)) ||
       led!==8)
      $fatal(1,"bad UART payload %h LED=%h",packet,led);
    $display("PASS UART 115200 8N1 freeze: payload=%h LED=%h",packet,led);
    $finish;
  end

  initial begin #6000000; $fatal(1,"UART did not finish"); end
endmodule


