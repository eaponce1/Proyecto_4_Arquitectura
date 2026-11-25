$ErrorActionPreference = 'Stop'
$root = (Resolve-Path (Join-Path $PSScriptRoot '../../..')).Path
Push-Location -LiteralPath $root
try {
    $p = 'proyecto4/alternativas/competitiva_definitiva'
    python -X utf8 -B "$p/test_invariantes.py"
    if ($LASTEXITCODE -ne 0) { throw 'Fallo invariantes o causalidad' }
    # The final selection is frozen. Research reruns must use a clean copy.
    python -X utf8 -B "$p/generar_firmware.py"
    if ($LASTEXITCODE -ne 0) { throw 'Fallo generacion Assembly' }
    python -X utf8 -B "$p/validar_equivalencia.py"
    if ($LASTEXITCODE -ne 0) { throw 'Fallo equivalencia RV32E' }
    python -X utf8 -B "$p/validar_rtl.py" --solo-estres
    if ($LASTEXITCODE -ne 0) { throw 'Fallo Icarus' }
    python -X utf8 -B "$p/validar_rtl.py" --oficial
    if ($LASTEXITCODE -ne 0) { throw 'Fallo bancos oficiales' }
    wsl.exe -d Ubuntu -- bash "$p/ejecutar_verilator_wsl.sh"
    if ($LASTEXITCODE -ne 0) { throw 'Fallo Verilator multiserie' }
} finally { Pop-Location }
