`timescale 1ns/1ps
module tb_custom0_unit;
  reg [31:0] instr;
  wire illegal;
  wire [4:0] op;
  wire [1:0] asel;
  wire bsel;
  wire [31:0] imm, target;
  wire rfwe;
  wire [1:0] wdsel;
  wire branch, jal, jalr, lsureq, lsuwe;
  wire [1:0] lsutype;
  wire lsusign;
  reg [31:0] a,b,c;
  wire [31:0] result;
  wire cmp;
  espino_decoder dec(.instr_i(instr), .illegal_insn_o(illegal),
    .alu_operator_o(op), .alu_op_a_sel_o(asel), .alu_op_b_sel_o(bsel),
    .imm_operand_o(imm), .imm_target_o(target), .rf_we_o(rfwe),
    .rf_wd_sel_o(wdsel), .is_branch_o(branch), .is_jal_o(jal),
    .is_jalr_o(jalr), .lsu_req_o(lsureq), .lsu_we_o(lsuwe),
    .lsu_type_o(lsutype), .lsu_sign_o(lsusign));
  espino_alu alu(.operator_i(op), .operand_a_i(a), .operand_b_i(b),
    .operand_c_i(c), .result_o(result), .cmp_result_o(cmp));
  task check(input [31:0] oldsum, oldest, current, expected);
    begin
      c=oldsum; a=oldest; b=current; #1;
      if (result !== expected) $fatal(1,"sma update %h-%h+%h = %h expected %h",oldsum,oldest,current,result,expected);
    end
  endtask
  initial begin
    // smaupd x10,x11,x3: opcode custom-0, funct3=0, funct7=0
    instr=(11<<20)|(10<<7)|3<<15|7'h0b;
    #1;
    if (illegal || !rfwe || op!=5'd16 || bsel!=0) $fatal(1,"decode custom0 invalido");
    check(32'd1000,32'd100,32'd120,32'd1020);
    check(32'd0,32'd0,32'd0,32'd0);
    check(32'hfffffff0,32'd1,32'd20,32'h3);
    // Unrecognized funct3 must be illegal and suppress writeback.
    instr[14:12]=3'b001; #1;
    if (!illegal || rfwe) $fatal(1,"custom0 ilegal aceptado");
    $display("PASS custom0 decode/arithmetic");
    $finish;
  end
endmodule
