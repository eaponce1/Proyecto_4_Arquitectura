# Diagnóstico de 1111 en selftest

## Evidencia en placa y en la imagen programada

Se verificó la flash con iceprog -c build/selftest.bin en modo de comparación. El comando no escribe flash, mantiene la FPGA en reset durante la lectura y vuelve a liberarla. Resultado: VERIFY OK, CDONE alto al terminar. Después de esta verificación, el usuario volvió a observar D4..D1 = 1111. Se confirmó el contenido de flash, por lo que una imagen antigua no explica esta lectura.

SHA-256 confirmado de selftest.bin: 48975E55BF4D0F38D3217BA7615E4DAD7DC405FBDF749F21B108C6315DB7BE80.

Se extrajo el circuito del mismo BIN con iceunpack e icebox_vlog. Icarus ejecutó el circuito reconstruido hasta el ciclo 110000. LED 0000 en ciclos 1 y 100, primer hito 0001 en 501 y 1010 en 98282, retenido hasta 110000, más allá del umbral terminal. Se añadió un retardo uniforme de 1 ps a los assign del Verilog generado para la simulación funcional. Esto comprueba la lógica de la imagen y la inicialización modelada de sus celdas, sin modelar skew, variaciones físicas ni los retardos post-route. El análisis estático independiente con icetime sobre el ASC extraído del BIN estimó 25,73 ns (38,86 MHz) y aprobó la restricción de 40 ns; esto no es una medición física.

## Reset y ruta de error

- El wrapper tiene por_cnt de cuatro bits, inicializado a cero. Saturación en 15. rst_ni se libera después del flanco 15 y el flanco 16 es el primero operativo. Maestro, Espino y SPI reciben reset activo bajo. El monitor recibe el inverso como reset síncrono activo alto.
- previous_access, in_tick, tick_seen, hits, error y led tienen valor inicial y de reset cero. Los conteos del monitor se derivan del índice y de los flags. No hay un registro adicional error_code. `led` es el registro que captura el error_code y alimenta o_LED. `error` es error_sticky y bloquea escrituras posteriores a led.
- La FSM del maestro arranca en IDLE y el contador gap_count en cero. Reinicia gap_count al terminar una trama y al aceptar ACK. price_index, half_count, rx_shift y los pulsos frame_start, response_valid, ack_accepted y sclk_rise se ponen en cero. bit_index se pone en siete. SCLK y MOSI quedan bajos y CS_n alto. done y sent se ponen en cero. La envoltura pone en cero price_ack_pending y status_pending.
- miso_bad se inicializa en cero. La rama de reset del maestro no vuelve a asignarlo. SELECT lo limpia antes de muestrear los bits. El monitor solamente usa su resultado con response_valid, que sí se reinicia.
- timeout_o = (WAIT_ACK || DONE) && (gap_count == 8191). El monitor calcula timeout_fault = (stage != 10) && timeout_o. Con señales conocidas, led captura 1111 únicamente si timeout_fault es la causa seleccionada y no había un error latcheado. Los otros términos tienen prioridad y sus códigos son 1011 a 1110. El valor combinacional por defecto de fault_code es 1111, pero fault habilita su uso. No aparece por defecto en led.
- Antes de la primera trama no se habilita el timeout en el modelo RTL. El caso IDLE comprueba 100 y 1000 flancos sin SPI. Los X observados antes del primer flanco durante POR desaparecen antes de la liberación. El test normal compara con identidad de cuatro estados las condiciones de fallo.
- PCF: reloj pin 15. D1 a D4 pines 56, 57, 59 y 60, activos en alto. El reporte nextpnr previo asigna cinco BEL de IO distintos.

## Experimentos sobre el RTL existente

Todos los ciclos se numeran desde el primer flanco del reloj. Los CSV contienen señales preflanco y un renglón postflanco al capturar 1111.

| Caso | Resultado medido |
|---|---|
| Encendido sin transacción | Los módulos maestro y monitor en interconexión de prueba con enable=0 siguen sin timeout ni error en 100 y 1000. |
| Primera transacción normal | Inicio 18, byte 500, lectura STATUS 508, PRICE 515, SUM10/READY observadas, MISO 531 y DECISION 542. Sin error al ciclo 1000. |
| ACK suprimido en el primer tick | Flanco 8721, WAIT_ACK, contador 8190 y salida de timeout baja. Flanco 8722, WAIT_ACK, contador 8191 y timeout como única causa. LED cambia a 1111 en el posflanco 8722, aproximadamente 0,349 ms desde el comienzo del reloj. |
| ACK llega en el límite | Flanco 8722, el maestro acepta ACK y transita a GAP. El monitor ve el timeout preflanco y enclava 1111. La expresión de timeout no toma en cuenta el ACK que llega ese mismo ciclo. |
| Se omite únicamente el hito de primer commit del monitor | Los 16 ticks se completan, todos sus eventos están drenados y master_done está activo. Último MISO en 98256. En el flanco 106447, DONE y contador 8191 activan 1111, aproximadamente 4,258 ms desde el comienzo. stage sigue distinto de 10 aunque no queda una transacción que espere respuesta. |
| Recuperación después del error | Se fuerza el POR a cero desde el testbench durante un flanco. El latch y el código regresan a cero. Al soltar POR y restaurar ACK se procesa un nuevo tick sin error. El fixture sin transacción permanece en cero. |

El simulador digital no reprodujo el fallo sin inyección, incluso usando la lógica extraída del BIN instalado. El código físico 1111 no registra si el primer timeout provino de WAIT_ACK o de DONE. La observación visual de "inmediato" no permite distinguir los intervalos medidos, todos inferiores a cinco milisegundos.

La corrección propuesta para las dos condiciones demostradas consiste en dar prioridad al ACK frente al umbral en WAIT_ACK, habilitar el watchdog final solo mientras falte completar la última transacción y codificar un hito de monitor ausente como fallo de secuencia. Una traza física temporizada de los LEDs desde el inicio de ejecución permitiría distinguir un bloqueo al empezar de uno al finalizar. El RTL y el BIN se conservan mientras no se identifique cuál sucedió físicamente.

## Reproducción desde pochoco_soc-main

```powershell
$p = 'proyecto4/pruebas_fisicas/demo_autonoma_bus_detail'
powershell -ExecutionPolicy Bypass -File "$p/verificar_timeout.ps1"
powershell -ExecutionPolicy Bypass -File "$p/verificar_bin_existente.ps1"
```

Trazas en build/timeout_normal.csv, timeout_drop_ack.csv, timeout_late_ack.csv, timeout_drop_milestone.csv y timeout_bitstream_delayed.log. La regresión del RTL en Icarus incluyó 18 comprobaciones PC Probe, las pruebas unitarias del monitor y los 16 ticks RTL con 16 DECISION, 16 MISO y 15 ACK. Los CSV oficiales se cotejaron otra vez con Python y mantienen 0 diferencias en los 20000 ticks de cada arquitectura.



## Corrección aplicada al selftest

En WAIT_ACK, timeout_enable requiere que price_consumed_i sea cero. La FSM usa la misma señal para aceptar el ACK, abandonar WAIT_ACK y poner gap_count en cero. Esa decisión es combinacional antes del flanco que registra el error. En DONE, timeout_enable exige que todavía falte algún evento de la última transacción. El indicador final_complete incluye eventos presentes en el mismo flanco para cancelar la espera sin depender de la actualización nonblocking de tick_seen. El monitor trata un hito de observación ausente tras complete como error de secuencia 1110.

El test de límite pasó con ACK en 8.721 y 8.722. El timeout de WAIT_ACK con ACK ausente o tardío sigue activo en 8.722. En la prueba de cierre sin el hito del primer commit, los 16 precios, DECISION y MISO se cotejan y el primer error cambia de 1111 en 106.447 (imagen anterior) a 1110 en 98.281 (corregida). El watchdog terminal sigue disparando 1111 en 106.447 si se suprime la DECISION final. Reset en 8.723 limpia el timeout y la repetición llega a 1010 en 107.006. El caso nominal llega a 1010 en 98.283.

El primer mapeo de la corrección requirió 1.306 LC y falló la colocación. Compartir el incremento de gap_count, reutilizar el flag de primer byte y generar el hito PASS desde el hito de finalización redujo el mapeo final a 1.258 LC. El registro LED retiene el primer error y tiene prioridad sobre la codificación de hitos. No se eliminaron verificaciones. Yosys produjo 1.070 LUT4 y 9 BRAM. nextpnr cerró 25 MHz con Fmax de 39,52 MHz. El BIN nuevo tiene SHA-256 50D8B7AE550978409E9EF97A324F09C3E13FDDD9D4B52D574D6376172FE5CF86. La imagen anterior y sus fuentes quedan en selftest_antes_watchdog.zip.

La causa física del 1111 anterior sigue sin distinguirse entre las condiciones reproducidas. La imagen actual queda lista para la prueba física manual descrita en README.md.

Para validar el archivo empaquetado también se simuló la lógica extraída del nuevo BIN. El resultado fue 1001 en el flanco 98.282 y 1010 en 98.283, retenido hasta 110.000. Esta prueba funcional es adicional a Icarus RTL y al cierre de timing y se reproduce con verificar_bin_existente.ps1.
