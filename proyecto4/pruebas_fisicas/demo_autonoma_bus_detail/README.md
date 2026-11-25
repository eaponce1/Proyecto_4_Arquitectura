> **Referencia de investigacion y validacion.** La imagen activa para programar se encuentra en la raiz del repositorio: [guia actual](../../../README.md). Este directorio conserva fuentes que necesitan los comparadores y bancos; sus builds y documentos completos anteriores estan en el [historial previo](https://github.com/eaponce1/Proyecto_4_Arquitectura/tree/66eede4c46e211c02dc5ef22de18f86e22e775c5/proyecto4/pruebas_fisicas/demo_autonoma_bus_detail). Los comandos y resultados historicos de abajo no identifican el BIN vigente.

﻿# Demostración integral SPI del Pochoco SoC

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

## Reproducir las rondas 1 y 2 de práctica

Desde pochoco_soc-main, cada comando genera una corrida oficial de 20.000 ticks. Los resultados de ronda 3 se conservan.

```powershell
foreach ($r in 1,2) {
    foreach ($v in 'mmio','software') {
        python -B proyecto4/resultados/validacion_oficial/ejecutar_validacion.py --variant $v --round $r --fast-idle
        if ($LASTEXITCODE -ne 0) { throw "Falló la corrida $v en ronda $r" }
    }
}
```

Las cuatro corridas completaron 20.000 ticks y aprobaron los cuatro criterios. Las decisiones coinciden con Python en las tres rondas. Los ciclos, los tiempos de ejecución de Icarus y los archivos de respaldo se detallan en el [informe de las tres rondas](../../resultados/validacion_oficial/informe_comparativo_tres_rondas.md).


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


### Seguimiento tras observar D1 en la revisión FF757BD2

La flash de la placa coincidió con la revisión FF757BD2 por iceprog -c (VERIFY OK). El usuario observó D1 solo, que en esa revisión confirma recepción del byte y ausencia de lectura STATUS posterior al byte y de lectura PRICE.

La siguiente revisión mantiene la misma ruta build/timeout_diagnostico.bin y distingue el caso anterior con dos observaciones sticky por tick. 0001 significa sin commit ni solicitud de datos tras el byte. 1000 significa que Espino hizo commit pero no emitió una solicitud de datos. 1001 significa que hubo solicitud de datos y ninguna se reconoció como lectura STATUS. Los códigos 0110, 0111 y 1010 conservan su significado. Las tres inyecciones nuevas pasaron en Icarus y conservaron la captura. El nominal pasó 16 precios, decisiones y respuestas MISO con 15 ACK. Los bits de captura ACK aceptado y frame_start se reconstruyen como cero bajo timeout, porque sus transiciones llevan a GAP y LOW respectivamente. master_done se deriva del estado DONE en el flanco de timeout. El banco comprobó las reconstrucciones contra las señales originales.

La nueva compilación ocupa 1.277/1.280 LC. Info: Max frequency for clock 'i_Clk$SB_IO_IN_$glb_clk': 39.69 MHz (PASS at 25.00 MHz). SHA-256: 4B839740C68EE945C18B85EAFCF310454C75AB7C0B965CF4B73C372B4EC1FA1E. El BIN FF757BD2 quedó en timeout_diagnostico_status_d1.zip. La revisión nueva aún no tiene resultado físico.

### Seguimiento tras observar D4 en la revisión 4B839740

La placa dio VERIFY OK con esta revisión y el usuario observó D4 solo. El monitor registró al menos un commit tras el byte SPI, sin solicitud de datos posterior. Este resultado no identifica todavía el PC donde se detuvo el flujo.

La siguiente revisión clasifica el último PC que hizo commit en esa condición. 0101 es 0x14 (lw STATUS), 0110 es 0x18 (andi), 0111 es 0x1C (beq), y 1000 es un PC distinto. 0001 conserva la ausencia de commits y solicitudes. 1001 indica solicitud posterior sin PRICE observado. El watchdog final pendiente usa 0010. En esta revisión 0110 y 0111 tienen el significado de PC indicado aquí, no el significado STATUS de la versión anterior. 1010 conserva el PASS nominal.

El BIN anterior está en timeout_diagnostico_bus_d4.zip. La revisión de PC pasó las inyecciones de cada clase, incluyendo una dirección 0x114 para descartar alias de bits bajos, e Icarus completo con 16 DECISION y MISO coincidentes con Python. El flujo completo se reproduce con sintetizar.ps1 -TimeoutDiagnostic -Mapping default. La imagen ocupa 1.280/1.280 LC. Info: Max frequency for clock 'i_Clk$SB_IO_IN_$glb_clk': 35.18 MHz (PASS at 25.00 MHz). SHA-256: E02DAC67FC7D0DDE0C268D50D37A04FCBC19926AA0BCA22D21D89F6D91182BD3. La nueva prueba física está pendiente.

### Lectura completa por USB tras observar D4 en E02DAC67

La flash coincidió con E02DAC67 (VERIFY OK). D4 en esa revisión identifica un timeout sin solicitud de datos posterior al byte y con último commit observado fuera de 0x14, 0x18 y 0x1C. No informa el PC exacto.

La sonda temporal build/timeout_uart.bin toma PC_ID e instrucción completos antes del timeout y los envía por el USB de la Go Board a 115200 baudios, 8N1, en un registro A5 + PC_ID de 32 bits + instrucción de 32 bits, en little-endian. La captura usa cuatro BRAM y el TX usa el pin 74 ya usado para el eco UART. Los LEDs indican 0000 durante ejecución sin error observado, 1000 por timeout y 1101 por fallo MISO. Esta sonda físicamente conserva el control SPI, la decisión de Espino, el cálculo SMA10, el comparador MISO y el watchdog, que en esta imagen espera la DECISION al final. El monitor integral sigue cotejándose en simulación. La sonda no reemplaza el selftest ni la imagen de competencia.

Ejecutar desde pochoco_soc-main:

```powershell
$p = 'proyecto4/pruebas_fisicas/demo_autonoma_bus_detail'
powershell -ExecutionPolicy Bypass -File "$p/sintetizar.ps1" -TimeoutUART -Mapping default
iceprog "$p/build/timeout_uart.bin"
python "$p/leer_timeout_uart.py" --port COM10
```

El lector abre COM10 primero, verifica la flash con iceprog -c y deja salir a la FPGA de reset para capturar el informe breve. No escribe la flash. Devuelve PC_ID, INSN y la comparación contra trade.hex si el PC está dentro del código. Conservar la salida completa.

La prueba de UART decodificó en Icarus 0x00004120 y 0xDEADBEEF después del timeout inyectado, y comprobó que un cambio de PC posterior conserva el registro enviado. El banco integral pasó los 16 precios y bytes MISO/DECISION frente a Python. Los logs están en build/compilacion_timeout_uart.log y build/timeout_uart_nextpnr.log.
Sonda UART: 1.275/1.280 LC y 13 BRAM. Info: Max frequency for clock 'i_Clk$SB_IO_IN_$glb_clk': 38.86 MHz (PASS at 25.00 MHz). SHA-256: 681F0B048C11CF309D3114DD96B2A796B67403A79150B6DCE728BF5267CEDCE1.

La lectura física de esa imagen devolvió dos veces `PC_ID=0x00000048 INSN=0x00048863`, con la palabra verificada contra `trade.hex`. D4 señala que se enclavó el timeout. El apagado entre encendidos concuerda con el reset de `iceprog -c` al verificar la flash y arrancar otra vez. La captura contiene el último commit registrado en la trama activa antes de vencer el watchdog. Para saber qué trama falló y cómo se comportó el branch, hacen falta el valor de `x9` y el estado del maestro.

En `trade.s`, PC 0x48 es `beq x9,x0,REVISAR_COMISION_VENTA`, con destino 0x58. En la corrida RTL nominal, el branch se ejecutó únicamente en el tick 15, con `x9` de 16 a 0. Al comparar cero con cero, el branch se tomó y el firmware completó la venta. Las redes exportadas de Yosys y reconstruidas desde el ASC conservaron LED 0000 y UART inactiva tras 5 ms de simulación lógica. Las trazas están en `build/tb_uart_branch_ref.log`, `build/timeout_uart_netlist.log` y `build/timeout_uart_routed.log`.

### Contexto del commit durante el timeout

La sonda temporal conserva el reloj, SPI, el Espino, el firmware, el cálculo SMA10 y la comparación MISO. Devuelve el número de trama 1–16, el estado WAIT_ACK o DONE en el flanco del timeout, y el PC, el operando A y la señal de branch tomado registrados en el último commit de esa trama. RS1_VALUE captura la salida A del banco de registros. En PC 0x48, corresponde a `x9`. BRANCH_TAKEN observa la decisión real del comparador. Ese bit ocupa el bit 0 del campo de PC, que vale cero para las instrucciones alineadas del firmware.

| D4…D1 | Estado en esta sonda |
| --- | --- |
| 0000 | Sin timeout ni fallo MISO enclavados |
| 1000 | Timeout enclavado con contexto disponible por UART si hubo un commit en la trama |
| 1101 | Error de comparación MISO enclavado |

La cabecera UART es 0xC0 más el índice de trama para WAIT_ACK y 0xD0 más el índice para DONE. Siguen dos palabras de 32 bits en little-endian con el PC y el resultado del branch, y el operando A, respectivamente. La lectura verifica la flash y reinicia la FPGA antes de esperar los nueve bytes. La sonda sirve para diagnosticar el fallo físico del autotest integral.

Icarus verificó el paquete WAIT_ACK a los 348,86 µs con ACK ausente y el paquete DONE a los 4,25786 ms al omitir el evento de la última DECISION en el monitor. La corrida nominal pasó con 16 precios, DECISION y MISO, 15 ACK en orden y cero diferencias con Python. El flujo para HX1K/VQ100 utilizó 1.277/1.280 LC, 1.098 LUT4 y 13 BRAM. El enrutado cerró a 25 MHz con Fmax de 39,85 MHz. La imagen diagnóstica tiene 32.220 bytes. Su SHA-256 es `18C60ADB78312791F5F0400C943BFCF154A54AC86BD704CBF40BE38234A0FA55`.

Los resultados están en `build/compilacion_timeout_contexto.log`, `build/timeout_contexto_yosys.log` y `build/timeout_contexto_nextpnr.log`. La captura física con esta imagen está pendiente. Para reproducir el flujo y probar manualmente desde `pochoco_soc-main`:

```powershell
$p = 'proyecto4/pruebas_fisicas/demo_autonoma_bus_detail'
powershell -ExecutionPolicy Bypass -File "$p/sintetizar.ps1" -TimeoutContext -Mapping default
Get-FileHash "$p/build/timeout_contexto.bin"
iceprog "$p/build/timeout_contexto.bin"
python "$p/leer_timeout_uart.py" --port COM10 --contexto
```

### Salida prematura del sondeo de STATUS

La imagen de contexto `18C60ADB…` dio `VERIFY OK` y `TIMEOUT=WAIT_ACK TICK=1 PC_ID=0x00000048 RS1_VALUE=0xFFFFFC3D BRANCH_TAKEN=0` en placa. En PC 0x48 se compara `x9` contra `x0`. El operando `0xFFFFFC3D` representa −963 y queda fuera de la cantidad inicial de venta, que el firmware limita a 0–63 antes de entrar al bucle. Las lecturas repetidas, con verificación y reset de solo lectura, registraron también PC 0x84 y 0xD0 en WAIT_ACK de la primera trama. Un reinicio se quedó sin bytes UART. Los últimos PCs observados dependen del arranque.

En Icarus, el primer commit de PC 0x1C ocurre en el ciclo 33. Los operandos son cero y el BEQ redirige el siguiente commit a PC 0x14. El primer byte llega en el ciclo 500 y el Espino solicita PRICE en el 515. Al anular el resultado de los branches, o al bloquear solo su redirección y conservar JAL, PRICE se solicita en el ciclo 35, el bucle de venta entra con `x9=0` en el 56 y el watchdog vence en el 8722. Ambas inyecciones registran 963 commits en PC 0x48 hasta ese límite. Reproducen el mecanismo y el orden de magnitud del contador observado en placa. El PC muestreado justo antes del timeout en esas simulaciones puede diferir del PC físico. Esta evidencia ubica el problema en la ruta de ejecución temprana, con la etapa exacta todavía pendiente.

La sonda de arranque observa el BEQ en PC 0x1C antes del primer byte. Enclava el primer salto cuyo siguiente commit se aparta de PC 0x14. Tras el watchdog emite un byte UART con los siguientes campos:

| Campo del lector | Significado |
| --- | --- |
| `RS1_ZERO`, `RS2_ZERO` | Los operandos completos del BEQ son cero por cada puerto del banco |
| `STATUS_NEW` | Se observó `new_price=1` en una respuesta de STATUS durante el sondeo anterior al primer byte |
| `INSN_OK` | La palabra del BEQ coincide con `0xFE010CE3` |
| `BRANCH_TAKEN` | Resultado del branch observado a la entrada del controlador |
| `PC_SET` | Orden de redirección del controlador hacia fetch |
| `NEXT_COMMIT_0X14` | El siguiente commit volvió a la instrucción LW STATUS |

D4 permanece encendido tras el timeout. D4+D3+D1 identifican un fallo MISO. Si los operandos son cero, `BRANCH_TAKEN=0` apunta a decode o comparación. Si el branch se toma y `PC_SET=0`, la divergencia está en la redirección del controlador. Si ambas señales valen uno y el PC siguiente difiere, la comprobación pasa al destino y a fetch. Las sondas modifican únicamente la observación del clon diagnóstico.

Icarus aprobó las inyecciones de comparación y redirección. También capturó una salida prematura luego de 21 saltos correctos y completó la secuencia nominal de 16 ticks con las 16 DECISION y respuestas MISO exactas frente a Python. Yosys obtuvo 1.080 LUT4 y 9 BRAM. nextpnr utilizó 1.262/1.280 LC y cerró timing a 25 MHz con Fmax enrutada de 42,24 MHz. Los logs están en `build/compilacion_timeout_arranque.log`, `build/timeout_arranque_yosys.log` y `build/timeout_arranque_nextpnr.log`. La imagen tiene SHA-256 `581B1D3CE7B29FE9B991FF9C82D3C4A2CE862BDAC07F2CD12170421B57C93D0A`. Queda pendiente la lectura en la Go Board.

```powershell
$p = 'proyecto4/pruebas_fisicas/demo_autonoma_bus_detail'
powershell -ExecutionPolicy Bypass -File "$p/sintetizar.ps1" -BootBranch -Mapping default
Get-FileHash "$p/build/timeout_arranque.bin"
iceprog "$p/build/timeout_arranque.bin"
1..3 | ForEach-Object { python "$p/leer_timeout_uart.py" --port COM10 --arranque }
```

Las tres lecturas verifican la flash y reinician la FPGA sin volver a escribirla.

### Verificación de la palabra que llega al decoder

La Go Board verificó `581B1D3C…` y devolvió tres veces
`RS1_ZERO=0 RS2_ZERO=1 STATUS_NEW=0 INSN_OK=0 BRANCH_TAKEN=0 PC_SET=0 NEXT_COMMIT_0X14=0`
en PC_ID 0x1C. D4 parpadeó durante las lecturas que reinician la FPGA. En el commit capturado, el decoder recibió una palabra distinta del BEQ esperado con STATUS todavía sin precio. Por ello, los indicadores de comparación y redirección de ese commit se interpretan a partir de la instrucción realmente leída.

Se verificaron las 71 palabras del firmware contra las dos copias de la RAM etiquetadas en el netlist de Yosys, deshaciendo la permutación de bits de `brams_map.v`. Las dos tienen `0xFE010CE3` en el índice 7, PC 0x1C. Tras desempaquetar `timeout_arranque.bin`, los nueve bloques de inicialización BRAM coinciden con el ASC enrutado. Los logs de la comprobación están en `build/timeout_arranque_bram_init_firmware.log` y `build/timeout_arranque_bram.log`.

La sonda `timeout_fetch` captura los 32 bits observados por el decoder en el commit de PC_ID 0x1C. Si hay una salida prematura del sondeo, conserva la muestra que la precedió. Emite una cabecera 0xB4 o 0xB5 seguida de la palabra en little-endian. El lector compara la palabra contra el firmware y muestra sus direcciones de origen posibles en `MATCH_PC`. `EARLY_EXIT=1` indica que el siguiente commit se apartó de 0x14 antes del primer byte. Icarus verificó tanto el BEQ correcto como la recuperación exacta de un `LW PRICE` inyectado en esa posición.

La corrida integrada aprobó los 16 ticks con coincidencia de DECISION y MISO respecto de Python. El banco integral cotejó 36.914 pares PC_ID/instrucción contra `trade.hex`. Yosys obtuvo 1.090 LUT4 y 11 BRAM. nextpnr utilizó 1.276/1.280 LC y cerró timing a 25 MHz con Fmax de 37,83 MHz. SHA-256 de la sonda `timeout_fetch.bin` `EC483AFD5E2F872DA9C200614E83A9645E8064E3CD352ACD112C7728E6818CBD`. La lectura física de la palabra está pendiente.

```powershell
$p = 'proyecto4/pruebas_fisicas/demo_autonoma_bus_detail'
powershell -ExecutionPolicy Bypass -File "$p/sintetizar.ps1" -FetchWord -Mapping default
Get-FileHash "$p/build/timeout_fetch.bin"
iceprog "$p/build/timeout_fetch.bin"
python "$p/leer_timeout_uart.py" --port COM10 --fetch
```

### Ajuste del puerto de instrucciones en la demo integral

La imagen `EC483AFD…` produjo `WORD=0x00000000 EXPECTED=0xFE010CE3 MATCH_PC=ninguna EARLY_EXIT=1` con D4 encendido. Dos reinicios con verificación de solo lectura repitieron la palabra nula. El tercero quedó sin bytes UART. La inyección `+zero_word` de Icarus devuelve la misma palabra y marca la salida prematura. La constatación física localiza el problema en el dato disponible al decoder durante el commit observado. El mecanismo eléctrico que produce ese cero requiere confirmación en placa.

El candidato integral `selftest_fetch_re` cambia únicamente la conexión de habilitación de lectura de las dos BRAM x16 del puerto de instrucciones. La señal de solicitud pasa a `RE` y `RCLKE` queda a uno. El modelo lógico x16 actualiza RDATA con ambas entradas altas en el flanco de reloj. Lattice documenta el uso de RE en configuración x16. El mapeo conserva el mismo reloj, direcciones, datos, escritura, tiempos lógicos del ciclo y contenido INIT, además de la ruta de datos y el firmware. [Guía de memoria de iCE40](https://www.latticesemi.com/~/media/LatticeSemi/Documents/ApplicationNotes/MO/MemoryUsageGuideforiCE40Devices.pdf)

El modo `-FetchReadEnable` sintetiza la demo con el monitor integral, aplica el cambio a las dos celdas verificadas en el netlist de Yosys, y simula ese netlist con las primitivas iCE40. Los bits de los LEDs se leen en orden D4…D1. `1010` en la imagen integral es D4 y D2 encendidos con D3 y D1 apagados, después de verificar los 16 ticks. La prueba física se realiza por programación manual.

La regresión RTL aprobó 16 precios, 16 escrituras DECISION, 16 MISO, 15 ACK y 36.914 pares PC_ID/instrucción. También comprobó el watchdog, el reset y la inyección de error MISO. La simulación del netlist mantuvo `1010` hasta el ciclo 98.314. El mapeo `default` obtuvo 1.260/1.280 LC, 1.074 LUT4, 9 BRAM y Fmax enrutada de 35,25 MHz. `icetime` también aprobó la restricción de 25 MHz. El intento con `-Mapping dff` ocupó 1.289 LC y se descartó antes de generar BIN.

SHA-256 de `build/selftest_fetch_re.bin` `E035B903938A4D933E1E13D88827A64629B3BDC24795C8C759F84489095F9FA0`. Los resultados están en `build/compilacion_selftest_fetch_re.log`, `build/selftest_fetch_re_mapped.log`, `build/selftest_fetch_re_nextpnr.log` y `build/selftest_fetch_re_icetime.log`. La prueba física reportó `VERIFY OK` y los cuatro LEDs encendidos (`1111`, watchdog). Seleccionar RE por sí solo no resolvió el fallo físico.

```powershell
$p = 'proyecto4/pruebas_fisicas/demo_autonoma_bus_detail'
powershell -ExecutionPolicy Bypass -File "$p/sintetizar.ps1" -FetchReadEnable -Mapping default
Get-FileHash "$p/build/selftest_fetch_re.bin"
iceprog "$p/build/selftest_fetch_re.bin"
```

### Registro de las entradas de lectura de instrucciones

El modo `-FetchPhase` prepara las entradas RADDR y RE de las dos BRAM x16 de instrucciones en el flanco descendente. Las BRAM leen en el flanco ascendente. El cambio añade ocho flip-flops al mapeo de tecnología. La comparación del netlist comprueba que únicamente cambian esas conexiones de lectura y se agregan esos ocho registros. El puerto de datos, las operaciones de escritura, el contenido INIT y las comprobaciones de los 16 ticks se conservan. Así se prueba la estabilidad de las entradas de fetch alrededor del flanco de lectura como hipótesis del fallo físico.

El primer mapeo con las señales declaradas en el top ocupaba 1.287 LC y se descartó. Insertar los registros después de sintetizar el RTL permitió mantener el resto del mapeo lógico. El nuevo enrutado utiliza 1.268/1.280 LC y 9 BRAM. El camino crítico es de flanco ascendente a descendente y la Fmax enrutada informada por nextpnr es 30,42 MHz. La restricción es de 25 MHz. La comparación estructural se guarda en `build/selftest_fetch_fase_diff.log` y la comprobación de timing en `build/selftest_fetch_fase_nextpnr.log`.

La síntesis desde las fuentes actuales y el mapeo de entradas produjeron un netlist idéntico al simulado. La regresión contrastó 16 decisiones y 16 MISO con Python y la simulación del netlist mantuvo el código integral `1010` hasta el ciclo 98.314. `icepack` produjo 32.220 bytes. El SHA-256 de `build/selftest_fetch_fase.bin` es `19B504B6D81CDE36C0A81F3C7AE7C5D1D08A4F38B4E99CA0C0D49FDEC145FB55`. Los registros de reproducción, simulación y empaquetado están en `build/selftest_fetch_fase_repro.log`, `build/selftest_fetch_fase_mapped.log` y `build/selftest_fetch_fase_bin.log`.

```powershell
$p = 'proyecto4/pruebas_fisicas/demo_autonoma_bus_detail'
powershell -ExecutionPolicy Bypass -File "$p/sintetizar.ps1" -FetchPhase -Mapping default
Get-FileHash "$p/build/selftest_fetch_fase.bin"
iceprog "$p/build/selftest_fetch_fase.bin"
```

La Go Board verificó la grabación de la imagen `19B504B6…` y quedó en `1111` con los cuatro LEDs encendidos. El watchdog volvió a vencer en placa.

### Demo autónoma con ROM de instrucciones en LUTs

La imagen `selftest_fetch_rom.bin` carga las mismas 71 palabras de `trade.hex` en una ROM de LUTs. El puerto de datos conserva su RAM y direccionamiento MMIO. La demo compacta el PC a siete bits de dirección de palabra. El script comprueba que los 22 saltos directos están alineados y dentro del programa, y el banco integrado verifica que el firmware use MMIO para todos sus accesos de datos. El fetch mantiene la latencia síncrona y el enrutamiento del SoC y del monitor conserva la misma comprobación de precios, DECISION y MISO.

La implementación con PC de 32 bits ocupó 1.422 LC. Con la dirección de palabra ajustada al firmware, el build obtuvo 1.234/1.280 LC, 1.096 LUT4, 7 BRAM y Fmax enrutada de 43,94 MHz. Yosys mapeó la ROM de instrucciones a lógica. Icarus cotejó 36.914 commits, 16 precios, 16 decisiones, 16 respuestas MISO y 15 ACK. La simulación del netlist conservó `1010` hasta el ciclo 98.314. El BIN tiene 32.220 bytes y SHA-256 `57EC067D20918FEE0C283AA1BD20A270C5ED5F1B711018D0057BCBCAD38A3068`.

```powershell
$p = 'proyecto4/pruebas_fisicas/demo_autonoma_bus_detail'
powershell -ExecutionPolicy Bypass -File "$p/sintetizar.ps1" -FetchROM -Mapping default
Get-FileHash "$p/build/selftest_fetch_rom.bin"
iceprog "$p/build/selftest_fetch_rom.bin"
```

En placa, `1010` corresponde a solo D4 y D2 encendidos de forma estable. El usuario reportó los cuatro LEDs encendidos con esta imagen. Una verificación de solo lectura devolvió `VERIFY OK` para el BIN exacto `57EC067D…`. El watchdog persiste con la ROM en LUTs y la evidencia de flash quedó en `build/confirmacion_rom_flash.log`.

### Autotest con reloj dividido y confirmación por UART

El modo `-SlowROM` usa la ROM de instrucciones en LUTs. Un flip-flop y un buffer global generan el reloj de 12,5 MHz nominal a partir del reloj de placa de 25 MHz. El reset se libera de forma registrada después de 1.024 ciclos del SoC, aproximadamente 81,92 µs. Este modo conserva la comprobación integral de los 16 precios, las decisiones y MISO. Los LEDs presentan el resultado terminal.

La UART TX por pin 74 conserva 115200 baudios, 8N1, con el reloj de placa. Envía un byte con el prefijo 0xA y el código LED al terminar. `0xAA` es PASS, `0xAB` error de precio, `0xAC` error de decisión, `0xAD` error MISO, `0xAE` error de secuencia y `0xAF` watchdog. El lector abre COM10 antes de verificar la flash en modo de solo lectura y reiniciar la FPGA.

La regresión RTL comprobó los 16 ticks, 15 ACK y 36.914 pares PC_ID/instrucción. La unidad UART simuló `0xAA` y `0xAF`. El enrutado con `-Mapping dff` registró 1.270/1.280 LC, 1.122 LUT4 y 7 BRAM. nextpnr informó 44,29 MHz para la red del SoC y aprobó una restricción de 25 MHz. La frecuencia operativa de este autotest sigue siendo 12,5 MHz. Las mediciones oficiales corresponden a las imágenes de competencia.

La simulación del netlist conservó `1010` y transmitió `0xAA`. El BIN `build/selftest_fetch_rom_lento.bin` tiene 32.220 bytes y SHA-256 `0CCD156590DAECF3F9C3E6031E7E987B0CE6A0795BB801A9672C88CCC91FB9CC`.

**PASS físico confirmado el 23 de noviembre de 2026.** En la Go Board se observaron únicamente D2 y D4 encendidos (`1010`). `iceprog -c` devolvió `VERIFY OK` para el BIN exacto y COM10 recibió `AUTOTEST LED=1010 UART=0xAA RESULT=PASS` en tres arranques. El código terminal acredita que el monitor completó los 16 ticks, con accesos MMIO, decisiones y MISO verificados. Los registros `build/confirmacion_rom_lento_flash.log` y `build/resultado_fisico_rom_lento.log` se incluyen en el ZIP de entrega.

```powershell
$p = 'proyecto4/pruebas_fisicas/demo_autonoma_bus_detail'
powershell -ExecutionPolicy Bypass -File "$p/sintetizar.ps1" -SlowROM -Mapping dff
Get-FileHash "$p/build/selftest_fetch_rom_lento.bin"
iceprog "$p/build/selftest_fetch_rom_lento.bin"
python "$p/leer_timeout_uart.py" --port COM10 --autotest
```
