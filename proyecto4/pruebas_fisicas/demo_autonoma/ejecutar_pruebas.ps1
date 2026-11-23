$ErrorActionPreference = 'Stop'
$repo = (Resolve-Path (Join-Path $PSScriptRoot '..\..\..')).Path
Set-Location $repo
$build = Join-Path $PSScriptRoot 'build'
New-Item -ItemType Directory -Force -Path $build | Out-Null
python (Join-Path $PSScriptRoot 'python\generar_vectores.py')
if ($LASTEXITCODE -ne 0) { throw 'No se pudieron generar vectores Python.' }
$sources = @(
  'proyecto4/pruebas_fisicas/demo_autonoma/tb/tb_demo_autonoma.sv',
  'proyecto4/pruebas_fisicas/demo_autonoma/rtl/demo_autonoma_top.v',
  'proyecto4/pruebas_fisicas/demo_autonoma/rtl/pochoco_soc_demo.v',
  'proyecto4/pruebas_fisicas/demo_autonoma/rtl/price_spi_master.v',
  'proyecto4/alternativas/mmio_sma10/rtl/pochoco_ram.v',
  'proyecto4/alternativas/mmio_sma10/rtl/pochoco_spi_slave.v',
  'proyecto4/alternativas/mmio_sma10/rtl/pochoco_sma10.v',
  'proyecto4/alternativas/mmio_sma10/tb/ram_model.v'
) + (Get-ChildItem 'rtl/espino_core/*.v' | ForEach-Object { $_.FullName })
$sim = Join-Path $build 'tb_demo_autonoma.vvp'
& iverilog -g2012 -s tb_demo_autonoma -o $sim $sources
if ($LASTEXITCODE -ne 0) { throw 'Icarus no pudo compilar el testbench.' }
& vvp $sim
if ($LASTEXITCODE -ne 0) { throw 'Falló el testbench integrado.' }
