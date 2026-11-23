param([ValidateSet("default","dff","nocarry")][string]$Mapping="dff",[switch]$TimeoutDiagnostic,[switch]$TimeoutUART,[switch]$TimeoutContext,[switch]$BootBranch,[switch]$FetchWord,[switch]$FetchReadEnable,[switch]$FetchPhase,[switch]$FetchROM,[switch]$SlowROM)
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
$pcf="$PSScriptRoot/goboard_demo_autonoma_bus_detail.pcf"
$pinCount=5
if(@(@($TimeoutDiagnostic,$TimeoutUART,$TimeoutContext,$BootBranch,$FetchWord,$FetchReadEnable,$FetchPhase,$FetchROM,$SlowROM) | Where-Object {$_}).Count -gt 1){throw 'Select one build mode'}
$tests=@('ejecutar_pruebas','verificar_timeout','verificar_arranque')
if($TimeoutDiagnostic){
  $bin=Join-Path $b 'timeout_diagnostico.bin'
  $artifact="$b/timeout_diagnostico"
  $yosysLog="$b/timeout_diagnostico_yosys.log"
  $pnrLog="$b/timeout_diagnostico_nextpnr.log"
  $elaboration='chparam -set TIMEOUT_DIAG 1 demo_autonoma_bus_detail_top;'
  $tests=@('ejecutar_pruebas','verificar_timeout_diagnostico')
}

if($TimeoutUART){
  $bin=Join-Path $b 'timeout_uart.bin'
  $artifact="$b/timeout_uart"
  $yosysLog="$b/timeout_uart_yosys.log"
  $pnrLog="$b/timeout_uart_nextpnr.log"
  $elaboration='chparam -set TIMEOUT_DIAG 2 demo_autonoma_bus_detail_top; expose demo_autonoma_bus_detail_top/w:debug_uart_tx;'
  $pcf="$PSScriptRoot/goboard_timeout_uart.pcf"
  $pinCount=6
  $tests=@('verificar_timeout_uart')
}
if($TimeoutContext){
  $artifact="$b/timeout_contexto"
  $bin="$artifact.bin"
  $yosysLog="${artifact}_yosys.log"
  $pnrLog="${artifact}_nextpnr.log"
  $elaboration='chparam -set TIMEOUT_DIAG 3 demo_autonoma_bus_detail_top; expose demo_autonoma_bus_detail_top/w:debug_uart_tx;'
  $pcf="$PSScriptRoot/goboard_timeout_uart.pcf"
  $pinCount=6
  $tests=@('verificar_timeout_uart')
}
if($BootBranch){
  $artifact="$b/timeout_arranque"
  $bin="$artifact.bin"
  $yosysLog="${artifact}_yosys.log"
  $pnrLog="${artifact}_nextpnr.log"
  $elaboration='chparam -set TIMEOUT_DIAG 4 demo_autonoma_bus_detail_top; expose demo_autonoma_bus_detail_top/w:debug_uart_tx;'
  $pcf="$PSScriptRoot/goboard_timeout_uart.pcf"
  $pinCount=6
  $tests=@('verificar_timeout_uart')
}
if($FetchWord){
  $artifact="$b/timeout_fetch"
  $bin="$artifact.bin"
  $yosysLog="${artifact}_yosys.log"
  $pnrLog="${artifact}_nextpnr.log"
  $elaboration='chparam -set TIMEOUT_DIAG 5 demo_autonoma_bus_detail_top; expose demo_autonoma_bus_detail_top/w:debug_uart_tx;'
  $pcf="$PSScriptRoot/goboard_timeout_uart.pcf"
  $pinCount=6
  $tests=@('verificar_timeout_uart')
}
if($FetchReadEnable){
  $artifact="$b/selftest_fetch_re"
  $bin="$artifact.bin"
  $yosysLog="${artifact}_yosys.log"
  $pnrLog="${artifact}_nextpnr.log"
}
if($FetchPhase){
  $artifact="$b/selftest_fetch_fase"
  $bin="$artifact.bin"
  $yosysLog="${artifact}_yosys.log"
  $pnrLog="${artifact}_nextpnr.log"
}
$mapInstructionRam=($FetchReadEnable -or $FetchPhase)
if($FetchROM){
  $artifact="$b/selftest_fetch_rom"
  $bin="$artifact.bin"
  $yosysLog="${artifact}_yosys.log"
  $pnrLog="${artifact}_nextpnr.log"
  $elaboration='chparam -set FETCH_ROM 1 demo_autonoma_bus_detail_top;'
}
if($SlowROM){
  $artifact="$b/selftest_fetch_rom_lento"
  $bin="$artifact.bin"
  $yosysLog="${artifact}_yosys.log"
  $pnrLog="${artifact}_nextpnr.log"
  $elaboration='chparam -set FETCH_ROM 1 -set SLOW_CLOCK 1 demo_autonoma_bus_detail_top; expose demo_autonoma_bus_detail_top/w:debug_uart_tx;'
  $pcf="$PSScriptRoot/goboard_timeout_uart.pcf"
  $pinCount=6
}
# Never leave a stale bitstream looking like the output of this source revision.
if(Test-Path -LiteralPath $bin){Remove-Item -LiteralPath $bin -Force}

if($FetchROM -or $SlowROM){
  & python -B (Join-Path $PSScriptRoot 'verificar_pc_rom.py') | Tee-Object "$b/rom_pc_rango.log"
  if($LASTEXITCODE){throw 'Firmware outside the immutable ROM fetch range'}
}
foreach($test in $tests){
  $testArgs=@()
  if($TimeoutContext){$testArgs=@('-Context')}
  if($BootBranch){$testArgs=@('-BootBranch')}
  if($FetchWord){$testArgs=@('-FetchWord')}
  if($FetchROM -and $test -eq 'ejecutar_pruebas'){$testArgs=@('-FetchROM')}
  if($SlowROM -and $test -eq 'ejecutar_pruebas'){$testArgs=@('-SlowROM')}
  & powershell -NoProfile -ExecutionPolicy Bypass -File (Join-Path $PSScriptRoot "$test.ps1") @testArgs |
    Tee-Object "$b/$test.watchdog.log"
  if($LASTEXITCODE){throw "Regression failed: $test"}
}
if(!$TimeoutDiagnostic -and !$TimeoutUART -and !$TimeoutContext -and !$BootBranch -and !$FetchWord){
  & vvp "$b/arranque_actual.vvp" +bad_miso | Tee-Object "$b/arranque_miso_inyectado.log"
  if($LASTEXITCODE){throw 'SPI MISO injection failed'}
}
& python -B (Join-Path $PSScriptRoot 'comparar_python.py') | Tee-Object "$b/comparacion_python_watchdog.log"
if($LASTEXITCODE){throw 'Python equivalence failed'}

$rtl=@(
  'proyecto4/pruebas_fisicas/demo_autonoma_bus_detail/rtl/demo_autonoma_bus_detail_top.v',
  'proyecto4/pruebas_fisicas/demo_autonoma_bus_detail/rtl/demo_integral_monitor.v',
  'proyecto4/pruebas_fisicas/demo_autonoma_bus_detail/rtl/timeout_pc_uart.v',
  'proyecto4/pruebas_fisicas/demo_autonoma_bus_detail/rtl/first_post_byte_pc_probe.v',
  'proyecto4/pruebas_fisicas/demo_autonoma_bus_detail/rtl/pochoco_soc_cpu_trace.v',
  'proyecto4/pruebas_fisicas/demo_autonoma_bus_detail/rtl/price_spi_master_cpu_trace.v',
  'proyecto4/pruebas_fisicas/demo_autonoma_bus_detail/rtl/espino_core_cpu_trace.v',
  'proyecto4/alternativas/mmio_sma10/rtl/pochoco_ram.v',
  'proyecto4/alternativas/mmio_sma10/rtl/pochoco_spi_slave.v',
  'proyecto4/alternativas/mmio_sma10/rtl/pochoco_sma10.v'
)+(Get-ChildItem 'rtl/espino_core/*.v'|ForEach-Object{$_.FullName.Substring($repo.Length+1).Replace('\','/')})

$json="$artifact.json"
$rawJson=if($mapInstructionRam){"${artifact}_yosys.json"}else{$json}
$mapFlag=if($Mapping -eq "default"){""}else{"-$Mapping"}
$ys="read_verilog -sv $($rtl -join ' '); $elaboration hierarchy -top demo_autonoma_bus_detail_top; synth_ice40 $mapFlag -top demo_autonoma_bus_detail_top; check -assert; stat; write_json `"$rawJson`""
& yosys -p $ys *> $yosysLog
if($LASTEXITCODE -ne 0){Get-Content $yosysLog -Tail 40;throw 'Yosys failed; no bitstream generated.'}
Get-Content $yosysLog -Tail 25

if($mapInstructionRam){
  $ramArgs=@()
  if($FetchPhase){$ramArgs=@('--registered-inputs')}
  & python -B (Join-Path $PSScriptRoot 'mapear_fetch_re.py') $rawJson $json @ramArgs
  if($LASTEXITCODE){throw 'Instruction BRAM remap failed'}
}
if($mapInstructionRam -or $FetchROM -or $SlowROM){
  $mapped="${artifact}_mapped.v"
  & yosys -Q -q -p "read_json `"$json`"; check -assert; write_verilog -noattr `"$mapped`""
  if($LASTEXITCODE){throw 'Mapped netlist check failed'}
  $yosysDir=Split-Path (Get-Command yosys).Source -Parent
  $cells=Join-Path $yosysDir '../share/yosys/ice40/cells_sim.v'
  if(!(Test-Path -LiteralPath $cells)){throw "Missing iCE40 simulation model: $cells"}
  $gateDefine=if($SlowROM){'-DAUTOTEST_UART'}else{'-DAUTOTEST_LEDS'}
  & iverilog -g2012 $gateDefine -s tb_fetch_re_mapped -o "${artifact}_mapped.vvp" "$PSScriptRoot/tb/tb_fetch_re_mapped.sv" $mapped $cells
  if($LASTEXITCODE){throw 'Mapped selftest could not compile'}
}

$asc="$artifact.asc"

$pins=@(Get-Content $pcf | ForEach-Object {if($_ -match '^set_io\s+\S+\s+(\d+)\s*$'){$Matches[1]}})
if($pins.Count -ne $pinCount -or @($pins | Sort-Object -Unique).Count -ne $pinCount){throw 'Invalid or duplicated PCF pins.'}
& nextpnr-ice40 --hx1k --package vq100 --freq 25 --seed 1 --json $json --pcf $pcf --asc $asc *> $pnrLog
if($LASTEXITCODE -ne 0){Get-Content $pnrLog -Tail 40;throw 'nextpnr failed; no bitstream packed.'}

$pnr=Get-Content $pnrLog -Raw
Get-Content $pnrLog -Tail 30
if($pnr -notmatch 'ICESTORM_LC:\s*([0-9]+)\s*/\s*1280'){
  throw 'LC usage could not be confirmed; no bitstream generated.'
}
$lc=[int]$Matches[1]
if($lc -gt 1280){throw "LC overflow $lc/1280; no bitstream generated."}
$clockCount=if($SlowROM){2}else{1}
$clockResults=@($pnr -split "\r?\n" | Where-Object {$_ -match "Max frequency"} |
  Select-Object -Last $clockCount)
if($clockResults.Count -ne $clockCount -or
   @($clockResults | Where-Object {$_ -notmatch 'PASS at 25\.00 MHz'}).Count -gt 0){
  throw '25 MHz timing was not confirmed; no bitstream generated.'
}

if($mapInstructionRam -or $FetchROM -or $SlowROM){
  & vvp "${artifact}_mapped.vvp" | Tee-Object "${artifact}_mapped.log"
  if($LASTEXITCODE){throw 'Mapped selftest failed; no bitstream generated.'}
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



















