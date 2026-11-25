$ErrorActionPreference='Stop'
$repo=(Resolve-Path (Join-Path $PSScriptRoot '..\..\..')).Path
Set-Location $repo
python proyecto4\pruebas_fisicas\demo_autonoma_cpu_trace\python\generar_vectores.py
if($LASTEXITCODE -ne 0){throw 'Python reference generation failed.'}
$src=@('proyecto4/pruebas_fisicas/demo_autonoma_cpu_trace/tb/tb_demo_autonoma_cpu_trace.sv','proyecto4/pruebas_fisicas/demo_autonoma_cpu_trace/rtl/demo_autonoma_cpu_trace_top.v','proyecto4/pruebas_fisicas/demo_autonoma_cpu_trace/rtl/pochoco_soc_cpu_trace.v','proyecto4/pruebas_fisicas/demo_autonoma_cpu_trace/rtl/price_spi_master_cpu_trace.v','proyecto4/pruebas_fisicas/demo_autonoma_cpu_trace/rtl/espino_core_cpu_trace.v','proyecto4/alternativas/mmio_sma10/rtl/pochoco_ram.v','proyecto4/alternativas/mmio_sma10/rtl/pochoco_spi_slave.v','proyecto4/alternativas/mmio_sma10/rtl/pochoco_sma10.v','proyecto4/alternativas/mmio_sma10/tb/ram_model.v')+(Get-ChildItem 'rtl/espino_core/*.v'|ForEach-Object{$_.FullName.Substring($repo.Length+1).Replace('\','/')})
$out='proyecto4/pruebas_fisicas/demo_autonoma_cpu_trace/build/tb_demo_autonoma_cpu_trace.vvp'
New-Item -ItemType Directory -Force -Path (Split-Path $out)|Out-Null
& iverilog -g2012 -s tb_demo_autonoma_cpu_trace -o $out $src
if($LASTEXITCODE -ne 0){throw 'Icarus compilation failed.'}
& vvp $out
if($LASTEXITCODE -ne 0){throw 'Icarus simulation failed.'}
