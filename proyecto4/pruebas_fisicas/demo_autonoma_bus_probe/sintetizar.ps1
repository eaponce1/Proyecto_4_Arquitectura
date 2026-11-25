$ErrorActionPreference='Continue'
$repo=(Resolve-Path (Join-Path $PSScriptRoot '..\..\..')).Path
Set-Location $repo
$b='proyecto4/pruebas_fisicas/demo_autonoma_bus_probe/build'
New-Item -ItemType Directory -Force -Path $b|Out-Null
$rtl=@('proyecto4/pruebas_fisicas/demo_autonoma_bus_probe/rtl/demo_autonoma_bus_probe_top.v','proyecto4/pruebas_fisicas/demo_autonoma_bus_probe/rtl/pochoco_soc_bus_probe.v','proyecto4/pruebas_fisicas/demo_autonoma_bus_probe/rtl/price_spi_master_probe.v','proyecto4/alternativas/mmio_sma10/rtl/pochoco_ram.v','proyecto4/alternativas/mmio_sma10/rtl/pochoco_spi_slave.v','proyecto4/alternativas/mmio_sma10/rtl/pochoco_sma10.v')+(Get-ChildItem 'rtl/espino_core/*.v'|ForEach-Object{$_.FullName.Substring($repo.Length+1).Replace('\','/')})
$json="$b/demo_autonoma_bus_probe.json"
$ys="read_verilog -sv $($rtl -join ' '); hierarchy -top demo_autonoma_bus_probe_top; synth_ice40 -top demo_autonoma_bus_probe_top -json `"$json`"; stat"
& yosys -p $ys *> "$b/yosys.log"
if($LASTEXITCODE -ne 0){Get-Content "$b/yosys.log" -Tail 30;throw 'Yosys failed.'}
Get-Content "$b/yosys.log" -Tail 20
$asc="$b/demo_autonoma_bus_probe.asc";$pcf='proyecto4/pruebas_fisicas/demo_autonoma_bus_probe/goboard_demo_autonoma_bus_probe.pcf'
& nextpnr-ice40 --hx1k --package vq100 --freq 25 --seed 1 --json $json --pcf $pcf --asc $asc *> "$b/nextpnr.log"
if($LASTEXITCODE -ne 0){Get-Content "$b/nextpnr.log" -Tail 30;throw 'nextpnr failed; no bitstream packed.'}
$pnr=Get-Content "$b/nextpnr.log" -Raw;Get-Content "$b/nextpnr.log" -Tail 25
if($pnr -notmatch 'ICESTORM_LC:\s*([0-9]+)\s*/\s*1280'){throw 'LC usage unconfirmed; no bitstream.'}
if([int]$Matches[1] -gt 1280){throw "LC overflow $($Matches[1])/1280; no bitstream."}
if($pnr -notmatch 'Max frequency.*PASS at 25\.00 MHz'){throw 'Timing failed/unconfirmed; no bitstream.'}
& icepack $asc "$b/demo_autonoma_bus_probe.bin"
if($LASTEXITCODE -ne 0){throw 'icepack failed.'}
Write-Host "Independent diagnostic bitstream: $repo\$b\demo_autonoma_bus_probe.bin"
