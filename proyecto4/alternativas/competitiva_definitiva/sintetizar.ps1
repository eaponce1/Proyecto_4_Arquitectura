$ErrorActionPreference = 'Stop'
$root = (Resolve-Path (Join-Path $PSScriptRoot '../../..')).Path
Push-Location -LiteralPath $root
try {
    python -X utf8 -B 'proyecto4/alternativas/competitiva_definitiva/sintetizar.py'
    if ($LASTEXITCODE -ne 0) { throw 'Fallo una puerta de validacion o sintesis; no utilizar un BIN parcial' }
} finally { Pop-Location }
