param([switch]$Context,[switch]$BootBranch,[switch]$FetchWord)
$ErrorActionPreference='Stop'
Set-Location (Resolve-Path (Join-Path $PSScriptRoot '..\..\..'))
$p='proyecto4/pruebas_fisicas/demo_autonoma_bus_detail'
$b="$p/build"
New-Item -ItemType Directory -Force $b | Out-Null
$common=@(Get-ChildItem rtl/espino_core/*.v | ForEach-Object FullName)
$common+=@('pochoco_ram','pochoco_spi_slave','pochoco_sma10' | ForEach-Object {"proyecto4/alternativas/mmio_sma10/rtl/$_.v"})
$common+='proyecto4/alternativas/mmio_sma10/tb/ram_model.v'
$rtl=@(Get-ChildItem "$p/rtl/*.v" | ForEach-Object FullName)
$mode=if($FetchWord){5}elseif($BootBranch){4}elseif($Context){3}else{2}
$output=if($FetchWord){'fetch'}elseif($BootBranch){'arranque'}elseif($Context){'contexto'}else{'uart'}
$unit=if($FetchWord){'tb_timeout_fetch_word'}elseif($BootBranch){'tb_timeout_boot_branch'}else{'tb_timeout_pc_uart'}
foreach($test in @($unit,'tb_demo_autonoma_bus_detail')){
  & iverilog -g2012 -s $test "-P$test.TIMEOUT_DIAG=$mode" -o "$b/${test}_$output.vvp" "$p/tb/$test.sv" @rtl @common
  if($LASTEXITCODE){throw "Compilation failed: $test"}
  & vvp "$b/${test}_$output.vvp" | Tee-Object "$b/${test}_$output.log"
  if($LASTEXITCODE){throw "Failed: $test"}
  if($Context -and $test -eq 'tb_timeout_pc_uart'){
    & vvp "$b/${test}_$output.vvp" +done | Tee-Object "$b/${test}_${output}_done.log"
    if($LASTEXITCODE){throw 'Failed: DONE UART packet'}
  }
  if($BootBranch -and $test -eq $unit){
    & vvp "$b/${test}_$output.vvp" +redirect | Tee-Object "$b/${test}_redirect.log"
    if($LASTEXITCODE){throw 'Failed: conditional redirect injection'}
    & vvp "$b/${test}_$output.vvp" +late | Tee-Object "$b/${test}_late.log"
    if($LASTEXITCODE){throw 'Failed: late polling exit injection'}
  }
  if($FetchWord -and $test -eq $unit){
    & vvp "$b/${test}_$output.vvp" +bad_word | Tee-Object "$b/${test}_bad_word.log"
    if($LASTEXITCODE){throw 'Failed: instruction fetch mismatch injection'}
    & vvp "$b/${test}_$output.vvp" +zero_word | Tee-Object "$b/${test}_zero_word.log"
    if($LASTEXITCODE){throw 'Failed: zero instruction injection'}
  }
}
