`timescale 1ns/1ps
module tb_custom0_unit;
  reg [31:0] instr,a,b,c;
  wire illegal,we;
  wire [4:0] op;
  wire [31:0] result;
  espino_decoder dec(.instr_i(instr),.illegal_insn_o(illegal),.alu_operator_o(op),
    .alu_op_a_sel_o(),.alu_op_b_sel_o(),.imm_operand_o(),.imm_target_o(),
    .rf_we_o(we),.rf_wd_sel_o(),.is_branch_o(),.is_jal_o(),.is_jalr_o(),
    .lsu_req_o(),.lsu_we_o(),.lsu_type_o(),.lsu_sign_o());
  espino_alu alu(.operator_i(op),.operand_a_i(a),.operand_b_i(b),.operand_c_i(c),.result_o(result),.cmp_result_o());
  reg [31:0] expected,valid;
  integer seed=12345;
  initial begin
    valid=(3<<20)|(12<<15)|(10<<7)|32'h0b;
    instr=valid;a=100;b=120;c=1000;#1;
    if(illegal || !we || op!=16 || result!==1020)$fatal(1,"custom decode/arithmetic");
    for(integer i=0;i<1024;i++)begin
      a=$random(seed);b=$random(seed);c=$random(seed);expected=c-a+b;#1;
      if(result!==expected)$fatal(1,"custom modulo 2^32 i=%0d",i);
    end
    instr=valid|32'h00001000;#1;if(!illegal || we)$fatal(1,"funct3 invalido aceptado");
    instr=valid|32'h02000000;#1;if(!illegal || we)$fatal(1,"funct7 invalido aceptado");
    instr=valid|32'h00080000;#1;if(!illegal || we)$fatal(1,"rs1 x16+ aceptado");
    instr=valid|32'h01000000;#1;if(!illegal || we)$fatal(1,"rs2 x16+ aceptado");
    instr=valid|32'h00000800;#1;if(!illegal || we)$fatal(1,"rd x16+ aceptado");
    $display("PASS custom0 1024 vectores modulo32 y cinco codificaciones invalidas");$finish;
  end
endmodule
