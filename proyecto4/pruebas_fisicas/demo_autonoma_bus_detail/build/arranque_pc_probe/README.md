# Captura del primer commit después del byte SPI

El capturador toma PC_ID y la palabra de instrucción en el primer flanco con `(byte_seen_q || byte_done_i) && instr_valid_id && !stall`. Conserva la captura hasta reset. Los cuatro LEDs muestran el índice de palabra PC_ID[5:2]. Yosys puede eliminar los registros completos de PC e instrucción porque el top solo expone los cuatro bits LED. Los registros completos se comprueban en Icarus.

La comparación con el Espino original muestra únicamente el cambio de nombre del módulo local y seis salidas de observación con sus asignaciones. El puerto A de RAM registra la instrucción en el flanco con a_req_i. PC_ID e instrucción se observan en la etapa ID, con la validez y el stall de ese mismo ciclo. La traza confirma el LW en el flanco de commit 501.

## Interpretación física

El PCF coincide con el del repositorio. Reloj pin 15. D1 a D4 corresponden a 56, 57, 59 y 60 respectivamente, sin duplicados. La salida RTL usa 1 para encendido, según el mapeo y comportamiento físico reportado de la variante anterior.

| D4 a D1 | Lectura |
|---|---|
| 0000 | Espera del primer byte o captura con PC[5:2]=0 |
| 0001 | Byte recibido y espera de commit o captura con PC[5:2]=1 |
| 0011 | Captura con PC congruente a 0x0C módulo 64 |
| 0101 | Captura congruente a 0x14, LW STATUS en Icarus |
| 0110 | Captura congruente a 0x18, ANDI en el firmware |
| 0111 | Captura congruente a 0x1C, BEQ en el firmware |
| 1000 | Captura congruente a 0x20, LW PRICE en el firmware |
| Cualquier otro | Multiplicar el código binario por cuatro para obtener PC módulo 64 |

El código físico esperado es 0101, D1 y D3. Los LEDs no muestran los bits superiores del PC ni la instrucción. Tampoco indican el final de los 16 ticks. Una captura 0101 permite contrastar el primer commit físico con Icarus. La prueba física completa sigue pendiente.

## Reproducción desde pochoco_soc-main

```powershell
powershell -ExecutionPolicy Bypass -File proyecto4/pruebas_fisicas/demo_autonoma_bus_detail/ejecutar_pruebas.ps1
powershell -ExecutionPolicy Bypass -File proyecto4/pruebas_fisicas/demo_autonoma_bus_detail/sintetizar.ps1
```

El segundo comando elimina el BIN anterior, vuelve a ejecutar las pruebas y exige síntesis, chequeo de netlist, PCF válido, place and route y timing antes de empaquetar.

- Icarus unitario PASS, 18 comprobaciones.
- Icarus integrado PASS, 16 precios, 16 lecturas de cada uno de PRICE, SUM10 y READY, 16 DECISION y 16 MISO cotejados con los vectores Python. Se observaron 12.162 lecturas STATUS y 15 ACK ordenados.
- La traza de ciclos 498 a 510 está en build/simulacion_integrada.log. Byte y solicitud STATUS en 500, LW en 501, ANDI en 503, BEQ en 505 y siguiente STATUS en 508. MISO de la primera trama en 531 y primera escritura DECISION en 542. MISO de la segunda trama se coteja con esa primera decisión.
- Yosys produjo 964 LUT4 y 9 BRAM. El chequeo de la netlist reportó cero problemas.
- nextpnr HX1K/VQ100 usó 1.140/1.280 LC y cerró 25 MHz con Fmax final de 42,33 MHz.

## Programación manual

Conectar por USB y ejecutar desde la raíz del proyecto. Verificar el hash antes de programar. iceprog debe reportar VERIFY OK. Después de reiniciar, anotar los LEDs D4 a D1.

```powershell
$bin = 'proyecto4/pruebas_fisicas/demo_autonoma_bus_detail/build/demo_autonoma_bus_detail.bin'
Get-FileHash -Algorithm SHA256 $bin
iceprog $bin
```

SHA-256 esperado `CF9C849A1D7FAFD710D66B021CC5C9053A7CB7B9806D86BA69061D46201AF25C`.
