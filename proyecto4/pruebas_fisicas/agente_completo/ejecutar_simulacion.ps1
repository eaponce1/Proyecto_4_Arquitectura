$ErrorActionPreference = 'Continue'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..\..\..')).Path
Set-Location $root
python proyecto4/pruebas_fisicas/agente_completo/python/generar_vectores.py
if ($LASTEXITCODE -ne 0) { throw 'Falló la generación de vectores Python' }
$out = 'proyecto4/pruebas_fisicas/agente_completo/build/tb_agente_completo.vvp'
$rtl = Get-ChildItem proyecto4/alternativas/mmio_sma10/rtl -Recurse -Filter '*.v' | ForEach-Object FullName
$sources = @($rtl) + @(
  'proyecto4/alternativas/mmio_sma10/tb/ram_model.v',
  'proyecto4/pruebas_fisicas/agente_completo/rtl/pochoco_soc_observable.v',
  'proyecto4/pruebas_fisicas/agente_completo/rtl/price_generator.v',
  'proyecto4/pruebas_fisicas/agente_completo/rtl/decision_verifier.v',
  'proyecto4/pruebas_fisicas/agente_completo/rtl/agente_completo_top.v',
  'proyecto4/pruebas_fisicas/agente_completo/tb/tb_agente_completo.sv'
)
& iverilog -g2012 -s tb_agente_completo -o $out $sources
if ($LASTEXITCODE -ne 0) { throw "Icarus compilation failed: $LASTEXITCODE" }
& vvp $out
if ($LASTEXITCODE -ne 0) { throw "Simulation failed: $LASTEXITCODE" }
