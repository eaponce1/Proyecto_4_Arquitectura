param([int]$Jobs = 2, [string]$Zip = '')
$ErrorActionPreference = 'Stop'
if (-not $Zip) {
    $candidatos = @(
        (Join-Path ([Environment]::GetFolderPath('UserProfile')) 'Downloads\proyecto4.zip'),
        (Join-Path $PSScriptRoot 'proyecto4.zip'),
        (Join-Path (Split-Path $PSScriptRoot -Parent) 'proyecto4.zip')
    )
    $Zip = $candidatos | Where-Object { Test-Path -LiteralPath $_ -PathType Leaf } | Select-Object -First 1
}
if (-not $Zip) { throw 'No se encontro proyecto4.zip. Indica su ruta con -Zip, o usa la repeticion desde trazas archivadas.' }
$rutaZip = (Resolve-Path -LiteralPath $Zip).Path
$rutaLinux = (& wsl.exe -d Ubuntu -- wslpath -a -u $rutaZip)
if ($LASTEXITCODE -ne 0) { throw 'No se pudo convertir la ruta del ZIP para WSL' }
$rutaLinux = $rutaLinux.Trim()
& wsl.exe -d Ubuntu --cd $PSScriptRoot -- bash tools/probar_todas_acciones_wsl.sh --jobs $Jobs --zip $rutaLinux
if ($LASTEXITCODE -ne 0) { throw 'Fallo el testbench. Revisa build/testbench_todas_acciones y el resumen.' }
Write-Host 'Resultados: resultados_simulacion/testbench_todas_acciones/ABRIR_RESULTADOS.html'
