`timescale 1ns/1ps
module tb_demo_autonoma_bus_detail;
  localparam integer N=16;
  reg clk=0;
  always #20 clk=~clk;

  wire [3:0] led;
  integer cycle=0;
  integer byte_count=0,price_count=0,sum_count=0,ready_count=0;
  integer decision_count=0,miso_count=0,ack_count=0,status_count=0;
  integer first_byte_cycle=0,first_post_commit_cycle=0;
  integer pc14_cycle=0,pc18_cycle=0,pc1c_cycle=0;
  integer first_request_after_beq=0,first_status_after_beq=0;
  integer first_price_cycle=0,first_sumready_cycle=0;
  integer first_decision_cycle=0,first_miso_cycle=0,second_miso_cycle=0;
  reg tb_byte_seen=0;
  reg tb_beq_seen=0;
  reg first_post_commit_seen=0;
  reg fetch_seen=0;

  reg [7:0] prices[0:N-1];
  reg [7:0] writes_expected[0:N-1];
  reg [7:0] miso_expected[0:N-1];

  demo_autonoma_bus_detail_top dut(.i_Clk(clk),.o_LED(led));

  initial begin
    $readmemh("proyecto4/pruebas_fisicas/demo_autonoma_bus_detail/data/prices.hex",prices);
    $readmemh("proyecto4/pruebas_fisicas/demo_autonoma_bus_detail/data/expected_writes.hex",writes_expected);
    $readmemh("proyecto4/pruebas_fisicas/demo_autonoma_bus_detail/data/expected_decisions.hex",miso_expected);
  end

  always @(posedge clk) begin
    cycle=cycle+1;
    if(cycle>=498 && cycle<=510)
      $display("TRACE %0d PC_ID=%08h instr=%08h commit=%b stall=%b byte_done=%b data_req=%b",
        cycle,dut.pc_id,dut.instr_id,dut.commit_evt,dut.core_stall,dut.spi_byte_done,dut.data_req);
    if(dut.frame_start && (ack_count!=miso_count || price_count!=miso_count))
      $fatal(1,"frame started before preceding PRICE/ACK");

    if(dut.rst_ni && dut.instr_req)
      fetch_seen=1;

    if(dut.spi_byte_done) begin
      if(byte_count>=N || dut.spi_price!==prices[byte_count])
        $fatal(1,"SPI price mismatch tick=%0d got=%0d expected=%0d",
          byte_count,dut.spi_price,prices[byte_count]);
      byte_count=byte_count+1;
      tb_byte_seen=1;
      if(first_byte_cycle==0) first_byte_cycle=cycle;
    end

    // The first committed instruction after the first byte must be the
    // STATUS load at PC_ID 0x14. This checks the raw signals, not LED stages.
    if((tb_byte_seen || dut.spi_byte_done) && dut.commit_evt) begin
      if(!first_post_commit_seen) begin
        first_post_commit_seen=1;
        first_post_commit_cycle=cycle;
        if(dut.pc_id!==32'h14 || dut.instr_id!==32'h0000A103)
          $fatal(1,"first post-byte commit unexpected: PC_ID=%08h instr=%08h",
            dut.pc_id,dut.instr_id);
      end

      if(dut.pc_id===32'h14) begin
        if(dut.instr_id!==32'h0000A103)
          $fatal(1,"PC 0x14 instruction mismatch: %08h",dut.instr_id);
        if(pc14_cycle==0) pc14_cycle=cycle;
      end
      if(dut.pc_id===32'h18) begin
        if(dut.instr_id!==32'h00117113)
          $fatal(1,"PC 0x18 instruction mismatch: %08h",dut.instr_id);
        if(pc18_cycle==0) pc18_cycle=cycle;
      end
      if(dut.pc_id===32'h1C) begin
        if(dut.instr_id!==32'hFE010CE3)
          $fatal(1,"PC 0x1C instruction mismatch: %08h",dut.instr_id);
        if(pc1c_cycle==0) pc1c_cycle=cycle;
        tb_beq_seen=1;
      end
    end

    if(tb_beq_seen && dut.data_req && first_request_after_beq==0) begin
      first_request_after_beq=cycle;
      if(!dut.lsu_busy || !dut.core_stall)
        $fatal(1,"post-BEQ request lacks expected LSU busy/stall: req=%b busy=%b stall=%b",
          dut.data_req,dut.lsu_busy,dut.core_stall);
    end

    if(dut.status_read) begin
      status_count=status_count+1;
      if(tb_beq_seen && first_status_after_beq==0)
        first_status_after_beq=cycle;
    end

    if(dut.price_read) begin
      price_count=price_count+1;
      if(first_price_cycle==0) first_price_cycle=cycle;
    end
    if(dut.sum_read) begin
      sum_count=sum_count+1;
      if(first_sumready_cycle==0) first_sumready_cycle=cycle;
    end
    if(dut.ready_read) begin
      ready_count=ready_count+1;
      if(first_sumready_cycle==0) first_sumready_cycle=cycle;
    end

    if(dut.decision_write) begin
      if(decision_count>=N || dut.data_wdata[7:0]!==writes_expected[decision_count])
        $fatal(1,"DECISION mismatch tick=%0d got=%02h expected=%02h",
          decision_count,dut.data_wdata[7:0],writes_expected[decision_count]);
      decision_count=decision_count+1;
      if(first_decision_cycle==0) first_decision_cycle=cycle;
    end

    if(dut.response_valid) begin
      if(miso_count>=N || dut.response!==miso_expected[miso_count])
        $fatal(1,"MISO mismatch frame=%0d got=%02h expected=%02h",
          miso_count,dut.response,miso_expected[miso_count]);
      miso_count=miso_count+1;
      if(miso_count==1) first_miso_cycle=cycle;
      if(miso_count==2) second_miso_cycle=cycle;
    end

    if(dut.ack_accepted) begin
      if(price_count!=ack_count+1 || byte_count!=price_count)
        $fatal(1,"ACK without matching PRICE read");
      ack_count=ack_count+1;
    end
  end

  initial begin
    wait(dut.master_done &&
         byte_count==N && price_count==N && sum_count==N && ready_count==N &&
         decision_count==N && miso_count==N);
    repeat(3) @(posedge clk);
    #1;

    if(!fetch_seen)
      $fatal(1,"Espino fetch was not observed");
    if(first_post_commit_cycle!=501 || !first_post_commit_seen || !dut.pc_probe_valid)
      $fatal(1,"first post-byte commit was not captured");
    if(dut.pc_probe_led!==4'b0101 ||
       dut.pc_probe_pc!==32'h14 ||
       dut.pc_probe_instr!==32'h0000A103)
      $fatal(1,"PC probe mismatch LED=%b PC=%08h INSTR=%08h",
        dut.pc_probe_led,dut.pc_probe_pc,dut.pc_probe_instr);

    if(byte_count!=N || price_count!=N || sum_count!=N || ready_count!=N ||
       decision_count!=N || miso_count!=N)
      $fatal(1,"full-run counts incomplete bytes=%0d PRICE=%0d SUM=%0d READY=%0d DECISION=%0d MISO=%0d",
        byte_count,price_count,sum_count,ready_count,decision_count,miso_count);

    if(ack_count!=N-1)
      $fatal(1,"stop-and-wait ACK count=%0d expected=%0d",ack_count,N-1);

    if(first_byte_cycle==0 || first_post_commit_cycle==0 ||
       pc14_cycle==0 || pc18_cycle==0 || pc1c_cycle==0 ||
       first_request_after_beq==0 || first_status_after_beq==0 ||
       first_price_cycle==0 || first_sumready_cycle==0 ||
       first_decision_cycle==0 || first_miso_cycle==0)
      $fatal(1,"missing event byte=%0d commit=%0d PC14=%0d PC18=%0d PC1C=%0d req=%0d status=%0d PRICE=%0d SUM/READY=%0d DECISION=%0d MISO=%0d",
        first_byte_cycle,first_post_commit_cycle,pc14_cycle,pc18_cycle,pc1c_cycle,
        first_request_after_beq,first_status_after_beq,first_price_cycle,
        first_sumready_cycle,first_decision_cycle,first_miso_cycle);

    if(!(first_byte_cycle<first_post_commit_cycle &&
         first_post_commit_cycle==pc14_cycle &&
         pc14_cycle<pc18_cycle && pc18_cycle<pc1c_cycle &&
         pc1c_cycle<first_request_after_beq &&
         first_request_after_beq<=first_status_after_beq &&
         first_status_after_beq<first_price_cycle &&
         first_price_cycle<first_sumready_cycle &&
         first_sumready_cycle<first_decision_cycle &&
         first_miso_cycle<first_decision_cycle && first_decision_cycle<second_miso_cycle))
      $fatal(1,"event order mismatch byte=%0d commit=%0d PC14=%0d PC18=%0d PC1C=%0d req=%0d status=%0d PRICE=%0d SUM/READY=%0d DECISION=%0d MISO=%0d",
        first_byte_cycle,first_post_commit_cycle,pc14_cycle,pc18_cycle,pc1c_cycle,
        first_request_after_beq,first_status_after_beq,first_price_cycle,
        first_sumready_cycle,first_decision_cycle,first_miso_cycle);

    $display("PASS PC probe: first post-byte commit PC_ID=%08h instr=%08h LED=%b",
      dut.pc_probe_pc,dut.pc_probe_instr,dut.pc_probe_led);
    $display("PASS full 16 ticks: prices=%0d STATUS reads=%0d PRICE=%0d SUM=%0d READY=%0d DECISION=%0d MISO=%0d ACK=%0d",
      byte_count,status_count,price_count,sum_count,ready_count,decision_count,miso_count,ack_count);
    $display("PASS first-tick order: byte=%0d commit=%0d PC14=%0d PC18=%0d PC1C=%0d request=%0d STATUS=%0d PRICE=%0d SUM/READY=%0d DECISION=%0d MISO=%0d",
      first_byte_cycle,first_post_commit_cycle,pc14_cycle,pc18_cycle,pc1c_cycle,
      first_request_after_beq,first_status_after_beq,first_price_cycle,
      first_sumready_cycle,first_decision_cycle,first_miso_cycle);
    $finish;
  end

  initial begin
    #20000000;
    $fatal(1,"timeout: LED=%b ticks=%0d DECISION=%0d MISO=%0d PC_ID=%08h instr=%08h req=%b stall=%b lsu_busy=%b",
      led,byte_count,decision_count,miso_count,dut.pc_id,dut.instr_id,
      dut.data_req,dut.core_stall,dut.lsu_busy);
  end
endmodule


