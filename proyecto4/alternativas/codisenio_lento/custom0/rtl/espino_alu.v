// Copyright 2026 Universidad de los Andes.
// Licensed under the Solderpad Hardware License, Version 0.51 (the "License");
// you may not use this file except in compliance with the License.
// SPDX-License-Identifier: SHL-0.51
//
// Course: Arquitectura de Computadores (2026)
// 
// Authors:
// - Nicolás Villegas <navillegas@miuandes.cl>

module espino_alu (
  input  wire [4:0]  operator_i,
  input  wire [31:0] operand_a_i,
  input  wire [31:0] operand_b_i,
  input  wire [31:0] operand_c_i,
  output reg  [31:0] result_o,
  output reg         cmp_result_o
);

  localparam [4:0] ALU_ADD  = 5'd0,
                   ALU_SUB  = 5'd1,
                   ALU_XOR  = 5'd2,
                   ALU_OR   = 5'd3,
                   ALU_AND  = 5'd4,
                   ALU_SLL  = 5'd5,
                   ALU_SRL  = 5'd6,
                   ALU_SRA  = 5'd7,
                   ALU_SLT  = 5'd8,
                   ALU_SLTU = 5'd9,
                   ALU_EQ   = 5'd10,
                   ALU_NE   = 5'd11,
                   ALU_LT   = 5'd12,
                   ALU_GE   = 5'd13,
                   ALU_LTU  = 5'd14,
                   ALU_GEU  = 5'd15,
                   ALU_SMAUPD = 5'd16;

  // Un solo sumador/restador de 33 bits sirve para ADD, SUB y las 6 comparaciones.
  // Para todo lo que no es ADD, invertimos b y metemos cin=1  =>  a + ~b + 1 = a - b.
  wire        sub_mode  = (operator_i != ALU_ADD);
  wire [31:0] b_mux     = sub_mode ? ~operand_b_i : operand_b_i;
  wire [32:0] sum_ext   = {1'b0, operand_a_i} + {1'b0, b_mux} + {32'b0, sub_mode};
  wire [31:0] adder_res = sum_ext[31:0];
  wire        carry_out = sum_ext[32];

  // a < b (unsigned)  <=>  no hubo acarreo en a + ~b + 1
  wire cmp_ltu = ~carry_out;
  // a == b  <=>  a - b == 0
  wire cmp_eq  = (adder_res == 32'b0);
  // a < b (signed): signo del resultado corregido por overflow de la resta
  wire sign_a = operand_a_i[31];
  wire sign_b = operand_b_i[31];
  wire sign_r = adder_res[31];
  wire ovf    = (sign_a ^ sign_b) & (sign_a ^ sign_r);
  wire cmp_lt = sign_r ^ ovf;


  always @* begin
    case (operator_i)
      ALU_EQ:  cmp_result_o =  cmp_eq;
      ALU_NE:  cmp_result_o = ~cmp_eq;
      ALU_LT:  cmp_result_o =  cmp_lt;
      ALU_GE:  cmp_result_o = ~cmp_lt;
      ALU_LTU: cmp_result_o =  cmp_ltu;
      ALU_GEU: cmp_result_o = ~cmp_ltu;
      default: cmp_result_o = 1'b0;
    endcase
  end

  always @* begin
    case (operator_i)
      ALU_ADD:  result_o = adder_res;              // b_mux=b, cin=0 => a+b
      ALU_SUB:  result_o = adder_res;               // b_mux=~b, cin=1 => a-b
      ALU_XOR:  result_o = operand_a_i ^ operand_b_i;
      ALU_OR:   result_o = operand_a_i | operand_b_i;
      ALU_AND:  result_o = operand_a_i & operand_b_i;
      ALU_SLT:  result_o = {31'b0, cmp_lt};
      ALU_SLTU: result_o = {31'b0, cmp_ltu};
      ALU_SMAUPD: result_o = (operand_c_i - operand_a_i) + operand_b_i;
      // Shifts disabled to save LUTs
      default:  result_o = adder_res;               // igual que antes: default = a+b
    endcase
  end

endmodule
