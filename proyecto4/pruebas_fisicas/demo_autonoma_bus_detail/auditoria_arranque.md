# Auditoría de arranque

Icarus compara el RTL actual con el RTL del ZIP aprobado. En ambos el POR arranca en cero, cuenta hasta 15 y libera rst_ni después del flanco 15. El primer flanco operativo es 16. El maestro parte en IDLE, pasa a SELECT en 16 y activa CS_n después del flanco 17. En los logs PRE se observa el pulso frame_start en 18, byte_done en 500 (19,98 us desde el primer flanco) y response_valid en 531 (21,20 us). Ambos pasan los primeros 550 flancos. La imagen previa carece del monitor integral.

El monitor tiene reset síncrono activo alto, conectado a !rst_ni. LED, error, previous_access, in_tick, tick_seen y hits arrancan y se resetean en cero. Los contadores son expresiones derivadas del índice del maestro (inicializado a cero) y los flags, no bancos adicionales de registros. El maestro usa reset activo bajo. CS_n queda inactivo alto, SCLK bajo, y los pulsos de trama y respuesta quedan en cero. miso_bad tiene inicialización a cero y se limpia al entrar en SELECT. El PCF coincide con el base. Reloj pin 15 y LEDs D1..D4 en 56, 57, 59 y 60, respectivamente. Un uno enciende el LED.

Fuera de reset, el latch llamado error toma error || fault y el LED toma 1111 en ese mismo flanco si fault vale uno. El desglose del test vigila timeout, trama nueva sin cerrar el tick anterior, byte duplicado o precio incorrecto, acceso fuera del tick o repetido, SMA sin PRICE, DECISION prematura o incorrecta y MISO incorrecto. STATUS por sí solo no genera error.

El timeout exige WAIT_ACK o DONE y gap_count saturado en 8191. En el arranque normal no puede dispararse antes de SPI. Si la primera trama termina en su ciclo habitual y nunca llega ACK, el primer timeout de ese caso sería el flanco 8722. El maestro compara bits desde el primer flanco ascendente de SCLK, antes de que el slave termine de recibir el precio. El monitor solo acepta o rechaza MISO con response_valid, después de los ocho bits. El test inyectó MISO alto en la primera trama y comprobó que el único término de error es MISO y que 1111 aparece en el flanco 531. Es una reproducción controlada, no una identificación de la causa física.

Icarus muestra X en algunas salidas antes del primer flanco bajo reset. En el siguiente muestreo ya están inicializadas, y ningún término de fault es X tras liberar reset. Los X del simulador no equivalen a un bit físico alto. Como todos los errores se fusionan en un solo latch, el patrón 1111 no conserva el origen ni el ciclo. La secuencia completa tarda milisegundos, por lo que una observación visual inmediata tampoco ubica el fallo dentro del arranque.

## Reproducción desde pochoco_soc-main

```powershell
powershell -ExecutionPolicy Bypass -File proyecto4/pruebas_fisicas/demo_autonoma_bus_detail/verificar_arranque.ps1
vvp proyecto4/pruebas_fisicas/demo_autonoma_bus_detail/build/arranque_actual.vvp +bad_miso
```

Logs en build/arranque_actual.log, build/arranque_anterior.log y build/arranque_miso_inyectado.log. El RTL y el BIN permanecen intactos.
La simulación funcional de la netlist JSON con las primitivas iCE40 no produjo el primer renglón de traza antes de interrumpirla. No se usa como evidencia de aprobación ni de fallo.
