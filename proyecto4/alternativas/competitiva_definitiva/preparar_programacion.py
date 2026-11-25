"""Empaqueta la imagen auditada para programacion manual, sin acceder al USB."""
from pathlib import Path
import csv
import hashlib
import json
import shutil
import subprocess
import sys
import zipfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
WORKSPACE = ROOT.parent
DEST = WORKSPACE / 'LISTO_PARA_PROGRAMAR'
ARCHIVE = WORKSPACE / 'Pochoco_Trader_programacion.zip'

PROGRAMAR = r'''param([switch]$SoloVerificar)
$ErrorActionPreference = 'Stop'
$binEsperado = '44e48b3701159a79148990e6610254d573985049dd4a0c4a0ab690461c838366'
$bin = Join-Path $PSScriptRoot 'competition.bin'
$manifest = Join-Path $PSScriptRoot 'SHA256.txt'
foreach ($linea in (Get-Content -LiteralPath $manifest)) {
    if ([string]::IsNullOrWhiteSpace($linea)) { continue }
    $partes = $linea -split '  ', 2
    if ($partes.Count -ne 2 -or $partes[0] -notmatch '^[0-9a-f]{64}$') { throw 'Manifiesto invalido' }
    $archivo = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot $partes[1]))
    $base = [IO.Path]::GetFullPath($PSScriptRoot).TrimEnd('\') + '\'
    if (-not $archivo.StartsWith($base, [StringComparison]::OrdinalIgnoreCase)) { throw 'Ruta fuera del paquete' }
    if (-not (Test-Path -LiteralPath $archivo -PathType Leaf)) { throw "Falta: $($partes[1])" }
    if ((Get-FileHash -Algorithm SHA256 -LiteralPath $archivo).Hash.ToLowerInvariant() -ne $partes[0]) {
        throw "SHA-256 distinto: $($partes[1]). No programar."
    }
}
if ((Get-FileHash -Algorithm SHA256 -LiteralPath $bin).Hash.ToLowerInvariant() -ne $binEsperado) {
    throw 'El BIN no corresponde a la imagen validada'
}
if ((Get-Item -LiteralPath $bin).Length -ne 32220) { throw 'Tamano de BIN incorrecto' }
$iceprog = Get-Command iceprog.exe -CommandType Application -ErrorAction SilentlyContinue | Select-Object -First 1
$ejecutable = if ($iceprog) { $iceprog.Source } else { 'C:\Tools\oss-cad-suite\bin\iceprog.exe' }
if (-not (Test-Path -LiteralPath $ejecutable -PathType Leaf)) { throw 'No se encontro iceprog.exe. Instalar OSS CAD Suite o agregarlo al PATH.' }
Write-Host "PASS archivos y SHA-256. BIN: $bin"
Write-Host "Programador: $ejecutable"
if ($SoloVerificar) {
    Write-Host 'PASS verificacion local. No se ejecuto iceprog ni se accedio a la placa.'
    exit 0
}
$logs = Join-Path $PSScriptRoot 'logs'
New-Item -ItemType Directory -Path $logs -Force | Out-Null
$log = Join-Path $logs ('programacion_' + (Get-Date -Format 'yyyyMMdd_HHmmss') + '.txt')
Set-Content -LiteralPath $log -Encoding UTF8 -Value ("BIN SHA256=$binEsperado`r`nInicio=" + (Get-Date -Format o))
function Ejecutar-Iceprog([string[]]$Argumentos) {
    Add-Content -LiteralPath $log -Encoding UTF8 -Value ('iceprog ' + ($Argumentos -join ' '))
    $anterior = $ErrorActionPreference
    try {
        $ErrorActionPreference = 'Continue'
        & $ejecutable @Argumentos 2>&1 | ForEach-Object {
            $texto = $_.ToString()
            Write-Host $texto
            Add-Content -LiteralPath $log -Encoding UTF8 -Value $texto
        }
        $codigo = $LASTEXITCODE
    } finally { $ErrorActionPreference = $anterior }
    Add-Content -LiteralPath $log -Encoding UTF8 -Value "Salida=$codigo"
    if ($codigo -ne 0) { throw "iceprog fallo ($codigo). Consultar $log" }
}
Ejecutar-Iceprog -Argumentos @($bin)
Ejecutar-Iceprog -Argumentos @('-c', $bin)
Add-Content -LiteralPath $log -Encoding UTF8 -Value 'PASS escritura y comparacion de flash; falta ensayo SPI con la maestra.'
Write-Host 'PASS escritura y comparacion de flash. Reiniciar y realizar el ensayo SPI.'
Write-Host "Log: $log"
'''

README = '''# Programar Pochoco Trader en la Go Board

Usar solamente **competition.bin** de esta carpeta. Es la imagen HX1K/VQ100 auditada; no cargar el HEX con iceprog. El HEX y Assembly se adjuntan como referencia. No necesitas volver a ensamblar ni sintetizar.

## 1. Programacion manual

Conecta la Go Board por USB. Conserva tu imagen anterior como respaldo. Abre PowerShell en esta carpeta y ejecuta:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\\programar.ps1
```

El script comprueba los hashes, escribe la flash usando iceprog y compara la flash con el BIN (`iceprog -c`). Si falla una etapa, se detiene y guarda el log. Solo se programa cuando TU ejecutas ese comando. Requiere OSS CAD Suite; busca iceprog en PATH o en `C:\\Tools\\oss-cad-suite\\bin`.

Para comprobar los archivos sin acceder a la placa:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\\programar.ps1 -SoloVerificar
```

BIN SHA-256: `44e48b3701159a79148990e6610254d573985049dd4a0c4a0ab690461c838366`.

## 2. Conexion a la maestra

| Senal | PMOD segun documentacion del proyecto | Pin FPGA |
|---|---|---:|
| CS_n | PS1 | 65 |
| MOSI desde maestra | PS2 | 64 |
| MISO hacia maestra | PS3 | 63 |
| SCLK | PS4 | 62 |

Confirmar el conector fisico con `goboard_spi_externo.pcf`. SPI modo 0, 8 bits, MSB primero, hasta 1 MHz; niveles de 3,3 V y tierra comun. VCC del PMOD libre; Go Board alimentada por USB.

Reinicia la Go Board antes de cada serie y espera D1 antes de iniciar la maestra. D1 indica ejecucion; D2 recepcion de precio; D3 lectura de PRICE; D4 alguna decision no nula. D4 encendido no demuestra por si solo una operacion ejecutada.

## 3. Primera comprobacion con la maestra

Usa `prueba_spi_48_ticks.csv`, 48 ticks a 100 us o mas. La salida se compara con `miso_esperado_48_ticks.csv`:

- Tick 0: MISO `0x00` (inicial).
- Tick 1: MISO `0x7F` (comprar 63).
- Tick 2: MISO `0x64` (comprar 36).
- Tick 33: MISO `0xBF` (vender 63).
- Tick 34: MISO `0xA4` (vender 36).
- Final: caja $9.980, acciones 0, cuatro ordenes, comisiones $20.

Los indices comienzan en cero. Una decision calculada en tick n sale por MISO en n+1 y se ejecuta a ese precio siguiente. Si MISO permanece siempre en cero, la prueba falla. Reinicia de nuevo para comenzar cualquier serie de 20.000 ticks.

## Estado de la entrega

Validacion digital aprobada: 160.000 ticks Python/RV32E/RTL; bancos oficiales adaptados 4/4; escenarios Icarus y tres cadencias; sintesis y netlist. Uso: 1.257/1.280 LC y 9/16 BRAM. Espino funciona a 12,5 MHz; peor latencia observada 25,68 us.

**Programacion y funcionamiento fisico: pendientes hasta que los realices.** El agente no ejecuto iceprog. La estrategia supera mantener en 6/8 muestras conocidas; peor patrimonio $8.615 y drawdown maximo 61,11%. No se ha demostrado superioridad en series secretas. El informe y la evidencia resumida estan incluidos; las fuentes y logs completos permanecen en `Proyecto_4_Arquitectura-main/proyecto4/alternativas/competitiva_definitiva/` del espacio de trabajo.
'''

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    subprocess.run([sys.executable, '-X', 'utf8', '-B', str(HERE/'auditar_entrega.py')], cwd=ROOT, check=True)
    assert not DEST.exists() and not ARCHIVE.exists(), 'No sobrescribir una entrega existente'
    DEST.mkdir()
    for source, name in [
        (HERE/'build/competition.bin','competition.bin'), (HERE/'trade.hex','trade.hex'),
        (HERE/'trade.s','trade.s'), (HERE/'INFORME_FINAL.md','INFORME_FINAL.md'),
        (ROOT/'proyecto4/pruebas_fisicas/spi_externo_robusto/goboard_spi_externo.pcf','goboard_spi_externo.pcf'),
        (HERE/'resultados/auditoria_entrega.json','auditoria_entrega.json'),
        (HERE/'build/resultados.json','resultados_build.json'),
    ]:
        shutil.copy2(source,DEST/name)
    e=DEST/'evidencia';e.mkdir()
    for name in ['matriz_aceptacion.csv','comparacion_final.csv','comparacion_existentes.csv',
                 'validacion_por_grupos.csv','walk_forward.csv','timing_rondas.csv',
                 'bancos_oficiales.json','equivalencia_rv32e.json','equivalencia_rtl.json',
                 'equivalencia_verilator.json','auditoria_fuentes_cierre.json','seleccion.json']:
        shutil.copy2(HERE/'resultados'/name,e/name)
    for name in ['yosys.log','nextpnr.log','icepack.log']:
        shutil.copy2(HERE/'build'/name,e/name)
    (DEST/'programar.ps1').write_text(PROGRAMAR,encoding='ascii')
    (DEST/'LEEME_PRIMERO.md').write_text(README,encoding='utf-8')
    rows=list(csv.DictReader((HERE/'resultados/sintetico_integracion_cadencias_ticks.csv').open()))
    assert len(rows)==48
    with (DEST/'prueba_spi_48_ticks.csv').open('w',newline='') as f:
        w=csv.writer(f);w.writerow(['tick','price']);w.writerows((r['tick'],r['precio']) for r in rows)
    with (DEST/'miso_esperado_48_ticks.csv').open('w',newline='') as f:
        w=csv.writer(f);w.writerow(['tick','price','miso_hex','decision_nueva_hex','caja','acciones','patrimonio','comisiones_acumuladas'])
        for r in rows:w.writerow([r['tick'],r['precio'],f"0x{int(r['miso']):02X}",f"0x{int(r['decision']):02X}",r['caja'],r['acciones'],r['patrimonio'],r['comisiones_acum']])
    assert [int(rows[t]['miso']) for t in [0,1,2,33,34]]==[0,0x7f,0x64,0xbf,0xa4]
    assert (rows[-1]['caja'],rows[-1]['acciones'],rows[-1]['comisiones_acum'])==('9980','0','20')
    files=sorted(p for p in DEST.rglob('*') if p.is_file())
    (DEST/'SHA256.txt').write_text(''.join(sha(p)+'  '+p.relative_to(DEST).as_posix()+'\n' for p in files),encoding='ascii')
    with zipfile.ZipFile(ARCHIVE,'x',compression=zipfile.ZIP_DEFLATED) as z:
        for p in sorted(DEST.rglob('*')):
            if p.is_file():z.write(p,p.relative_to(WORKSPACE).as_posix())
    with zipfile.ZipFile(ARCHIVE) as z:
        assert z.testzip() is None
        assert sum(n.endswith('.bin') for n in z.namelist())==1
        assert hashlib.sha256(z.read('LISTO_PARA_PROGRAMAR/competition.bin')).hexdigest()==sha(HERE/'build/competition.bin')
    (WORKSPACE/'Pochoco_Trader_programacion_SHA256.txt').write_text(sha(ARCHIVE)+'  '+ARCHIVE.name+'\n',encoding='ascii')
    print('PAQUETE',DEST,'\nZIP',ARCHIVE,'\nSHA256 ZIP',sha(ARCHIVE))

if __name__=='__main__':main()
