"""Build reproducible del Proyecto 4 sobre Go Board HX1K, sin programar la placa."""
from pathlib import Path
import hashlib, re, shutil, subprocess, sys
ROOT=Path(__file__).resolve().parents[3]
OUT=Path(__file__).resolve().parent/"build"/"competition"
VAR=ROOT/"proyecto4"/"alternativas"/"mmio_sma10"
RTL=VAR/"rtl"
TOP=VAR/"trade_top.v"
PCF=ROOT/"goboard.pcf"
HEX=VAR/"sw"/"trade.hex"

# Guard checks: abort before synthesis if the selected base/top/image/pin map differs.
top_text=TOP.read_text(encoding="utf-8")
soc_text=(RTL/"pochoco_soc.v").read_text(encoding="utf-8")
ram_text=(RTL/"pochoco_ram.v").read_text(encoding="utf-8")
spi_text=(RTL/"pochoco_spi_slave.v").read_text(encoding="utf-8")
sma_text=(RTL/"pochoco_sma10.v").read_text(encoding="utf-8")
pcf_text=PCF.read_text(encoding="utf-8")
assert re.search(r"\.EnableSpi\s*\(\s*1\s*\)",top_text), "EnableSpi no está habilitado"
assert 'MemFile("proyecto4/alternativas/mmio_sma10/sw/trade.hex")' in top_text, "El top no carga el trade.hex de MMIO base"
assert "$readmemh(MemFile, mem)" in ram_text, "La RAM no carga MemFile"
assert "pochoco_sma10 u_sma10" in soc_text and ".sum_o(sma_sum)" in soc_text and ".sma_sum_i(sma_sum)" in soc_text, "SMA10 no está cableado al SoC/SPI"
assert "price_valid_i(EnableSpi ? sma_price_valid : 1'b0)" in soc_text, "El evento de precio no está habilitado por EnableSpi"
assert "6'd3:       rdata_o <= {20'b0, sma_sum_i};" in spi_text and "6'd4:       rdata_o <= {31'b0, sma_ready_i};" in spi_text, "Mapa MMIO SUM10/READY inesperado"
assert "SB_RAM40_4K" in sma_text, "No es el periférico SMA10 base"
expected={"i_Clk","o_LED[0]","o_LED[1]","o_LED[2]","o_LED[3]","i_Switch[0]","i_Switch[1]","i_Switch[2]","i_Switch[3]","o_Segment1_A","o_Segment1_B","o_Segment1_C","o_Segment1_D","o_Segment1_E","o_Segment1_F","o_Segment1_G","o_Segment2_A","o_Segment2_B","o_Segment2_C","o_Segment2_D","o_Segment2_E","o_Segment2_F","o_Segment2_G","i_SPI_SCLK","i_SPI_MOSI","i_SPI_CS_n","o_SPI_MISO"}
pins={m.group(1):m.group(2) for m in re.finditer(r"^\s*set_io\s+(\S+)\s+(\d+)\s*$",pcf_text,re.M)}
assert set(pins)==expected, f"Señales PCF diferentes; faltan={expected-set(pins)}, extras={set(pins)-expected}"
assert len(set(pins.values()))==len(pins), "Hay pines físicos duplicados"
assert pins["i_Clk"]=="15", "Pin de clock distinto al del PCF revisado"
assert {pins[x] for x in ("i_SPI_SCLK","i_SPI_MOSI","o_SPI_MISO","i_SPI_CS_n")}=={"62","64","63","65"}, "Pines SPI inesperados"
assert HEX.is_file() and HEX.stat().st_size>0, "Falta trade.hex"
words=[s.strip() for s in HEX.read_text(encoding="ascii").splitlines() if s.strip()]
assert all(re.fullmatch(r"[0-9a-fA-F]{8}",w) for w in words), "trade.hex contiene una palabra malformada"
for tool in ("yosys","nextpnr-ice40","icepack"):
    if not shutil.which(tool): raise SystemExit(f"Falta {tool} en PATH")

OUT.mkdir(parents=True,exist_ok=True)
json=OUT/"competition.json"; asc=OUT/"competition.asc"; binfile=OUT/"competition.bin"
binfile.unlink(missing_ok=True)
report=OUT/"competition_timing.json"
sources=sorted(p.relative_to(ROOT).as_posix() for p in RTL.rglob("*.v"))+[TOP.relative_to(ROOT).as_posix()]
ycmd=[shutil.which("yosys"),"-p",f'read_verilog {" ".join(sources)}; synth_ice40 -top trade_top -json {json.relative_to(ROOT).as_posix()}']
y=subprocess.run(ycmd,cwd=ROOT,text=True,capture_output=True)
(OUT/"yosys.log").write_text(y.stdout+y.stderr,encoding="utf-8")
if y.returncode: raise SystemExit(f"Yosys falló ({y.returncode}); revisar {OUT/'yosys.log'}")
print(f"Yosys PASS; trade.hex: {len(words)} palabras; EnableSpi=1; top trade_top")
pcmd=[shutil.which("nextpnr-ice40"),"--seed","1","--freq","25","--hx1k","--package","vq100","--json",json.relative_to(ROOT).as_posix(),"--pcf",PCF.relative_to(ROOT).as_posix(),"--asc",asc.relative_to(ROOT).as_posix(),"--report",report.relative_to(ROOT).as_posix()]
p=subprocess.run(pcmd,cwd=ROOT,text=True,capture_output=True)
(OUT/"nextpnr.log").write_text(p.stdout+p.stderr,encoding="utf-8")
if p.returncode: raise SystemExit(f"nextpnr falló ({p.returncode}); no se empaqueta binario; revisar {OUT/'nextpnr.log'}")
pack=subprocess.run([shutil.which("icepack"),asc.relative_to(ROOT).as_posix(),binfile.relative_to(ROOT).as_posix()],cwd=ROOT,text=True,capture_output=True)
(OUT/"icepack.log").write_text(pack.stdout+pack.stderr,encoding="utf-8")
if pack.returncode: binfile.unlink(missing_ok=True); raise SystemExit(f"icepack falló ({pack.returncode}); revisar {OUT/'icepack.log'}")
log=p.stdout+p.stderr
lcs=re.findall(r"ICESTORM_LC:\s*(\d+)\s*/\s*1280",log)
rams=re.findall(r"ICESTORM_RAM:\s*(\d+)\s*/\s*16",log)
luts=re.findall(r"^\s*(\d+)\s+SB_LUT4\s*$",y.stdout+y.stderr,re.M)
freq=re.findall(r"Max frequency for clock.*?:\s*([0-9.]+) MHz \(PASS at 25.00 MHz\)",log,re.S)
if not (lcs and rams and luts and freq): raise SystemExit("No pude extraer métricas reales; artefactos generados, inspeccionar logs")
text=f'''# Preparación física Go Board: Proyecto 4 MMIO SMA10 base

## Configuración comprobada

- Top: `trade_top` de `proyecto4/alternativas/mmio_sma10/trade_top.v`.
- SoC: copia base del Proyecto 2 en `proyecto4/alternativas/mmio_sma10/rtl/`.
- Parámetro: `EnableSpi=1`.
- Imagen: `proyecto4/alternativas/mmio_sma10/sw/trade.hex`, {len(words)} palabras hexadecimales de 32 bits. `pochoco_ram` la carga con `$readmemh(MemFile, mem)`.
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
- LUT4: {luts[-1]}.
- Logic Cells: {lcs[-1]}/1280.
- BRAM: {rams[-1]}/16.
- Fmax post-route: {freq[-1]} MHz.
- Margen de frecuencia a 25 MHz: {float(freq[-1])-25:.2f} MHz.
- Binario: `{binfile.relative_to(ROOT).as_posix()}` ({binfile.stat().st_size} bytes).

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
'''
(OUT/"informe_programacion_fisica.md").write_text(text,encoding="utf-8")
print(f"nextpnr PASS; LUT4={luts[-1]}, LC={lcs[-1]}/1280, BRAM={rams[-1]}/16, Fmax={freq[-1]} MHz")
print(f"icepack PASS; {binfile} ({binfile.stat().st_size} bytes); la placa no fue programada")


print('SHA-256',hashlib.sha256(binfile.read_bytes()).hexdigest())

