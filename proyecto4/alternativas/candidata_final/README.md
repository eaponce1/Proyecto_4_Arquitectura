> **Referencia de investigacion y validacion.** La imagen activa para programar se encuentra en la raiz del repositorio: [guia actual](../../../README.md). Este directorio conserva fuentes que necesitan los comparadores y bancos; sus builds y documentos completos anteriores estan en el [historial previo](https://github.com/eaponce1/Proyecto_4_Arquitectura/tree/66eede4c46e211c02dc5ef22de18f86e22e775c5/proyecto4/alternativas/candidata_final). Los comandos y resultados historicos de abajo no identifican el BIN vigente.

# Candidata de Pochoco Trader

Firmware de investigación basado en tendencia y confirmación SMA10, con posición objetivo escalonada y contabilidad exacta de la orden del tick anterior. El [informe](INFORME.md) registra la evidencia física, el diagnóstico, la validación digital y el resultado fuera de muestra.

Descargas locales de la candidata verificada digitalmente: [BIN](build/competition.bin), [Assembly](trade.s), [HEX](trade.hex), [PDF](INFORME.pdf) y [manifiesto SHA-256](SHA256_entrega.txt).

## Ejecutar en Windows

Desde la raíz `pochoco_soc-main`, con Python, Icarus y OSS CAD Suite en PATH:

```powershell
$p = 'proyecto4/alternativas/candidata_final'
Get-Command python, iverilog, vvp, yosys, nextpnr-ice40, icepack
python -X utf8 -B "$p/backtest.py"
if ($LASTEXITCODE -ne 0) { throw 'Fallo el backtest' }
python -B sw/assembler.py "$p/trade_candidate.s" -o "$p/trade_candidate.hex"
if ($LASTEXITCODE -ne 0) { throw 'Fallo el ensamblado' }
python -X utf8 -B "$p/validar_candidata.py"
if ($LASTEXITCODE -ne 0) { throw 'Fallo la validacion o el build' }
python -X utf8 -B "$p/diagnosticar_candidata.py"
if ($LASTEXITCODE -ne 0) { throw 'Fallo el diagnostico por escenario' }
```

El ejecutor entrega `build/competition.bin` solo si el HEX coincide, la cartera y decisiones cotejan con Python, el banco termina los 20.000 ticks y las pruebas RTL y de puertas, síntesis y P&R aprueban. Para reproducir la huella usa un directorio limpio con las mismas rutas relativas y versiones. `--salida <otra_carpeta>` valida su propia imagen. Un cambio en la ruta del HEX puede cambiar nombres de celdas y el resultado de enrutado. El banco conserva SPI de 1 MHz y usa períodos de 30 µs para la serie completa y 100 µs para el ensayo RTL de reserva. La estimación de margen en las tres rondas usa los ciclos medidos. El reloj real de Espino es 12,5 MHz y nextpnr tiene restricción de 25 MHz para el target iCE40 HX1K/VQ100.

Se usaron Python 3.13.3, Icarus/VVP 14.0 devel `s20260301-626-g7e3d0c6bd-dirty`, Yosys 0.70+176 `365bb887b` y nextpnr-ice40 0.11.1-68 `g1daf1f5c`. El ejecutable `icepack.exe` tiene SHA-256 `A5BEEC407C1A0AE8D22547DB91F9818A182CF3D2BB5BE552ACBF97A77227CB7F`.

Para medir la política congelada con otro CSV compatible `tick,price` de 20.000 filas:

```powershell
python -X utf8 -B "$p/backtest.py" --solo-evaluar --serie .\ruta\serie.csv --salida .\resultados_otra_serie
```

## Ensayo físico manual

Con la Go Board conectada solo por USB, verificar el SHA-256 de `build/competition.bin` contra `build/resultados.json`. Con el canal del grupo confirmado, programar solo la Go Board. El BIN candidato requiere su propia verificación física.

```powershell
$p = 'proyecto4/alternativas/candidata_final'
$bin = "$p/build/competition.bin"
$esperado = (Get-Content "$p/build/resultados.json" -Raw | ConvertFrom-Json).sha256_bin
if ((Get-FileHash -Algorithm SHA256 $bin).Hash -ne $esperado) { throw 'BIN distinto al validado' }
iceprog $bin
if ($LASTEXITCODE -ne 0) { throw 'Fallo la programacion' }
iceprog -c $bin
if ($LASTEXITCODE -ne 0) { throw 'Fallo la verificacion de flash' }
```

Con el conector de prueba aislado, conectar GND común y las señales de 3,3 V. La Go Board se alimenta por USB. El VCC del PMOD queda libre.

| PMOD | Señal | Pin FPGA |
|---|---|---:|
| PS1 | CS_n activo en bajo | 65 |
| PS2 | MOSI desde la maestra | 64 |
| PS3 | MISO hacia la entrada del canal del grupo | 63 |
| PS4 | SCLK desde la maestra | 62 |

El reloj de entrada de 25 MHz usa pin 15. D1 se enciende al ejecutar Espino, D2 al recibir un byte, D3 al leer PRICE y D4 al escribir la primera decisión no nula. Con el CSV de práctica exacto y tick 0 tras reiniciar, la primera compra aparece por MISO en tick 385 como `0x60` y la primera venta en tick 1025 como `0xA0`. Cotejar ambos retornos y registrar la huella del BIN, el canal, el período y el CSV usados. [PCF y protocolo implementado](../../pruebas_fisicas/spi_externo_robusto/README.md)

