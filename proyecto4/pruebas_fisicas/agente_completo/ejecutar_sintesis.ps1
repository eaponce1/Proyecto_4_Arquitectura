$ErrorActionPreference = 'Continue'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..\..\..')).Path
Set-Location $root
$outDir = 'proyecto4/pruebas_fisicas/agente_completo/build'
New-Item -ItemType Directory -Force -Path $outDir | Out-Null
$rtlBase = Get-ChildItem 'proyecto4/alternativas/mmio_sma10/rtl' -Recurse -Filter '*.v' | ForEach-Object { Resolve-Path -Relative $_.FullName }
$rtlTop = @(
  'proyecto4/pruebas_fisicas/agente_completo/rtl/pochoco_soc_observable.v',
  'proyecto4/pruebas_fisicas/agente_completo/rtl/price_generator.v',
  'proyecto4/pruebas_fisicas/agente_completo/rtl/decision_verifier.v',
  'proyecto4/pruebas_fisicas/agente_completo/rtl/agente_completo_top.v'
)
$sources = @($rtlBase) + $rtlTop
$json = "$outDir/agente_completo.json"
$asc = "$outDir/agente_completo.asc"
$bin = "$outDir/agente_completo.bin"
$srcArgs = $sources -join ' '
$yosysCmd = "read_verilog $srcArgs; synth_ice40 -top agente_completo_top -json $json"
$yosysLog = "$outDir/yosys.log"
& yosys -p $yosysCmd *> $yosysLog
$yosysStatus = $LASTEXITCODE
Get-Content $yosysLog -Tail 45
if ($yosysStatus -ne 0) { throw "Yosys fallo: $yosysStatus" }
& nextpnr-ice40 --seed 1 --freq 25 --hx1k --package vq100 --json $json --pcf proyecto4/pruebas_fisicas/agente_completo/goboard_agente_completo.pcf --asc $asc *> "$outDir/nextpnr.log"
$pnrStatus = $LASTEXITCODE
Get-Content "$outDir/nextpnr.log" -Tail 55
if ($pnrStatus -eq 0 -and (Test-Path $asc)) { & icepack $asc $bin }
Write-Output "nextpnr_exit=$pnrStatus"
if ($pnrStatus -ne 0) { throw "nextpnr no completo; revisar uso de recursos/timing en $outDir/nextpnr.log" }
