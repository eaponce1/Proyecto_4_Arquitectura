$ErrorActionPreference='Stop'
$repo=(Resolve-Path (Join-Path $PSScriptRoot '..\..\..')).Path
Set-Location $repo
$build=Join-Path $PSScriptRoot 'build'
New-Item -ItemType Directory -Force -Path $build | Out-Null
python (Join-Path $PSScriptRoot 'python\generar_vectores.py')
if($LASTEXITCODE -ne 0){throw 'Python vector generation failed.'}
$common=@(
  'proyecto4/alternativas/mmio_sma10/rtl/pochoco_ram.v',
  'proyecto4/alternativas/mmio_sma10/rtl/pochoco_spi_slave.v',
  'proyecto4/alternativas/mmio_sma10/rtl/pochoco_sma10.v',
  'proyecto4/alternativas/mmio_sma10/tb/ram_model.v'
)+(Get-ChildItem 'rtl/espino_core/*.v'|ForEach-Object{$_.FullName})
$baseline=@(
  'proyecto4/pruebas_fisicas/demo_autonoma_trace/tb/tb_baseline_trace.sv',
  'proyecto4/pruebas_fisicas/demo_autonoma_handshake/rtl/demo_autonoma_handshake_top.v',
  'proyecto4/pruebas_fisicas/demo_autonoma_handshake/rtl/error_monitor.v',
  'proyecto4/pruebas_fisicas/demo_autonoma_handshake/rtl/price_spi_master_handshake.v',
  'proyecto4/pruebas_fisicas/demo_autonoma/rtl/pochoco_soc_demo.v'
)+$common
$baseOut=Join-Path $build 'baseline_trace.vvp'
& iverilog -g2012 -s tb_baseline_trace -o $baseOut $baseline
if($LASTEXITCODE -ne 0){throw 'Baseline trace compile failed.'}
& vvp $baseOut
if($LASTEXITCODE -ne 0){throw 'Baseline trace did not complete.'}
$instrumented=@(
  'proyecto4/pruebas_fisicas/demo_autonoma_trace/tb/tb_demo_autonoma_trace.sv',
  'proyecto4/pruebas_fisicas/demo_autonoma_trace/rtl/demo_autonoma_trace_top.v',
  'proyecto4/pruebas_fisicas/demo_autonoma_trace/rtl/price_spi_master_trace.v',
  'proyecto4/pruebas_fisicas/demo_autonoma/rtl/pochoco_soc_demo.v'
)+$common
$sim=Join-Path $build 'instrumented_trace.vvp'
& iverilog -g2012 -s tb_demo_autonoma_trace -o $sim $instrumented
if($LASTEXITCODE -ne 0){throw 'Instrumented trace compile failed.'}
& vvp $sim
if($LASTEXITCODE -ne 0){throw 'Instrumented integrated trace failed.'}
