# Demostración integral SPI del Pochoco SoC

La captura física previa 0101 queda preservada en pc_probe_aprobado.zip, que contiene sus fuentes, scripts, vectores, PCF y BIN. SHA-256 del BIN aprobado: CF9C849A1D7FAFD710D66B021CC5C9053A7CB7B9806D86BA69061D46201AF25C. SHA-256 del ZIP: 082922E4F5F8E98794CCE35E0344EA8C099AF07DAD1FDE67946C64E6CC9722E2.

El monitor nuevo usa señales de observación. Mantiene un índice saturado de precios y cinco flags del tick actual. El conteo de cada acceso equivale a los ticks cerrados más su flag del tick actual. Un precio siguiente exige que el anterior tenga PRICE, SUM10, READY, DECISION y MISO. Las solicitudes de un mismo tipo mantenidas en ciclos consecutivos se cuentan una vez. Los vectores de referencia en data/ alimentan las comparaciones de precio, DECISION y MISO. La primera respuesta MISO corresponde al valor inicial. Las siguientes corresponden a la decisión anterior.

El maestro comparte un contador de 13 bits para el intervalo entre tramas y el watchdog. En WAIT_ACK, el ACK válido inhibe el timeout en el mismo flanco y reinicia el contador. En DONE, el watchdog se desarma cuando se completa el último tick, incluidos los eventos que llegan en el flanco actual. Un hito de monitor ausente tras completar los 16 ticks se reporta como error de secuencia. El error queda enclavado. Los hitos normales son acumulativos. Si llegan juntos, todos se retienen y el código puede saltar al último hito consecutivo observado. Un código significa que se observaron todos los hitos anteriores. Los códigos intermedios pueden durar muy poco para percibirlos a simple vista.

| D4..D1 | Hito |
|---|---|
| 0000 | Reset o espera del primer precio |
| 0001 | Primer precio SPI recibido |
| 0010 | Primer commit posterior al precio en PC 0x14 |
| 0011 | Respuesta STATUS con new_price=1 |
| 0100 | Lectura PRICE |
| 0101 | Lectura SUM10 |
| 0110 | Lectura READY |
| 0111 | Escritura DECISION |
| 1000 | Respuesta MISO recibida |
| 1001 | 16 ticks completos |
| 1010 | PASS integral de los vectores y la secuencia |
| 1011 | Precio duplicado o incorrecto |
| 1100 | DECISION duplicada, prematura o incorrecta |
| 1101 | MISO incorrecto |
| 1110 | Trama, acceso o secuencia SMA fuera de orden, o hito de cierre faltante con los 16 ticks completos |
| 1111 | Expiró la espera de ACK o el último tick sigue pendiente |

## Reproducción desde pochoco_soc-main

```powershell
powershell -ExecutionPolicy Bypass -File proyecto4/pruebas_fisicas/demo_autonoma_bus_detail/ejecutar_pruebas.ps1
powershell -ExecutionPolicy Bypass -File proyecto4/pruebas_fisicas/demo_autonoma_bus_detail/sintetizar.ps1
```

- Icarus unitario aprobado. El monitor prueba simultaneidad, solicitud mantenida, DECISION duplicada, precio sobrescrito, MISO incorrecto y timeout.
- Icarus integrado aprobado con LED 1010, 16 precios, 16 lecturas de cada registro PRICE, SUM10 y READY, 16 DECISION, 16 MISO y 15 ACK en orden. El log build/simulacion_integrada.log incluye la comparación exacta con los vectores Python y la traza del primer commit.

- El build histórico con error genérico utilizó 1.082 LUT4 y 9 BRAM. El PCF asigna cinco pines únicos y el chequeo de netlist aprobó.
- La versión histórica de error genérico ocupó 1.273/1.280 LC. Fmax final 39,90 MHz y PASS a 25 MHz. Quedan 7 LC libres. El objetivo preferido de 1.220 LC quedó a 53 LC.
- La compilación histórica generó build/demo_autonoma_bus_detail.bin. SHA-256 B1E855DE663F99A2C796495CB09C8CF08E538B231FA82CC777D846E286EBE430.
- La comprobación física integral sigue pendiente.

## Auditoría de área

| Implementación medida | LUT4 | LC | LC recuperadas |
|---|---:|---:|---:|
| Monitor integral original | 1117 | 1331 | — |
| Índice y temporizador del maestro reutilizados y segundo registro MISO eliminado | 1104 | 1305 | 26 |
| Comparación MISO bit a bit y contabilidad por trama | 1094 | 1293 | 12 |
| Índice de 4 bits y código LED derivado de los flags | 1082 | 1273 | 20 |

Los logs completos se conservan en build/. La ocupación del PC Probe con evidencia física fue 1140 LC, frente a 1331 del monitor inicial. Además de la lógica de diagnóstico, la comparación integral mantiene vivo el camino de recepción MISO que el PC Probe podía podar.

La netlist inicial asignó 95 LUT4 y 63 FF con prefijo u_monitor, incluyendo el watchdog, los flags de transacción y el estado del indicador. nextpnr reportó 930 celdas LUT4 sin FF, 187 con LUT4 y FF y 181 solo con FF. El mayor grupo de nombres en la netlist es u_soc.u_ram, 726 LUT4 y cuatro BRAM. La síntesis plana comparte y renombra lógica que usa datos de RAM, por lo que ese prefijo no equivale al costo aislado de la RAM. Las nueve BRAM se atribuyen a RAM principal (4), banco de registros (4) e historial SMA10 (1). La diferencia de LC entre ejecuciones es la medida de ahorro, no la suma de prefijos.

Los bytes previstos son 00, 50 y 90, así que se pueden representar con dos bits en la referencia. La lectura de la ROM constante ya permite a síntesis eliminar los cinco bits siempre cero. La comparación conserva los ocho bits transmitidos, incluidos los que deben ser cero. El maestro acumula un único flag de discrepancia al muestrear cada bit de MISO. Icarus conserva también el byte ensamblado y lo coteja con el vector original. No se modificó el formato DECISION ni los vectores Python.



## Objetivos y programación manual

Desde pochoco_soc-main:

```powershell
$p = 'proyecto4/pruebas_fisicas/demo_autonoma_bus_detail'
powershell -ExecutionPolicy Bypass -File "$p/sintetizar.ps1"
powershell -ExecutionPolicy Bypass -File "$p/verificar_arranque.ps1"
vvp "$p/build/arranque_actual.vvp" +bad_miso
python -B "$p/comparar_python.py"
python -B "$p/competition.py"
```

- selftest usa demo_autonoma_bus_detail_top, goboard_demo_autonoma_bus_detail.pcf y su generador local. Salida build/selftest.bin, SHA-256 50D8B7AE550978409E9EF97A324F09C3E13FDDD9D4B52D574D6376172FE5CF86. Yosys -dff, 1.070 LUT4, 1.258/1.280 LC y 9 BRAM. Fmax post-route de 39,52 MHz y PASS a 25 MHz. El selftest anterior queda en selftest_antes_watchdog.zip.
- competition usa trade_top y goboard.pcf, sin generador ni datos del autotest. Salida build/competition/competition.bin, SHA-256 0150BF6FCE608FD463B15EB945F84354B151E581C71A36B47629E889EC0B6DFD. 1055 LUT4, 1279 LC, 13 BRAM, Fmax 40,50 MHz.
- Ambas imágenes cargan el firmware MMIO base de 71 palabras. Su SHA-256 es B7611ED78166A6E503EB09E4082FDD0C5811118CF08E68DEF32CE1ECD9C77706. Para verificar un ensamblado sin tocar el HEX de entrega, usar python sw/assembler.py proyecto4/alternativas/mmio_sma10/sw/trade.s -o con una ruta temporal distinta de trade.hex, y comparar hashes.

El primer error queda fijo en el registro LED hasta reset. Prioridad en el mismo flanco: 1011 precio, 1100 DECISION, 1101 MISO, 1110 secuencia, 1111 timeout. La prueba de inyección MISO obtiene 1101 en flanco 531. Las pruebas de monitor registran el ciclo de cada caso en build/selftest_errores.log. La netlist contiene los cuatro FF SB_DFFE del POR. La corrección de los dos defectos reproducidos está validada en simulación. La prueba física con el BIN corregido sigue pendiente.

Primero, con la maestra desconectada, verifica el hash y programa manualmente selftest:

```powershell
Get-FileHash "$p/build/selftest.bin"
iceprog "$p/build/selftest.bin"
```

Usa el SHA-256 del selftest corregido indicado arriba. Tras VERIFY OK y reinicio, espera 1010 (D4 y D2). Si queda un código de error, registra los cuatro LEDs. 1010 acredita los 16 ticks de este autotest local.

Para competir, programa manualmente la otra imagen:

```powershell
Get-FileHash "$p/build/competition/competition.bin"
iceprog "$p/build/competition/competition.bin"
```

Conecta GND común y señales de 3,3 V. PMOD PS4 SCLK (pin 62), PS2 MOSI (64), PS1 CS_n (65) y PS3 MISO (63), este último independiente del resto de los grupos. SPI modo 0, 8 bits, MSB primero y SCLK hasta 1 MHz. La trama n emite la DECISION que estaba escrita al iniciarla, calculada a partir del precio n−1. Conserva la misma imagen para las tres rondas. La competencia física sigue pendiente.

## Reproducir las rondas pendientes

Desde pochoco_soc-main, cada comando genera una corrida oficial de 20.000 ticks. Los resultados de ronda 3 se conservan.

```powershell
foreach ($r in 1,2) {
    foreach ($v in 'mmio','software') {
        python -B proyecto4/resultados/validacion_oficial/ejecutar_validacion.py --variant $v --round $r
        if ($LASTEXITCODE -ne 0) { throw "Falló la corrida $v en ronda $r" }
    }
}
```

Las cuatro corridas se lanzaron en esta revisión y estaban en curso al generar el informe. El cotejo Python disponible compara los CSV completos de ronda 3. La herramienta de síntesis no usa esos CSV para construir competition.


## Regresión del watchdog corregido

Los flancos se cuentan desde el primer flanco del reloj.

| Caso | Flanco | Resultado |
|---|---:|---|
| Arranque e IDLE sin SPI | 100 y 1.000 | Sin error |
| ACK un ciclo antes del umbral | 8.721 | ACK aceptado, contador cero y la secuencia llega a 1010 |
| ACK en el umbral | 8.722 | ACK aceptado, contador cero y la secuencia llega a 1010 |
| ACK posterior al umbral | 8.722 / 8.723 | 1111 en 8.722, retenido después del ACK en 8.723 |
| ACK ausente y reset | 8.722 / 8.723 | 1111 real, luego reset a 0000 |
| Repetición completa tras reset | 107.006 | 1010, 16 decisiones y 16 MISO cotejados |
| Autotest nominal | 98.283 | 1010 retenido hasta 106.480 |
| 16 ticks completos con hito omitido | 98.281 | 1110 retenido hasta 106.480 |
| Último tick incompleto | 106.447 | 1111 real, se suprime la última DECISION en el banco |

El script sintetizar.ps1 elimina el BIN de salida, ejecuta Icarus unitario e integrado, las siete trazas de watchdog, arranque, inyección MISO y comparación Python. Solo empaqueta si todo pasa y nextpnr cumple el límite de área y el reloj de 25 MHz. En build/ quedan los CSV timeout_*.csv, simulacion_integrada.log, los logs de regresión, yosys.log y nextpnr.log. diagnostico_timeout_1111.md conserva la reproducción del defecto anterior y explica la corrección.

La simulación funcional del circuito extraído de este mismo selftest.bin dio 1001 en 98.282, 1010 en 98.283 y conservó 1010 hasta 110.000. Para repetirla, ejecutar verificar_bin_existente.ps1. Su log es build/timeout_bitstream_delayed.log. La decodificación del BIN no reprograma la placa.

## Imagen temporal para distinguir WAIT_ACK de DONE en placa

Usar **build/timeout_diagnostico.bin** para esta prueba. La imagen conserva firmware, SPI, manejo de ACK y verificaciones del selftest. El parámetro TIMEOUT_DIAG habilita únicamente la captura y la salida LED diagnósticas. El selftest corregido y selftest_antes_watchdog.zip conservan sus hashes.

| D4…D1 | Interpretación en timeout_diagnostico.bin |
|---|---|
| 0000 | Reset o ejecución en curso |
| 0001 | WAIT_ACK. Se recibió el byte. No se observó consulta STATUS posterior al byte ni lectura PRICE |
| 0010 | DONE. La última DECISION se observó, pero falta otro evento para completar el último tick |
| 0011 | WAIT_ACK. El monitor observó lectura PRICE, pero el maestro no tenía ACK válido al vencer el contador |
| 0100 | WAIT_ACK. No se observó byte_done para la trama de este tick |
| 0101 | DONE. Falta la última escritura DECISION |
| 0110 | WAIT_ACK. Hubo consulta STATUS después del byte, sin observar respuesta con new_price=1 ni lectura PRICE |
| 0111 | WAIT_ACK. Se observó respuesta STATUS con new_price=1, sin lectura PRICE |
| 1010 | PASS integral de los 16 ticks |
| 1011 | Precio duplicado o incorrecto |
| 1100 | DECISION duplicada, prematura o incorrecta |
| 1101 | MISO incorrecto |
| 1110 | Error de secuencia o hito faltante |
| Otros | Reservados en la imagen diagnóstica |

El código 0011 acredita el evento que debería producir el ACK, la lectura de PRICE. El snapshot verifica el ACK válido a la entrada del maestro y el pulso registrado ACK aceptado de forma separada. En un WAIT_ACK conforme al RTL, un ACK válido en ese flanco inhibe el timeout. La ausencia del byte puede disparar 1110 antes de que venza el contador si llega una respuesta sin un tick abierto. En la prueba de 0100 se aisló el timeout de ese fallo anterior, que permanece habilitado en el hardware. El primer código de error se conserva hasta reset.

La captura toma en el flanco del timeout el estado del maestro, el índice, ACK válido, ACK aceptado, frame_start, byte_done, price_pending, DECISION observada, master_done y final_complete. price_pending replica la bandera new_price_q del esclavo con prioridad de byte_done sobre lectura PRICE. Icarus coteja la réplica con el registro real. Se verificó que la netlist conserva 14 FF de captura. El bit de validez implica gap_count=8191, timeout_enable=1 y rst_ni=1. El estado se codifica con su bit diferente en WAIT_ACK=5 y DONE=7. En esos estados sent_count es el índice de trama más uno, y decision_count es el índice más la DECISION del tick actual. El banco coteja los valores reconstruidos con los valores observados. Los LEDs exponen la clasificación; el resto del contexto queda retenido internamente y se imprime completo en simulación. final_complete describe el tick activo y solo corresponde al último de los 16 cuando master_done está activo.

### Resultados ejecutados

| Inyección en Icarus | Flanco | LED |
|---|---:|---|
| Byte recibido, sin lectura PRICE ni ACK | 8.722 | 0001 |
| Consultas STATUS, respuesta STATUS forzada a cero | 8.722 | 0110 |
| Hito STATUS válido inyectado al observador y PRICE bloqueado | 8.722 | 0111 |
| PRICE leído, ACK suprimido a la entrada del maestro | 8.722 | 0011 |
| byte_done ausente, con timeout aislado | 8.722 | 0100 |
| Última DECISION suprimida | 106.447 | 0101 |
| Respuesta final omitida solo en el monitor, DECISION presente | 106.447 | 0010 |
| Nominal, 16 precios, 16 DECISION y 16 MISO iguales a los vectores Python | Comprobado hasta 110.000 | 1010 |

En cada inyección se comprobaron el valor de las señales en el flanco, la captura y el código retenido. El caso 0011 comprobó que el código y los datos siguen fijos incluso si el maestro acepta un ACK tardío y cambia a GAP. Los flancos de timeout de la tabla corresponden a los escenarios del banco. Un timeout de una trama posterior en placa puede tener otro flanco.

El primer mapeo de la captura ocupó 1.314 LC y no se empaquetó. La captura compacta y la visualización sin hitos intermedios ocuparon 1.279/1.280 LC, 1.081 LUT4 y 9/16 BRAM. nextpnr HX1K/VQ100 aprobó 25 MHz y estimó 40,25 MHz post-route. Los reportes están en build/timeout_diagnostico_yosys.log y build/timeout_diagnostico_nextpnr.log. Los logs de captura se llaman build/timeout_diagnostic_*.log.

### Compilar y programar manualmente

Desde la raíz pochoco_soc-main:

```powershell
$p = 'proyecto4/pruebas_fisicas/demo_autonoma_bus_detail'
powershell -NoProfile -ExecutionPolicy Bypass -File "$p/sintetizar.ps1" -TimeoutDiagnostic
$bin = "$p/build/timeout_diagnostico.bin"
Get-FileHash -Algorithm SHA256 $bin
iceprog $bin
```

El hash esperado del BIN diagnóstico es **FF757BD2942B489159B07F8D811E0F5B5F80F957B849E1FFD9F073BDD530899C**. El selftest corregido sigue en build/selftest.bin con SHA-256 50D8B7AE550978409E9EF97A324F09C3E13FDDD9D4B52D574D6376172FE5CF86. Tras VERIFY OK, reiniciar y registrar D4…D1. La imagen diagnóstica previa (SHA-256 9866F3D8D4F08241D59D3509B043AAF2508A2FCDDD174D6A2BBEDC0926C26742) mostró D1 solo según la observación del usuario. Eso identifica WAIT_ACK con el byte recibido y sin lectura PRICE. Su BIN y fuentes están archivados en timeout_diagnostico_d1_aprobado.zip. El nombre del ZIP indica una lectura diagnóstica confirmada, no un PASS integral. Falta probar la revisión nueva para separar 0001, 0110 y 0111 en placa.

