# Prueba física independiente del SPI Slave Pochoco

Esta prueba es un fixture dedicado para `pochoco_spi_slave.v`, en un proyecto
separado. No modifica el SoC base, `proyecto4/alternativas/mmio_sma10/` ni la
versión optimizada. No incluye Espino: un controlador RTL de prueba realiza
las lecturas/escrituras del bus del SPI Slave, manteniendo el fixture pequeño
para HX1K.

## Transacciones verificadas

El maestro de prueba genera cinco bytes de precio, modo SPI compatible con el
slave, y verifica el byte MISO de cada transacción:

| Tick | Precio transmitido | MISO esperado (DECISION anterior) | Verificación del bus |
|---:|---:|---:|---|
| 1 | `0x35` | `0x00` inicial | STATUS.new_price=1, PRICE=`0x35`; escribir DECISION=`0x41` |
| 2 | `0x56` | `0x41` | STATUS y PRICE; escribir `0x42` |
| 3 | `0x2C` | `0x42` | STATUS y PRICE; escribir `0x43` |
| 4 | `0x7A` | `0x43` | STATUS y PRICE; escribir `0x44` |
| 5 | `0x12` | `0x44` | MISO confirma la decisión escrita en el tick 4 |

El MISO de tick n debe igualar la decisión escrita después de recibir el precio
del tick n−1. Un error de lectura STATUS/PRICE escribe el centinela `0x7F`, que
hace fallar la comparación MISO siguiente. La primera transacción espera MISO
cero tras reset.

Offsets usados en la interfaz MMIO del SPI Slave: STATUS byte 0, PRICE byte 4,
DECISION byte 8. El controlador verifica `new_price_q` y el precio leído antes
de escribir DECISION. Se comprueban cuatro pares STATUS/PRICE y cinco
respuestas MISO.

## Jumpers para prueba física de pads

La placa debe ejecutar el bitstream de este fixture. Conectar los jumpers así:

| Salida del maestro de prueba | Entrada del SPI Slave | Acción |
|---|---|---|
| PMOD PS7, pin FPGA 78 | PMOD PS4, pin FPGA 62 | SCLK |
| PMOD PS8, pin FPGA 79 | PMOD PS2, pin FPGA 64 | MOSI |
| PMOD PS9, pin FPGA 80 | PMOD PS1, pin FPGA 65 | CS_n |
| PMOD PS3, pin FPGA 63 | PMOD PS10, pin FPGA 81 | retorno MISO al maestro |

PS1–PS4 corresponden a las señales del slave; PS7–PS10 están libres en el PCF
de la placa. La asignación coincide con `goboard.pcf` y el esquema de Go Board.
Usar GND común y niveles lógicos de 3,3 V. No conectar el riel de alimentación
como señal. Si se omiten jumpers, el fixture debe indicar FAIL o no completar
las validaciones.

## LEDs

- LED0: PASS; sólo se enciende cuando las comprobaciones del bus y todas las
  respuestas MISO pasaron.
- LED1: FAIL; fallo de precio/STATUS/MISO.
- LED2: maestro enviando la secuencia.
- LED3: maestro terminó las cinco transacciones.

## Alcance

Esta prueba valida físicamente el SPI Slave, sus registros STATUS/PRICE/DECISION
y la respuesta MISO con desfase, incluyendo la ruta de pads mediante jumpers.
No valida la ejecución de Espino ni el cableado `EnableSpi` dentro del SoC,
porque se aísla el slave para no exceder la capacidad LC de la placa. El RTL de
integración y `EnableSpi=1` se revisaron por separado; no se alteran aquí.


## Auditor?a de la placa y del RTL

- El PCF original asigna reloj a paquete 15, LEDs a 56/57/59/60 y SPI del slave a 62/63/64/65. Las nuevas se?ales se asignan s?lo a los pines no usados 78?81 (PMOD PS7?PS10); el PCF independiente verifica que no haya pines repetidos ni puertos top sin constraint.
- Seg?n el esquema Go Board, PS1?PS4 est?n conectados a pines FPGA 65/64/63/62; PS7?PS10 a 78/79/80/81. PS5/PS11 son riel +3,3 V y PS6/PS12 GND. La placa se alimenta por USB; no se debe aplicar 5 V a las se?ales SPI. El clock onboard es 25 MHz.
- `pochoco_spi_slave.v` sincroniza SCLK/MOSI/CS, recibe el byte al completar 8 flancos, deja PRICE/STATUS accesibles en offsets 1/0 y carga DECISION en el transmisor. Al pr?ximo CS activo, `tx_hold` carga `tx_shift`; as? MISO devuelve la decisi?n anterior.
- La integraci?n base del SoC tiene `EnableSpi=1`, conecta `price_valid/price` al SMA10 y el esclavo a la ventana SPI. Esta prueba, deliberadamente peque?a, instanc?a el mismo slave directamente y controla su bus MMIO sin Espino. Por tanto verifica el bloque f?sico y el contrato de registros, no ejecuta el software del SoC ni prueba el cableado del SoC de extremo a extremo.
- El top test no tiene entrada de reset; mantiene reset interno durante 16 ciclos. LEDs: LED0 PASS, LED1 FAIL, LED2 transacci?n en curso, LED3 secuencia terminada.

## Resultados ejecutados en herramientas

- Icarus Verilog loopback digital: PASS; cuatro STATUS/PRICE esperados y cinco bytes MISO correctos (`00, 41, 42, 43, 44`).
- Yosys: PASS.
- nextpnr-ice40, HX1K/VQ100, objetivo 25 MHz: PASS; 158 LUT4, 217/1280 LC, 0/16 BRAM, Fmax post-route 143,20 MHz.
- icepack: PASS; `build/spi_physical_test.bin`, 32.220 bytes.
- La prueba f?sica a?n no se ha ejecutado: requiere cargar este bitstream y conectar los cuatro jumpers. La Go Board permanece con la imagen MMIO SMA10 base.

## Comandos

Desde la ra?z `pochoco_soc-main`:

```powershell
iverilog -g2012 -s tb_spi_physical_test -o proyecto4/pruebas_fisicas/spi_slave/build/tb_spi_physical_test.vvp proyecto4/pruebas_fisicas/spi_slave/rtl/spi_test_master.v proyecto4/pruebas_fisicas/spi_slave/rtl/spi_register_checker.v proyecto4/pruebas_fisicas/spi_slave/rtl/spi_physical_test_top.v proyecto4/alternativas/mmio_sma10/rtl/pochoco_spi_slave.v proyecto4/pruebas_fisicas/spi_slave/tb/tb_spi_physical_test.sv
vvp proyecto4/pruebas_fisicas/spi_slave/build/tb_spi_physical_test.vvp
python proyecto4/pruebas_fisicas/spi_slave/build/build_spi_test.py
```

Para programar manualmente el fixture (no ejecutado):

```powershell
iceprog proyecto4/pruebas_fisicas/spi_slave/build/spi_physical_test.bin
```

Al programarlo, la configuraci?n de flash de la placa cambiar? temporalmente del SoC MMIO SMA10 base a este fixture. Los fuentes, `.hex` y artefactos base quedan intactos; para volver a la aplicaci?n base se debe programar su bitstream guardado.
