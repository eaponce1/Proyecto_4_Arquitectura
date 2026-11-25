$ErrorActionPreference = 'Stop'
$repo = (Resolve-Path (Join-Path $PSScriptRoot '..\..\..')).Path
Set-Location $repo
$build = Join-Path $PSScriptRoot 'build'
New-Item -ItemType Directory -Force -Path $build | Out-Null
python (Join-Path $PSScriptRoot 'python\generar_vectores.py')
if ($LASTEXITCODE -ne 0) { throw 'Python vector generation failed.' }

$unit = Join-Path $build 'tb_error_monitor.vvp'
& iverilog -g2012 -s tb_error_monitor -o $unit `
  'proyecto4/pruebas_fisicas/demo_autonoma_handshake/tb/tb_error_monitor.sv' `
  'proyecto4/pruebas_fisicas/demo_autonoma_handshake/rtl/error_monitor.v'
if ($LASTEXITCODE -ne 0) { throw 'Could not compile error monitor test.' }
& vvp $unit
if ($LASTEXITCODE -ne 0) { throw 'Error monitor test failed.' }

$sources = @(
  'proyecto4/pruebas_fisicas/demo_autonoma_handshake/tb/tb_demo_autonoma_handshake.sv',
  'proyecto4/pruebas_fisicas/demo_autonoma_handshake/rtl/demo_autonoma_handshake_top.v',
  'proyecto4/pruebas_fisicas/demo_autonoma_handshake/rtl/error_monitor.v',
  'proyecto4/pruebas_fisicas/demo_autonoma_handshake/rtl/price_spi_master_handshake.v',
  'proyecto4/pruebas_fisicas/demo_autonoma/rtl/pochoco_soc_demo.v',
  'proyecto4/alternativas/mmio_sma10/rtl/pochoco_ram.v',
  'proyecto4/alternativas/mmio_sma10/rtl/pochoco_spi_slave.v',
  'proyecto4/alternativas/mmio_sma10/rtl/pochoco_sma10.v',
  'proyecto4/alternativas/mmio_sma10/tb/ram_model.v'
) + (Get-ChildItem 'rtl/espino_core/*.v' | ForEach-Object { $_.FullName })
$sim = Join-Path $build 'tb_demo_autonoma_handshake.vvp'
& iverilog -g2012 -s tb_demo_autonoma_handshake -o $sim $sources
if ($LASTEXITCODE -ne 0) { throw 'Could not compile integrated test.' }
& vvp $sim
if ($LASTEXITCODE -ne 0) { throw 'Integrated handshake test failed.' }
