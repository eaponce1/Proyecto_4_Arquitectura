`timescale 1ns/1ps
module tb_demo_autonoma_debug;
  localparam integer NTICKS = 16;
  reg clk = 1'b0;
  always #20 clk = ~clk;
  wire [3:0] led;
  integer fetches=0, commits=0, status_reads=0, price_reads=0;
  integer sum_reads=0, ready_reads=0, decision_writes=0;
  integer spi_ticks=0, miso_checks=0, lost_ticks=0;
  integer buys=0, sells=0;
  reg price_seen=0;
  reg [7:0] expected_miso[0:NTICKS-1];
  reg [7:0] expected_write[0:NTICKS-1];
  reg [7:0] expected_price[0:NTICKS-1];

  demo_autonoma_debug_top dut(.i_Clk(clk), .o_LED(led));
  initial begin
    $readmemh("proyecto4/pruebas_fisicas/demo_autonoma_debug/data/expected_decisions.hex", expected_miso);
    $readmemh("proyecto4/pruebas_fisicas/demo_autonoma_debug/data/expected_writes.hex", expected_write);
    $readmemh("proyecto4/pruebas_fisicas/demo_autonoma_debug/data/prices.hex", expected_price);
  end

  always @(posedge clk) begin
    if (dut.instr_req) fetches = fetches + 1;
    if (dut.u_soc.u_core.instr_valid_id && !dut.u_soc.u_core.stall) commits = commits + 1;
    if (dut.status_read) status_reads = status_reads + 1;
    if (dut.price_read) begin price_reads = price_reads + 1; price_seen = 1; end
    if (dut.sum_read) sum_reads = sum_reads + 1;
    if (dut.ready_read) ready_reads = ready_reads + 1;
    if (dut.decision_write) begin
      if (!price_seen) $fatal(1, "DECISION escrita sin lectura PRICE");
      if (decision_writes >= NTICKS || dut.data_wdata[7:0] !== expected_write[decision_writes])
        $fatal(1, "DECISION distinta de Python idx=%0d actual=%02h esperada=%02h",
               decision_writes, dut.data_wdata[7:0], expected_write[decision_writes]);
      if (dut.data_wdata[7:6] == 2'b01) buys = buys + 1;
      if (dut.data_wdata[7:6] == 2'b10) sells = sells + 1;
      decision_writes = decision_writes + 1;
      price_seen = 0;
    end
    if (dut.u_soc.u_spi.byte_done) begin
      if (spi_ticks > 0 && dut.u_soc.u_spi.new_price_q) begin
        lost_ticks = lost_ticks + 1;
        $fatal(1, "Precio previo no consumido antes del tick %0d", spi_ticks);
      end
      if (spi_ticks >= NTICKS || dut.u_soc.sma_price !== expected_price[spi_ticks])
        $fatal(1, "PRICE distinto idx=%0d actual=%0d esperado=%0d",
               spi_ticks, dut.u_soc.sma_price, expected_price[spi_ticks]);
      spi_ticks = spi_ticks + 1;
    end
    if (dut.u_master.response_valid_o) begin
      if (miso_checks >= NTICKS || dut.u_master.response_o !== expected_miso[miso_checks])
        $fatal(1, "MISO distinto idx=%0d actual=%02h esperado=%02h",
               miso_checks, dut.u_master.response_o, expected_miso[miso_checks]);
      miso_checks = miso_checks + 1;
    end
  end

  initial begin
    wait(dut.master_done && dut.sent_count == NTICKS && dut.decision_count == NTICKS);
    repeat (3) @(posedge clk);
    if (dut.error_code !== 2'b00 || led[3:1] !== 3'b000 || led[0] !== 1'b1)
      $fatal(1, "Ejecucion correcta con flags incorrectos: code=%b LED=%b", dut.error_code, led);
    if (fetches == 0 || commits == 0) $fatal(1, "No se observó actividad del Espino");
    if (status_reads < NTICKS || price_reads != NTICKS || sum_reads != NTICKS || ready_reads != NTICKS)
      $fatal(1, "MMIO incompleto STATUS=%0d PRICE=%0d SUM10=%0d READY=%0d",
             status_reads, price_reads, sum_reads, ready_reads);
    if (spi_ticks != NTICKS || decision_writes != NTICKS || miso_checks != NTICKS || lost_ticks != 0)
      $fatal(1, "TICKS=%0d DECISION=%0d MISO=%0d lost=%0d",
             spi_ticks, decision_writes, miso_checks, lost_ticks);
    if (buys == 0 || sells == 0) $fatal(1, "La secuencia no ejercitó compra y venta");
    $display("PASS integrated debug: ticks=%0d fetch=%0d commit=%0d STATUS=%0d PRICE=%0d SUM10=%0d READY=%0d DECISION=%0d MISO=%0d buy=%0d sell=%0d error_code=%b LED=%b",
             spi_ticks, fetches, commits, status_reads, price_reads, sum_reads,
             ready_reads, decision_writes, miso_checks, buys, sells, dut.error_code, led);
    $finish;
  end

  initial begin
    #20000000;
    $fatal(1, "Timeout master_done=%b sent=%0d decisions=%0d code=%b LED=%b",
           dut.master_done, dut.sent_count, dut.decision_count, dut.error_code, led);
  end
endmodule
