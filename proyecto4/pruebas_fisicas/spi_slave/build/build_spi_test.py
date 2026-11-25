"""Construye fixture SPI separado para Go Board; no programa el hardware."""
from pathlib import Path
import re,shutil,subprocess
ROOT=Path(__file__).resolve().parents[4]
HERE=Path(__file__).resolve().parents[1]
OUT=HERE/"build"
PCF=HERE/"goboard_spi_test.pcf"
SOURCES=[HERE/"rtl"/"spi_test_master.v",HERE/"rtl"/"spi_register_checker.v",HERE/"rtl"/"spi_physical_test_top.v",ROOT/"proyecto4"/"alternativas"/"mmio_sma10"/"rtl"/"pochoco_spi_slave.v"]
for tool in ("yosys","nextpnr-ice40","icepack"):
    if not shutil.which(tool): raise SystemExit(f"Falta {tool} en PATH")
# Ensure every top port has an explicit, unique board pin.
expected={"i_Clk","o_LED[0]","o_LED[1]","o_LED[2]","o_LED[3]","i_SPI_SCLK","i_SPI_MOSI","i_SPI_CS_n","o_SPI_MISO","o_TEST_SCLK","o_TEST_MOSI","o_TEST_CS_n","i_TEST_MISO"}
constraints=PCF.read_text(encoding="utf-8")
pins={m.group(1):m.group(2) for m in re.finditer(r"^\s*set_io\s+(\S+)\s+(\d+)\s*$",constraints,re.M)}
assert set(pins)==expected, f"PCF signals differ: missing {expected-set(pins)}, extra {set(pins)-expected}"
assert len(set(pins.values()))==len(pins),"duplicate package pin"
assert (pins["o_TEST_SCLK"],pins["o_TEST_MOSI"],pins["o_TEST_CS_n"],pins["i_TEST_MISO"]) == ("78","79","80","81")
OUT.mkdir(parents=True,exist_ok=True)
json=OUT/"spi_physical_test.json"; asc=OUT/"spi_physical_test.asc"; bit=OUT/"spi_physical_test.bin"; report=OUT/"timing_report.json"
read=" ".join(x.relative_to(ROOT).as_posix() for x in SOURCES)
y=subprocess.run([shutil.which("yosys"),"-p",f"read_verilog {read}; synth_ice40 -top spi_physical_test_top -json {json.relative_to(ROOT).as_posix()}"],cwd=ROOT,text=True,capture_output=True)
(OUT/"yosys.log").write_text(y.stdout+y.stderr,encoding="utf-8")
if y.returncode: raise SystemExit(f"Yosys failed: {OUT/'yosys.log'}")
p=subprocess.run([shutil.which("nextpnr-ice40"),"--seed","1","--freq","25","--hx1k","--package","vq100","--json",json.relative_to(ROOT).as_posix(),"--pcf",PCF.relative_to(ROOT).as_posix(),"--asc",asc.relative_to(ROOT).as_posix(),"--report",report.relative_to(ROOT).as_posix()],cwd=ROOT,text=True,capture_output=True)
(OUT/"nextpnr.log").write_text(p.stdout+p.stderr,encoding="utf-8")
if p.returncode: raise SystemExit(f"nextpnr failed: {OUT/'nextpnr.log'}")
i=subprocess.run([shutil.which("icepack"),asc.relative_to(ROOT).as_posix(),bit.relative_to(ROOT).as_posix()],cwd=ROOT,text=True,capture_output=True)
(OUT/"icepack.log").write_text(i.stdout+i.stderr,encoding="utf-8")
if i.returncode: raise SystemExit(f"icepack failed: {OUT/'icepack.log'}")
ylog=y.stdout+y.stderr; plog=p.stdout+p.stderr
luts=re.findall(r"^\s*(\d+)\s+SB_LUT4\s*$",ylog,re.M)
lcs=re.findall(r"ICESTORM_LC:\s*(\d+)\s*/\s*1280",plog)
rams=re.findall(r"ICESTORM_RAM:\s*(\d+)\s*/\s*16",plog)
freqs=re.findall(r"Max frequency for clock.*?:\s*([0-9.]+) MHz \(PASS at 25.00 MHz\)",plog,re.S)
if not (luts and lcs and rams and freqs): raise SystemExit("could not parse P&R metrics")
print(f"Yosys PASS; nextpnr HX1K/VQ100 PASS 25MHz; LUT4={luts[-1]}, LC={lcs[-1]}/1280, BRAM={rams[-1]}/16, Fmax={freqs[-1]}MHz")
print(f"icepack PASS: {bit} ({bit.stat().st_size} bytes); not programmed")
