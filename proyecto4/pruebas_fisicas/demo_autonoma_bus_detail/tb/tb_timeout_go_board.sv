`timescale 1ns/1ps
module tb_timeout_go_board;
  localparam integer LIMIT_EDGE=8722;
  localparam integer SETTLE=8200;
  reg clk=0;
  always #20 clk=~clk;

  wire [3:0] led;
  demo_autonoma_bus_detail_top dut(.i_Clk(clk),.o_LED(led));

  // Exercise real master and monitor in IDLE, with enable independent of POR.
  reg idle_rst_n=0;
  wire idle_timeout, idle_start, idle_error;
  wire [3:0] idle_led;
  price_spi_master_probe idle_master(
    .clk_i(clk),.rst_ni(idle_rst_n),.enable_i(1'b0),.price_consumed_i(1'b0),
    .final_complete_i(1'b0),.miso_i(1'b0),.timeout_o(idle_timeout),.frame_start_o(idle_start));
  demo_integral_monitor idle_monitor(
    .clk(clk),.rst(!idle_rst_n),.byte_done(1'b0),.first_commit(1'b0),
    .status_valid(1'b0),.access(4'd0),.frame_index(4'd0),
    .transport_timeout(idle_timeout),.frame_start(idle_start),.response_ok(1'b1),
    .price(8'd0),.decision(8'd0),.response_valid(1'b0),.master_done(1'b0),
    .led(idle_led),.error(idle_error));

  integer cycle=0, prices=0, writes=0, misos=0, acks=0;
  integer first_error=0, last_response=0, last_write=0, max_led=0;
  reg replay=0;
  reg early_ack, limit_ack, late_ack, drop_ack, drop_milestone, drop_final_decision;
  reg sampled_timeout, sampled_closure;
  integer sampled_gap;
  reg [7:0] expected_price[0:15], expected_write[0:15], expected_miso[0:15];

  initial begin
    $readmemh("proyecto4/pruebas_fisicas/demo_autonoma_bus_detail/data/prices.hex",expected_price);
    $readmemh("proyecto4/pruebas_fisicas/demo_autonoma_bus_detail/data/expected_writes.hex",expected_write);
    $readmemh("proyecto4/pruebas_fisicas/demo_autonoma_bus_detail/data/expected_decisions.hex",expected_miso);
    early_ack=$test$plusargs("early_ack");
    limit_ack=$test$plusargs("limit_ack");
    late_ack=$test$plusargs("late_ack");
    drop_ack=$test$plusargs("drop_ack");
    drop_milestone=$test$plusargs("drop_milestone");
    drop_final_decision=$test$plusargs("drop_final_decision");
    if(drop_milestone) force dut.u_monitor.first_commit=1'b0;
    if(early_ack || limit_ack || late_ack || drop_ack)
      force dut.price_ack_pending=1'b0;
    $display("cycle,phase,rst_ni,por_count,frame_start,master_state,timeout_counter,timeout_enable,timeout_condition,error_sticky,error_code,o_LED");
  end

  initial begin
    repeat(15) @(negedge clk);
    idle_rst_n=1;
  end

  task trace(input [31:0] phase);
    $display("%0d,%0s,%b,%0d,%b,%0d,%0d,%b,%b,%b,%b,%b",cycle,phase,
      dut.rst_ni,dut.u_soc.por_cnt,dut.frame_start,dut.u_master.state,
      dut.u_master.gap_count,dut.u_master.timeout_enable,dut.master_timeout,
      dut.monitor_error,dut.monitor_error ? led : 4'd0,led);
  endtask

  task check_reset;
    begin
      if({led,dut.monitor_error,dut.u_monitor.hits,dut.u_monitor.tick_seen,
          dut.u_monitor.in_tick,dut.u_monitor.previous_access} !== 0)
        $fatal(1,"monitor reset values incorrect cycle=%0d",cycle);
      if(dut.u_master.state!==dut.u_master.IDLE || dut.u_master.gap_count!==0 ||
         dut.u_master.price_index!==0 || dut.u_master.bit_index!==7 ||
         dut.u_master.half_count!==0 || dut.u_master.rx_shift!==0 ||
         dut.u_master.miso_bad!==0 || dut.u_master.done_o!==0 ||
         dut.u_master.response_valid_o!==0 || dut.u_master.sent_o!==0 ||
         dut.frame_start!==0 || dut.ack_accepted!==0 || dut.sclk_rise!==0 ||
         dut.sclk!==0 || dut.mosi!==0 || dut.cs_n!==1 ||
         dut.price_ack_pending!==0 || dut.status_pending!==0 || dut.master_timeout!==0)
        $fatal(1,"master or wrapper reset values incorrect cycle=%0d",cycle);
    end
  endtask

  always @(posedge clk) begin
    cycle=cycle+1;
    trace("pre");
    sampled_timeout=dut.master_timeout;
    sampled_closure=dut.u_monitor.closure_fault;
    sampled_gap=dut.u_master.gap_count;
    if(!dut.rst_ni) begin
      prices=0; writes=0; misos=0; acks=0; max_led=0;
      last_response=0; last_write=0;
    end else begin
      if(dut.spi_byte_done) begin
        if(prices>=16 || dut.spi_price!==expected_price[prices])
          $fatal(1,"price mismatch at cycle=%0d tick=%0d",cycle,prices);
        prices=prices+1;
      end
      if(dut.decision_write) begin
        if(writes>=16 || dut.data_wdata[7:0]!==expected_write[writes])
          $fatal(1,"DECISION mismatch at cycle=%0d tick=%0d",cycle,writes);
        writes=writes+1;
        last_write=cycle;
      end
      if(dut.response_valid) begin
        if(misos>=16 || dut.response!==expected_miso[misos])
          $fatal(1,"MISO mismatch at cycle=%0d tick=%0d",cycle,misos);
        misos=misos+1;
        last_response=cycle;
      end
      if(dut.ack_accepted) acks=acks+1;
    end
    if(cycle<=15 && dut.rst_ni!==0) $fatal(1,"early POR release");
    if(cycle==16 && dut.rst_ni!==1) $fatal(1,"late POR release");
    if(cycle>=16 && cycle<=1000 &&
       (dut.master_timeout!==0 || dut.u_monitor.fault!==0 || dut.monitor_error!==0))
      $fatal(1,"unexpected startup fault/X at cycle %0d",cycle);
    #1;
    if(cycle<=15 || !dut.rst_ni) check_reset;
    if(idle_master.state!==idle_master.IDLE || idle_master.gap_count!==0 ||
       idle_timeout!==0 || idle_start!==0 || idle_error!==0 || idle_led!==0)
      $fatal(1,"idle timeout or start at cycle %0d",cycle);
    if(cycle==100 || cycle==1000) $display("PASS idle at cycle=%0d",cycle);
    if((^led)===1'bx) $fatal(1,"unknown LED at cycle=%0d",cycle);

    if(dut.monitor_error && first_error==0) begin
      first_error=cycle;
      trace("post");
      if(drop_milestone) begin
        if(led!==14 || sampled_closure!==1 || sampled_timeout!==0 ||
           cycle!=last_write+1 || prices!=16 || writes!=16 || misos!=16 || acks!=15 ||
           !dut.u_monitor.complete || dut.u_master.timeout_enable || dut.u_master.gap_count>=8191)
          $fatal(1,"missing finish milestone was not a sequence error");
        $display("PASS missing milestone: 1110 at cycle=%0d (last DECISION=%0d)",cycle,last_write);
      end else if(drop_final_decision) begin
        if(led!==15 || sampled_timeout!==1 || sampled_closure!==0 || sampled_gap!=8191 ||
           dut.u_master.state!==dut.u_master.DONE || cycle!=last_response+8191 ||
           prices!=16 || writes!=15 || misos!=16)
          $fatal(1,"missing final decision was not a real terminal timeout");
        $display("PASS final transaction pending: 1111 at cycle=%0d (last MISO=%0d)",cycle,last_response);
        $finish;
      end else begin
        if(!(drop_ack || late_ack) || led!==15 || sampled_timeout!==1 ||
           sampled_gap!=8191 || cycle!=LIMIT_EDGE || dut.ack_accepted)
          $fatal(1,"unexpected or premature fault at cycle=%0d LED=%b",cycle,led);
        $display("PASS WAIT_ACK timeout: 1111 at cycle=%0d",cycle);
      end
    end

    if((early_ack && cycle==LIMIT_EDGE-1) || (limit_ack && cycle==LIMIT_EDGE)) begin
      if(sampled_gap!=(early_ack ? 8190 : 8191) || sampled_timeout!==0 ||
         dut.monitor_error!==0 || !dut.ack_accepted || dut.u_master.gap_count!=0 ||
         dut.u_master.state!==dut.u_master.GAP)
        $fatal(1,"ACK failed to win at cycle=%0d",cycle);
      trace("post");
      $display("PASS ACK accepted at cycle=%0d (counter before edge=%0d)",cycle,sampled_gap);
    end
    if(late_ack && cycle==LIMIT_EDGE+1) begin
      if(first_error!=LIMIT_EDGE || !dut.ack_accepted || led!==15 ||
         dut.u_master.state!==dut.u_master.GAP)
        $fatal(1,"late ACK changed first timeout");
      trace("post");
      $display("PASS late ACK at cycle=%0d leaves the timeout latched",cycle);
      $finish;
    end

    if(drop_ack && cycle==LIMIT_EDGE+1) begin
      if(first_error!=LIMIT_EDGE || led!==0 || dut.monitor_error!==0)
        $fatal(1,"reset after timeout failed");
      $display("PASS reset clears registers at cycle=%0d",cycle);
    end
    if(drop_milestone && last_write!=0 && writes==16 && cycle==last_write+SETTLE) begin
      if(first_error!=last_write+1 || led!==14 || dut.master_timeout!==0 ||
         dut.u_master.timeout_enable)
        $fatal(1,"terminal watchdog re-armed after all 16 ticks");
      $display("PASS sequence error unchanged beyond terminal threshold at cycle=%0d",cycle);
      $finish;
    end
    if(!dut.monitor_error && dut.rst_ni && led>max_led) begin
      max_led=led;
      if(led===10) $display("PASS 1010 at cycle=%0d",cycle);
    end
    if(!drop_milestone && !drop_final_decision && writes==16 && cycle==last_write+SETTLE) begin
      if(led!==10 || dut.monitor_error!==0 || dut.master_timeout!==0 ||
         dut.u_master.timeout_enable || prices!=16 || misos!=16 || acks!=15 ||
         (drop_ack && (!replay || first_error!=LIMIT_EDGE)))
        $fatal(1,"16-tick run or replay did not retain PASS");
      $display("PASS 16 prices, 16 DECISION, 16 MISO, 15 ACK through cycle=%0d replay=%b",cycle,replay);
      $finish;
    end
  end

  initial begin
    #1;
    if(early_ack || limit_ack || late_ack) begin
      wait(dut.u_master.state==dut.u_master.WAIT_ACK &&
           dut.u_master.gap_count==(early_ack ? 8190 : 8191));
      if(late_ack) wait(dut.monitor_error);
      @(negedge clk);
      force dut.price_ack_pending=1'b1;
      @(negedge clk);
      release dut.price_ack_pending;
    end
    if(drop_final_decision) begin
      wait(dut.frame_index==15);
      force dut.decision_write=1'b0;
    end
  end

  initial if($test$plusargs("drop_ack")) begin
    wait(first_error!=0);
    @(negedge clk);
    force dut.u_soc.por_cnt=4'd0;
    release dut.price_ack_pending;
    @(negedge clk);
    release dut.u_soc.por_cnt;
    replay=1;
  end

  initial begin
    #5600000;
    $fatal(1,"testbench watchdog");
  end
endmodule
