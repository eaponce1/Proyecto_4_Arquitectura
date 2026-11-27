`timescale 1ns/1ps
module tb_candidata;
  parameter integer TICKS = 20000, FASE_NS = 0, PERIODO_NS = 30000;
  parameter integer PALABRAS_FIRMWARE = 71;
  parameter ARCHIVO_FIRMWARE = "proyecto4/alternativas/mmio_sma10/sw/trade.hex";
  parameter integer REG_CAJA = -1, REG_ACCIONES = -1;
  parameter integer K_START=0, K_END=0, ES_MMIO=1;
  localparam integer SPI_NS = 9500, CICLO_SOC_NS = 80;
  localparam integer PRESUPUESTO = (PERIODO_NS - SPI_NS) / CICLO_SOC_NS;
  localparam integer COMISION = 5;

  reg clk = 0, sclk = 0, mosi = 0, cs_n = 1;
  wire miso;
  wire [3:0] leds;
  always #20 clk = ~clk;
`ifdef NETLIST
  trade_spi_externo dut (
`else
  trade_spi_externo #(
    .PALABRAS_FIRMWARE(PALABRAS_FIRMWARE), .ARCHIVO_FIRMWARE(ARCHIVO_FIRMWARE)
  ) dut (
`endif
    .i_Clk(clk), .i_SPI_SCLK(sclk), .i_SPI_MOSI(mosi), .i_SPI_CS_n(cs_n),
    .o_SPI_MISO(miso), .o_LED(leds)
  );

  reg [7:0] precios [0:TICKS-1], misos [0:TICKS-1], decisiones [0:TICKS-1];
  reg [63:0] carteras [0:TICKS-1];
  string vectores, cartera_path, metricas;
  integer tick = 0, fd = 0, progreso = 1000;
  integer caja = 10000, acciones = 0, patrimonio = 10000, pico = 10000, drawdown = 0;
  integer compras = 0, ventas = 0, comisiones = 0, fill = 0;
  bit comprobar_cartera = 0, hubo_decision = 0;
  reg [7:0] recibido = 0, anterior = 0;

  task automatic ejecutar_en_maestra(input integer precio);
    integer cantidad, limite;
    begin
      cantidad = int'(recibido[5:0]);
      fill = 0;
      case (recibido[7:6])
        2'b01: begin
          limite = caja >= COMISION ? (caja - COMISION) / precio : 0;
          fill = cantidad < limite ? cantidad : limite;
          if (fill > 0) begin
            caja -= fill * precio + COMISION;
            acciones += fill;
            compras++;
            comisiones += COMISION;
          end
        end
        2'b10: begin
          fill = cantidad < acciones ? cantidad : acciones;
          if (fill > 0 && caja + fill * precio >= COMISION) begin
            caja += fill * precio - COMISION;
            acciones -= fill;
            ventas++;
            comisiones += COMISION;
          end else begin
            fill = 0;
          end
        end
        default: begin end
      endcase
      if (caja < 0 || acciones < 0) $fatal(1, "Caja o acciones negativas en tick %0d", tick);
      patrimonio = caja + acciones * precio;
      if (patrimonio > pico) pico = patrimonio;
      if (pico - patrimonio > drawdown) drawdown = pico - patrimonio;
    end
  endtask

  task automatic probar_orden(
    input reg [7:0] decision, input integer precio, caja_final, acciones_finales,
    input integer ejecutadas, comisiones_finales
  );
    begin
      recibido = decision;
      ejecutar_en_maestra(precio);
      if (caja != caja_final || acciones != acciones_finales || fill != ejecutadas
          || comisiones != comisiones_finales)
        $fatal(1, "Contabilidad %02h a %0d: caja=%0d acciones=%0d fill=%0d comisión=%0d",
               decision, precio, caja, acciones, fill, comisiones);
    end
  endtask

  task automatic probar_contabilidad;
    begin
      probar_orden(8'h41, 100, 9895, 1, 1, 5);       // Comprar 1
      probar_orden(8'h7f, 100, 3590, 64, 63, 10);    // Comprar 63
      probar_orden(8'h7f, 255, 15, 78, 14, 15);      // Compra parcial
      probar_orden(8'h81, 100, 110, 77, 1, 20);      // Venta parcial
      probar_orden(8'hbf, 100, 6405, 14, 63, 25);
      probar_orden(8'hbf, 100, 7800, 0, 14, 30);     // Liquidar inventario
      probar_orden(8'h81, 100, 7800, 0, 0, 30);      // Venta sin acciones
      probar_orden(8'h40, 1, 7800, 0, 0, 30);        // Compra de 0
      probar_orden(8'hff, 1, 7800, 0, 0, 30);        // Acción reservada
      caja = 0;
      acciones = 1;
      probar_orden(8'h81, 1, 0, 1, 0, 30);          // No alcanza para comisión
      $display("PASS contabilidad: compra 1/63, límites de caja e inventario, comisiones");
    end
  endtask

`ifndef NETLIST
  bit vio_reset = 0, activo = 0, limpiar_price = 0, verificar_bus = 0;
  bit status_nuevo = 0, vio_price = 0, vio_sum = 0, vio_ready = 0;
  bit carga_previa = 0;
  integer llegadas = 0, escrituras = 0, ic = 0, peor_caso = 0, peor_ic = 0;
  integer latencia = 0, status_leidos = 0, status_simultaneos = 0;
  reg [7:0] decision_escrita;
  integer suma_esperada = 0, ultima_caja = 0, ultimas_acciones = 0;
  integer cargas_mantenidas = 0;
  longint prof_price=-1, prof_start=-1, prof_end=-1;
  integer prof_ic=0, prof_reads=0, prof_writes=0, prof_alu=0;

  longint ciclo = 0, llegada = 0, ciclos_totales = 0, ic_total = 0;
  reg [31:0] esperado_bus, registros [0:15];

  // Las señales de solicitud y commit se muestrean como el periférico, en posedge.
  // rdata se coteja en el flanco siguiente, después de la actualización síncrona.
  /* verilator lint_off BLKSEQ */
  always @(posedge dut.clk_soc) begin
    ciclo++;
    if (!dut.rst_ni) begin
      vio_reset = 1;
      for (integer i = 0; i < 16; i++) registros[i] = 0;
    end else begin
      if (verificar_bus && dut.u_soc.dbg_spi_rdata !== esperado_bus)
        $fatal(1, "BUS tick=%0d ciclo=%0d rdata=%08h esperado=%08h",
               tick, ciclo, dut.u_soc.dbg_spi_rdata, esperado_bus);
      verificar_bus = 0;
      if (limpiar_price && dut.u_soc.u_spi.new_price_q !== 1'b0)
        $fatal(1, "PRICE no limpió STATUS.new_price tick=%0d", tick);
      limpiar_price = 0;

      if (carga_previa && dut.u_soc.u_core.lsu_req && !dut.u_soc.u_core.lsu_we) begin
        if (dut.u_soc.dbg_data_req)
          $fatal(1, "LSU volvió a emitir una carga mantenida tick=%0d", tick);
        if (activo) cargas_mantenidas++;
      end
      carga_previa = dut.u_soc.u_core.lsu_req && !dut.u_soc.u_core.lsu_we;

      if (dut.u_soc.u_core.rf_we && dut.u_soc.u_core.rf_waddr != 0)
        registros[dut.u_soc.u_core.rf_waddr] = dut.u_soc.u_core.rf_wdata;
      if (dut.byte_done) begin
        prof_price=-1; prof_start=-1; prof_end=-1;
        prof_ic=0; prof_reads=0; prof_writes=0; prof_alu=0;
      end
      if (activo && !dut.byte_done) begin
        if (dut.lee_price) prof_price=ciclo;
        if (dut.u_soc.dbg_instr_valid && dut.u_soc.dbg_pc_id==K_START && prof_start<0)
          prof_start=ciclo;
        if (dut.u_soc.dbg_instr_valid && dut.u_soc.dbg_pc_id==K_END && prof_end<0)
          prof_end=ciclo;
        if (dut.commit && dut.u_soc.dbg_pc_id>=K_START && dut.u_soc.dbg_pc_id<K_END) begin
          prof_ic++;
          if (dut.u_soc.dbg_instr_id[6:0]==7'h0b) prof_alu+=2;
          else if ((dut.u_soc.dbg_instr_id[6:0]==7'h13 || dut.u_soc.dbg_instr_id[6:0]==7'h33)
                   && dut.u_soc.dbg_instr_id[14:12]==0) prof_alu++;
        end
        if (dut.u_soc.dbg_data_req && dut.u_soc.dbg_pc_id>=K_START && dut.u_soc.dbg_pc_id<K_END) begin
          if (dut.u_soc.dbg_data_we) prof_writes++; else prof_reads++;
        end
        if (dut.commit && dut.u_soc.dbg_pc_id==K_END) begin
          if (registros[10] !== suma_esperada || registros[13] !== (tick>=9 ? 32'd1 : 32'd0))
            $fatal(1,"Kernel distinto tick=%0d SUM=%0d/%0d READY=%0d",tick,registros[10],suma_esperada,registros[13]);
        end
        if (dut.escribe_decision && (prof_price<llegada || prof_start<prof_price || prof_end<=prof_start || ciclo<prof_end))
          $fatal(1,"Perfil fuera de orden tick=%0d precio=%0d inicio=%0d fin=%0d",tick,prof_price,prof_start,prof_end);
      end
      if (dut.commit && (dut.u_soc.dbg_pc_id >= 4 * PALABRAS_FIRMWARE
                        || dut.u_soc.u_core.illegal_insn !== 1'b0))
        $fatal(1, "Instrucción inválida tick=%0d pc=%08h insn=%08h",
               tick, dut.u_soc.dbg_pc_id, dut.u_soc.dbg_instr_id);

      if (dut.byte_done) begin
        if (activo || llegadas != tick || tick >= TICKS || dut.precio_spi !== precios[tick]
            || dut.u_soc.u_spi.new_price_q !== 1'b0)
          $fatal(1, "RX tick=%0d ciclo=%0d recibido=%02h esperado=%02h llegadas=%0d activo=%b",
                 tick, ciclo, dut.precio_spi, precios[tick], llegadas, activo);
        llegada = ciclo;
        llegadas++;
        activo = 1;
        status_nuevo = 0;
        vio_price = 0;
        vio_sum = 0;
        vio_ready = 0;
        status_leidos = 0;
        ic = 0;
        suma_esperada += int'(precios[tick]);
        if (tick >= 10) suma_esperada -= int'(precios[tick-10]);
      end else if (activo && dut.commit) ic++;

      if (dut.u_soc.dbg_status_read && activo) begin
        if (dut.u_soc.dbg_data_addr !== 32'h80010000)
          $fatal(1, "Dirección STATUS inesperada tick=%0d", tick);
        status_leidos++;
        if (dut.byte_done) status_simultaneos++;
        if (dut.u_soc.u_spi.new_price_q) status_nuevo = 1;
        esperado_bus = {30'b0, dut.u_soc.u_spi.cs_active, dut.u_soc.u_spi.new_price_q};
        verificar_bus = 1;
      end
      if (dut.lee_price) begin
        if (!activo || !status_nuevo || vio_price || dut.u_soc.u_spi.new_price_q !== 1'b1
            || dut.u_soc.dbg_data_addr !== 32'h80010004)
          $fatal(1, "PRICE fuera de orden tick=%0d ciclo=%0d status=%0d", tick, ciclo, status_leidos);
        vio_price = 1;
        limpiar_price = 1;
        esperado_bus = {24'b0, precios[tick]};
        verificar_bus = 1;
      end
      if (dut.lee_sum) begin
        if (!activo || !vio_price || vio_sum || dut.u_soc.dbg_data_addr !== 32'h8001000c)
          $fatal(1, "SUM10 fuera de orden tick=%0d", tick);
        vio_sum = 1;
        esperado_bus = suma_esperada;
        verificar_bus = 1;
      end
      if (dut.lee_ready) begin
        if (!activo || !vio_price || vio_ready || dut.u_soc.dbg_data_addr !== 32'h80010010)
          $fatal(1, "READY fuera de orden tick=%0d", tick);
        vio_ready = 1;
        esperado_bus = tick >= 9 ? 1 : 0;
        verificar_bus = 1;
      end
      if (dut.escribe_decision) begin
        if (!activo || escrituras != tick || !vio_price || (ES_MMIO && (!vio_sum || !vio_ready)) || !dut.commit
            || dut.u_soc.dbg_data_addr !== 32'h80010008
            || dut.bus_escritura[7:0] !== decisiones[tick])
          $fatal(1, "DECISION tick=%0d ciclo=%0d escrita=%02h esperada=%02h activo=%b PRICE/SUM10/READY=%b%b%b",
                 tick, ciclo, dut.bus_escritura[7:0], decisiones[tick], activo, vio_price, vio_sum, vio_ready);
        latencia = int'(ciclo - llegada);
        if (latencia >= PRESUPUESTO || ic == 0)
          $fatal(1, "Presupuesto tick=%0d latencia=%0d máximo exclusivo=%0d IC=%0d",
                 tick, latencia, PRESUPUESTO, ic);
        if (latencia > peor_caso) peor_caso = latencia;
        if (ic > peor_ic) peor_ic = ic;
        ciclos_totales += latencia;
        ic_total += ic;
        if (REG_CAJA >= 0) ultima_caja = registros[REG_CAJA];
        if (REG_ACCIONES >= 0) ultimas_acciones = registros[REG_ACCIONES];
        decision_escrita = dut.bus_escritura[7:0];
        escrituras++;
        activo = 0;
      end
    end
  end
  /* verilator lint_on BLKSEQ */
`endif

  initial begin
    if ($test$plusargs("contabilidad_sola")) begin
      probar_contabilidad();
      $finish;
    end
    if (TICKS < 1 || PRESUPUESTO < 1 || FASE_NS < 0
        || REG_CAJA < -1 || REG_CAJA > 15 || REG_ACCIONES < -1 || REG_ACCIONES > 15)
      $fatal(1, "Parámetros inválidos");
    if (!$value$plusargs("vectores=%s", vectores)) $fatal(1, "Se requiere +vectores=carpeta");
    if (!$value$plusargs("progreso=%d", progreso)) progreso = 1000;
    comprobar_cartera = $value$plusargs("cartera=%s", cartera_path);
    if ($value$plusargs("metricas=%s", metricas)) begin
      fd = $fopen(metricas, "w");
      if (fd == 0) $fatal(1, "No se pudo abrir CSV %s", metricas);
      $fdisplay(fd, "tick,periodo_ns,precio,miso_hex,decision_hex,fill,caja,acciones,comisiones_acum,patrimonio,drawdown_max,suma10,status_leidos,ic,ciclos,cpi,kernel_ciclos,kernel_ic,kernel_lecturas,kernel_escrituras,rx_ciclos,cartera_ciclos,decision_ciclos,alu_kernel");
    end
    $readmemh({vectores, "/precios.hex"}, precios, 0, TICKS-1);
    $readmemh({vectores, "/miso.hex"}, misos, 0, TICKS-1);
    $readmemh({vectores, "/escrituras.hex"}, decisiones, 0, TICKS-1);
    if (comprobar_cartera) $readmemh(cartera_path, carteras, 0, TICKS-1);

    #(120113 + FASE_NS);
    if (leds !== 4'b0001) $fatal(1, "El core no arrancó LED=%b", leds);
`ifndef NETLIST
    if (!vio_reset || dut.rst_ni !== 1'b1) $fatal(1, "Falta secuencia reset→arranque");
`endif

    for (tick = 0; tick < TICKS; tick++) begin
      if ((^({precios[tick], misos[tick], decisiones[tick]})) === 1'bx || precios[tick] == 0)
        $fatal(1, "Vector inválido o incompleto tick=%0d", tick);
      cs_n = 0;
      #1000;
      for (integer b = 7; b >= 0; b--) begin
        mosi = precios[tick][b];
        #500 sclk = 1;
        recibido[b] = miso;
        #500 sclk = 0;
      end
      #500 cs_n = 1;
      if (recibido !== misos[tick] || recibido !== anterior)
        $fatal(1, "MISO/desfase tick=%0d observado=%02h Python=%02h anterior=%02h",
               tick, recibido, misos[tick], anterior);
      ejecutar_en_maestra(int'(precios[tick]));
      if (comprobar_cartera && (patrimonio > 16777215 || acciones > 255
          || {caja[31:0], patrimonio[23:0], acciones[7:0]} !== carteras[tick]))
        $fatal(1, "CARTERA tick=%0d caja=%0d patrimonio=%0d acciones=%0d vector=%016h",
               tick, caja, patrimonio, acciones, carteras[tick]);
      #(PERIODO_NS - SPI_NS);
`ifndef NETLIST
      if (llegadas != tick + 1 || escrituras != tick + 1 || activo)
        $fatal(1, "TIMEOUT tick=%0d llegadas=%0d escrituras=%0d ciclo=%0d",
               tick, llegadas, escrituras, ciclo);
      if ((REG_CAJA >= 0 && ultima_caja !== caja) || (REG_ACCIONES >= 0 && ultimas_acciones !== acciones))
        $fatal(1, "CARTERA RTL tick=%0d caja=%0d/%0d acciones=%0d/%0d",
               tick, ultima_caja, caja, ultimas_acciones, acciones);
      if (fd != 0) $fdisplay(fd, "%0d,%0d,%0d,%02h,%02h,%0d,%0d,%0d,%0d,%0d,%0d,%0d,%0d,%0d,%0d,%.6f,%0d,%0d,%0d,%0d,%0d,%0d,%0d,%0d",
                            tick, PERIODO_NS, precios[tick], recibido, decision_escrita,
                            fill, caja, acciones, comisiones, patrimonio, drawdown,
                            suma_esperada, status_leidos, ic, latencia, real'(latencia) / ic,
                            prof_end-prof_start,prof_ic,prof_reads,prof_writes,prof_price-llegada,
                            prof_start-prof_price,latencia+llegada-prof_end,prof_alu);
`else
      if (fd != 0) $fdisplay(fd, "%0d,%0d,%0d,%02h,%02h,%0d,%0d,%0d,%0d,%0d,%0d,,,,,",
                            tick, PERIODO_NS, precios[tick], recibido, decisiones[tick],
                            fill, caja, acciones, comisiones, patrimonio, drawdown);
`endif
      anterior = decisiones[tick];
      hubo_decision |= anterior != 0;
      if (progreso > 0 && (tick + 1) % progreso == 0)
        $display("PROGRESO ticks=%0d/%0d", tick + 1, TICKS);
    end
    if (fd != 0) $fclose(fd);
    if (leds !== {hubo_decision, 3'b111}) $fatal(1, "Hitos inesperados LED=%b", leds);
`ifndef NETLIST
    $display("METRICAS ticks=%0d periodo_ns=%0d ciclos_total=%0d ic_total=%0d peor_caso=%0d presupuesto=%0d peor_ic=%0d status_y_byte_done=%0d cargas_mantenidas=%0d ciclos_promedio=%.6f ic_promedio=%.6f cpi_global=%.6f",
             TICKS, PERIODO_NS, ciclos_totales, ic_total, peor_caso, PRESUPUESTO, peor_ic, status_simultaneos, cargas_mantenidas,
             real'(ciclos_totales)/TICKS, real'(ic_total)/TICKS, real'(ciclos_totales)/ic_total);
    $display("PASS %0d STATUS, PRICE, SUM10, READY y DECISION; peor caso %0d/%0d ciclos",
             TICKS, peor_caso, PRESUPUESTO);
`endif
    $display("CARTERA patrimonio=%0d caja=%0d acciones=%0d compras=%0d ventas=%0d comisiones=%0d drawdown=%0d",
             patrimonio, caja, acciones, compras, ventas, comisiones, drawdown);
    $display("PASS %0d MISO frente a Python, fase %0d ns, LED=%b", TICKS, FASE_NS, leds);
    $finish;
  end
endmodule
