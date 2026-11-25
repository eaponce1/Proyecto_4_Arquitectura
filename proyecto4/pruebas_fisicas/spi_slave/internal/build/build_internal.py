"""Construye el modo interno de la prueba SPI; nunca programa la placa."""
from pathlib import Path
import re,shutil,subprocess
ROOT=Path(__file__).resolve().parents[5]
HERE=Path(__file__).resolve().parents[1]
OUT=HERE/"build"
PCF=HERE/"goboard_spi_internal.pcf"
SOURCES=[HERE/"rtl"/"spi_test_master.v",HERE/"rtl"/"spi_register_checker.v",HERE/"rtl"/"spi_physical_internal_top.v",ROOT/"proyecto4"/"alternativas"/"mmio_sma10"/"rtl"/"pochoco_spi_slave.v"]
for tool in ("yosys","nextpnr-ice40","icepack"):
    if not shutil.which(tool): raise SystemExit(f"Falta {tool} en PATH")
# Check complete, unique top-level pin assignment and reserved probe pins.
expected={"i_Clk","o_LED[0]","o_LED[1]","o_LED[2]","o_LED[3]","o_MON_SCLK","o_MON_MOSI","o_MON_CS_n","o_MON_MISO"}
constraints=PCF.read_text(encoding="utf-8")
pins={m.group(1):m.group(2) for m in re.finditer(r"^\s*set_io\s+(\S+)\s+(\d+)\s*$",constraints,re.M)}
assert set(pins)==expected, f"PCF mismatch: missing={expected-set(pins)}, extra={set(pins)-expected}"
assert len(set(pins.values()))==len(pins),"duplicated FPGA package pin"
assert (pins["o_MON_SCLK"],pins["o_MON_MOSI"],pins["o_MON_CS_n"],pins["o_MON_MISO"]) == ("78","79","80","81")
# Guard that the chosen slave source is the MMIO-base SPI slave.
slave=ROOT/"proyecto4"/"alternativas"/"mmio_sma10"/"rtl"/"pochoco_spi_slave.v"
assert slave.is_file()
OUT.mkdir(parents=True,exist_ok=True)
json=OUT/"spi_slave_internal.json"; asc=OUT/"spi_slave_internal.asc"; bit=OUT/"spi_slave_internal.bin"; report=OUT/"timing_report.json"
read=" ".join(x.relative_to(ROOT).as_posix() for x in SOURCES)
y=subprocess.run([shutil.which("yosys"),"-p",f"read_verilog {read}; synth_ice40 -top spi_physical_internal_top -json {json.relative_to(ROOT).as_posix()}"],cwd=ROOT,text=True,capture_output=True)
(OUT/"yosys.log").write_text(y.stdout+y.stderr,encoding="utf-8")
if y.returncode: raise SystemExit(f"Yosys failed; see {OUT/'yosys.log'}")
p=subprocess.run([shutil.which("nextpnr-ice40"),"--seed","1","--freq","25","--hx1k","--package","vq100","--json",json.relative_to(ROOT).as_posix(),"--pcf",PCF.relative_to(ROOT).as_posix(),"--asc",asc.relative_to(ROOT).as_posix(),"--report",report.relative_to(ROOT).as_posix()],cwd=ROOT,text=True,capture_output=True)
(OUT/"nextpnr.log").write_text(p.stdout+p.stderr,encoding="utf-8")
if p.returncode: raise SystemExit(f"nextpnr failed; see {OUT/'nextpnr.log'}")
i=subprocess.run([shutil.which("icepack"),asc.relative_to(ROOT).as_posix(),bit.relative_to(ROOT).as_posix()],cwd=ROOT,text=True,capture_output=True)
(OUT/"icepack.log").write_text(i.stdout+i.stderr,encoding="utf-8")
if i.returncode: raise SystemExit(f"icepack failed; see {OUT/'icepack.log'}")
ylog=y.stdout+y.stderr; plog=p.stdout+p.stderr
luts=re.findall(r"^\s*(\d+)\s+SB_LUT4\s*$",ylog,re.M)
lcs=re.findall(r"ICESTORM_LC:\s*(\d+)\s*/\s*1280",plog)
rams=re.findall(r"ICESTORM_RAM:\s*(\d+)\s*/\s*16",plog)
freqs=re.findall(r"Max frequency for clock.*?:\s*([0-9.]+) MHz \(PASS at 25.00 MHz\)",plog,re.S)
if not (luts and lcs and rams and freqs): raise SystemExit("could not parse physical metrics")
print(f"Yosys PASS; nextpnr HX1K/VQ100 PASS @25MHz; LUT4={luts[-1]}, LC={lcs[-1]}/1280, BRAM={rams[-1]}/16, Fmax={freqs[-1]}MHz")
print(f"icepack PASS: {bit} ({bit.stat().st_size} bytes); not programmed")

