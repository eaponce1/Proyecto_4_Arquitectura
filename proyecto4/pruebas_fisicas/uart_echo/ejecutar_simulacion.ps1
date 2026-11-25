$ErrorActionPreference = 'Continue'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..\..\..')).Path
Set-Location $root
$build = 'proyecto4/pruebas_fisicas/uart_echo/build'
New-Item -ItemType Directory -Force -Path $build | Out-Null
$sim = "$build/tb_uart_echo.vvp"
$sources = @(
  'proyecto4/pruebas_fisicas/uart_echo/rtl/uart_rx.v',
  'proyecto4/pruebas_fisicas/uart_echo/rtl/uart_tx.v',
  'proyecto4/pruebas_fisicas/uart_echo/rtl/uart_echo_top.v',
  'proyecto4/pruebas_fisicas/uart_echo/tb/tb_uart_echo.sv'
)
& iverilog -g2012 -s tb_uart_echo -o $sim $sources
if ($LASTEXITCODE -ne 0) { throw "Icarus compilation failed: $LASTEXITCODE" }
& vvp $sim
if ($LASTEXITCODE -ne 0) { throw "UART echo simulation failed: $LASTEXITCODE" }
