`timescale 1ns/1ps
module tb_demo_autonoma_cpu_trace;
  localparam integer N=16;
  reg clk=0;always #20 clk=~clk;
  wire [3:0] led;
  integer cyc=0,fetches=0,commits_after_byte=0,bytes=0,data_reqs=0;
  integer status_reqs=0,status_valid=0,price_reads=0,sum_reads=0,ready_reads=0;
  integer decision_writes=0,miso_responses=0,first_byte_cycle=0;
  integer first_commit_cycle=0,first_data_cycle=0,first_status_cycle=0,first_status_valid_cycle=0;
  integer first_price_cycle=0,first_sumready_cycle=0,first_decision_cycle=0,first_miso_cycle=0;
  integer stall_cycles=0,pc_advance_after_status=0;
  reg status_pending=0,seen_byte=0;
  reg [31:0] previous_pc=0,pc_at_status=0;
  reg [10:0] stage_seen=0;
  reg [3:0] last_stage=0;
  reg [7:0] prices[0:N-1],decisions[0:N-1],miso_expected[0:N-1];
  demo_autonoma_cpu_trace_top dut(.i_Clk(clk),.o_LED(led));
  wire ref_instr_req,ref_data_req,ref_data_we;
  wire [31:0] ref_instr_addr,ref_data_addr,ref_data_wdata;
  wire [3:0] ref_data_be;
  espino_core #(.BootAddr(32'h0)) ref_core(
    .clk_i(clk),.rst_ni(dut.rst_ni),.instr_req_o(ref_instr_req),
    .instr_addr_o(ref_instr_addr),.instr_rdata_i(dut.u_soc.instr_rdata),
    .data_req_o(ref_data_req),.data_we_o(ref_data_we),.data_be_o(ref_data_be),
    .data_addr_o(ref_data_addr),.data_wdata_o(ref_data_wdata),
    .data_rdata_i(dut.u_soc.data_rdata));
  initial begin
    $readmemh("proyecto4/pruebas_fisicas/demo_autonoma_cpu_trace/data/prices.hex",prices);
    $readmemh("proyecto4/pruebas_fisicas/demo_autonoma_cpu_trace/data/expected_writes.hex",decisions);
    $readmemh("proyecto4/pruebas_fisicas/demo_autonoma_cpu_trace/data/expected_decisions.hex",miso_expected);
  end
  always @(posedge clk) begin
    cyc=cyc+1;
    if(cyc>=498 && cyc<=512)
      $display("CPUWIN cycle=%0d pc=%08h pc_id=%08h instr_req=%b instr_valid=%b instr=%08h commit=%b stall=%b rf_ready=%b ops_valid=%b lsu_req=%b lsu_busy=%b data_req=%b we=%b addr=%08h rdata=%08h",
        cyc,dut.core_pc,dut.pc_id,dut.instr_req,dut.u_soc.u_core.u_id.instr_valid_i,
        dut.u_soc.u_core.u_id.instr_rdata_i,dut.commit_evt,dut.core_stall,
        dut.u_soc.u_core.rf_ready,dut.u_soc.u_core.u_id.ops_valid_q,
        dut.u_soc.u_core.u_id.lsu_req_o,dut.u_soc.u_core.lsu_busy,
        dut.data_req,dut.data_we,dut.data_addr,dut.data_rdata);
    if(cyc>=502 && cyc<=506)
      $display("BRANCH cycle=%0d pc=%08h pc_id=%08h insn=%08h valid=%b commit=%b stall=%b rf_ready=%b branch_taken=%b jump=%b pc_set=%b target=%08h",
        cyc,dut.core_pc,dut.pc_id,dut.u_soc.u_core.u_id.instr_rdata_i,
        dut.u_soc.u_core.u_id.instr_valid_i,dut.commit_evt,dut.core_stall,
        dut.u_soc.u_core.rf_ready,dut.u_soc.u_core.branch_taken,
        dut.u_soc.u_core.jump,dut.u_soc.u_core.pc_set,dut.u_soc.u_core.pc_target);
    if(dut.instr_req) fetches=fetches+1;
    if(dut.core_stall) stall_cycles=stall_cycles+1;
    if(dut.spi_byte_done) begin
      if(bytes>=N || dut.spi_price!==prices[bytes])$fatal(1,"PRICE mismatch idx=%0d got=%0d exp=%0d",bytes,dut.spi_price,prices[bytes]);
      bytes=bytes+1;
      if(bytes==1)begin first_byte_cycle=cyc;seen_byte=1;$display("TRACE byte_done cycle=%0d price=%0d",cyc,dut.spi_price);end
    end
    if(seen_byte && cyc>first_byte_cycle && dut.commit_evt) begin
      commits_after_byte=commits_after_byte+1;
      if(first_commit_cycle==0)begin first_commit_cycle=cyc;$display("TRACE first post-byte commit cycle=%0d pc=%08h pc_id=%08h stall=%b",cyc,dut.core_pc,dut.pc_id,dut.core_stall);end
    end
    if(seen_byte && cyc>first_byte_cycle && dut.data_req) begin
      data_reqs=data_reqs+1;
      if(first_data_cycle==0)begin first_data_cycle=cyc;$display("TRACE first post-byte data_req cycle=%0d we=%b addr=%08h rdata=%08h stall=%b",cyc,dut.data_we,dut.data_addr,dut.data_rdata,dut.core_stall);end
      if(dut.data_addr==32'h80010000 && !dut.data_we)begin
        status_reqs=status_reqs+1;
        if(first_status_cycle==0)begin first_status_cycle=cyc;pc_at_status=dut.core_pc;status_pending=1;$display("TRACE STATUS req cycle=%0d addr=%08h we=%b be=%b PC=%08h instr_req=%b",cyc,dut.data_addr,dut.data_we,dut.data_be,dut.core_pc,dut.instr_req);end
      end
    end
    if(status_pending && dut.data_rdata[0]===1'b1)begin
      status_pending=0;status_valid=status_valid+1;
      if(first_status_valid_cycle==0)begin first_status_valid_cycle=cyc;$display("TRACE STATUS valid cycle=%0d rdata=%08h spi_rdata=%08h PC=%08h instr_req=%b",cyc,dut.data_rdata,dut.spi_rdata,dut.core_pc,dut.instr_req);end
    end
    if(status_valid>0 && dut.instr_req && dut.core_pc!=pc_at_status && pc_advance_after_status==0)begin
      pc_advance_after_status=cyc;$display("TRACE PC advanced cycle=%0d old=%08h new=%08h",cyc,pc_at_status,dut.core_pc);
    end
    if(dut.price_read)begin price_reads=price_reads+1;if(price_reads==1)begin first_price_cycle=cyc;$display("TRACE PRICE read cycle=%0d addr=%08h rdata=%08h",cyc,dut.data_addr,dut.data_rdata);end end
    if(dut.sum_read||dut.ready_read)begin sum_reads=sum_reads+dut.sum_read;ready_reads=ready_reads+dut.ready_read;if(first_sumready_cycle==0)begin first_sumready_cycle=cyc;$display("TRACE SUM/READY cycle=%0d SUM=%b READY=%b addr=%08h rdata=%08h",cyc,dut.sum_read,dut.ready_read,dut.data_addr,dut.data_rdata);end end
    if(dut.decision_write)begin
      if(decision_writes>=N || dut.data_wdata[7:0]!==decisions[decision_writes])$fatal(1,"DECISION/Python mismatch tick=%0d got=%02h exp=%02h",decision_writes,dut.data_wdata[7:0],decisions[decision_writes]);
      decision_writes=decision_writes+1;
      if(first_decision_cycle==0)begin first_decision_cycle=cyc;$display("TRACE DECISION write cycle=%0d data=%02h",cyc,dut.data_wdata[7:0]);end
    end
    if(dut.response_valid)begin
      if(miso_responses>=N || dut.response!==miso_expected[miso_responses])$fatal(1,"MISO/Python mismatch idx=%0d got=%02h exp=%02h",miso_responses,dut.response,miso_expected[miso_responses]);
      miso_responses=miso_responses+1;
      if(miso_responses==2)begin first_miso_cycle=cyc;$display("TRACE first prior-decision MISO correct cycle=%0d value=%02h",cyc,dut.response);end
    end
    if(dut.stage>10)$fatal(1,"Invalid stage %0d",dut.stage);
    previous_pc=dut.core_pc;
  end
  always @(posedge clk) begin
    #1;
    if(dut.rst_ni) begin
      if(ref_instr_req!==dut.instr_req || ref_instr_addr!==dut.instr_addr ||
         ref_data_req!==dut.data_req || ref_data_we!==dut.data_we ||
         ref_data_be!==dut.data_be || ref_data_addr!==dut.data_addr ||
         ref_data_wdata!==dut.data_wdata)
        $fatal(1,"Trace core differs from original Espino interface at cycle %0d",cyc);
      if((ref_core.u_id.instr_valid_i & ~ref_core.stall)!==dut.commit_evt)
        $fatal(1,"Commit tap differs from original Espino at cycle %0d",cyc);
      if(dut.stage<last_stage)$fatal(1,"LED milestone regressed %0d -> %0d",last_stage,dut.stage);
      stage_seen[dut.stage]=1'b1;
      last_stage=dut.stage;
    end
  end
  initial begin
    wait(dut.master_done && bytes==N && decision_writes==N && miso_responses==N);
    repeat(3) @(posedge clk);
    if(fetches==0||commits_after_byte==0||first_commit_cycle==0||first_data_cycle==0||first_status_cycle==0||first_status_valid_cycle==0||first_price_cycle==0||first_sumready_cycle==0||first_decision_cycle==0||first_miso_cycle==0||pc_advance_after_status==0)
      $fatal(1,"Missing milestone fetch=%0d commit=%0d data=%0d status=%0d valid=%0d price=%0d sumready=%0d decision=%0d miso=%0d pc=%0d",fetches,commits_after_byte,first_data_cycle,first_status_cycle,first_status_valid_cycle,first_price_cycle,first_sumready_cycle,first_decision_cycle,first_miso_cycle,pc_advance_after_status);
    if(dut.stage!=10||led!=10||stage_seen[10:1]!=10'h3ff)
      $fatal(1,"LED trace incomplete stage=%h LED=%h seen=%h",dut.stage,led,stage_seen);
    if(price_reads!=N||sum_reads!=N||ready_reads!=N||data_reqs==0||stall_cycles==0)$fatal(1,"Bus counts PRICE=%0d SUM=%0d READY=%0d req=%0d stalls=%0d",price_reads,sum_reads,ready_reads,data_reqs,stall_cycles);
    $display("PASS CPU trace: fetch=%0d commits_after_byte=%0d data_req=%0d STATUS=%0d valid=%0d PRICE=%0d SUM=%0d READY=%0d DECISION=%0d MISO=%0d lost=0",fetches,commits_after_byte,data_reqs,status_reqs,status_valid,price_reads,sum_reads,ready_reads,decision_writes,miso_responses);
    $display("First STATUS path cycles: byte_done=%0d commit=%0d data_req=%0d status_req=%0d valid=%0d PC_advance=%0d; final LED=%b",first_byte_cycle,first_commit_cycle,first_data_cycle,first_status_cycle,first_status_valid_cycle,pc_advance_after_status,led);
    $finish;
  end
  initial begin #20000000;$fatal(1,"CPU trace timeout LED=%b stage=%h byte=%0d commit=%0d req=%0d STATUS=%0d valid=%0d PC=%08h data=%b/%b/%08h/%08h",led,dut.stage,bytes,commits_after_byte,data_reqs,status_reqs,status_valid,dut.core_pc,dut.data_req,dut.data_we,dut.data_addr,dut.data_rdata);end
endmodule
