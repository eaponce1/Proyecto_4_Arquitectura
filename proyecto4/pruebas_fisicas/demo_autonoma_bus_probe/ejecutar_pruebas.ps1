$ErrorActionPreference='Stop'
$repo=(Resolve-Path (Join-Path $PSScriptRoot '..\..\..')).Path
Set-Location $repo
python proyecto4\pruebas_fisicas\demo_autonoma_bus_probe\python\generar_vectores.py
$rtl=@('proyecto4/pruebas_fisicas/demo_autonoma_bus_probe/rtl/demo_autonoma_bus_probe_top.v','proyecto4/pruebas_fisicas/demo_autonoma_bus_probe/rtl/pochoco_soc_bus_probe.v','proyecto4/pruebas_fisicas/demo_autonoma_bus_probe/rtl/price_spi_master_probe.v','proyecto4/alternativas/mmio_sma10/rtl/pochoco_ram.v','proyecto4/alternativas/mmio_sma10/rtl/pochoco_spi_slave.v','proyecto4/alternativas/mmio_sma10/rtl/pochoco_sma10.v','proyecto4/alternativas/mmio_sma10/tb/ram_model.v')+(Get-ChildItem 'rtl/espino_core/*.v'|ForEach-Object{$_.FullName.Substring($repo.Length+1).Replace('\','/')})
$tb='proyecto4/pruebas_fisicas/demo_autonoma_bus_probe/tb/tb_demo_autonoma_bus_probe.sv'
$out='proyecto4/pruebas_fisicas/demo_autonoma_bus_probe/build/tb_demo_autonoma_bus_probe.vvp'
New-Item -ItemType Directory -Force -Path (Split-Path $out)|Out-Null
& iverilog -g2012 -s tb_demo_autonoma_bus_probe -o $out ($rtl+$tb)
if($LASTEXITCODE -ne 0){throw 'Icarus compile failed.'}
& vvp $out
if($LASTEXITCODE -ne 0){throw 'Icarus simulation failed.'}
