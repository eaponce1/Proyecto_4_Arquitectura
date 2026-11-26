param([string]$Zip = '', [int]$Jobs = 2)
$ErrorActionPreference = 'Stop'
if (-not $Zip) {
    $candidatos = @(
        (Join-Path ([Environment]::GetFolderPath('UserProfile')) 'Downloads\Proyecto_4_Series_Practica_export.zip'),
        (Join-Path $PSScriptRoot 'docs\referencia\Proyecto_4_Series_Practica_export.zip')
    )
    $Zip = $candidatos | Where-Object { Test-Path -LiteralPath $_ -PathType Leaf } | Select-Object -First 1
}
if (-not $Zip) { throw 'No se encontro el ZIP de practica; indica su ruta con -Zip' }
$rutaZip = (Resolve-Path -LiteralPath $Zip).Path
$rutaLinux = (& wsl.exe -d Ubuntu -- wslpath -a -u $rutaZip)
if ($LASTEXITCODE -ne 0) { throw 'No se pudo convertir la ruta del ZIP' }
$rutaLinux = $rutaLinux.Trim()
& wsl.exe -d Ubuntu --cd $PSScriptRoot -- bash tools/probar_zip_practica_wsl.sh --zip $rutaLinux --jobs $Jobs
if ($LASTEXITCODE -ne 0) { throw 'Fallo el testbench; revisa build/testbench_zip_practica/' }
Write-Host 'Resultados: resultados_simulacion/testbench_zip_practica/INFORME.md'
