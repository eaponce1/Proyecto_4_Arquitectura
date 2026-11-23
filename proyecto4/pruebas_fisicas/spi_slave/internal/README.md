# Modo interno de la prueba SPI física

Esta variante vive en `proyecto4/pruebas_fisicas/spi_slave/internal/`. El
maestro y `pochoco_spi_slave` se conectan directamente por nets RTL internos:
SCLK, MOSI, CS_n y MISO. No utiliza los puertos externos SPI ni necesita
jumpers.

## Secuencia verificada

Mantiene los cinco precios y decisiones de la prueba loopback:

| Tick | Precio | MISO esperado (decisión previa) | Bus del slave |
|---:|---:|---:|---|
| 1 | `0x35` | `0x00` | STATUS.new_price=1; PRICE=`0x35`; escribe DECISION=`0x41` |
| 2 | `0x56` | `0x41` | STATUS/PRICE; escribe DECISION=`0x42` |
| 3 | `0x2C` | `0x42` | STATUS/PRICE; escribe DECISION=`0x43` |
| 4 | `0x7A` | `0x43` | STATUS/PRICE; escribe DECISION=`0x44` |
| 5 | `0x12` | `0x44` | Verifica DECISION del tick 4 |

El checker hace lecturas STATUS y PRICE antes de escribir DECISION. El maestro
verifica MISO con el desfase de un tick. La prueba HDL cuenta cinco aserciones y
cinco liberaciones de CS_n, además de comprobar el resultado PASS/FAIL.

## Indicadores en la placa

- **PASS:** LED0 encendido, LED1 apagado, LED2 apagado, LED3 encendido.
- **FAIL:** LED1 encendido y LED0 apagado. LED3 indica que el maestro terminó;
  LED2 encendido indica que está ejecutando la secuencia.
- Un resultado incompleto no se considera PASS.

Las salidas sonda opcionales se llevan a PMOD PS7–PS10 (pines FPGA 78–81):
SCLK, MOSI, CS_n y MISO. Sirven para observar con analizador lógico, pero no
participan en el protocolo interno ni requieren conectar jumpers. PS1–PS4 no
se usan en este build.

## Comandos reproducibles

Desde `pochoco_soc-main`:

```powershell
iverilog -g2012 -s tb_spi_physical_internal -o proyecto4/pruebas_fisicas/spi_slave/internal/build/tb_spi_physical_internal.vvp proyecto4/pruebas_fisicas/spi_slave/internal/rtl/spi_test_master.v proyecto4/pruebas_fisicas/spi_slave/internal/rtl/spi_register_checker.v proyecto4/pruebas_fisicas/spi_slave/internal/rtl/spi_physical_internal_top.v proyecto4/alternativas/mmio_sma10/rtl/pochoco_spi_slave.v proyecto4/pruebas_fisicas/spi_slave/internal/tb/tb_spi_physical_internal.sv
vvp proyecto4/pruebas_fisicas/spi_slave/internal/build/tb_spi_physical_internal.vvp
python proyecto4/pruebas_fisicas/spi_slave/internal/build/build_internal.py
```

El script de build valida que todos los puertos top tengan pines únicos, ejecuta
Yosys, nextpnr para HX1K/VQ100 a 25 MHz e icepack. Genera `build/spi_slave_internal.bin`,
independiente del binario de loopback externo y del bitstream MMIO SMA10 base.
No programa la Go Board.



## Validacion ejecutada

- Testbench Icarus: **PASS**; cinco tramas CS completas, cuatro lecturas STATUS/PRICE correctas, cuatro escrituras DECISION y cinco comparaciones MISO del desfase. LED final `1001` (PASS y DONE).
- Yosys: **PASS**.
- nextpnr HX1K/VQ100 a 25 MHz: **PASS**; 161 LUT4, 220/1280 LC, 0/16 BRAM, Fmax post-route 146,43 MHz.
- icepack: **PASS**; binario independiente de 32.220 bytes.
- No se programo la Go Board; el binario MMIO base no se sobrescribio.

El comando para ejecutar la simulacion y el build esta arriba. El binario queda en `build/spi_slave_internal.bin`; se distingue del build anterior, que usa `build/spi_physical_test.bin`.
