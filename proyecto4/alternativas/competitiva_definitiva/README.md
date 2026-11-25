> **Imagen integrada vigente:** usar [competition.bin de la raiz](../../../competition.bin) y la [guia principal](../../../README.md). El BIN de `build/` en esta alternativa conserva el build de desarrollo previo; la integracion actual y sus recursos estan en `../../../build/trader/validacion.json`. La politica y su HEX son los mismos.

# Pochoco Trader — candidata única para validación física

La entrega nueva está aislada de todas las variantes anteriores. Consulta [INFORME_FINAL.md](INFORME_FINAL.md) y [resultados/matriz_aceptacion.csv](resultados/matriz_aceptacion.csv) antes de usarla. El BIN solo se crea cuando pasan las puertas digitales; las pruebas físicas siguen pendientes.

La política es Momentum32 con trailing stop de 20 puntos: exposición inicial alcista, revisión cada 8 ticks, salida con delta32 <= -16 o caída de 20 desde el pico de la posición; reentrada con delta32 >= 6. Espino calcula cada decisión. La contabilidad aplica primero la orden pendiente al precio recibido, con comisión $5 y recorte de cantidad a caja/inventario. Puede perder gran parte del capital en saltos bruscos.

En las ocho muestras conocidas supera a mantener en 6/8; peor patrimonio $8.615 y máximo drawdown porcentual 61,11%. El procedimiento obtiene ventaja en 5/8 series excluyendo empresa y en 14/24 ventanas walk-forward. Esto NO demuestra superioridad en series secretas. Momentum32 original reproduce exactamente los ocho resultados proporcionados; la candidata añade protección ante caída gradual a costa de otros resultados. La revisión y sus limitaciones están documentadas.

## Artefactos y evidencia

- Firmware: [trade.s](trade.s), [trade.hex](trade.hex).
- Imagen: `build/competition.bin`, únicamente si existe junto a `build/resultados.json` y pasa el manifiesto [SHA256_entrega.txt](SHA256_entrega.txt).
- Equivalencia completa: `resultados/equivalencia_rv32e.json`, `resultados/equivalencia_verilator.json` y CSV de cada tick.
- Icarus: `resultados/equivalencia_rtl.json`, `build/rtl/`, bancos y diffs en `build/oficial/`.
- Síntesis y rutas: `build/yosys.log`, `build/nextpnr.log`, `build/timing.json`, `build/fuentes_validadas.json`.
- Investigación: `resultados/comparacion_existentes.csv`, `comparacion_final.csv`, `validacion_por_grupos.csv`, `walk_forward.csv`, `sensibilidad.csv`, `estadisticas_*.csv` y gráficos PNG.

## Reproducir

Desde la raíz `Proyecto_4_Arquitectura-main`, Python 3, Icarus/VVP y OSS CAD Suite en PATH. Para las series completas se usa Ubuntu WSL con Python, g++ y make. El ejecutor extrae temporalmente el paquete Verilator si no está disponible; no instala paquetes del sistema. La investigación gráfica necesita matplotlib y numpy. Los datos están incluidos en `datos/`.

```powershell
$p = 'proyecto4/alternativas/competitiva_definitiva'
python -X utf8 -B "$p/test_invariantes.py"
& "$p/ejecutar_pruebas.ps1"
# En una copia limpia sin build/competition.bin:
& "$p/sintetizar.ps1"
python -X utf8 -B "$p/generar_informe.py"
python -X utf8 -B "$p/auditar_entrega.py"
```

La selección está congelada en `resultados/seleccion.json`. Para repetir TODA la investigación, usar una copia independiente y ejecutar `python -X utf8 -B "$p/validar_estrategia.py"`; ese comando recalcula los resultados de desarrollo. No usarlo para ajustar mirando una serie secreta. `revision_v1_descartada/` conserva la revisión anterior. No sobrescribir respaldos históricos.

Para ejecutar también los ocho casos completos en Icarus (mucho más lento):

```powershell
python -X utf8 -B "$p/validar_rtl.py"
```

Verilator verifica los 160.000 ticks a la cadencia real de 100 µs, pero opera en dos estados. Icarus comprueba X y ejecuta los casos adversos y las tres cadencias. Las corridas largas iniciales de Icarus se interrumpieron y NO son evidencia PASS. Ambos bancos oficiales usan adaptaciones explícitas de interfaz y reloj, preservando literalmente su contabilidad y aserciones; consultar sus diffs.

## Prueba física manual — no ejecutada

Realizar únicamente cuando la matriz confirme todas las puertas digitales. No existe una afirmación de funcionamiento físico de este BIN. Conservar una imagen física anterior de respaldo y registrar canal, CSV, ronda, hash y resultado de cada sesión por separado.

Los siguientes comandos son para que el usuario los ejecute manualmente; el agente no los ejecutó:

```powershell
$p = 'proyecto4/alternativas/competitiva_definitiva'
$bin = Join-Path $p 'build/competition.bin'
$meta = Get-Content (Join-Path $p 'build/resultados.json') -Raw | ConvertFrom-Json
if ((Get-FileHash -Algorithm SHA256 -LiteralPath $bin).Hash.ToLowerInvariant() -ne $meta.sha256_bin) {
    throw 'BIN distinto al validado'
}
if ((Get-FileHash -Algorithm SHA256 -LiteralPath (Join-Path $p 'trade.hex')).Hash.ToLowerInvariant() -ne $meta.sha256_hex) {
    throw 'HEX distinto al validado'
}
iceprog $bin
if ($LASTEXITCODE -ne 0) { throw 'Fallo programacion' }
iceprog -c $bin
if ($LASTEXITCODE -ne 0) { throw 'Fallo verificacion flash' }
```

PCF usado sin cambios: PS1 CS_n/pin 65; PS2 MOSI/64; PS3 MISO/63; PS4 SCLK/62. Entrada de reloj pin 15, 25 MHz; Espino funciona a 12,5 MHz. Confirmar físicamente el conector según la placa y el PCF. SPI modo 0, 8 bits MSB primero, hasta 1 MHz, señales 3,3 V, GND común; VCC del PMOD libre y Go Board alimentada por USB.

Tras programar, reiniciar antes de la serie y esperar el LED de ejecución D1 antes de iniciar la maestra (POR tarda unos 82 µs). D2 registra recepción SPI, D3 lectura de PRICE y D4 una DECISION no nula. Una serie nueva exige reinicio físico; el protocolo no contiene un comando de reinicio de cartera.

Usar primero la serie sintética `integracion_cadencias` (48 ticks): `[100]*8 + [220]*24 + [100]*16`. Esperar compra `0x7F` calculada en tick 0 y recibida por MISO en tick 1; venta `0xBF` calculada en tick 32 y recibida en tick 33. Registrar ambos bytes, inventario y comisiones; un retorno siempre cero debe fallar la prueba. Después ejecutar los 20.000 ticks del CSV elegido. La primera decisión calculada después del último tick no se ejecuta sin una trama adicional.

Una compilación, simulación o síntesis aprobada no sustituye esa prueba con la Go Board y la FPGA maestra.
