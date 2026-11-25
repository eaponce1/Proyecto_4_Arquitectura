// Testbench Proyecto 4: emula a la FPGA maestra.
// Correr desde la raíz del repositorio:
//   python3 tools/pochoasm.py sw/trade.s -o sw/trade.hex
//   iverilog -g2012 -s tb_proyecto_4 -o /tmp/tb_p4 $(yosys-config --datdir)/ice40/cells_sim.v rtl/*.v rtl/espino_core/*.v tb/tb_proyecto_4.sv
//   vvp -n /tmp/tb_p4

`timescale 1ns/1ps

module tb_proyecto_4;

  // Configuración: pueden cambiar estos valores
  localparam string PROGRAMA   = "proyecto4/alternativas/mmio_sma10/sw/trade.hex";
  localparam string SERIE      = "proyecto4/resultados/validacion_oficial/practica_meta.csv";
  localparam int    PERIODO_NS = 1000000;   // ronda 1: 10000000, ronda 2: 1000000, ronda 3: 100000
  localparam int    NTICKS     = 16;     // la serie completa tiene 20000

  localparam int CAJA0    = 10000;
  localparam int COMISION = 5;
  localparam int SPI_NS   = 9500;          // duración de una transacción SPI

  // Pochoco SoC a 25 MHz
  logic clk = 0;
  time reanudar_reloj = 0;
  always begin
    #20;
    if ($time < reanudar_reloj) #(reanudar_reloj-$time);
    clk = ~clk;
  end

  logic sclk = 0, mosi = 0, cs_n = 1;
  wire  miso;

  pochoco_soc #(.MemFile(PROGRAMA), .EnableSpi(1)) dut (
    .i_Clk(clk), .o_LED(), .i_Switch(4'b0000),
    .o_Segment1_A(), .o_Segment1_B(), .o_Segment1_C(), .o_Segment1_D(),
    .o_Segment1_E(), .o_Segment1_F(), .o_Segment1_G(),
    .o_Segment2_A(), .o_Segment2_B(), .o_Segment2_C(), .o_Segment2_D(),
    .o_Segment2_E(), .o_Segment2_F(), .o_Segment2_G(),
    .i_SPI_SCLK(sclk), .i_SPI_MOSI(mosi), .i_SPI_CS_n(cs_n), .o_SPI_MISO(miso));

  // Lee la serie de precios (CSV "tick,price")
  int precio [20000];

  task automatic leer_serie;
    int fd, t, r;
    string encabezado;
    fd = $fopen(SERIE, "r");
    if (fd == 0) begin $display("ERROR: no se encontro %s", SERIE); $finish; end
    r = $fgets(encabezado, fd);
    for (int n = 0; n < NTICKS; n++) r = $fscanf(fd, "%d,%d\n", t, precio[n]);
    $fclose(fd);
  endtask

  // SPI modo 0: envía el precio y recibe la decisión
  int bits_x = 0;

  task automatic spi(input logic [7:0] enviar, output logic [7:0] recibido);
    cs_n = 0;
    #1000;
    for (int b = 7; b >= 0; b--) begin
      mosi = enviar[b];
      #500 sclk = 1;
      if (miso !== 1'b0 && miso !== 1'b1) bits_x++;
      recibido[b] = (miso === 1'b1);
      #500 sclk = 0;
    end
    #500 cs_n = 1;
  endtask

  // Contabilidad oficial
  int caja = CAJA0, acciones = 0, w = CAJA0, peak = CAJA0, max_dd = 0;
  int ordenes = 0;

  task automatic ejecutar(input logic [7:0] decision, input int p);
    int q = decision[5:0];
    case (decision[7:6])
      2'b01: begin                                         // comprar lo que alcance
        if (q > (caja - COMISION) / p) q = (caja - COMISION) / p;
        if (q > 0) begin caja -= q * p + COMISION; acciones += q; ordenes++; end
      end
      2'b10: begin                                         // vender lo que se tenga
        if (q > acciones) q = acciones;
        if (q > 0 && caja + q * p >= COMISION) begin caja += q * p - COMISION; acciones -= q; ordenes++; end
      end
      default: ;                                           // 00 y 11: mantener
    endcase
    w = caja + acciones * p;
    if (w > peak) peak = w;
    if (peak - w > max_dd) max_dd = peak - w;
  endtask

  // Mide los ciclos entre que llega el precio y el programa escribe DECISION
  int ciclos = 0, peor_caso = 0, respuestas = 0, precios_perdidos = 0;
  longint unsigned ciclos_acumulados = 0;
  bit esperando = 0;

  always @(posedge clk) begin
    ciclos++;
    if (dut.u_spi.byte_done) begin
      if (dut.u_spi.new_price_q) precios_perdidos++;      // el precio anterior no se leyó
      ciclos = 0;
      esperando = 1;
    end else if (esperando && dut.u_spi.wr && dut.u_spi.off == 2) begin
      if (ciclos > peor_caso) peor_caso = ciclos;
      respuestas++;
      ciclos_acumulados = ciclos_acumulados + ciclos;
      esperando = 0;
    end
  end

  // Chequeos
  int total_tests = 0, tests_aprobados = 0;

  task automatic chequear(input bit ok, input string nombre);
    total_tests++;
    if (ok) begin tests_aprobados++; $display("PASS %s", nombre); end
    else $display("FAIL %s", nombre);
  endtask

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

  // Simulación
  logic [7:0] decision;
  int fd, ref_q, ref_w, presupuesto;

  initial begin
    leer_serie();
    fd = $fopen("C:/Users/Edu Ponce/Downloads/Proyecto-2_Juego-en-Assembly-main (1)/Proyecto-2_Juego-en-Assembly-main/pochoco_soc-main/proyecto4/resultados/validacion_oficial/contraste_rapido/mmio_sma10_base/ronda_2/decisiones.csv", "w");
    $fdisplay(fd, "tick,precio,decision,caja,acciones,patrimonio");
    #4000;

    for (int n = 0; n < NTICKS; n++) begin
      spi(precio[n], decision);                            // decisión tomada con el precio anterior
      ejecutar(decision, precio[n]);                       // se ejecuta al precio actual
      $fdisplay(fd, "%0d,%0d,%02h,%0d,%0d,%0d", n, precio[n], decision, caja, acciones, w);
      esperar_periodo_verificado($time + PERIODO_NS - SPI_NS);
    end
    $fclose(fd);

    ref_q       = (CAJA0 - COMISION) / precio[0];
    ref_w       = CAJA0 - COMISION - ref_q * precio[0] + ref_q * precio[NTICKS - 1];
    presupuesto = (PERIODO_NS - SPI_NS) / 40;

    $display("Patrimonio final:          %0d", w);
    $display("Ordenes ejecutadas:        %0d", ordenes);
    $display("Perdida maxima:            %0d", max_dd);
    $display("No operar:                 %0d", CAJA0);
    $display("Comprar y mantener:        %0d", ref_w);
    $display("Peor caso precio->decision: %0d ciclos (disponibles: %0d)", peor_caso, presupuesto);
    $display("Ciclos promedio precio->decision: %0.2f (%0d respuestas)", respuestas ? (1.0*ciclos_acumulados) / respuestas : 0.0, respuestas);
    $display("Suma de ciclos de respuesta: %0d", ciclos_acumulados);
    $display("Detalle por tick en decisiones.csv");

    chequear(bits_x == 0,           "MISO sin valores X");
    chequear(respuestas > 0,        "el programa escribe DECISION");
    chequear(precios_perdidos == 0, "el programa lee todos los precios");
    chequear(peor_caso < presupuesto, "la decision llega antes del siguiente tick");

    $display("Espera verificada: %0d intervalos, %0d ciclos omitidos, time_ns=%0d",
             esperas_aceleradas, ciclos_omitidos, $time);
    $display("Testbenchs aprobados: %0d/%0d", tests_aprobados, total_tests);
    $finish;
  end

endmodule
