# Informe de diagnóstico CPU/MMIO: demo_autonoma_cpu_trace

## Alcance y conclusión física actual

La observación previa de `demo_autonoma_bus_probe` fue `0010`. En ese diseño ese código era el hito `byte_done`; no observaba commit, `data_req`, STATUS ni PC después del byte. Por ello, esa medición **no permite afirmar que el Espino se haya detenido**, solo que el slave recibió el precio.

La nueva variante instrumenta esas señales. El resultado actual es de simulación RTL: en ella el Espino sigue ejecutando y completa la ruta STATUS. La causa física exacta todavía debe confirmarse programando manualmente esta variante; no se programó la placa durante esta tarea.

## Implementación

Todos los archivos están bajo esta carpeta. El wrapper es una copia diagnóstica reducida con salidas adicionales de observación; SPI Slave, SMA10, RAM y firmware siguen siendo los componentes base. Para sintetizar `commit` y `pc_id`, la carpeta incluye `espino_core_cpu_trace.v`, una copia nombrada aparte del core que añade solo salidas pasivas `dbg_commit_o`, `dbg_stall_o` y `dbg_pc_id_o`. No se tocó `rtl/espino_core/espino_core.v`. La prueba compara en paralelo la copia instrumentada con el core original y exige igualdad de fetch, dirección, request/write, byte enables, bus address/write data y commit.

El registro `seen[9:0]` captura hitos con bits sticky. La etapa LED consume esos hitos en secuencia, a un por ciclo. Esto evita perder sucesos concurrentes por semántica nonblocking y hace visibles 0100 (data request) y 0101 (STATUS) incluso cuando corresponden a una sola transferencia.

## Hallazgo de la ruta STATUS

La dirección `0x80010000` selecciona el SPI MMIO (bits 31 y 16 activos) y offset 0 (`REG_STATUS`). El periférico registra la salida `rdata_o`; el dato STATUS es `{30'b0, cs_active, new_price_q}`. `byte_done` fija `new_price_q` a uno con asignación no bloqueante. En la lectura que coincide con ese mismo borde, el dato previo es visible; la siguiente lectura resuelve la espera.

Traza Icarus observada:

| Ciclo | Evento/señales |
|---:|---|
| 500 | `byte_done`, precio 200; coincide una lectura STATUS prematura |
| 501 | Commit del Espino posterior al byte; `stall=0` |
| 508 | `data_req=1`, `data_we=0`, `data_addr=0x80010000`, `be=1111`, `instr_req=0` por stall |
| 509 | `data_rdata=0x00000003`; `new_price=1`, `instr_req=1` |
| 511 | PC/fetch progresa de `0x18` a `0x1c` |
| 515 | Lectura PRICE en `0x80010004` |
| 529 | Lectura SUM10 |
| 542 | Escritura DECISION `0x00` |
| 7046 | Respuesta MISO de la segunda trama `0x00`, coincide con DECISION previa |

La petición DATA detiene temporalmente fetch mediante `lsu_busy`; al completar la lectura, el request se retira, se recibe el dato y el flujo de instrucciones continúa. No se observó deadlock de bus ni divergencia entre el core original y el clon instrumentado.

## Resultados de validación

- Icarus: PASS, todos los códigos de hito 0001 a 1010 fueron alcanzados en orden; los sucesos simultáneos quedaron retenidos y emitidos secuencialmente.
- Integración completa: 16 precios, 16 lecturas PRICE, 16 SUM10, 16 READY, 16 escrituras DECISION, 16 respuestas MISO comparadas con Python, 0 ticks perdidos.
- Equivalencia del tap: los puertos externos del core original y del clon instrumentado coinciden en cada ciclo comprobado; `commit` también coincide con `instr_valid_id && !stall` del core original.
- Yosys: PASS. Se comprobaron los taps sintetizados sin referencias jerárquicas flotantes.
- nextpnr-ice40 HX1K/VQ100, 25 MHz: PASS. 1253/1280 LC, margen de 27 LC; 1030 LUT4, 9/16 BRAM; Fmax final 41,43 MHz.
- icepack: generó el binario independiente. No se programó la Go Board.

## Reproducibilidad

```powershell
powershell -ExecutionPolicy Bypass -File proyecto4\pruebas_fisicas\demo_autonoma_cpu_trace\ejecutar_pruebas.ps1
powershell -ExecutionPolicy Bypass -File proyecto4\pruebas_fisicas\demo_autonoma_cpu_trace\sintetizar.ps1
```

Binario: `build/demo_autonoma_cpu_trace.bin`  
SHA-256: `5ED16252FAC06581CA7084A287C8D2D50D1772871945951B2D98D7CB952F0B63`

## Lectura del próximo resultado físico

Con este diseño, `0010` significa `byte_done` alcanzado, pero todavía no commit posterior; `0011` confirma commit, `0100` el request de datos, `0101` la lectura STATUS, `0110` la respuesta STATUS válida y `1010` una respuesta MISO correcta. Así se podrá distinguir si la ejecución física avanza por el core, por la interfaz MMIO y hasta la respuesta serial.
