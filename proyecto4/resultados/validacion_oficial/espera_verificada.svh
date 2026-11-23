  // Prove one period of the eight-clock polling loop in the four-state RTL.
  longint ciclos_omitidos = 0;
  int esperas_aceleradas = 0;
  bit comprobando_sondeo = 0;
  bit sondeo_valido;
  int lecturas_status;

  always @(posedge clk) if (comprobando_sondeo) begin
    if (dut.data_req === 1'b1 && dut.data_we === 1'b0 &&
        dut.data_addr === 32'h8001_0000)
      lecturas_status++;
    else if (dut.data_req !== 1'b0)
      sondeo_valido = 0;
    if (!((dut.u_core.u_rf.wr === 1'b0) ||
          (dut.u_core.u_rf.wr === 1'b1 && dut.u_core.rf_waddr === 4'd2)))
      sondeo_valido = 0;
    if (dut.u_spi.byte_done !== 1'b0)
      sondeo_valido = 0;
  end

  function automatic logic [511:0] estado_sondeo();
    // Only x2 can be written in the checked loop. Other memories retain state.
    estado_sondeo = {
      dut.u_core.u_if.pc_q, dut.u_core.u_if.pc_id_q, dut.u_core.u_if.valid_q,
      dut.u_core.u_id.ops_valid_q, dut.u_core.u_lsu.busy_q,
      dut.u_core.rf_rdata_a, dut.u_core.rf_rdata_b,
      dut.u_core.u_rf.u_bankA.u_lo.mem[2], dut.u_core.u_rf.u_bankA.u_hi.mem[2],
      dut.u_core.u_rf.u_bankB.u_lo.mem[2], dut.u_core.u_rf.u_bankB.u_hi.mem[2],
      dut.instr_rdata, dut.ram_b_rdata, dut.rd_is_per, dut.rd_is_spi,
      dut.u_spi.sclk_sync, dut.u_spi.mosi_sync, dut.u_spi.cs_sync,
      dut.u_spi.rx_shift, dut.u_spi.tx_shift, dut.u_spi.bit_cnt,
      dut.u_spi.tx_hold, dut.u_spi.price_q, dut.u_spi.new_price_q, dut.spi_rdata,
`ifdef OFFICIAL_IDLE_MMIO
      dut.u_sma10.pointer_q, dut.u_sma10.count_q, dut.u_sma10.sum_q, dut.u_sma10.history_rdata,
`endif
      dut.u_periph.led_q, dut.u_periph.digit_q, dut.u_periph.led_cycle_q,
      dut.per_rdata
    };
  endfunction

  function automatic bit puede_comprobar_sondeo();
    puede_comprobar_sondeo = !esperando &&
      (dut.por_cnt === 4'hf) && (dut.u_spi.new_price_q === 1'b0) &&
      (cs_n === 1'b1) && (sclk === 1'b0) &&
      (dut.u_spi.cs_sync === 3'b111) && (dut.u_spi.sclk_sync === 3'b000) &&
      (dut.u_spi.mosi_sync === {3{mosi}}) &&
      (dut.u_periph.btn_meta_q === 4'hf) &&
      (dut.u_periph.btn_sync_q === 4'hf) &&
      (dut.u_periph.btn_candidate_q === 4'hf) &&
      (dut.u_periph.debounce_q <= 249999) &&
      !$isunknown(dut.u_periph.cycle_q);
  endfunction

  task automatic esperar_periodo_verificado(input time deadline);
    logic [511:0] inicio;
    int intentos, omitir, falta_debounce;
    bit salto;
    intentos = 0;
    salto = 0;
    while (!salto && intentos < 64 && deadline > $time + 400) begin
      intentos++;
      @(negedge clk);
      #1;
      if (puede_comprobar_sondeo()) begin
        inicio = estado_sondeo();
        sondeo_valido = 1;
        lecturas_status = 0;
        comprobando_sondeo = 1;
        repeat (8) @(negedge clk);
        #1;
        comprobando_sondeo = 0;
        if (sondeo_valido && lecturas_status == 1 && puede_comprobar_sondeo() &&
            (estado_sondeo() === inicio)) begin
          // Resume the next rising edge on its original phase.
          omitir = ((deadline - $time - 40) / 320) * 8;
          if (omitir > 0) begin
            reanudar_reloj = $time + 19 + 40 * omitir;
            ciclos_omitidos += omitir;
            esperas_aceleradas++;
            salto = 1;

            // Advance the two free-running counters and the button debounce
            // exactly over the skipped clocks.
            ciclos += omitir;
            dut.u_periph.cycle_q += omitir;
            falta_debounce = 249999 - dut.u_periph.debounce_q;
            if (omitir > falta_debounce) begin
              dut.u_periph.debounce_q = 249999;
              dut.u_periph.btn_q = dut.u_periph.btn_candidate_q;
            end else
              dut.u_periph.debounce_q += omitir;
          end
        end
      end else repeat (7) @(negedge clk);
    end
    #(deadline - $time);
  endtask
