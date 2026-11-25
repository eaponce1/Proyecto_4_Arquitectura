# Diagnóstico del acceso STATUS del Espino

Variante de diagnóstico independiente para observar el primer acceso de datos del Espino después del primer precio SPI. El wrapper local añade solo puertos de observación del bus; instancia sin cambios `espino_core`, RAM, SPI Slave y SMA10 MMIO base. Firmware: `proyecto4/alternativas/mmio_sma10/sw/trade.hex`.

## Lo que significa el `1111` observado antes

En `demo_autonoma_spi_probe`, los cuatro LEDs llegan a `1111` al detectar `spi_byte_done`. Esa palabra no muestra actividad del Espino ni un acceso STATUS. Por sí sola confirma la recepción del byte por el slave, pero no permite inferir el estado del core o del bus. El nuevo mapeo dedica los LEDs al fetch y al ciclo de lectura de STATUS.

## LEDs de esta variante

Los códigos quedan retenidos en el primer avance alcanzado. D1 es bit 0 y D4 bit 3.

| D4..D1 | Interpretación |
|---|---|
| `0000` | Reset todavía activo / sin fetch observado |
| `0001` | Espino solicita fetch de instrucciones |
| `0010` | SPI Slave produjo el primer `byte_done` |
| `0011` | Espino presentó una lectura a `0x80010000` (`we=0`, `be=1111`) |
| `0100` | El bus devolvió STATUS con `new_price=1` |
| `0101` | El fetch/PC del Espino avanzó después de la respuesta |
| `0110` | Primera respuesta STATUS no tenía `new_price=1` |
| `1010` | Primera transacción de datos posterior al precio tenía dirección/dirección de escritura inesperada |

Si queda en `0001`, revisar fetch/reset/ROM. `0010` significa que el slave recibió el precio, pero todavía no se observó solicitud STATUS. `0011` indica que el bus sí seleccionó STATUS; `0110` separa una respuesta sin `new_price`; `0100` confirma datos válidos, y `0101` confirma que el core continuó.

## Auditoría y causa acotada

El mapa MMIO del wrapper selecciona SPI cuando `data_addr[31]=1` y `data_addr[16]=1`. Para `0x80010000`, `spi_sel=1`, `spi_req=data_req`, y el offset `data_addr[7:2]` vale cero (`REG_STATUS`). El periférico usa STATUS en offset 0, PRICE en offset 1, DECISION en offset 2, SUM10 en offset 3 y READY en offset 4.

El slave actualiza `price_q` y `new_price_q` con asignaciones no bloqueantes al ocurrir `byte_done`. En Icarus, el core presenta una lectura STATUS coincidente con ese mismo borde (ciclo 500); esa lectura ve el valor anterior y devuelve `0x00000002` (CS activo, `new_price=0`). Es una lectura prematura esperable por el sondeo, no una pérdida del precio. El firmware vuelve a sondear; en el ciclo 508 la solicitud exacta a `0x80010000` retorna `0x00000003` al ciclo 509. El IF sale del stall y el PC avanza desde `0x18` a `0x1c` durante el ciclo 511. PRICE en `0x80010004` entrega `0xC8` (200).

Por tanto, el RTL y el testbench no reproducen un bloqueo permanente en STATUS. La causa física exacta no queda demostrada solo por el patrón `1111` anterior, porque ese patrón no observaba fetch, `data_req` ni `data_rdata`. Esta variante aporta esas observaciones y permitirá separar un core que no solicita STATUS de una lectura mal decodificada, una respuesta inválida o un core que no reanuda. La corrección mínima demostrada por ahora es mejorar la instrumentación; no se justifica cambiar el core ni el periférico base.

## Simulación observada

La prueba además comprueba STATUS, PRICE, SUM10, READY, las 16 escrituras DECISION y las 16 respuestas MISO frente a vectores generados por Python. El handshake de memoria se observa en señales del wrapper; `instr_req=0` durante la solicitud STATUS indica stall, luego `data_rdata=3`, después `instr_req` vuelve a activarse y el PC progresa. ACK al maestro es sticky hasta el próximo `byte_done`, pues la lectura PRICE puede preceder a `WAIT_ACK`.

Ejecución desde `pochoco_soc-main`:

```powershell
powershell -ExecutionPolicy Bypass -File proyecto4\pruebas_fisicas\demo_autonoma_bus_probe\ejecutar_pruebas.ps1
powershell -ExecutionPolicy Bypass -File proyecto4\pruebas_fisicas\demo_autonoma_bus_probe\sintetizar.ps1
```

Resultados medidos en esta corrida:

- Icarus: PASS, 16/16 precios, PRICE, decisiones y MISO; lectura STATUS correcta; stall y reanudación del PC confirmados.
- Primera lectura STATUS posterior al byte: request ciclo 508, respuesta `0x00000003` ciclo 509, PC observado avanzando ciclo 511.
- Yosys/nextpnr HX1K/VQ100: 1026 LUT4, 1243/1280 LC, 9/16 BRAM, Fmax final reportada 40,40 MHz; PASS a 25 MHz.
- Binario independiente: `build/demo_autonoma_bus_probe.bin`. No se ha programado la Go Board.

SHA-256 del binario: `AF8B6BE84205E8882402324DF7545F2817EC49973769E9BF5DF81CBAB36B7513`.

El próximo paso físico es programar manualmente este binario separado y anotar el código LED. Ese patrón ubica la falla en el camino observable; no modificar firmware, Espino ni MMIO SMA10 base basándose solo en la simulación.
