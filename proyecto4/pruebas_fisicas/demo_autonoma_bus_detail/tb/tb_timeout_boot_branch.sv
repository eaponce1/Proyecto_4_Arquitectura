`timescale 1ns/1ps
module tb_timeout_boot_branch #(parameter TIMEOUT_DIAG=4);
  localparam integer BIT_NS=8680;
  reg clk=0;
  always #20 clk=~clk;
  wire [3:0] led;
  demo_autonoma_bus_detail_top #(.TIMEOUT_DIAG(TIMEOUT_DIAG)) dut(clk,led);
  wire tx=dut.debug_uart_tx;
  wire jump_only=dut.commit_evt && dut.u_soc.u_core.jump;
  wire inject_redirect=$test$plusargs("redirect");
  wire inject_late=$test$plusargs("late");
  integer cycle=0, branch_count=0;
  reg price_was_read=0;

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

  initial begin
    #1;
    if(inject_late) repeat(200) @(negedge clk);
    if(inject_redirect)
      force dut.u_soc.u_core.pc_set=jump_only;
    else
      force dut.u_soc.u_core.branch_taken=0;
  end

  always @(posedge clk) begin
    cycle=cycle+1;
    if(dut.price_read) begin
      if(price_was_read || cycle!=(inject_late ? 203 : 35))
        $fatal(1,"unexpected PRICE at cycle %0d",cycle);
      price_was_read=1;
    end
    if(dut.commit_evt && dut.pc_id==32'h48) begin
      if(dut.operand_a!==32'd0-branch_count || dut.operand_b!==0)
        $fatal(1,"sale loop did not decrement normally");
      branch_count=branch_count+1;
    end
    if(dut.master_timeout && !dut.g_timeout_uart.uart_timeout) begin
      if(cycle!=8722 || !price_was_read || branch_count!=(inject_late ? 945 : 963) ||
         dut.frame_index!==0 || dut.master_done || dut.ack_accepted)
        $fatal(1,"unexpected watchdog context, cycle=%0d branches=%0d",cycle,branch_count);
      $display("WAIT_ACK cycle=%0d tick=1, %0d commits at PC 0x48",cycle,branch_count);
    end
  end

  reg [7:0] header;
  initial begin
    read_byte(header);
    if(header!==(inject_redirect ? 8'hbC : 8'hb8))
      $fatal(1,"unexpected first-branch flags: %h",header);
    if(led!==4'h8) $fatal(1,"expected watchdog LED");
    $display("PASS boot BEQ UART header=%02h x2=0 x0=0; next commit outside poll",header);
    $finish;
  end
  initial begin #1500000; $fatal(1,"boot capture timeout"); end
endmodule
