$ErrorActionPreference='Stop'
Set-Location (Resolve-Path (Join-Path $PSScriptRoot '..\..\..'))
$p='proyecto4/pruebas_fisicas/demo_autonoma_bus_detail'
$b="$p/build"
$bin="$b/selftest.bin"
$hash=(Get-FileHash -LiteralPath $bin -Algorithm SHA256).Hash
Write-Host "Input BIN SHA-256: $hash"
$yosysBin=Split-Path (Get-Command yosys -CommandType Application).Source
$primitives=Join-Path $yosysBin '..\share\yosys\ice40\cells_sim.v'

& iceunpack -u $bin "$b/timeout_from_bin.asc"
if($LASTEXITCODE){throw 'Failed to unpack existing BIN'}
& icebox_vlog -s "$b/timeout_from_bin.asc" | Set-Content -Encoding ascii "$b/timeout_from_bin_raw.v"
if($LASTEXITCODE){throw 'Failed to extract existing BIN logic'}
& python "$p/tb/adaptar_bitstream_icarus.py" "$b/timeout_from_bin_raw.v" "$b/timeout_from_bin_delayed.v"
if($LASTEXITCODE){throw 'Failed to adapt IceStorm output'}
& iverilog -g2012 -s tb_bitstream_timeout -o "$b/tb_bitstream_delayed.vvp" "$p/tb/tb_bitstream_timeout.sv" "$b/timeout_from_bin_delayed.v" $primitives
if($LASTEXITCODE){throw 'Failed to compile reconstructed BIN model'}
& vvp -i "$b/tb_bitstream_delayed.vvp" | Tee-Object "$b/timeout_bitstream_delayed.log"
if($LASTEXITCODE){throw 'Reconstructed BIN failed functional simulation'}
