$ErrorActionPreference = 'Continue'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..\..\..')).Path
Set-Location $root
$build = 'proyecto4/pruebas_fisicas/uart_echo/build'
New-Item -ItemType Directory -Force -Path $build | Out-Null
$json = "$build/uart_echo.json"
$asc = "$build/uart_echo.asc"
$bin = "$build/uart_echo.bin"
$rtl = 'proyecto4/pruebas_fisicas/uart_echo/rtl/uart_rx.v proyecto4/pruebas_fisicas/uart_echo/rtl/uart_tx.v proyecto4/pruebas_fisicas/uart_echo/rtl/uart_echo_top.v'
& yosys -p "read_verilog $rtl; synth_ice40 -top uart_echo_top -json $json" *> "$build/yosys.log"
$ys = $LASTEXITCODE
Get-Content "$build/yosys.log" -Tail 35
if ($ys -ne 0) { throw "Yosys failed: $ys" }
& nextpnr-ice40 --seed 1 --freq 25 --hx1k --package vq100 --json $json --pcf proyecto4/pruebas_fisicas/uart_echo/goboard_uart_echo.pcf --asc $asc *> "$build/nextpnr.log"
$pnr = $LASTEXITCODE
Get-Content "$build/nextpnr.log" -Tail 40
if ($pnr -ne 0) { throw "nextpnr failed: $pnr" }
& icepack $asc $bin
if ($LASTEXITCODE -ne 0) { throw "icepack failed: $LASTEXITCODE" }
Get-Item $bin | Select-Object FullName,Length
