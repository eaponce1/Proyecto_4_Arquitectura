$ErrorActionPreference='Stop'
Set-Location (Resolve-Path (Join-Path $PSScriptRoot '..\..\..'))
$p='proyecto4/pruebas_fisicas/demo_autonoma_bus_detail'
$common=@(Get-ChildItem rtl/espino_core/*.v | ForEach-Object FullName)
$common+=@('pochoco_ram','pochoco_spi_slave','pochoco_sma10' | ForEach-Object {"proyecto4/alternativas/mmio_sma10/rtl/$_.v"})
$common+='proyecto4/alternativas/mmio_sma10/tb/ram_model.v'
$rtl=@(Get-ChildItem "$p/rtl/*.v" | ForEach-Object FullName)
$out="$p/build/tb_timeout_go_board.vvp"
& iverilog -g2012 -s tb_timeout_go_board -o $out "$p/tb/tb_timeout_go_board.sv" @rtl @common
if($LASTEXITCODE){throw 'Compilation failed'}
foreach($scenario in @('normal','early_ack','limit_ack','late_ack','drop_ack','drop_milestone','drop_final_decision')){
  $log="$p/build/timeout_$scenario.csv"
  & vvp $out "+$scenario" > $log
  Select-String -Path $log -Pattern '^PASS|^REPRO|^FATAL' | ForEach-Object Line
  if($LASTEXITCODE){throw "Scenario failed: $scenario"}
}



