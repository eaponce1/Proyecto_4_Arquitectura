$ErrorActionPreference = 'Stop'

function Escribir-Log([string] $Mensaje) {
    Add-Content -LiteralPath $log -Encoding UTF8 -Value $Mensaje
    Write-Host $Mensaje
}

function Ejecutar-Etapa([string] $Etapa, [string] $Herramienta, [string[]] $Argumentos) {
    Escribir-Log "=== $Etapa ==="
    $anterior = $ErrorActionPreference
    $reloj = [Diagnostics.Stopwatch]::StartNew()
    try {
        # Windows PowerShell 5 convierte stderr nativo en objetos ErrorRecord.
        # Registrarlos y usar el codigo de salida permite conservar las advertencias.
        $ErrorActionPreference = 'Continue'
        $PSNativeCommandUseErrorActionPreference = $false
        & $Herramienta @Argumentos 2>&1 | ForEach-Object { Escribir-Log $_.ToString() }
        $codigo = $LASTEXITCODE
    } finally {
        $ErrorActionPreference = $anterior
        $reloj.Stop()
    }
    Escribir-Log ('{0}: salida={1}, tiempo={2:F2} s' -f $Etapa, $codigo, $reloj.Elapsed.TotalSeconds)
    if ($codigo -ne 0) { throw "$Etapa fallo con codigo $codigo" }
}

$root = Split-Path -Parent $PSScriptRoot
Push-Location -LiteralPath $root
$log = Join-Path $root 'tb/build/icarus.log'
try {
    New-Item -ItemType Directory -Path 'tb/build' -Force | Out-Null
    Set-Content -LiteralPath $log -Encoding UTF8 -Value 'Proyecto 4 | MMIO SMA10 base | 2000 ticks | 100000 ns por tick'
    $firmware = 'proyecto4/alternativas/mmio_sma10/sw/trade.hex'
    $serie = 'proyecto4/resultados/validacion_oficial/practica_meta.csv'
    $rtlDir = 'proyecto4/alternativas/mmio_sma10/rtl'
    $ram = 'tests/ram_model.v'
    $testbench = 'tb/tb_proyecto_4.sv'
    $validador = 'tb/comparar_tb_proyecto4.py'
    $vvpFile = 'tb/build/tb_proyecto_4.vvp'
    $decisiones = 'tb/build/decisiones.csv'
    $requeridos = @($firmware, $serie, $ram, $testbench, $validador,
        "$rtlDir/pochoco_soc.v", "$rtlDir/pochoco_spi_slave.v", "$rtlDir/pochoco_sma10.v")
    foreach ($archivo in $requeridos) {
        if (-not (Test-Path -LiteralPath $archivo -PathType Leaf)) {
            throw "Falta el archivo $archivo"
        }
    }
    $iverilog = (Get-Command iverilog -CommandType Application -TotalCount 1).Source
    $vvp = (Get-Command vvp -CommandType Application -TotalCount 1).Source
    $python = (Get-Command python -CommandType Application -TotalCount 1).Source
    $src = @(Get-ChildItem -LiteralPath $rtlDir -Recurse -Filter '*.v' -File |
            Sort-Object FullName | Select-Object -ExpandProperty FullName)
    $hash = (Get-FileHash -Algorithm SHA256 -LiteralPath $firmware).Hash
    Escribir-Log "Firmware: $firmware (SHA-256 $hash)"
    Escribir-Log "CSV: $serie"
    $validacion = @('-B', $validador, '--serie', $serie, '--ticks', '2000')
    Ejecutar-Etapa 'Validacion CSV' $python $validacion
    Ejecutar-Etapa 'Compilacion Icarus' $iverilog (
        @('-g2012', '-s', 'tb_proyecto_4', '-o', $vvpFile) + $src + @($ram, $testbench))
    Ejecutar-Etapa 'Simulacion VVP' $vvp @('-n', $vvpFile)
    if (-not (Select-String -LiteralPath $log -Pattern '^Testbenchs aprobados: 4/4$' -Quiet)) {
        throw 'VVP termino sin confirmar los cuatro criterios del banco'
    }
    Ejecutar-Etapa 'Comparacion RTL con Python' $python (
        $validacion + @('--resultado', $decisiones, '--log', $log))
    Escribir-Log 'PASS integral: 2000 ticks, banco del profesor 4/4, equivalencia Python'
    Escribir-Log "Log: $log"
    Escribir-Log "Decisiones: $decisiones"
} catch {
    $mensaje = "FAIL: $($_.Exception.Message)"
    if (Test-Path -LiteralPath $log -PathType Leaf) { Escribir-Log $mensaje }
    else { Write-Host $mensaje }
    exit 1
} finally {
    Pop-Location
}
