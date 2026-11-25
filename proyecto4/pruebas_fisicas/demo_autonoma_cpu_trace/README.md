# demo_autonoma_cpu_trace

Variante independiente para localizar el avance del Espino y el primer acceso MMIO después del primer `byte_done`. Usa los precios deterministas de las pruebas autónomas, el firmware `trade.hex`, el SPI Slave MMIO SMA10 y los bloques base sin cambiar esos archivos.

## LEDs, código D4..D1

El monitor conserva los hitos observados y los presenta en orden, un código por ciclo. Una máscara sticky captura sucesos que comparten ciclo; por eso una solicitud `data_req` que también es lectura STATUS no pierde el hito 0100 y después muestra 0101.

| Código | Hito confirmado |
|---|---|
| `0001` | Fetch inicial observado |
| `0010` | Primer `byte_done` |
| `0011` | Commit del Espino posterior al byte (`instr_valid_id && !stall`) |
| `0100` | Primera solicitud `data_req` posterior al commit |
| `0101` | Solicitud de lectura STATUS |
| `0110` | Respuesta STATUS con `new_price=1` |
| `0111` | Lectura PRICE |
| `1000` | Lectura SUM10 o READY |
| `1001` | Escritura DECISION |
| `1010` | Primera respuesta MISO correcta de la decisión previa |

El primer MISO comprobable con una decisión del agente es el de la segunda trama: la primera trama comienza con DECISION inicial cero, antes de que el Espino haya escrito la decisión del tick 1.

## Captura real de señales

El wrapper diagnóstico expone `instr_req`, dirección/PC, `data_req`, `data_we`, `data_addr`, `data_rdata`, señales decodificadas de STATUS/PRICE/SUM10/READY/DECISION y `byte_done`. Para obtener `commit`, stall y PC ID, `rtl/espino_core_cpu_trace.v` es una copia independiente del RTL Espino con nombre de módulo separado y tres salidas de observación; esas salidas no retroalimentan la lógica. El Espino original no se modifica. El testbench instancia además el core original en paralelo y compara sus interfaces principales y el commit ciclo a ciclo contra la copia instrumentada.

La respuesta STATUS tiene latencia síncrona. La lectura que coincide con `byte_done` puede recibir el valor anterior; el firmware sondea otra vez. El monitor exige la respuesta posterior con `new_price=1` y no confunde la solicitud STATUS con su respuesta.

## Pruebas reproducibles

Desde la raíz `pochoco_soc-main`:

```powershell
powershell -ExecutionPolicy Bypass -File proyecto4\pruebas_fisicas\demo_autonoma_cpu_trace\ejecutar_pruebas.ps1
powershell -ExecutionPolicy Bypass -File proyecto4\pruebas_fisicas\demo_autonoma_cpu_trace\sintetizar.ps1
```

La simulación compara precios, decisiones y MISO contra vectores Python; verifica todos los códigos LED, stall/respuesta/PC, los cuatro registros leídos y las 16 escrituras DECISION. El handshake de consumo PRICE es sticky hasta el siguiente `byte_done`, para que el maestro no pierda el ACK si la lectura precede a `WAIT_ACK`.

## Resultados

- Icarus: PASS; 16 precios, 16 PRICE, 16 SUM10, 16 READY, 16 DECISION, 16 MISO y 0 ticks perdidos.
- Secuencia del primer tick: `byte_done` ciclo 500; primer commit posterior ciclo 501; STATUS `data_req`/lectura en ciclo 508; respuesta `0x00000003` en ciclo 509; PC observado avanzando `0x18`→`0x1c` en ciclo 511; PRICE ciclo 515; SUM10 ciclo 529; DECISION ciclo 542.
- Primer MISO de decisión previa correcto: segunda trama, ciclo 7046, byte `0x00`.
- Yosys/nextpnr HX1K/VQ100: 1030 LUT4, 1253/1280 LC, 9/16 BRAM; Fmax final 41,43 MHz y PASS a 25 MHz.
- Binario independiente: `build/demo_autonoma_cpu_trace.bin`, SHA-256 `5ED16252FAC06581CA7084A287C8D2D50D1772871945951B2D98D7CB952F0B63`.

La placa no se programa automáticamente. Para completar el diagnóstico físico, programar manualmente este binario y anotar el último código alcanzado. La simulación muestra el comportamiento RTL; no afirma que la ejecución física ya esté validada.
