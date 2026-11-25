$ErrorActionPreference = 'Continue'
$repo = (Resolve-Path (Join-Path $PSScriptRoot '..\..\..')).Path
Set-Location $repo
$build = Join-Path $PSScriptRoot 'build'
New-Item -ItemType Directory -Force -Path $build | Out-Null
$rtl = @(
  'proyecto4/pruebas_fisicas/demo_autonoma_debug/rtl/demo_autonoma_debug_top.v',
  'proyecto4/pruebas_fisicas/demo_autonoma_debug/rtl/error_monitor.v',
  'proyecto4/pruebas_fisicas/demo_autonoma/rtl/price_spi_master.v',
  'proyecto4/pruebas_fisicas/demo_autonoma/rtl/pochoco_soc_demo.v',
  'proyecto4/alternativas/mmio_sma10/rtl/pochoco_ram.v',
  'proyecto4/alternativas/mmio_sma10/rtl/pochoco_spi_slave.v',
  'proyecto4/alternativas/mmio_sma10/rtl/pochoco_sma10.v'
) + (Get-ChildItem 'rtl/espino_core/*.v' | ForEach-Object { $_.FullName.Substring($repo.Length + 1).Replace('\','/') })
$read = $rtl -join ' '
$json = 'proyecto4/pruebas_fisicas/demo_autonoma_debug/build/demo_autonoma_debug.json'
$ys = "read_verilog -sv $read; hierarchy -top demo_autonoma_debug_top; synth_ice40 -top demo_autonoma_debug_top -json `"$json`"; stat"
$yosysLog = Join-Path $build 'yosys.log'
if (Test-Path $yosysLog) { Remove-Item -LiteralPath $yosysLog }
& yosys -p $ys *> $yosysLog
if ($LASTEXITCODE -ne 0) { Get-Content $yosysLog -Tail 40; throw 'Yosys failed.' }
Get-Content $yosysLog -Tail 25

$asc = 'proyecto4/pruebas_fisicas/demo_autonoma_debug/build/demo_autonoma_debug.asc'
$pcf = 'proyecto4/pruebas_fisicas/demo_autonoma_debug/goboard_demo_autonoma_debug.pcf'
$pnrLog = Join-Path $build 'nextpnr.log'
if (Test-Path $pnrLog) { Remove-Item -LiteralPath $pnrLog }
& nextpnr-ice40 --hx1k --package vq100 --freq 25 --seed 1 --json $json --pcf $pcf --asc $asc *> $pnrLog
$pnrExit = $LASTEXITCODE
Get-Content $pnrLog -Tail 35
if ($pnrExit -ne 0) { Write-Warning 'nextpnr failed; no bitstream will be packed.'; exit $pnrExit }
$pnrText = Get-Content $pnrLog -Raw
if ($pnrText -match 'ICESTORM_LC:\s*([0-9]+)\s*/\s*1280') {
  $lc = [int]$Matches[1]
  if ($lc -gt 1280) { Write-Warning "Design exceeds HX1K: $lc/1280 LC; no bitstream packed."; exit 2 }
} else {
  Write-Warning 'Could not confirm LC utilization; no bitstream packed.'; exit 3
}
if ($pnrText -notmatch 'Max frequency.*PASS at 25\.00 MHz') {
  Write-Warning 'Timing at 25 MHz was not confirmed; no bitstream packed.'; exit 4
}
$bin = Join-Path $build 'demo_autonoma_debug.bin'
& icepack $asc $bin
if ($LASTEXITCODE -ne 0) { throw 'icepack failed.' }
Write-Host "Independent diagnostic bitstream: $bin"
