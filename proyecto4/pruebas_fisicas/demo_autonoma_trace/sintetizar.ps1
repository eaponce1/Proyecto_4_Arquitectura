$ErrorActionPreference='Continue'
$repo=(Resolve-Path (Join-Path $PSScriptRoot '..\..\..')).Path
Set-Location $repo
$build=Join-Path $PSScriptRoot 'build'
New-Item -ItemType Directory -Force -Path $build|Out-Null
$rtl=@(
 'proyecto4/pruebas_fisicas/demo_autonoma_trace/rtl/demo_autonoma_trace_top.v',
 'proyecto4/pruebas_fisicas/demo_autonoma_trace/rtl/price_spi_master_trace.v',
 'proyecto4/pruebas_fisicas/demo_autonoma/rtl/pochoco_soc_demo.v',
 'proyecto4/alternativas/mmio_sma10/rtl/pochoco_ram.v',
 'proyecto4/alternativas/mmio_sma10/rtl/pochoco_spi_slave.v',
 'proyecto4/alternativas/mmio_sma10/rtl/pochoco_sma10.v'
)+(Get-ChildItem 'rtl/espino_core/*.v'|ForEach-Object{$_.FullName.Substring($repo.Length+1).Replace('\','/')})
$read=$rtl -join ' '
$json='proyecto4/pruebas_fisicas/demo_autonoma_trace/build/demo_autonoma_trace.json'
$ys="read_verilog -sv $read; hierarchy -top demo_autonoma_trace_top; synth_ice40 -top demo_autonoma_trace_top -json `"$json`"; stat"
$yl=Join-Path $build 'yosys.log';if(Test-Path $yl){Remove-Item -LiteralPath $yl}
& yosys -p $ys *> $yl
if($LASTEXITCODE -ne 0){Get-Content $yl -Tail 30;throw 'Yosys failed.'}
Get-Content $yl -Tail 20
$asc='proyecto4/pruebas_fisicas/demo_autonoma_trace/build/demo_autonoma_trace.asc'
$pcf='proyecto4/pruebas_fisicas/demo_autonoma_trace/goboard_demo_autonoma_trace.pcf'
$pl=Join-Path $build 'nextpnr.log';if(Test-Path $pl){Remove-Item -LiteralPath $pl}
& nextpnr-ice40 --hx1k --package vq100 --freq 25 --seed 1 --json $json --pcf $pcf --asc $asc *> $pl
$rc=$LASTEXITCODE;Get-Content $pl -Tail 25
if($rc -ne 0){Write-Warning 'nextpnr failed; no bitstream packed.';exit $rc}
$pnr=Get-Content $pl -Raw
if($pnr -match 'ICESTORM_LC:\s*([0-9]+)\s*/\s*1280'){$lc=[int]$Matches[1];if($lc -gt 1280){Write-Warning "LC overflow $lc/1280; no bitstream.";exit 2}}else{Write-Warning 'LC usage unconfirmed; no bitstream.';exit 3}
if($pnr -notmatch 'Max frequency.*PASS at 25\.00 MHz'){Write-Warning 'Timing at 25 MHz failed/unconfirmed; no bitstream.';exit 4}
$bin=Join-Path $build 'demo_autonoma_trace.bin'
& icepack $asc $bin
if($LASTEXITCODE -ne 0){throw 'icepack failed.'}
Write-Host "Trace bitstream: $bin"
