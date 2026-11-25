`timescale 1ns/1ps
module tb_boot_branch_inject;
  reg clk=0;
  always #20 clk=~clk;
  wire [3:0] led;
  demo_autonoma_bus_detail_top #(.TIMEOUT_DIAG(3)) dut(clk,led);
  integer cycle=0;
  integer sale_commits=0;
  reg [31:0] last_pc=0,last_a=0;
  wire suppress_branch = $test$plusargs("suppress_branch");
  wire inject_x0_b = $test$plusargs("inject_x0_b");
  wire inject_x0_a = $test$plusargs("inject_x0_a");
  wire suppress_redirect = $test$plusargs("suppress_redirect");
  initial begin
    #1;
    if(suppress_branch)
      force dut.u_soc.u_core.branch_taken=1'b0;
  end
  wire [31:0] original_b=dut.u_soc.u_core.u_rf.rdata_b_o;
  wire [31:0] original_a=dut.u_soc.u_core.u_rf.rdata_a_o;
  wire [31:0] corrupt_b=(dut.u_soc.u_core.rf_raddr_b==0) ? 32'h80000000 : original_b;
  wire [31:0] corrupt_a=(dut.u_soc.u_core.rf_raddr_a==0) ? 32'h80000000 : original_a;
  wire jump_only=dut.instr_valid_id && !dut.core_stall && dut.u_soc.u_core.jump;
  initial begin
    #1;
    if(inject_x0_b) force dut.u_soc.u_core.u_id.rf_rdata_b_i=corrupt_b;
    if(inject_x0_a) force dut.u_soc.u_core.u_id.rf_rdata_a_i=corrupt_a;
    if(suppress_redirect) force dut.u_soc.u_core.pc_set=jump_only;
  end
  always @(posedge clk) begin
    cycle=cycle+1;
    if(dut.rst_ni && dut.commit_evt) begin
      if(cycle<=70 || dut.frame_index==0 && (dut.pc_id==32'h48 && sale_commits<3))
        $display("C=%0d PC=%08h INSN=%08h A=%08h B=%08h branch=%b redirect=%b",
          cycle,dut.pc_id,dut.instr_id,dut.u_soc.u_core.u_id.rf_rdata_a_i,
          dut.u_soc.u_core.u_id.rf_rdata_b_i,dut.branch_taken,dut.u_soc.u_core.pc_set);
      if(dut.pc_id==32'h48) sale_commits=sale_commits+1;
      if(!dut.master_timeout) begin last_pc=dut.pc_id; last_a=dut.operand_a; end
    end
    if(dut.price_read || dut.spi_byte_done || dut.ack_accepted)
      $display("C=%0d PRICE=%b BYTE=%b ACK=%b addr=%h",cycle,dut.price_read,dut.spi_byte_done,dut.ack_accepted,dut.data_addr);
    if(dut.master_timeout)
    begin
      $display("TIMEOUT cycle=%0d frame=%0d state=%0d last_pc=%08h last_A=%08h sale_commits=%0d",
        cycle,dut.frame_index+1,dut.debug_master_state,last_pc,last_a,sale_commits);
      $finish;
    end
    if(dut.ack_accepted) begin $display("FIRST_ACK"); $finish; end
    if(cycle==11000) $fatal(1,"missing expected outcome");
  end
endmodule
