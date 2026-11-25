`timescale 1ns/1ps
module tb_trade_spi_externo;
  parameter integer TICKS = 2000, FASE_NS = 0, PERIODO_NS = 100000;
  parameter integer PALABRAS_FIRMWARE = 71;
  parameter ARCHIVO_FIRMWARE = "proyecto4/alternativas/mmio_sma10/sw/trade.hex";
  localparam integer PRESUPUESTO_CICLOS = (PERIODO_NS - 9500) / 80;
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
  reg [7:0] precio [0:TICKS-1], esperado_miso [0:TICKS-1], esperado_decision [0:TICKS-1];
  string vectores;
  integer tick = 0;
  reg [7:0] recibido;
  bit hubo_decision_no_nula = 0;

`ifndef NETLIST
  integer llegadas = 0, lecturas = 0, sumas = 0, ready = 0, escrituras = 0;
  integer ciclo = 0, llegada = 0, peor_caso = 0;
  always @(posedge dut.clk_soc) begin
    ciclo++;
    if (dut.rst_ni) begin
      if (dut.byte_done) begin
        if (llegadas != tick || dut.precio_spi !== precio[tick]) $fatal(1, "Precio SPI incorrecto tick %0d", tick);
        llegadas++;
        llegada = ciclo;
      end
      if (dut.lee_price) lecturas++;
      if (dut.lee_sum) sumas++;
      if (dut.lee_ready) ready++;
      if (dut.escribe_decision) begin
        if (escrituras != tick || llegadas != tick+1 || lecturas != tick+1
            || sumas != tick+1 || ready != tick+1
            || dut.bus_escritura[7:0] !== esperado_decision[tick])
          $fatal(1, "DECISION fuera de orden o distinta de Python tick %0d", tick);
        escrituras++;
        if (ciclo-llegada > peor_caso) peor_caso = ciclo-llegada;
      end
    end
  end
`endif

  initial begin
    if (!$value$plusargs("vectores=%s", vectores)) $fatal(1, "Se requiere la ruta de vectores");
    $readmemh({vectores,"/precios.hex"}, precio, 0, TICKS-1);
    $readmemh({vectores,"/miso.hex"}, esperado_miso, 0, TICKS-1);
    $readmemh({vectores,"/escrituras.hex"}, esperado_decision, 0, TICKS-1);
    #(120113 + FASE_NS);
    if (leds !== 4'b0001) $fatal(1, "El core no arranco: LED=%b", leds);
    for (tick = 0; tick < TICKS; tick++) begin
      if ($isunknown({precio[tick], esperado_miso[tick], esperado_decision[tick]}))
        $fatal(1, "Vectores incompletos en tick %0d", tick);
      hubo_decision_no_nula |= (esperado_decision[tick] != 0);
      cs_n = 0;
      #1000;
      for (integer b = 7; b >= 0; b--) begin
        mosi = precio[tick][b];
        #500 sclk = 1;
        recibido[b] = miso;
        #500 sclk = 0;
      end
      #500 cs_n = 1;
      if (recibido !== esperado_miso[tick])
        $fatal(1, "MISO tick %0d observado %02h esperado %02h", tick, recibido, esperado_miso[tick]);
      #(PERIODO_NS - 9500);
`ifndef NETLIST
      if (llegadas != tick+1 || escrituras != tick+1 || peor_caso >= PRESUPUESTO_CICLOS)
        $fatal(1, "Tick %0d incompleto o fuera de presupuesto", tick);
`endif
    end
    if (leds !== {hubo_decision_no_nula, 3'b111}) $fatal(1, "Hitos inesperados en LED=%b", leds);
`ifndef NETLIST
    $display("PASS %0d PRICE, SUM10, READY y DECISION; peor caso %0d/%0d ciclos", TICKS, peor_caso, PRESUPUESTO_CICLOS);
`endif
    $display("PASS %0d MISO frente a Python, fase %0d ns, LED=%b", TICKS, FASE_NS, leds);
    $finish;
  end
endmodule
