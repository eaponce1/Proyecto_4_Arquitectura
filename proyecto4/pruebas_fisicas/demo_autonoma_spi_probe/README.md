# Diagnóstico SPI autónomo

Variante independiente para localizar el avance entre el inicio del maestro y el ACK del Espino. No reemplaza ni modifica `demo_autonoma`, `demo_autonoma_trace`, `demo_autonoma_handshake`, el SoC estable ni el firmware. El SoC y el SPI Slave provienen del RTL MMIO SMA10; el maestro solo envía la secuencia fija de precios.

## Interpretación de LEDs

D1 corresponde al bit 0 y D4 al bit 3. En la recepción inicial, los indicadores son acumulativos:

| Código D4..D1 | Significado |
|---|---|
| `0001` | El maestro comenzó una trama |
| `0011` | `CS_n` fue observado activo |
| `0111` | El maestro produjo ocho flancos ascendentes de SCLK |
| `1111` | El SPI Slave generó `byte_done` |

Después de `byte_done`, los mismos LEDs muestran el avance del firmware/handshake:

| Código D4..D1 | Significado |
|---|---|
| `1111` | Byte recibido; aún no se observó el STATUS posterior al precio |
| `1110` | STATUS posterior al precio observado; falta leer PRICE |
| `1101` | PRICE leído; falta aceptar ACK el maestro |
| `1100` | ACK aceptado; PRICE y ACK completados |

Los eventos quedan retenidos para facilitar la observación. Un diseño que permanezca en `0111` completó ocho flancos del maestro pero no informó `byte_done`; eso acota la falla al camino de entrada sincronizada/detección del slave. Si se queda en `1111`, el byte ya llegó al slave y hay que observar el acceso de STATUS. `1110` acota el atasco antes de la lectura PRICE y `1101` antes de ACK.

## Hallazgo sobre el síntoma reportado

En la variante anterior `demo_autonoma_trace`, `0011` no significa “maestro y CS únicamente”: el contador `progress` avanza a `3` cuando `spi_byte_done` ocurre (código `demo_autonoma_trace_top.v`, etapa 2→3). Por tanto, con el mapeo documentado por esa variante, D1+D2 encendidos implican que el primer precio sí fue recibido y el bloqueo posterior está antes de observar el STATUS posterior a ese precio, o bien que la imagen programada no corresponde a ese RTL/mapeo. La variante de esta carpeta separa explícitamente las etapas SPI y MMIO para comprobarlo.

## Reproducción

Desde la raíz `pochoco_soc-main`:

```powershell
powershell -ExecutionPolicy Bypass -File proyecto4\pruebas_fisicas\demo_autonoma_spi_probe\ejecutar_pruebas.ps1
powershell -ExecutionPolicy Bypass -File proyecto4\pruebas_fisicas\demo_autonoma_spi_probe\sintetizar.ps1
```

El testbench compara la secuencia con vectores generados por la estrategia Python, cuenta los flancos SCLK crudos y su réplica sincronizada del detector del slave, comprueba `byte_done`, STATUS, PRICE, SUM10, READY, DECISION, respuesta MISO y el ACK. La réplica de sincronización es instrumentación observacional; el `byte_done` verificado es el del SoC.

## Resultados medidos en esta variante

- Simulación Icarus: PASS; 16 precios, 16 decisiones y 16 respuestas MISO; 15 ACK aceptados (no se requiere ACK después del último tick); 0 ticks perdidos.
- Primer byte: maestro inició en ciclo 18; ocho flancos del maestro y ocho flancos detectados por la réplica sincronizada; `byte_done` en ciclo 500; STATUS posterior al precio en ciclo 508; PRICE en ciclo 515; ACK aceptado en ciclo 532.
- Síntesis Yosys/nextpnr HX1K/VQ100: 985 LUT4, 1166/1280 LC, 9/16 BRAM; Fmax 39,67 MHz y PASS a 25 MHz.
- Binario independiente generado en `build/demo_autonoma_spi_probe.bin`. No se programa automáticamente.

La simulación demuestra la secuencia en RTL, no determina por sí sola qué ocurre en la placa. Para confirmar la causa física, programar manualmente este binario independiente y observar el código retenido.
