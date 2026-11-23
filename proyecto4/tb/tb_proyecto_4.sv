// Proyecto 4 master-FPGA simulation testbench.
// Run from the pochoco_soc-main directory; see proyecto4/README.md.
`timescale 1ns/1ps

module tb_proyecto_4;

  localparam string PROGRAMA = "proyecto4/sw/spi_smoke.hex";
  localparam string SERIE = "proyecto4/data/practica_meta.csv";
  localparam integer SERIE_TICKS = 20000;
  localparam integer CAJA0 = 10000;
  localparam integer COMISION = 5;
  localparam integer SPI_NS = 9500;

  logic clk = 0;
  always #20 clk = ~clk;

  logic sclk = 0, mosi = 0, cs_n = 1;
  wire miso;

  pochoco_soc #(
    .MemFile(PROGRAMA),
    .EnableSpi(1)
  ) dut (
    .i_Clk(clk), .o_LED(), .i_Switch(4'b0000),
    .o_Segment1_A(), .o_Segment1_B(), .o_Segment1_C(), .o_Segment1_D(),
    .o_Segment1_E(), .o_Segment1_F(), .o_Segment1_G(),
    .o_Segment2_A(), .o_Segment2_B(), .o_Segment2_C(), .o_Segment2_D(),
    .o_Segment2_E(), .o_Segment2_F(), .o_Segment2_G(),
    .i_SPI_SCLK(sclk), .i_SPI_MOSI(mosi), .i_SPI_CS_n(cs_n), .o_SPI_MISO(miso)
  );

  integer precio [0:SERIE_TICKS-1];
  integer tick_id [0:SERIE_TICKS-1];
  integer nticks_run = SERIE_TICKS;
  integer ronda = 1;
  integer periodo_ns;
  integer loaded_ticks = 0;
  integer bits_x = 0;

  task automatic leer_serie;
    integer fd, r, t, p;
    reg [1023:0] encabezado;
    begin
      fd = $fopen(SERIE, "r");
      if (fd == 0) $fatal(1, "No se encontro %s", SERIE);
      r = $fgets(encabezado, fd);
      if (r == 0) $fatal(1, "CSV vacio: %s", SERIE);
      if (encabezado != "tick,price\n")
        $display("Aviso: encabezado CSV recibido como '%s'", encabezado);
      while (loaded_ticks < SERIE_TICKS) begin
        r = $fscanf(fd, "%d,%d\n", t, p);
        if (r != 2) $fatal(1, "CSV incompleto o invalido en fila %0d", loaded_ticks + 2);
        if (t != loaded_ticks) $fatal(1, "Tick fuera de secuencia: fila %0d contiene %0d", loaded_ticks, t);
        if (p < 1 || p > 255) $fatal(1, "Precio fuera de rango en tick %0d: %0d", t, p);
        tick_id[loaded_ticks] = t;
        precio[loaded_ticks] = p;
        loaded_ticks = loaded_ticks + 1;
      end
      r = $fscanf(fd, "%d,%d", t, p);
      if (r == 2) $fatal(1, "El CSV tiene mas de %0d ticks", SERIE_TICKS);
      $fclose(fd);
      $display("CSV OK: %0d ticks, primero=%0d, ultimo=%0d", loaded_ticks, precio[0], precio[SERIE_TICKS-1]);
    end
  endtask

  task automatic spi(input logic [7:0] enviar, output logic [7:0] recibido);
    begin
      cs_n = 0;
      #1000;
      for (integer b = 7; b >= 0; b = b - 1) begin
        mosi = enviar[b];
        #500 sclk = 1;
        if (miso !== 1'b0 && miso !== 1'b1) bits_x = bits_x + 1;
        recibido[b] = (miso === 1'b1);
        #500 sclk = 0;
      end
      #500 cs_n = 1;
    end
  endtask

  integer caja = CAJA0, acciones = 0, w = CAJA0, peak = CAJA0, max_dd = 0;
  integer ordenes = 0;

  // Contabilidad de la FPGA maestra: conservada sin cambios semanticos.
  task automatic ejecutar(input logic [7:0] decision, input integer p);
    integer q;
    begin
      q = decision[5:0];
      case (decision[7:6])
        2'b01: begin
          if (q > (caja - COMISION) / p) q = (caja - COMISION) / p;
          if (q > 0) begin caja = caja - q * p - COMISION; acciones = acciones + q; ordenes = ordenes + 1; end
        end
        2'b10: begin
          if (q > acciones) q = acciones;
          if (q > 0 && caja + q * p >= COMISION) begin caja = caja + q * p - COMISION; acciones = acciones - q; ordenes = ordenes + 1; end
        end
        default: ;
      endcase
      w = caja + acciones * p;
      if (w > peak) peak = w;
      if (peak - w > max_dd) max_dd = peak - w;
    end
  endtask

  integer ciclos = 0, peor_caso = 0, respuestas = 0, precios_perdidos = 0;
  integer lecturas_status = 0, lecturas_price = 0, escrituras_decision = 0;
  bit esperando = 0;

  always @(posedge clk) begin
    ciclos = ciclos + 1;
    if (dut.u_spi.rd && dut.u_spi.off == 0) lecturas_status = lecturas_status + 1;
    if (dut.u_spi.rd && dut.u_spi.off == 1) lecturas_price = lecturas_price + 1;
    if (dut.u_spi.wr && dut.u_spi.off == 2) escrituras_decision = escrituras_decision + 1;
    if (dut.u_spi.byte_done) begin
      if (dut.u_spi.new_price_q) precios_perdidos = precios_perdidos + 1;
      ciclos = 0;
      esperando = 1;
    end else if (esperando && dut.u_spi.wr && dut.u_spi.off == 2) begin
      if (ciclos > peor_caso) peor_caso = ciclos;
      respuestas = respuestas + 1;
      esperando = 0;
    end
  end

  integer total_tests = 0, tests_aprobados = 0;
  task automatic chequear(input bit ok, input string nombre);
    begin
      total_tests = total_tests + 1;
      if (ok) begin tests_aprobados = tests_aprobados + 1; $display("PASS %s", nombre); end
      else $display("FAIL %s", nombre);
    end
  endtask

  logic [7:0] decision;
  integer n, fd, ref_q, ref_w, presupuesto;
  logic [7:0] decision_esperada = 8'h00;
  bit desfase_ok = 1'b1;

  initial begin
    if (!$value$plusargs("ROUND=%d", ronda)) ronda = 1;
    if (!$value$plusargs("TICKS=%d", nticks_run)) nticks_run = SERIE_TICKS;
    case (ronda)
      1: periodo_ns = 10000000;
      2: periodo_ns = 1000000;
      3: periodo_ns = 100000;
      default: $fatal(1, "ROUND debe ser 1, 2 o 3");
    endcase
    if (nticks_run < 1 || nticks_run > SERIE_TICKS)
      $fatal(1, "TICKS debe estar entre 1 y %0d", SERIE_TICKS);
    leer_serie();
    fd = $fopen("proyecto4/decisiones.csv", "w");
    if (fd == 0) $fatal(1, "No se pudo crear proyecto4/decisiones.csv");
    $fdisplay(fd, "tick,precio,decision,caja,acciones,patrimonio");
    #4000;

    for (n = 0; n < nticks_run; n = n + 1) begin
      spi(precio[n][7:0], decision);
      // El byte recibido al inicio del tick es la decision anterior.
      if (decision !== decision_esperada) desfase_ok = 1'b0;
      ejecutar(decision, precio[n]);
      $fdisplay(fd, "%0d,%0d,%02h,%0d,%0d,%0d", tick_id[n], precio[n], decision, caja, acciones, w);
      decision_esperada = 8'h41;
      #(periodo_ns - SPI_NS);
    end
    $fclose(fd);

    ref_q = (CAJA0 - COMISION) / precio[0];
    ref_w = CAJA0 - COMISION - ref_q * precio[0] + ref_q * precio[nticks_run-1];
    presupuesto = (periodo_ns - SPI_NS) / 40;

    $display("Ronda: %0d; periodo: %0d ns; ticks simulados: %0d", ronda, periodo_ns, nticks_run);
    $display("Patrimonio final:          %0d", w);
    $display("Ordenes ejecutadas:        %0d", ordenes);
    $display("Perdida maxima:            %0d", max_dd);
    $display("No operar:                 %0d", CAJA0);
    $display("Comprar y mantener:        %0d", ref_w);
    $display("Peor caso precio->decision: %0d ciclos (disponibles: %0d)", peor_caso, presupuesto);
    $display("Lecturas STATUS=%0d PRICE=%0d; escrituras DECISION=%0d", lecturas_status, lecturas_price, escrituras_decision);

    chequear(loaded_ticks == SERIE_TICKS, "CSV completo: 20000 ticks consecutivos");
    chequear(bits_x == 0, "MISO sin valores X");
    chequear(lecturas_status > 0, "el procesador lee STATUS");
    chequear(lecturas_price >= nticks_run-1, "el procesador lee PRICE en cada tick utilizable");
    chequear(escrituras_decision >= nticks_run-1, "el procesador escribe DECISION");
    chequear(respuestas > 0, "se observan respuestas del procesador");
    chequear(precios_perdidos == 0, "el procesador lee los precios antes del tick siguiente");
    chequear(peor_caso < presupuesto, "la decision llega antes del siguiente tick");
    chequear(desfase_ok, "MISO transporta la decision previa tick a tick");
    $display("Testbenches aprobados: %0d/%0d", tests_aprobados, total_tests);
    if (tests_aprobados != total_tests) $fatal(1, "Fallaron chequeos del testbench Proyecto 4");
    $finish;
  end
endmodule
