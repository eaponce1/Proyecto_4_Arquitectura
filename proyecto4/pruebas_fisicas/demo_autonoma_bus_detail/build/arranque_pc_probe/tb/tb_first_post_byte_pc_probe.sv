`timescale 1ns/1ps
module tb_first_post_byte_pc_probe;
  reg clk=0;
  always #20 clk=~clk;

  reg rst_ni=0;
  reg byte_done=0;
  reg instr_valid=0;
  reg stall=0;
  reg [31:0] pc_id=0;
  reg [31:0] instr_id=0;

  wire [3:0] led;
  wire snapshot_valid;
  wire [31:0] snapshot_pc,snapshot_instr;
  integer checks=0;

  first_post_byte_pc_probe dut(
    .clk_i(clk),
    .rst_ni(rst_ni),
    .byte_done_i(byte_done),
    .instr_valid_id_i(instr_valid),
    .stall_i(stall),
    .pc_id_i(pc_id),
    .instr_id_i(instr_id),
    .led_o(led),
    .snapshot_valid_o(snapshot_valid),
    .snapshot_pc_o(snapshot_pc),
    .snapshot_instr_o(snapshot_instr)
  );

  task tick;
    begin @(posedge clk); #1; end
  endtask

  task check_result(
    input [3:0] expected_led,
    input expected_valid,
    input [31:0] expected_pc,
    input [31:0] expected_instr,
    input [255:0] label
  );
    begin
      checks=checks+1;
      if (led !== expected_led ||
          snapshot_valid !== expected_valid ||
          snapshot_pc !== expected_pc ||
          snapshot_instr !== expected_instr) begin
        $display("FAIL %0s led=%b valid=%b pc=%08h instr=%08h expected led=%b valid=%b pc=%08h instr=%08h",
          label,led,snapshot_valid,snapshot_pc,snapshot_instr,
          expected_led,expected_valid,expected_pc,expected_instr);
        $fatal(1);
      end
    end
  endtask

  task reset_probe;
    begin
      @(negedge clk);
      rst_ni=0; byte_done=0; instr_valid=0; stall=0; pc_id=0; instr_id=0;
      tick();
      check_result(4'b0000,1'b0,32'b0,32'b0,"reset");
      @(negedge clk); rst_ni=1;
    end
  endtask

  initial begin
    reset_probe();

    // A pre-byte commit must not be captured.
    instr_valid=1; stall=0; pc_id=32'h0C; instr_id=32'h00000013;
    tick();
    check_result(4'b0000,1'b0,32'b0,32'b0,"pre-byte commit ignored");

    // Byte arrives; the probe waits for a committed instruction.
    @(negedge clk); instr_valid=0; byte_done=1;
    tick();
    check_result(4'b0001,1'b0,32'b0,32'b0,"byte received waiting");

    // Valid instruction held in stall is not a commit.
    @(negedge clk);
    byte_done=0; instr_valid=1; stall=1;
    pc_id=32'h14; instr_id=32'h0000A103;
    tick();
    check_result(4'b0001,1'b0,32'b0,32'b0,"stalled instruction ignored");

    // First committed post-byte instruction is exact LW STATUS.
    @(negedge clk); stall=0;
    tick();
    check_result(4'b0101,1'b1,32'h14,32'h0000A103,"PC14 exact LW");

    // Later instructions cannot overwrite the one-shot snapshot.
    @(negedge clk); pc_id=32'h18; instr_id=32'h00117113;
    tick();
    check_result(4'b0101,1'b1,32'h14,32'h0000A103,"snapshot sticky");

    // Simultaneous first byte and commit is captured on the same edge.
    reset_probe();
    byte_done=1; instr_valid=1; stall=0;
    pc_id=32'h14; instr_id=32'h0000A103;
    tick();
    check_result(4'b0101,1'b1,32'h14,32'h0000A103,"byte and commit simultaneous");

    // Correct PC but wrong instruction has a distinct physical code.
    reset_probe();
    byte_done=1; tick();
    @(negedge clk); byte_done=0; instr_valid=1; stall=0;
    pc_id=32'h14; instr_id=32'h0000A183;
    tick();
    check_result(4'b0101,1'b1,32'h14,32'h0000A183,"PC14 snapshot captures instruction mismatch");

    // Known later PCs have their own code and exact-word check.
    reset_probe();
    byte_done=1; tick();
    @(negedge clk); byte_done=0; instr_valid=1; stall=0;
    pc_id=32'h18; instr_id=32'h00117113;
    tick();
    check_result(4'b0110,1'b1,32'h18,32'h00117113,"PC18 ANDI");

    reset_probe();
    byte_done=1; tick();
    @(negedge clk); byte_done=0; instr_valid=1; stall=0;
    pc_id=32'h1C; instr_id=32'hFE010CE3;
    tick();
    check_result(4'b0111,1'b1,32'h1C,32'hFE010CE3,"PC1C BEQ");

    reset_probe();
    byte_done=1; tick();
    @(negedge clk); byte_done=0; instr_valid=1; stall=0;
    pc_id=32'h20; instr_id=32'h00000013;
    tick();
    check_result(4'b1000,1'b1,32'h20,32'h00000013,"PC20");

    reset_probe();
    byte_done=1; tick();
    @(negedge clk); byte_done=0; instr_valid=1; stall=0;
    pc_id=32'h0C; instr_id=32'h00000013;
    tick();
    check_result(4'b0011,1'b1,32'h0C,32'h00000013,"unexpected PC 0x0C raw code");

    $display("PASS first_post_byte_pc_probe: %0d checks",checks);
    $finish;
  end

  initial begin
    #100000;
    $fatal(1,"timeout");
  end
endmodule
