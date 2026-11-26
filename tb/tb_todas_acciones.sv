`timescale 1ns/1ps
// Usa el banco estricto existente: SPI real, MMIO, registros CPU y contabilidad.
module tb_todas_acciones;
  parameter integer TICKS = 20000, PERIODO_NS = 100000;
  tb_candidata #(
    .TICKS(TICKS), .PERIODO_NS(PERIODO_NS), .FASE_NS(0),
    .PALABRAS_FIRMWARE(130), .ARCHIVO_FIRMWARE("sw/trade.hex"),
    .REG_CAJA(15), .REG_ACCIONES(5)
  ) prueba();
endmodule
