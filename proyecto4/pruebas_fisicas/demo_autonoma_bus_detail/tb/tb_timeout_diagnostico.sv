`timescale 1ns/1ps
module tb_timeout_diagnostico;
  reg clk=0;
  always #20 clk=~clk;
  wire [3:0] led;
  demo_autonoma_bus_detail_top #(.TIMEOUT_DIAG(1)) dut(clk,led);

  integer cycle=0, received=0, decisions=0, responses=0, acks=0;
  integer fault_cycle=0;
  reg [3:0] expected_code=10;
  reg [16:0] saved_context;
  reg [7:0] prices[0:15], writes[0:15], miso[0:15];

  initial begin
    $readmemh("proyecto4/pruebas_fisicas/demo_autonoma_bus_detail/data/prices.hex",prices);
    $readmemh("proyecto4/pruebas_fisicas/demo_autonoma_bus_detail/data/expected_writes.hex",writes);
    $readmemh("proyecto4/pruebas_fisicas/demo_autonoma_bus_detail/data/expected_decisions.hex",miso);

    if($test$plusargs("no_commit_no_request")) begin
      expected_code=1;
      force dut.commit_evt=1'b0;
      force dut.u_soc.data_req=1'b0;
    end else if($test$plusargs("request_not_status")) begin
      expected_code=9;
      force dut.u_soc.spi_sel=1'b0;
      force dut.u_soc.data_rdata=32'd0;
    end else if($test$plusargs("commit_status") || $test$plusargs("commit_andi") ||
                $test$plusargs("commit_branch") || $test$plusargs("commit_other")) begin
      force dut.u_soc.data_req=1'b0;
      wait(dut.debug_in_tick);
      // Inject the observed tag early, then replace it to prove the latch
      // reports the last commit, rather than the first.
      force dut.pc_id=32'h00000014;
      repeat(5) @(negedge clk);
      force dut.commit_evt=1'b1;
      if($test$plusargs("commit_status")) begin
        expected_code=5;
        force dut.pc_id=32'h00000014;
      end else if($test$plusargs("commit_andi")) begin
        expected_code=6;
        force dut.pc_id=32'h00000018;
      end else if($test$plusargs("commit_branch")) begin
        expected_code=7;
        force dut.pc_id=32'h0000001c;
      end else begin
        expected_code=8;
        // Same low bits as 0x14, outside the exact polling address.
        force dut.pc_id=32'h00000114;
      end
    end else if($test$plusargs("price_read_no_ack")) begin
      expected_code=3;
      force dut.price_ack_pending=1'b0;
    end else if($test$plusargs("byte_missing")) begin
      expected_code=4;
      force dut.u_soc.data_req=1'b0;
      force dut.spi_byte_done=1'b0;
      // Isolate the timeout classifier. A response without an open tick
      // would otherwise rightly be diagnosed earlier as a sequence fault.
      force dut.u_monitor.response_valid=1'b0;
    end else if($test$plusargs("decision_missing")) begin
      expected_code=2;
      wait(dut.frame_index==15);
      force dut.decision_write=1'b0;
    end else if($test$plusargs("final_response_missing")) begin
      expected_code=2;
      wait(dut.frame_index==15);
      force dut.u_monitor.response_valid=1'b0;
    end
  end

  always @(posedge clk) begin
    cycle=cycle+1;
    if(dut.spi_byte_done) begin
      if(received>=16 || dut.spi_price!==prices[received])
        $fatal(1,"PRICE mismatch cycle=%0d",cycle);
      received=received+1;
    end
    if(dut.decision_write) begin
      if(decisions>=16 || dut.data_wdata[7:0]!==writes[decisions])
        $fatal(1,"DECISION mismatch cycle=%0d",cycle);
      decisions=decisions+1;
    end
    if(dut.response_valid) begin
      if(responses>=16 || dut.response!==miso[responses])
        $fatal(1,"MISO mismatch cycle=%0d",cycle);
      responses=responses+1;
    end
    if(dut.ack_accepted) acks=acks+1;

    if(dut.rst_ni && dut.g_timeout_diag.price_pending!==dut.u_soc.u_spi.new_price_q &&
       expected_code!=4)
      $fatal(1,"PRICE pending shadow differs from SPI Slave");

    if(dut.master_timeout && !dut.monitor_error) begin
      fault_cycle=cycle;
      saved_context={dut.debug_master_state,dut.sent_count,
        dut.price_ack_pending,dut.ack_accepted,dut.frame_start,dut.spi_byte_done,
        dut.g_timeout_diag.price_pending,dut.debug_decision_written,dut.master_done,
        dut.final_complete,1'b1};
      if(!dut.rst_ni || !dut.u_master.timeout_enable || dut.u_master.gap_count!==8191 ||
         dut.sent_count!==({1'b0,dut.frame_index}+5'd1))
        $fatal(1,"invalid timeout trigger cycle=%0d",cycle);
      #1;
      if(led!==expected_code || !dut.monitor_error ||
         saved_context!=={dut.g_timeout_diag.snapshot_state,
           dut.g_timeout_diag.snapshot_sent,
           dut.g_timeout_diag.snapshot_flags,dut.g_timeout_diag.snapshot_valid} ||
         dut.g_timeout_diag.snapshot_decision_count!==decisions[4:0] ||
         dut.g_timeout_diag.snapshot_gap_count!==8191 ||
         dut.g_timeout_diag.snapshot_timeout_enable!==1 ||
         dut.g_timeout_diag.snapshot_rst_ni!==1)
        $fatal(1,"snapshot or code mismatch cycle=%0d LED=%b expected=%b",
               cycle,led,expected_code);
      if((dut.g_timeout_diag.snapshot_state!==5 || cycle!=8722) &&
         (dut.g_timeout_diag.snapshot_state!==7 || cycle!=106447))
        $fatal(1,"unexpected timeout state/cycle %h/%0d",dut.g_timeout_diag.snapshot_state,cycle);
      $display("CAPTURE cycle=%0d LED=%b state=%0d gap=%0d enable=%b ACK_valid=%b ACK_accepted=%b frame_start=%b byte_done=%b price_pending=%b decisions=%0d sent=%0d done=%b complete=%b rst_ni=%b",
        cycle,led,dut.g_timeout_diag.snapshot_state,dut.g_timeout_diag.snapshot_gap_count,
        dut.g_timeout_diag.snapshot_timeout_enable,dut.g_timeout_diag.snapshot_flags[7],
        dut.g_timeout_diag.snapshot_flags[6],dut.g_timeout_diag.snapshot_flags[5],
        dut.g_timeout_diag.snapshot_flags[4],dut.g_timeout_diag.snapshot_flags[3],
        dut.g_timeout_diag.snapshot_decision_count,dut.g_timeout_diag.snapshot_sent,
        dut.g_timeout_diag.snapshot_flags[1],dut.g_timeout_diag.snapshot_flags[0],
        dut.g_timeout_diag.snapshot_rst_ni);
      // Allow an ACK after capture. The master can leave WAIT_ACK then,
      // but neither the saved context nor the LED may change.
      if(expected_code==3) force dut.price_ack_pending=1'b1;
    end else begin
      #1;
    end

    if(dut.monitor_error && fault_cycle==0)
      $fatal(1,"unexpected non-timeout fault cycle=%0d LED=%b",cycle,led);
    if(fault_cycle!=0 && cycle==fault_cycle+64) begin
      if(led!==expected_code || saved_context!=={dut.g_timeout_diag.snapshot_state,
         dut.g_timeout_diag.snapshot_sent,
         dut.g_timeout_diag.snapshot_flags,dut.g_timeout_diag.snapshot_valid})
        $fatal(1,"first fault did not stay latched");
      if(expected_code==3 && dut.debug_master_state!==6)
        $fatal(1,"sticky test did not leave WAIT_ACK");
      $display("PASS diagnostic code %b and stable snapshot",led);
      $finish;
    end
    if(cycle==110000) begin
      if(expected_code!==10 || led!==10 || dut.monitor_error ||
         dut.g_timeout_diag.snapshot_valid!==0 ||
         received!=16 || decisions!=16 || responses!=16 || acks!=15)
        $fatal(1,"nominal diagnostic selftest did not retain full PASS");
      $display("PASS nominal 1010: prices=%0d writes=%0d MISO=%0d ACK=%0d",
               received,decisions,responses,acks);
      $finish;
    end
  end
endmodule







