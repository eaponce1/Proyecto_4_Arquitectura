$ErrorActionPreference='Continue'
$repo=(Resolve-Path (Join-Path $PSScriptRoot '..\..\..')).Path
Set-Location $repo

$b='proyecto4/pruebas_fisicas/demo_autonoma_bus_detail/build'
New-Item -ItemType Directory -Force -Path $b|Out-Null
$bin=Join-Path $b 'demo_autonoma_bus_detail.bin'

# Never leave a stale bitstream looking like the output of this source revision.
if(Test-Path -LiteralPath $bin){Remove-Item -LiteralPath $bin -Force}

& (Join-Path $PSScriptRoot 'ejecutar_pruebas.ps1')

$rtl=@(
  'proyecto4/pruebas_fisicas/demo_autonoma_bus_detail/rtl/demo_autonoma_bus_detail_top.v',
  'proyecto4/pruebas_fisicas/demo_autonoma_bus_detail/rtl/first_post_byte_pc_probe.v',
  'proyecto4/pruebas_fisicas/demo_autonoma_bus_detail/rtl/pochoco_soc_cpu_trace.v',
  'proyecto4/pruebas_fisicas/demo_autonoma_bus_detail/rtl/price_spi_master_cpu_trace.v',
  'proyecto4/pruebas_fisicas/demo_autonoma_bus_detail/rtl/espino_core_cpu_trace.v',
  'proyecto4/alternativas/mmio_sma10/rtl/pochoco_ram.v',
  'proyecto4/alternativas/mmio_sma10/rtl/pochoco_spi_slave.v',
  'proyecto4/alternativas/mmio_sma10/rtl/pochoco_sma10.v'
)+(Get-ChildItem 'rtl/espino_core/*.v'|ForEach-Object{$_.FullName.Substring($repo.Length+1).Replace('\','/')})

$json="$b/demo_autonoma_bus_detail.json"
$ys="read_verilog -sv $($rtl -join ' '); hierarchy -top demo_autonoma_bus_detail_top; synth_ice40 -top demo_autonoma_bus_detail_top -json `"$json`"; check -assert; stat"
& yosys -p $ys *> "$b/yosys.log"
if($LASTEXITCODE -ne 0){Get-Content "$b/yosys.log" -Tail 40;throw 'Yosys failed; no bitstream generated.'}
Get-Content "$b/yosys.log" -Tail 25

$asc="$b/demo_autonoma_bus_detail.asc"
$pcf='proyecto4/pruebas_fisicas/demo_autonoma_bus_detail/goboard_demo_autonoma_bus_detail.pcf'
$pins=@(Get-Content $pcf | ForEach-Object {if($_ -match '^set_io\s+\S+\s+(\d+)\s*$'){$Matches[1]}})
if($pins.Count -ne 5 -or @($pins | Sort-Object -Unique).Count -ne 5){throw 'Invalid or duplicated PCF pins.'}
& nextpnr-ice40 --hx1k --package vq100 --freq 25 --seed 1 --json $json --pcf $pcf --asc $asc *> "$b/nextpnr.log"
if($LASTEXITCODE -ne 0){Get-Content "$b/nextpnr.log" -Tail 40;throw 'nextpnr failed; no bitstream packed.'}

$pnr=Get-Content "$b/nextpnr.log" -Raw
Get-Content "$b/nextpnr.log" -Tail 30
if($pnr -notmatch 'ICESTORM_LC:\s*([0-9]+)\s*/\s*1280'){
  throw 'LC usage could not be confirmed; no bitstream generated.'
}
$lc=[int]$Matches[1]
if($lc -gt 1280){throw "LC overflow $lc/1280; no bitstream generated."}
if(($pnr -split "\r?\n" | Where-Object {$_ -match "Max frequency"} | Select-Object -Last 1) -notmatch 'PASS at 25\.00 MHz'){
  throw '25 MHz timing was not confirmed; no bitstream generated.'
}

& icepack $asc $bin
if($LASTEXITCODE -ne 0){throw 'icepack failed; no bitstream generated.'}
$hash=(Get-FileHash -Algorithm SHA256 $bin).Hash
$size=(Get-Item $bin).Length
Write-Host "Independent PC-probe bitstream: $repo\$bin"
Write-Host "LC: $lc/1280"
Write-Host "SHA256: $hash"
Write-Host "Bytes: $size"



