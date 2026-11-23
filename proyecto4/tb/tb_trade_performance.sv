`timescale 1ns/1ps

// Instrumentacion externa de performance. No altera senales de entrada ni RTL:
// cuenta commits con instr_valid_id && !stall y observa accesos SPI/MMIO.
module tb_trade_performance;
  localparam integer N = 20000;
  reg clk = 0;
  always #20 clk = ~clk; // 25 MHz: 40 ns por ciclo
  reg sclk = 0, mosi = 0, cs_n = 1;
  wire miso;
  integer prices [0:N-1];
  integer expected [0:N-1];
  integer tick_count = 0, done_count = 0, lost_ticks = 0, mismatches = 0;
  integer status_reads = 0, price_reads = 0, decision_writes = 0;
  integer bit_x = 0;
  integer total_cycles, total_ic;
  integer status_cycles, status_ic, price_cycles, price_ic;
  integer portfolio_cycles, portfolio_ic, history_cycles, history_ic;
  integer sma_cycles, sma_ic, signal_cycles, signal_ic;
  integer active = 0, price_seen = 0;
  time started_at;
  integer fd, period_ns, i, b;
  integer nticks = N;
  reg [7:0] received;
  reg [1023:0] price_file, expected_file, output_file;

  pochoco_soc #(.MemFile("proyecto4/sw/trade.hex"), .EnableSpi(1)) dut (
    .i_Clk(clk), .o_LED(), .i_Switch(4'b0000),
    .o_Segment1_A(), .o_Segment1_B(), .o_Segment1_C(), .o_Segment1_D(),
    .o_Segment1_E(), .o_Segment1_F(), .o_Segment1_G(),
    .o_Segment2_A(), .o_Segment2_B(), .o_Segment2_C(), .o_Segment2_D(),
    .o_Segment2_E(), .o_Segment2_F(), .o_Segment2_G(),
    .i_SPI_SCLK(sclk), .i_SPI_MOSI(mosi), .i_SPI_CS_n(cs_n), .o_SPI_MISO(miso)
  );

  // PC ranges proceden de etiquetas/direcciones ensambladas de trade.s.
  always @(posedge clk) begin
    if (dut.u_spi.rd && dut.u_spi.off == 0) status_reads = status_reads + 1;
    if (dut.u_spi.rd && dut.u_spi.off == 1) price_reads = price_reads + 1;
    if (dut.u_spi.wr && dut.u_spi.off == 2) decision_writes = decision_writes + 1;

    if (active) begin
      total_cycles = total_cycles + 1;
      if (dut.u_core.instr_valid_id && !dut.u_core.stall) total_ic = total_ic + 1;
      case (dut.u_core.pc_id)
        32,36,40: begin
          status_cycles = status_cycles + 1;
          if (dut.u_core.instr_valid_id && !dut.u_core.stall) status_ic = status_ic + 1;
        end
        44: begin
          price_cycles = price_cycles + 1;
          if (dut.u_core.instr_valid_id && !dut.u_core.stall) price_ic = price_ic + 1;
        end
        default: begin
          if (dut.u_core.pc_id >= 48 && dut.u_core.pc_id <= 176) begin
            portfolio_cycles = portfolio_cycles + 1;
            if (dut.u_core.instr_valid_id && !dut.u_core.stall) portfolio_ic = portfolio_ic + 1;
          end else if (dut.u_core.pc_id >= 180 && dut.u_core.pc_id <= 224) begin
            history_cycles = history_cycles + 1;
            if (dut.u_core.instr_valid_id && !dut.u_core.stall) history_ic = history_ic + 1;
          end else if (dut.u_core.pc_id >= 228 && dut.u_core.pc_id <= 280) begin
            sma_cycles = sma_cycles + 1;
            if (dut.u_core.instr_valid_id && !dut.u_core.stall) sma_ic = sma_ic + 1;
          end else if (dut.u_core.pc_id >= 284 && dut.u_core.pc_id <= 352) begin
            signal_cycles = signal_cycles + 1;
            if (dut.u_core.instr_valid_id && !dut.u_core.stall) signal_ic = signal_ic + 1;
          end
        end
      endcase

      if (dut.u_spi.wr && dut.u_spi.off == 2) begin
        if (!price_seen) $fatal(1, "DECISION escrita antes da leitura PRICE no tick %0d", tick_count-1);
        $fdisplay(fd, "%0d,%0d,%0d,%0d,%0d,%0d,%0d,%0d,%0d,%0d,%0d,%0d,%0d,%0d,%0d,%0d,%0d,%0d,%0d,%0d",
          tick_count-1, prices[tick_count-1], total_ic, total_cycles, $time-started_at,
          status_ic, status_cycles, price_ic, price_cycles,
          portfolio_ic, portfolio_cycles, history_ic, history_cycles,
          sma_ic, sma_cycles, signal_ic, signal_cycles, dut.u_spi.tx_hold,
          dut.u_core.pc_id, dut.u_spi.new_price_q);
        done_count = done_count + 1;
        active = 0;
      end
    end

    if (dut.u_spi.byte_done) begin
      if (tick_count >= N) $fatal(1, "SPI recibio tick extra");
      if (active) $fatal(1, "DECISION anterior no se escribio antes del tick %0d", tick_count);
      if (tick_count > 0 && dut.u_spi.new_price_q) lost_ticks = lost_ticks + 1;
      total_cycles=0; total_ic=0; status_cycles=0; status_ic=0;
      price_cycles=0; price_ic=0; portfolio_cycles=0; portfolio_ic=0;
      history_cycles=0; history_ic=0; sma_cycles=0; sma_ic=0;
      signal_cycles=0; signal_ic=0;
      started_at = $time;
      price_seen = 0;
      active = 1;
      tick_count = tick_count + 1;
    end else if (active && dut.u_spi.rd && dut.u_spi.off == 1) begin
      price_seen = 1;
    end
  end

  task automatic spi_send(input [7:0] value, output [7:0] response);
    begin
      response = 0; cs_n = 0; #1000;
      for (integer bit_index=7; bit_index>=0; bit_index=bit_index-1) begin
        mosi=value[bit_index]; #500; sclk=1;
        if (miso !== 1'b0 && miso !== 1'b1) bit_x=bit_x+1;
        response[bit_index]=(miso === 1'b1);
        #500; sclk=0;
      end
      #500; cs_n=1;
    end
  endtask

  initial begin
    if (!$value$plusargs("PERIOD_NS=%d", period_ns)) $fatal(1,"Falta +PERIOD_NS");
    if (!$value$plusargs("TICKS=%d", nticks)) nticks = N;
    if (!$value$plusargs("PRICE_FILE=%s", price_file)) $fatal(1,"Falta +PRICE_FILE");
    if (!$value$plusargs("EXPECTED_FILE=%s", expected_file)) $fatal(1,"Falta +EXPECTED_FILE");
    if (!$value$plusargs("OUTPUT_FILE=%s", output_file)) $fatal(1,"Falta +OUTPUT_FILE");
    if (period_ns < 10000) $fatal(1,"Periodo menor al soporte del SPI maestro");
    if (nticks < 1 || nticks > N) $fatal(1,"TICKS fuera de 1..%0d", N);
    $readmemh(price_file, prices);
    $readmemh(expected_file, expected);
    fd=$fopen(output_file,"w");
    if (!fd) $fatal(1,"No se puede crear CSV de ciclos");
    $fdisplay(fd,"tick,price,ic_total,cycles_total,elapsed_ns,status_ic,status_cycles,price_ic,price_cycles,portfolio_ic,portfolio_cycles,history_ic,history_cycles,sma_ic,sma_cycles,signal_ic,signal_cycles,decision_written,pc_at_write,new_price_at_write");
    #4000;
    for (i=0; i<nticks; i=i+1) begin
      if (i>0 && dut.u_spi.new_price_q) $fatal(1,"Tick previo no consumido antes del tick %0d",i);
      spi_send(prices[i][7:0], received);
      if (received !== expected[i][7:0]) begin
        mismatches=mismatches+1;
        $fatal(1,"Tick %0d: MISO=%02h, Python esperaba=%02h",i,received,expected[i]);
      end
      if (i<nticks-1) #(period_ns-9500);
    end
    wait(done_count == nticks);
    #1000;
    $fclose(fd);
    if (tick_count != nticks || done_count != nticks || lost_ticks != 0 || mismatches != 0 || bit_x != 0)
      $fatal(1,"Validacion fallo: rx=%0d done=%0d lost=%0d mismatch=%0d X=%0d",tick_count,done_count,lost_ticks,mismatches,bit_x);
    if (status_reads < nticks || price_reads < nticks || decision_writes < nticks)
      $fatal(1,"MMIO incompleto status=%0d price=%0d decision=%0d",status_reads,price_reads,decision_writes);
    $display("PASS rendimiento: ticks=%0d completados=%0d perdidos=%0d MISO_mismatch=%0d STATUS=%0d PRICE=%0d DECISION=%0d",tick_count,done_count,lost_ticks,mismatches,status_reads,price_reads,decision_writes);
    $finish;
  end
endmodule
