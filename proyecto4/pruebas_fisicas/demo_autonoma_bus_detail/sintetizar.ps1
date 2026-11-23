param([ValidateSet("default","dff","nocarry")][string]$Mapping="dff",[switch]$TimeoutDiagnostic)
$ErrorActionPreference='Continue'
$repo=(Resolve-Path (Join-Path $PSScriptRoot '..\..\..')).Path
Set-Location $repo

$b='proyecto4/pruebas_fisicas/demo_autonoma_bus_detail/build'
New-Item -ItemType Directory -Force -Path $b|Out-Null
$bin=Join-Path $b 'selftest.bin'
$artifact="$b/demo_autonoma_bus_detail"
$yosysLog="$b/yosys.log"
$pnrLog="$b/nextpnr.log"
$elaboration=''
$tests=@('ejecutar_pruebas','verificar_timeout','verificar_arranque')
if($TimeoutDiagnostic){
  $bin=Join-Path $b 'timeout_diagnostico.bin'
  $artifact="$b/timeout_diagnostico"
  $yosysLog="$b/timeout_diagnostico_yosys.log"
  $pnrLog="$b/timeout_diagnostico_nextpnr.log"
  $elaboration='chparam -set TIMEOUT_DIAG 1 demo_autonoma_bus_detail_top;'
  $tests=@('ejecutar_pruebas','verificar_timeout_diagnostico')
}

# Never leave a stale bitstream looking like the output of this source revision.
if(Test-Path -LiteralPath $bin){Remove-Item -LiteralPath $bin -Force}

foreach($test in $tests){
  & powershell -NoProfile -ExecutionPolicy Bypass -File (Join-Path $PSScriptRoot "$test.ps1") |
    Tee-Object "$b/$test.watchdog.log"
  if($LASTEXITCODE){throw "Regression failed: $test"}
}
if(!$TimeoutDiagnostic){
  & vvp "$b/arranque_actual.vvp" +bad_miso | Tee-Object "$b/arranque_miso_inyectado.log"
  if($LASTEXITCODE){throw 'SPI MISO injection failed'}
}
& python -B (Join-Path $PSScriptRoot 'comparar_python.py') | Tee-Object "$b/comparacion_python_watchdog.log"
if($LASTEXITCODE){throw 'Python equivalence failed'}

$rtl=@(
  'proyecto4/pruebas_fisicas/demo_autonoma_bus_detail/rtl/demo_autonoma_bus_detail_top.v',
  'proyecto4/pruebas_fisicas/demo_autonoma_bus_detail/rtl/demo_integral_monitor.v',
  'proyecto4/pruebas_fisicas/demo_autonoma_bus_detail/rtl/first_post_byte_pc_probe.v',
  'proyecto4/pruebas_fisicas/demo_autonoma_bus_detail/rtl/pochoco_soc_cpu_trace.v',
  'proyecto4/pruebas_fisicas/demo_autonoma_bus_detail/rtl/price_spi_master_cpu_trace.v',
  'proyecto4/pruebas_fisicas/demo_autonoma_bus_detail/rtl/espino_core_cpu_trace.v',
  'proyecto4/alternativas/mmio_sma10/rtl/pochoco_ram.v',
  'proyecto4/alternativas/mmio_sma10/rtl/pochoco_spi_slave.v',
  'proyecto4/alternativas/mmio_sma10/rtl/pochoco_sma10.v'
)+(Get-ChildItem 'rtl/espino_core/*.v'|ForEach-Object{$_.FullName.Substring($repo.Length+1).Replace('\','/')})

$json="$artifact.json"
$mapFlag=if($Mapping -eq "default"){""}else{"-$Mapping"}
$ys="read_verilog -sv $($rtl -join ' '); $elaboration hierarchy -top demo_autonoma_bus_detail_top; synth_ice40 $mapFlag -top demo_autonoma_bus_detail_top; check -assert; stat; write_json `"$json`""
& yosys -p $ys *> $yosysLog
if($LASTEXITCODE -ne 0){Get-Content $yosysLog -Tail 40;throw 'Yosys failed; no bitstream generated.'}
Get-Content $yosysLog -Tail 25

$asc="$artifact.asc"
$pcf='proyecto4/pruebas_fisicas/demo_autonoma_bus_detail/goboard_demo_autonoma_bus_detail.pcf'
$pins=@(Get-Content $pcf | ForEach-Object {if($_ -match '^set_io\s+\S+\s+(\d+)\s*$'){$Matches[1]}})
if($pins.Count -ne 5 -or @($pins | Sort-Object -Unique).Count -ne 5){throw 'Invalid or duplicated PCF pins.'}
& nextpnr-ice40 --hx1k --package vq100 --freq 25 --seed 1 --json $json --pcf $pcf --asc $asc *> $pnrLog
if($LASTEXITCODE -ne 0){Get-Content $pnrLog -Tail 40;throw 'nextpnr failed; no bitstream packed.'}

$pnr=Get-Content $pnrLog -Raw
Get-Content $pnrLog -Tail 30
if($pnr -notmatch 'ICESTORM_LC:\s*([0-9]+)\s*/\s*1280'){
  throw 'LC usage could not be confirmed; no bitstream generated.'
}
$lc=[int]$Matches[1]
if($lc -gt 1280){throw "LC overflow $lc/1280; no bitstream generated."}
if(($pnr -split "\r?\n" | Where-Object {$_ -match "Max frequency"} | Select-Object -Last 1) -notmatch 'PASS at 25\.00 MHz'){
  throw '25 MHz timing was not confirmed; no bitstream generated.'
}

& icepack $asc $bin
if($LASTEXITCODE -ne 0 -or !(Test-Path -LiteralPath $bin)){
  if(Test-Path -LiteralPath $bin){Remove-Item -LiteralPath $bin -Force}
  throw 'icepack failed'
}
$hash=(Get-FileHash -Algorithm SHA256 $bin).Hash
$size=(Get-Item $bin).Length
Write-Host "Integral demonstration bitstream: $repo\$bin"
Write-Host "LC: $lc/1280"
Write-Host "SHA256: $hash"
Write-Host "Bytes: $size"


















