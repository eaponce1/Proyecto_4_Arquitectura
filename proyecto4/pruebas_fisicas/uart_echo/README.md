# Prueba UART echo para Go Board

Proyecto independiente que recibe un byte por UART desde el FTDI de la Go Board y devuelve el mismo byte. Formato: **115200 baud, 8 data bits, sin paridad, 1 stop bit (8N1)**. El reloj de la Go Board es 25 MHz; el divisor elegido es 217 ciclos/bit (25 MHz / 115200 ≈ 217).

## Auditoría de pines

El PCF de la raíz, `goboard.pcf`, asigna el reloj a paquete 15, pero no asigna UART. El esquema de la Go Board muestra el FTDI conectado por las nets UART_RX/UART_TX (hoja 1) y los nets al iCE40 (hoja 4). Contrasté la numeración con el constraints file de referencia de Go Board de Nandland:

| Señal del top | Pin paquete VQ100 | Dirección eléctrica | Conexión USB/FTDI |
|---|---:|---|---|
| `i_UART_RX` | 73 | Entrada FPGA | FTDI TX hacia FPGA RX |
| `o_UART_TX` | 74 | Salida FPGA | FPGA TX hacia FTDI RX |
| `i_Clk` | 15 | Entrada FPGA | Oscilador integrado de 25 MHz |

La asignación UART coincide con el archivo de constraints Go Board (`i_UART_RX=73`, `o_UART_TX=74`). El PC se conecta por el USB de la placa: no requiere jumpers UART externos. La placa queda en 3,3 V TTL a través de su FTDI integrado; no conectar una interfaz RS-232 de voltaje bipolar.

```text
PC COM10 TX  -> FTDI UART_RX -> FPGA pin 73 (i_UART_RX)
PC COM10 RX  <- FTDI UART_TX <- FPGA pin 74 (o_UART_TX)
PC USB       <-> FTDI <-> Go Board
```

Fuentes consultadas: [esquema oficial Go Board V1](https://nandland.com/goboard/images/Go_Board_V1.pdf), [constraints de referencia Go Board de Nandland](https://github.com/billiegoose/nandland-tutorial-projects/blob/master/Go_Board_Constraints.pcf), [tutorial oficial UART RX de Nandland](https://nandland.com/project-7-uart-part-1-receive-data-from-computer/). El tutorial confirma el reloj de 25 MHz y el divisor 217.

## Archivos

- `rtl/uart_rx.v`: receptor 8N1 con sincronización y muestreo al centro del bit.
- `rtl/uart_tx.v`: transmisor 8N1, LSB primero.
- `rtl/uart_echo_top.v`: conecta el byte recibido al transmisor.
- `goboard_uart_echo.pcf`: constraints independientes para HX1K/VQ100.
- `tb/tb_uart_echo.sv`: prueba los bytes `41 42 43 55 AA`.
- `test_uart_echo.py`: valida esos cinco bytes con COM10.

## Simulación

Desde la raíz `pochoco_soc-main`:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File proyecto4/pruebas_fisicas/uart_echo/ejecutar_simulacion.ps1
```

Resultado medido en Icarus Verilog: `PASS UART echo: 5 bytes, 115200 8N1: 41 42 43 55 aa`.

## Síntesis y bitstream

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File proyecto4/pruebas_fisicas/uart_echo/sintetizar.ps1
```

El flujo genera archivos solo dentro de `proyecto4/pruebas_fisicas/uart_echo/build/`. `icepack` se ejecuta al final únicamente si Yosys y nextpnr pasan. El resultado independiente se llama `uart_echo.bin`; no reemplaza el bitstream MMIO SMA10.

Síntesis/place-and-route ya ejecutados: Yosys reporta 114 LUT4; nextpnr HX1K/VQ100 usa 146/1.280 LC y 0/16 BRAM, con frecuencia máxima post-route de 135,96 MHz frente a 25 MHz objetivo. `icepack` generó `build/uart_echo.bin` de 32.220 bytes. El PCF quedó aceptado y nextpnr ubicó `i_UART_RX` en pin 73 y `o_UART_TX` en pin 74. Los logs reproducibles están junto al binario.

## Prueba física manual

1. Sintetizar y revisar recursos/timing de `build/uart_echo.bin`.
2. Programar manualmente el bitstream, por ejemplo con `iceprog proyecto4/pruebas_fisicas/uart_echo/build/uart_echo.bin` (no ejecutar este comando desde el script).
3. Verificar que Windows ve `COM10` y que ningún terminal tiene el puerto abierto.
4. Instalar pyserial si falta: `python -m pip install pyserial`.
5. Ejecutar `python proyecto4/pruebas_fisicas/uart_echo/test_uart_echo.py`.

El script abre COM10 a 115200 8N1, envía un byte y espera el eco antes de enviar el siguiente. Dependencia Python detectada durante esta tarea: pyserial 3.5. Debe informar PASS para `41`, `42`, `43`, `55` y `AA`. Si hay timeout, revisar que este bitstream UART echo esté programado, que el puerto sea COM10 y que el monitor serie esté cerrado. La prueba por COM no se ejecutó aquí: hasta la programación manual, la placa conserva el bitstream MMIO SMA10 base.
