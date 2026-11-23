# Alternativa custom-0: `smaupd`

Opcode `custom-0` (`0x0B`), `funct3=0`, `funct7=0`. El formato R usa
`smaupd rd, rs1, rs2` con semántica `rd <- rd - rs1 + rs2` módulo 2^32.
`rd` se lee mediante un tercer puerto síncrono de registros y luego recibe el
resultado; `rs1` es el precio saliente y `rs2` el precio entrante. La ALU añade
la operación 5'd16. El decoder rechaza otros funct3/funct7 y registros por
encima de x15. El assembler de Proyecto 4 conoce la mnemónica sin alterar el
assembler original del Proyecto 2.

En `trade.s`, al llenar el anillo se suma SMA10 una sola vez. Después cada tick
actualiza la suma con `smaupd` y mantiene las mismas comparaciones y decisiones
que la versión software. La sección de cartera y el desfase SPI no cambian.

## Verificación y limitación de placa

```powershell
python proyecto4/sw/assembler.py proyecto4/alternativas/custom0/sw/trade.s -o proyecto4/alternativas/custom0/sw/trade.hex
python proyecto4/alternativas/custom0/medir_custom0.py --ticks 20000
```

`tb/tb_custom0_unit.sv` verifica decodificación, aritmética y codificación
ilegal. La corrida de SoC compara cada MISO con Python y cuenta ticks/lecturas.
La versión sintetiza en Yosys, pero el place-and-route HX1K observado excede
la capacidad: 1350/1280 LCs, 14/16 BRAM; no se obtiene Fmax de placa. Por eso
esta implementación no se considera apta para programar la Go Board.
