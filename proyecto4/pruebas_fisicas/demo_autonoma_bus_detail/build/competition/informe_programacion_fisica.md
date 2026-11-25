# Preparación física Go Board: Proyecto 4 MMIO SMA10 base

## Configuración comprobada

- Top: `trade_top` de `proyecto4/alternativas/mmio_sma10/trade_top.v`.
- SoC: copia base del Proyecto 2 en `proyecto4/alternativas/mmio_sma10/rtl/`.
- Parámetro: `EnableSpi=1`.
- Imagen: `proyecto4/alternativas/mmio_sma10/sw/trade.hex`, 71 palabras hexadecimales de 32 bits. `pochoco_ram` la carga con `$readmemh(MemFile, mem)`.
- Periférico: `pochoco_sma10` cableado desde `price_valid/price` del SPI y devolviendo `SUM10/READY` al esclavo SPI/MMIO.
- Dispositivo P&R: iCE40 HX1K, encapsulado VQ100, PCF `goboard.pcf`, reloj objetivo 25 MHz.
- Fuente RTL usada: alternativa MMIO SMA10 **base**. No se usó `mmio_sma10_opt`.

El wrapper genérico `proyecto4/rtl/trade_top.v` apunta a `proyecto4/sw/trade.hex`; no se usó porque no apunta a la imagen de la alternativa MMIO seleccionada. Se usó el wrapper propio de `alternativas/mmio_sma10`, que sí apunta a la imagen adecuada.

## Pines del PCF

| Señal | Pin FPGA | Uso de placa |
|---|---:|---|
| `i_Clk` | 15 | Reloj onboard de 25 MHz |
| `i_SPI_SCLK` | 62 | PMOD PS4, reloj SPI |
| `i_SPI_MOSI` | 64 | PMOD PS2, datos maestro→placa |
| `o_SPI_MISO` | 63 | PMOD PS3, datos placa→maestro |
| `i_SPI_CS_n` | 65 | PMOD PS1, selección activa baja |

Los números son pines del paquete FPGA tomados del PCF local. El esquema oficial de la Go Board relaciona los pines de paquete 62/63/64/65 con PMOD PS4/PS3/PS2/PS1, respectivamente, y documenta rieles +3,3 V y GND en el PMOD. Conectar GND común y señales a niveles compatibles de 3,3 V; alimentación no es un GPIO ni se configura en PCF. [Esquema oficial de Go Board](https://nandland.com/goboard/images/Go_Board_V1.pdf).

No hay un pin de reset de usuario en este top. `pochoco_soc` genera POR internamente con un contador de 4 bits; los primeros 15 ciclos de reloj mantienen el SoC en reset. El pin de reset de configuración del FPGA no es una entrada del diseño.

## Síntesis y timing medidos

- Yosys: PASS.
- nextpnr: PASS @25 MHz, HX1K/VQ100, seed 1.
- LUT4: 1055.
- Logic Cells: 1279/1280.
- BRAM: 13/16.
- Fmax post-route: 40.50 MHz.
- Margen de frecuencia a 25 MHz: 15.50 MHz.
- Binario: `proyecto4/pruebas_fisicas/demo_autonoma_bus_detail/build/competition/competition.bin` (32220 bytes).

La ocupación es muy alta: queda poco margen de LC; no se agregaron funcionalidades. Este flujo es síntesis/P&R y empaquetado. No programa la placa.

## Comandos ejecutados para reproducir la construcción

```powershell
python proyecto4/programacion_fisica/generar_bitstream.py
```

Comandos de programación para ejecutar manualmente cuando se decida:

```powershell
iceprog proyecto4/programacion_fisica/competition.bin
```

**El comando `iceprog` no fue ejecutado.**
