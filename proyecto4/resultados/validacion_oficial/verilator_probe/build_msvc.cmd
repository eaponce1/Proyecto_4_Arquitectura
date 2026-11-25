@echo off
call "C:\Program Files (x86)\Microsoft Visual Studio\2019\BuildTools\VC\Auxiliary\Build\vcvars64.bat"
if errorlevel 1 exit /b 1
cd /d "%~dp0"
set "VL=C:\Tools\oss-cad-suite\share\verilator\include"
cl /nologo /O2 /std:c++20 /EHsc /bigobj /wd4996 /D_CRT_SECURE_NO_WARNINGS /DVL_TIME_CONTEXT /I "%VL%" /I "%VL%\vltstd" Vtb_proyecto_4*.cpp "%VL%\verilated.cpp" "%VL%\verilated_timing.cpp" "%VL%\verilated_threads.cpp" /Fe:sim_mmio_r2.exe
exit /b %ERRORLEVEL%
