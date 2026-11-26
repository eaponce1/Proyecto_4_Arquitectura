`timescale 1ns/1ps
// Mismo SPI modo 0 a 1 MHz, con CS previo al primer SCLK por pocas decenas de ns.
// El banco anterior esperaba 1 us y no ejercitaba esta coincidencia de sincronizadores.
module tb_spi_margen;
  parameter integer SETUP_NS=20, FASE_NS=0, TICKS=396, PERIODO_NS=40000;
  parameter ARCHIVO_FIRMWARE="sw/trade.hex";
  reg clk=0,sclk=0,mosi=0,cs_n=1;
  wire miso;
  wire [3:0] leds;
  always #20 clk=~clk;
`ifdef NETLIST
  trade_spi_externo dut(
`else
  trade_spi_externo #(.PALABRAS_FIRMWARE(130),.ARCHIVO_FIRMWARE(ARCHIVO_FIRMWARE)) dut(
`endif
    .i_Clk(clk),.i_SPI_SCLK(sclk),.i_SPI_MOSI(mosi),.i_SPI_CS_n(cs_n),.o_SPI_MISO(miso),.o_LED(leds));
  reg [7:0] prices[0:TICKS-1],expected[0:TICKS-1],decisions[0:TICKS-1];
  string vectors;
  integer mismatches=0,writes=0,received=0,tick=0;
  integer setup_actual=SETUP_NS;
  reg [7:0] value;
`ifndef NETLIST
  always @(posedge dut.clk_soc) begin
    if(dut.byte_done) begin
      if(received>=TICKS) $fatal(1,"Precio duplicado");
      if(dut.precio_spi!==prices[received]) $fatal(1,"Precio incorrecto tick=%0d",received);
      received++;
    end
    if(dut.escribe_decision) begin
      if(writes>=TICKS) $fatal(1,"Decision duplicada");
      if(dut.bus_escritura[7:0]!==decisions[writes]) $fatal(1,"Decision incorrecta tick=%0d",writes);
      writes++;
    end
  end
`endif
  initial begin
    if($value$plusargs("setup_ns=%d",setup_actual)) begin end
    if(!$value$plusargs("vectores=%s",vectors)) $fatal(1,"Falta +vectores");
    $readmemh({vectors,"/precios.hex"},prices);
    $readmemh({vectors,"/miso.hex"},expected);
    $readmemh({vectors,"/escrituras.hex"},decisions);
    #(120113+FASE_NS);
    for(tick=0;tick<TICKS;tick++) begin
      mosi=prices[tick][7];cs_n=0;
      #(setup_actual);
      for(integer b=7;b>=0;b--) begin
        sclk=1;
        value[b]=miso;
        #500;sclk=0;
        if(b>0) mosi=prices[tick][b-1];
        #500;
      end
      #500;cs_n=1;
      if(value[7:6]==2'b01 || value[7:6]==2'b10)
        $display("ORDEN tick=%0d MISO=%02h tipo=%0d cantidad=%0d",tick,value,value[7:6],value[5:0]);
      if(value!==expected[tick]) begin
        mismatches++;
        if(mismatches<=5)$display("MISO tick=%0d observado=%02h esperado=%02h",tick,value,expected[tick]);
      end
      #(PERIODO_NS-8500-setup_actual);
    end
`ifdef NETLIST
    $display("RESUMEN setup_ns=%0d fase_ns=%0d transferencias=%0d diferencias=%0d LED=%b (verificacion externa)",setup_actual,FASE_NS,TICKS,mismatches,leds);
`else
    $display("RESUMEN setup_ns=%0d fase_ns=%0d precios=%0d escrituras=%0d diferencias=%0d LED=%b",setup_actual,FASE_NS,received,writes,mismatches,leds);
`endif
`ifndef NETLIST
    if(received!=TICKS||writes!=TICKS)$fatal(1,"Precios o escrituras ausentes/duplicados");
`endif
    if(mismatches!=0)$fatal(1,"Fallo SPI con CS corto");
    if(leds!==4'b1111)$fatal(1,"No se observaron todos los hitos LED: %b",leds);
    $display("PASS SPI CS corto %0d ticks; compra y venta MISO exactas",TICKS);
    $finish;
  end
endmodule
