$ErrorActionPreference='Stop'
$repo=(Resolve-Path (Join-Path $PSScriptRoot '..\..\..')).Path
Set-Location $repo

$b='proyecto4/pruebas_fisicas/demo_autonoma_bus_detail/build'
New-Item -ItemType Directory -Force -Path $b|Out-Null

# 1) Unit test for the one-shot physical PC/instruction probe.
$probeSrc=@(
  'proyecto4/pruebas_fisicas/demo_autonoma_bus_detail/rtl/first_post_byte_pc_probe.v',
  'proyecto4/pruebas_fisicas/demo_autonoma_bus_detail/tb/tb_first_post_byte_pc_probe.sv'
)
$probeOut="$b/tb_first_post_byte_pc_probe.vvp"
& iverilog -g2012 -s tb_first_post_byte_pc_probe -o $probeOut $probeSrc
if($LASTEXITCODE -ne 0){throw 'PC probe unit-test compilation failed.'}
& vvp $probeOut
if($LASTEXITCODE -ne 0){throw 'PC probe unit test failed.'}

# 2) Full SoC integration regression, including all 16 SPI prices/decisions/MISO.
$src=@(
  'proyecto4/pruebas_fisicas/demo_autonoma_bus_detail/tb/tb_demo_autonoma_bus_detail.sv',
  'proyecto4/pruebas_fisicas/demo_autonoma_bus_detail/rtl/demo_autonoma_bus_detail_top.v',
  'proyecto4/pruebas_fisicas/demo_autonoma_bus_detail/rtl/first_post_byte_pc_probe.v',
  'proyecto4/pruebas_fisicas/demo_autonoma_bus_detail/rtl/pochoco_soc_cpu_trace.v',
  'proyecto4/pruebas_fisicas/demo_autonoma_bus_detail/rtl/espino_core_cpu_trace.v',
  'proyecto4/pruebas_fisicas/demo_autonoma_bus_detail/rtl/price_spi_master_cpu_trace.v',
  'proyecto4/alternativas/mmio_sma10/rtl/pochoco_ram.v',
  'proyecto4/alternativas/mmio_sma10/rtl/pochoco_spi_slave.v',
  'proyecto4/alternativas/mmio_sma10/rtl/pochoco_sma10.v',
  'proyecto4/alternativas/mmio_sma10/tb/ram_model.v'
)+(Get-ChildItem 'rtl/espino_core/*.v'|ForEach-Object{$_.FullName.Substring($repo.Length+1).Replace('\','/')})

$out="$b/tb_demo_autonoma_bus_detail.vvp"
& iverilog -g2012 -s tb_demo_autonoma_bus_detail -o $out $src
if($LASTEXITCODE -ne 0){throw 'Integrated Icarus compilation failed.'}
& vvp $out | Tee-Object -FilePath "$b/simulacion_integrada.log"
if($LASTEXITCODE -ne 0){throw 'Integrated 16-tick test failed.'}

