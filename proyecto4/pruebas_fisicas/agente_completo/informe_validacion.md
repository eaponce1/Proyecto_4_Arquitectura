# Informe de validación del agente completo

Fecha de ejecución: 22-11-2026. Variante aislada en `proyecto4/pruebas_fisicas/agente_completo/`.

## Diseño

El top conecta el maestro SPI de prueba directamente a SCLK, MOSI y CS_n del SPI Slave y devuelve el MISO del Slave al maestro. El maestro solo lee y transmite la tabla `prices.hex`. `trade.hex`, cargado por `pochoco_ram`, se ejecuta en el Espino Core; las escrituras DECISION se generan en el bus de datos del Espino. El Slave entrega PRICE/STATUS y recibe DECISION. El bloque MMIO SMA10 recibe `price_valid` y suministra SUM10/READY. El comparador de respuestas se encuentra en un camino de observación separado.

`pochoco_soc_observable.v` es una copia separada del top SoC de la variante MMIO base. Solo se renombra el módulo y se agregan taps de reset, bus/fetch y lecturas/escrituras para los indicadores. Los módulos funcionales se compilan desde `proyecto4/alternativas/mmio_sma10/rtl/`, no se copian ni se editan. Se compila el `trade.hex` ya existente de esa variante.

## Simulación

Comando ejecutado desde la raíz del repositorio:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File proyecto4/pruebas_fisicas/agente_completo/ejecutar_simulacion.ps1
```

Resultado real de Icarus Verilog:

```text
PASS agente completo: reset_low=1 reset_released=1 ticks=16 fetch=94156 commit=70652 STATUS=23410 PRICE=16 SUM10=16 READY=16 DECISION=16 MISO_check=16
```

La secuencia fue `c8` diez veces, `5a` tres veces y `dc` tres veces (precios 200, 90 y 220). El modelo Python generó una compra de 16 acciones y una venta de 16. `expected_writes.hex` valida las 16 escrituras del CPU, y `expected_decisions.hex` valida cada byte recibido desde MISO. La respuesta `0x50` aparece en la transacción posterior a su escritura y `0x90` igualmente llega en la transacción siguiente: el desfase queda cotejado tick a tick. STATUS se consulta en polling; cada PRICE se leyó y el procesador leyó SUM10/READY 16 veces cada uno. El test falla si un byte previo sigue pendiente al comenzar otro tick.

Icarus emitió el aviso conocido de que el firmware ocupa menos palabras que la RAM declarada (71 frente a 512); no afectó la simulación.

## Síntesis temprana

Comando ejecutado:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File proyecto4/pruebas_fisicas/agente_completo/ejecutar_sintesis.ps1
```

| Medida | MMIO base registrada | Agente completo interno |
|---|---:|---:|
| LUT4 (Yosys) | 1.055 | 1.295 |
| Logic Cells (nextpnr) | 1.279 / 1.280 | 1.550 / 1.280 (121%) |
| BRAM | 13 / 16 | 13 / 16 |
| Fmax | 40,50 MHz | No disponible |
| Place and route | PASS, 25 MHz | FAIL: no cabe en el dispositivo |
| `.bin` | existente, referencia | No generado |

El agregado usa +240 LUT4 sintetizadas y +271 LC respecto a los registros de la MMIO base. Yosys mapeó la ROM de 16 precios y la tabla esperada del verificador a flip-flops y multiplexores, no a BRAM; el SoC se mantiene en 13 BRAM. Nextpnr termina al intentar ubicar 1.550 LC frente a 1.280 y falla antes de calcular una frecuencia enrutada. Por ello no hay bitstream ni medida de timing para esta variante. No se ejecutó `icepack` ni se programó la placa.

Herramientas informadas por las instalaciones utilizadas: Python 3.13.3; Icarus Verilog 14.0 (devel, 2026-03-01); Yosys 0.70+176; nextpnr-ice40 0.11.1-68. El objetivo de P&R fue HX1K/VQ100, semilla 1 y restricción de 25 MHz.

## Límite y siguiente paso

La integración funciona en simulación, pero no es implementable en HX1K en su forma actual. La referencia MMIO base ya consume 1.279 LC; el maestro, la secuencia de precios y el verificador exceden en conjunto el límite. Según la regla acordada, el trabajo físico se detiene aquí. Para una nueva iteración de área haría falta autorización para rediseñar la representación de tabla/verificador o cambiar cómo se aporta la serie, sin tocar el algoritmo del Espino ni la MMIO base. El bitstream original se conserva.
