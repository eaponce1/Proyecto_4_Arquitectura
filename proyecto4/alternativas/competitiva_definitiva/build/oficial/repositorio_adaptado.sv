// Testbench Proyecto 4: emula a la FPGA maestra.
// Adaptado del banco del profesor para MMIO SMA10 base con Icarus en Windows.
// Correr desde la raíz con tb/ejecutar_tb_proyecto4.ps1.

`timescale 1ns/1ps

module tb_proyecto_4;

  // Configuración: pueden cambiar estos valores
  localparam PROGRAMA = "proyecto4/alternativas/competitiva_definitiva/trade.hex";
  localparam SERIE = "proyecto4/alternativas/competitiva_definitiva/datos/practica_meta_2022.csv";
  localparam SALIDA = "proyecto4/alternativas/competitiva_definitiva/build/oficial/repositorio_decisiones.csv";
  localparam int    PERIODO_NS = 100000;   // ronda 1: 10000000, ronda 2: 1000000, ronda 3: 100000
  localparam int    NTICKS     = 2000;     // la serie completa tiene 20000

  localparam int CAJA0    = 10000;
  localparam int COMISION = 5;
  localparam int SPI_NS   = 9500;          // duración de una transacción SPI

  // Pochoco SoC a 25 MHz
  logic clk = 0;
  always #20 clk = ~clk;

  logic sclk = 0, mosi = 0, cs_n = 1;
  wire  miso;

  trade_spi_externo #(.ARCHIVO_FIRMWARE(PROGRAMA)) dut (
    .i_Clk(clk), .o_LED(), .i_SPI_SCLK(sclk), .i_SPI_MOSI(mosi),
    .i_SPI_CS_n(cs_n), .o_SPI_MISO(miso));

  // Lee la serie de precios (CSV "tick,price")
  int precio [20000];

  task automatic leer_serie;
    int fd, t, r;
    reg [8*128-1:0] encabezado;
    fd = $fopen(SERIE, "r");
    if (fd == 0) $fatal(1, "No se encontro %s", SERIE);
    r = $fgets(encabezado, fd);
    if (r == 0) $fatal(1, "CSV sin encabezado: %s", SERIE);
    for (int n = 0; n < NTICKS; n++) begin
      r = $fscanf(fd, "%d,%d\n", t, precio[n]);
      if (r != 2 || t !== n) $fatal(1, "Fila CSV invalida para tick %0d", n);
      if (precio[n] < 1 || precio[n] > 255)
        $fatal(1, "Precio fuera de 1..255 en tick %0d: %0d", n, precio[n]);
    end
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
  int latencia_tick = 0;
  bit esperando = 0;

  always @(posedge dut.clk_soc) begin
    ciclos++;
    if (dut.u_soc.u_spi.byte_done) begin
      if (dut.u_soc.u_spi.new_price_q) precios_perdidos++;      // el precio anterior no se leyó
      ciclos = 0;
      esperando = 1;
    end else if (esperando && dut.u_soc.u_spi.wr && dut.u_soc.u_spi.off == 2) begin
      latencia_tick = ciclos;
      if (ciclos > peor_caso) peor_caso = ciclos;
      respuestas++;
      esperando = 0;
    end
  end

  // Comprueba el byte que recibe el slave, la lectura PRICE y cada escritura
  // DECISION. El conteo de escrituras incluye las que lleguen fuera de turno.
  int tramas = 0, bytes_recibidos = 0, lecturas_price = 0, escrituras_decision = 0;
  logic [7:0] decision_escrita;
  always @(posedge dut.clk_soc) begin
    if (dut.rst_ni) begin
      if (dut.u_soc.u_spi.byte_done) begin
        if (bytes_recibidos >= NTICKS || bytes_recibidos + 1 != tramas)
          $fatal(1, "SPI byte_done fuera de turno: trama %0d", tramas);
        if (dut.u_soc.u_spi.price_o !== precio[bytes_recibidos][7:0])
          $fatal(1, "Precio SPI incorrecto en tick %0d", bytes_recibidos);
        bytes_recibidos++;
      end
      if (dut.u_soc.u_spi.price_read) begin
        if (lecturas_price + 1 != bytes_recibidos || dut.u_soc.u_spi.new_price_q !== 1'b1
            || dut.u_soc.data_addr !== 32'h80010004)
          $fatal(1, "Lectura PRICE fuera de turno: trama %0d", tramas);
        if (dut.u_soc.u_spi.price_q !== precio[lecturas_price][7:0])
          $fatal(1, "PRICE latcheado incorrecto en tick %0d", lecturas_price);
        lecturas_price++;
      end
      if (dut.u_soc.u_spi.wr && dut.u_soc.u_spi.off == 2) begin
        if (escrituras_decision + 1 != lecturas_price || dut.u_soc.data_addr !== 32'h80010008)
          $fatal(1, "Escritura DECISION fuera de turno: trama %0d", tramas);
        decision_escrita = dut.u_soc.u_spi.wdata_i[7:0];
        if ($isunknown(decision_escrita))
          $fatal(1, "Escritura DECISION desconocida en tick %0d", escrituras_decision);
        escrituras_decision++;
      end
    end
  end

  // Chequeos
  int total_tests = 0, tests_aprobados = 0;

  task automatic chequear(input bit ok, input string nombre);
    total_tests++;
    if (ok) begin tests_aprobados++; $display("PASS %s", nombre); end
    else $display("FAIL %s", nombre);
  endtask

  // Simulación
  logic [7:0] decision;
  logic [7:0] decision_anterior = 8'h00;
  int fd, ref_q, ref_w, presupuesto;

  initial begin
    leer_serie();
    fd = $fopen(SALIDA, "w");
    if (fd == 0) $fatal(1, "No se pudo escribir %s", SALIDA);
    $fdisplay(fd, "tick,precio,decision,caja,acciones,patrimonio,decision_escrita,ciclos");
    #120113;

    for (int n = 0; n < NTICKS; n++) begin
      tramas++;
      spi(precio[n][7:0], decision);                       // decisión tomada con el precio anterior
      if (decision !== decision_anterior)
        $fatal(1, "MISO tick %0d: recibido %02h, DECISION anterior %02h",
               n, decision, decision_anterior);
      ejecutar(decision, precio[n]);                       // se ejecuta al precio actual
      #(PERIODO_NS - SPI_NS);
      if (bytes_recibidos != tramas || lecturas_price != tramas
          || escrituras_decision != tramas || respuestas != tramas
          || esperando || dut.u_soc.u_spi.new_price_q !== 1'b0)
        $fatal(1, "Tick %0d incompleto: SPI=%0d PRICE=%0d DECISION=%0d respuestas=%0d",
               n, bytes_recibidos, lecturas_price, escrituras_decision, respuestas);
      $fdisplay(fd, "%0d,%0d,%02h,%0d,%0d,%0d,%02h,%0d",
                n, precio[n], decision, caja, acciones, w, decision_escrita, latencia_tick);
      decision_anterior = decision_escrita;
    end
    $fclose(fd);

    ref_q       = (CAJA0 - COMISION) / precio[0];
    ref_w       = CAJA0 - COMISION - ref_q * precio[0] + ref_q * precio[NTICKS - 1];
    presupuesto = (PERIODO_NS - SPI_NS) / 80;

    $display("Patrimonio final:          %0d", w);
    $display("Ordenes ejecutadas:        %0d", ordenes);
    $display("Perdida maxima:            %0d", max_dd);
    $display("No operar:                 %0d", CAJA0);
    $display("Comprar y mantener:        %0d", ref_w);
    $display("Peor caso precio->decision: %0d ciclos (disponibles: %0d)", peor_caso, presupuesto);
    $display("Detalle por tick en %s", SALIDA);
    $display("Ticks procesados: %0d", tramas);
    $display("Bytes SPI recibidos: %0d", bytes_recibidos);
    $display("Lecturas PRICE: %0d", lecturas_price);
    $display("Escrituras DECISION: %0d", escrituras_decision);
    $display("Respuestas precio->decision: %0d", respuestas);
    $display("Bits MISO desconocidos: %0d", bits_x);
    $display("Precios perdidos: %0d", precios_perdidos);

    chequear(bits_x == 0,           "MISO sin valores X");
    chequear(respuestas > 0,        "el programa escribe DECISION");
    chequear(precios_perdidos == 0, "el programa lee todos los precios");
    chequear(peor_caso < presupuesto, "la decision llega antes del siguiente tick");

    $display("Testbenchs aprobados: %0d/%0d", tests_aprobados, total_tests);
    if (tests_aprobados != total_tests) $fatal(1, "Fallo un criterio del banco del profesor");
    $display("PASS una lectura PRICE y una escritura DECISION por tick");
    $display("PASS %0d bytes MISO coinciden con DECISION del tick anterior", tramas);
    $finish;
  end

endmodule
