`timescale 1ns/1ps
module tb_baseline_trace;
  reg clk=0; always #20 clk=~clk;
  wire [3:0] led;
  integer cycle=0, nstatus=0, nprice=0, nsum=0, nready=0, ndec=0, nbytes=0, nresp=0;
  reg cs_prev=1,core_started=0,status_after_price_seen=0;
  demo_autonoma_handshake_top dut(.i_Clk(clk),.o_LED(led));
  always @(posedge clk) begin
    cycle=cycle+1;
    if(dut.rst_ni && dut.instr_req && !core_started) begin core_started=1;$display("EV1 core fetch after reset at cycle %0d",cycle);end
    if(cs_prev && !dut.cs_n && dut.sent_count==0) $display("EV2 first CS_n assertion at cycle %0d state=%0d",cycle,dut.u_master.state);
    cs_prev=dut.cs_n;
    if(dut.u_soc.dbg_status_read) begin
      nstatus=nstatus+1;
      if(nstatus==1) $display("STATUS first read at cycle %0d (before first price=%b)",cycle,nbytes==0);
      if(nbytes>0 && !status_after_price_seen) begin status_after_price_seen=1;$display("EV4 STATUS read after first price at cycle %0d",cycle);end
    end
    if(dut.spi_byte_done) begin nbytes=nbytes+1; if(nbytes==1)$display("EV3 first slave price_valid at cycle %0d price=%0d",cycle,dut.u_soc.sma_price);end
    if(dut.price_read) begin nprice=nprice+1; if(nprice==1)$display("EV5 first PRICE read at cycle %0d",cycle);end
    if(dut.u_master.state==5 && dut.price_ack && nbytes==1 && ndec==0)
      $display("EV6 ACK visible to WAIT_ACK at cycle %0d",cycle);
    if(dut.sum_read) begin nsum=nsum+1; if(nsum==1)$display("EV7 SUM10 read at cycle %0d",cycle);end
    if(dut.ready_read) begin nready=nready+1; if(nready==1)$display("EV7 READY read at cycle %0d",cycle);end
    if(dut.decision_write) begin ndec=ndec+1; if(ndec==1)$display("EV8 first DECISION write at cycle %0d value=%02h",cycle,dut.data_wdata[7:0]);end
    if(dut.u_master.response_valid_o) begin
      nresp=nresp+1;
      if(nresp==2)$display("EV9 first tick's MISO returned on frame 2 at cycle %0d response=%02h",cycle,dut.u_master.response_o);
    end
  end
  initial begin
    wait(dut.master_done && dut.sent_count==16 && dut.decision_count==16);
    repeat(2) @(posedge clk);
    $display("BASELINE PASS ticks=%0d PRICE=%0d DECISION=%0d MISO=%0d STATUS=%0d SUM=%0d READY=%0d",nbytes,nprice,ndec,nresp,nstatus,nsum,nready);
    $finish;
  end
  initial begin #20000000; $fatal(1,"baseline trace timeout"); end
endmodule
