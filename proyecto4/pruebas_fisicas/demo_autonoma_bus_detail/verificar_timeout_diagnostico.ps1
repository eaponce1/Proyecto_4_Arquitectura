$ErrorActionPreference='Stop'
Set-Location (Resolve-Path (Join-Path $PSScriptRoot '..\..\..'))
$p='proyecto4/pruebas_fisicas/demo_autonoma_bus_detail'
$b="$p/build"
New-Item -Force -ItemType Directory $b | Out-Null
$common=@(Get-ChildItem rtl/espino_core/*.v | ForEach-Object FullName)
$common+=@('pochoco_ram','pochoco_spi_slave','pochoco_sma10' | ForEach-Object {"proyecto4/alternativas/mmio_sma10/rtl/$_.v"})
$common+='proyecto4/alternativas/mmio_sma10/tb/ram_model.v'
$rtl=@(Get-ChildItem "$p/rtl/*.v" | ForEach-Object FullName)
$out="$b/tb_timeout_diagnostico.vvp"
& iverilog -g2012 -s tb_timeout_diagnostico -o $out "$p/tb/tb_timeout_diagnostico.sv" @rtl @common
if($LASTEXITCODE){throw 'Diagnostic test compilation failed'}
foreach($test in @('ack_missing','status_zero','status_ready_no_price','price_read_no_ack','byte_missing','decision_missing','final_response_missing','normal')){
  & vvp $out "+$test" | Tee-Object "$b/timeout_diagnostic_$test.log"
  if($LASTEXITCODE){throw "Diagnostic test failed: $test"}
}

