param([string]$Map)
$source=@(
 'rtl/demo_autonoma_bus_detail_top.v','rtl/demo_integral_monitor.v','rtl/timeout_pc_uart.v',
 'rtl/first_post_byte_pc_probe.v','rtl/pochoco_soc_cpu_trace.v',
 'rtl/price_spi_master_cpu_trace.v','rtl/espino_core_cpu_trace.v'
)
$p='proyecto4/pruebas_fisicas/demo_autonoma_bus_detail'
$files=@($source | ForEach-Object {"$p/$_"})
$files+=@('pochoco_ram','pochoco_spi_slave','pochoco_sma10'|ForEach-Object {"proyecto4/alternativas/mmio_sma10/rtl/$_.v"})
$files+=@(Get-ChildItem rtl/espino_core/*.v | ForEach-Object {"rtl/espino_core/$($_.Name)"})
$opt=if($Map -eq 'default'){''}else{"-$Map"}
$report="$p/build/area_timeout_uart_$Map"
yosys -p "read_verilog -sv $($files -join ' '); chparam -set TIMEOUT_DIAG 2 demo_autonoma_bus_detail_top; expose demo_autonoma_bus_detail_top/w:debug_uart_tx; hierarchy -top demo_autonoma_bus_detail_top; synth_ice40 $opt -top demo_autonoma_bus_detail_top; check -assert; stat; write_json $report.json" *> "$report.yosys.log"
if($LASTEXITCODE){throw "Yosys failed"}
nextpnr-ice40 --hx1k --package vq100 --freq 25 --seed 1 --json "$report.json" --pcf "$p/goboard_timeout_uart.pcf" --pack-only *> "$report.pnr.log"
(Select-String 'ICESTORM_LC:' -Path "$report.pnr.log").Line

