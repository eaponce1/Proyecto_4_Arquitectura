`timescale 1ns/1ps
module tb_diagnostico;
  parameter integer TICKS = 194, PALABRAS = 71;
  parameter FIRMWARE = "proyecto4/alternativas/mmio_sma10/sw/trade.hex";
  localparam integer PERIODO_NS = 40000;

  reg clk = 0, sclk = 0, mosi = 0, cs_n = 1;
  wire miso;
  wire [3:0] leds;
  always #20 clk = ~clk;
  trade_spi_externo #(.PALABRAS_FIRMWARE(PALABRAS), .ARCHIVO_FIRMWARE(FIRMWARE)) dut (
    .i_Clk(clk), .i_SPI_SCLK(sclk), .i_SPI_MOSI(mosi), .i_SPI_CS_n(cs_n),
    .o_SPI_MISO(miso), .o_LED(leds)
  );

  reg [7:0] precios [0:TICKS-1], esperado_miso [0:TICKS-1], esperado_decision [0:TICKS-1];
  reg [31:0] espejo [0:15];
  string vector_path;
  integer fd, tick = 0, ciclos = 0, ciclo_rx = 0, latencia = 0, peor = 0;
  integer llegadas = 0, lecturas = 0, sumas = 0, revisiones = 0, escrituras = 0, status_visibles = 0;
  integer status_prev = 0;
  reg [31:0] cuenta_decision;
  reg [7:0] recibido, escrito;
  reg [11:0] suma_decision;
  reg listo_decision;

  always @(posedge dut.clk_soc) begin
    ciclos++;
    if (dut.rst_ni) begin
      if (dut.u_soc.u_core.rf_we && dut.u_soc.u_core.rf_waddr != 0)
        espejo[dut.u_soc.u_core.rf_waddr] = dut.u_soc.u_core.rf_wdata;
      if (dut.byte_done) begin
        if (llegadas != tick || dut.precio_spi !== precios[tick] || dut.u_soc.u_spi.new_price_q !== 0)
          $fatal(1, "RX invalido, duplicado o sobrescrito tick %0d", tick);
        ciclo_rx = ciclos;
        llegadas++;
      end
      if (dut.u_soc.dbg_status_read && dut.u_soc.u_spi.new_price_q)
        status_visibles++;
      if (dut.lee_price) lecturas++;
      if (dut.lee_sum) sumas++;
      if (dut.lee_ready) revisiones++;
      if (dut.escribe_decision) begin
        if (escrituras != tick || llegadas != tick+1 || lecturas != tick+1
            || sumas != tick+1 || revisiones != tick+1 || status_visibles == status_prev
            || dut.u_soc.u_spi.new_price_q !== 0
            || dut.bus_escritura[7:0] !== esperado_decision[tick]
            || espejo[3] !== {24'b0, precios[tick]})
          $fatal(1, "Invariante CPU/MMIO/DECISION tick %0d", tick);
        status_prev = status_visibles;
        escrito = dut.bus_escritura[7:0];
        suma_decision = dut.u_soc.sma_sum;
        listo_decision = dut.u_soc.sma_ready;
        cuenta_decision = espejo[6];
        latencia = ciclos-ciclo_rx;
        if (latencia > peor) peor = latencia;
        escrituras++;
      end
    end
  end

  initial begin
    foreach (espejo[r]) espejo[r] = 0;
    if (!$value$plusargs("vectores=%s", vector_path)) $fatal(1, "Falta ruta de vectores");
    $readmemh({vector_path,"/precios.hex"}, precios);
    $readmemh({vector_path,"/miso.hex"}, esperado_miso);
    $readmemh({vector_path,"/escrituras.hex"}, esperado_decision);
    fd = $fopen({vector_path,"/rtl.csv"}, "w");
    if (fd == 0) $fatal(1, "No se pudo abrir la traza");
    $fdisplay(fd, "tick,precio,suma10,ready,x3,x5,x6,x15,decision_mmio,miso,latencia_ciclos");
    #120113;
    if (leds !== 4'b0001) $fatal(1, "Arranque invalido LED=%b", leds);

    for (tick = 0; tick < TICKS; tick++) begin
      if ($isunknown({precios[tick], esperado_decision[tick], esperado_miso[tick]}))
        $fatal(1, "Vector incompleto tick %0d", tick);
      cs_n = 0;
      #1000;
      for (integer b = 7; b >= 0; b--) begin
        mosi = precios[tick][b];
        #500 sclk = 1;
        recibido[b] = miso;
        #500 sclk = 0;
      end
      #500 cs_n = 1;
      if (recibido !== esperado_miso[tick])
        $fatal(1, "MISO tick %0d observado %02h esperado %02h", tick, recibido, esperado_miso[tick]);
      #(PERIODO_NS-9500);
      if (escrituras != tick+1 || dut.u_soc.u_spi.tx_hold !== escrito
          || peor >= (PERIODO_NS-9500)/80)
        $fatal(1, "Deadline, MMIO o conteo invalido tick %0d", tick);
      $fdisplay(fd, "%0d,%0d,%0d,%0d,%0d,%0d,%0d,%0d,%02h,%02h,%0d",
                tick, precios[tick], suma_decision, listo_decision, espejo[3], espejo[5],
                cuenta_decision, espejo[15], escrito, recibido, latencia);
    end
    $fclose(fd);
    $display("PASS %0d ticks, STATUS=%0d PRICE=%0d SUM10=%0d READY=%0d DECISION=%0d; peor=%0d ciclos",
             TICKS, status_visibles, lecturas, sumas, revisiones, escrituras, peor);
    $finish;
  end
endmodule
