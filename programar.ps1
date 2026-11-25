param([switch]$SoloVerificar)
$ErrorActionPreference = 'Stop'
Push-Location -LiteralPath $PSScriptRoot
try {
    python -X utf8 -B tools/trader.py verify
    if ($LASTEXITCODE -ne 0) { throw 'Fallo la validacion del BIN activo' }
    $iceprog = Get-Command iceprog.exe -CommandType Application -ErrorAction SilentlyContinue | Select-Object -First 1
    $ejecutable = if ($iceprog) { $iceprog.Source } else { 'C:\Tools\oss-cad-suite\bin\iceprog.exe' }
    if (-not (Test-Path -LiteralPath $ejecutable -PathType Leaf)) { throw 'No se encontro iceprog.exe' }
    if ($SoloVerificar) { Write-Host 'PASS proyecto listo. No se ejecuto iceprog.'; exit 0 }
    $log = Join-Path $PSScriptRoot 'build/trader/programacion.log'
    Set-Content -LiteralPath $log -Encoding UTF8 -Value ('Inicio: ' + (Get-Date -Format o))
    function Ejecutar-Iceprog([string[]]$Argumentos) {
        $anterior = $ErrorActionPreference
        try {
            $ErrorActionPreference = 'Continue'
            $global:LASTEXITCODE = -999
            & $ejecutable @Argumentos 2>&1 | ForEach-Object {
                Write-Host $_.ToString()
                Add-Content -LiteralPath $log -Encoding UTF8 -Value $_.ToString()
            }
            $codigo = $LASTEXITCODE
        } finally { $ErrorActionPreference = $anterior }
        Add-Content -LiteralPath $log -Encoding UTF8 -Value "Salida=$codigo"
        if ($codigo -ne 0) { throw "Fallo iceprog ($codigo). Consultar $log" }
    }
    Ejecutar-Iceprog -Argumentos @('competition.bin')
    Ejecutar-Iceprog -Argumentos @('-c','competition.bin')
    Write-Host 'PASS escritura y verificacion de flash. Falta prueba fisica con la maestra.'
} finally { Pop-Location }
