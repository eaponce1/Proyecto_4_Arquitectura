$ErrorActionPreference='Stop'
Set-Location (Resolve-Path (Join-Path $PSScriptRoot '..\..\..'))
$p='proyecto4/pruebas_fisicas/demo_autonoma_bus_detail'
$build="$p/build"
$old="$build/arranque_pc_probe"
New-Item -Force -ItemType Directory $old | Out-Null
Expand-Archive -LiteralPath "$p/pc_probe_aprobado.zip" -DestinationPath $old -Force
$common=@(Get-ChildItem rtl/espino_core/*.v | ForEach-Object FullName)
$common+=@('pochoco_ram','pochoco_spi_slave','pochoco_sma10' | ForEach-Object {"proyecto4/alternativas/mmio_sma10/rtl/$_.v"})
$common+='proyecto4/alternativas/mmio_sma10/tb/ram_model.v'
foreach($mode in @('actual','anterior')){
  $rtl="$p/rtl"
  $defs=@()
  if($mode -eq 'anterior'){$rtl="$old/rtl";$defs=@('-DPREVIOUS')}
  $sources=@(Get-ChildItem "$rtl/*.v" | ForEach-Object FullName)
  $vvp="$build/arranque_$mode.vvp"
  & iverilog -g2012 @defs -s tb_demo_arranque -o $vvp "$p/tb/tb_demo_arranque.sv" @sources @common
  if($LASTEXITCODE){throw "Compilation failed: $mode"}
  & vvp $vvp | Tee-Object "$build/arranque_$mode.log"
  if($LASTEXITCODE){throw "Startup failed: $mode"}
}
