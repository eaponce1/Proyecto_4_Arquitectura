param([int]$Jobs = 2)
$ErrorActionPreference = 'Stop'
& wsl.exe -d Ubuntu --cd $PSScriptRoot -- bash tools/probar_todas_acciones_wsl.sh --jobs $Jobs
if ($LASTEXITCODE -ne 0) { throw 'Fallo el testbench. Revisa build/testbench_todas_acciones y el resumen.' }
Write-Host 'Resultados: resultados_simulacion/testbench_todas_acciones/ABRIR_RESULTADOS.html'
