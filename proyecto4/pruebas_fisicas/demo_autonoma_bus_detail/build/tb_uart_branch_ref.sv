`timescale 1ns/1ps
module tb_uart_branch_ref;
  tb_demo_autonoma_bus_detail #(.TIMEOUT_DIAG(2)) bench();
  integer count = 0;
  always @(posedge bench.clk) begin
    if (bench.dut.commit_evt && bench.dut.pc_id === 32'h48) begin
      count = count + 1;
      $display("BRANCH PC=48 tick=%0d x9=%08h x0=%08h taken=%b cycle~%0d",
        bench.dut.frame_index+1,bench.dut.u_soc.u_core.rf_rdata_a,
        bench.dut.u_soc.u_core.rf_rdata_b,bench.dut.u_soc.u_core.branch_taken,bench.cycle);
      if (bench.dut.frame_index!==4'd14 ||
        bench.dut.u_soc.u_core.rf_rdata_a !== 17-count ||
        bench.dut.u_soc.u_core.rf_rdata_b !== 32'b0 ||
        bench.dut.u_soc.u_core.branch_taken !== (count==17))
        $fatal(1,"unexpected nominal sale loop");
    end
  end
  final if (count!=17) $error("expected 17 commits at branch, got %0d",count);
endmodule
