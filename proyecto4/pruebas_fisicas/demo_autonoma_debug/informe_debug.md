# Informe de la variante de diagnóstico

## Cambios

La variante `demo_autonoma_debug` conserva el generador SPI, SoC MMIO SMA10,
Espino y firmware de `demo_autonoma`. Solo el nuevo top de diagnóstico añade
`error_code[1:0]`, que permanece en cero hasta el primer error y después queda
enclavado hasta reset. Las banderas de las tres condiciones provienen de las
mismas señales que antes alimentaban `error_seen`:

1. `spi_byte_done && price_pending` captura código `01`.
2. `decision_write && !price_read_since_tick` captura código `10`.
3. `decision_write && decision_count >= 16` captura código `11`.

La prioridad dentro de un mismo ciclo es 1, 2 y 3. D3 se activa con cualquier
código no cero. D2 muestra el bit bajo del código y D4 el bit alto; D1 conserva
la indicación de que comenzó el fetch del Espino. Por ello D4 deja de funcionar
como indicador de finalización en esta variante.

## Validación ejecutada

Comandos desde la raíz `pochoco_soc-main`:

```powershell
powershell -ExecutionPolicy Bypass -File proyecto4/pruebas_fisicas/demo_autonoma_debug/ejecutar_pruebas.ps1
powershell -ExecutionPolicy Bypass -File proyecto4/pruebas_fisicas/demo_autonoma_debug/sintetizar.ps1
```

| Prueba | Resultado real |
|---|---|
| Condición 1 aislada → código 1 | PASS |
| Condición 2 aislada → código 2 | PASS |
| Condición 3 aislada → código 3 | PASS |
| Un error posterior conserva el primero | PASS |
| Secuencia correcta no produce error | PASS |
| Simulación integrada / 16 precios | PASS |
| Escrituras del Espino contra Python | 16/16 coinciden |
| Respuestas MISO contra Python | 16/16 coinciden |
| Lecturas STATUS / PRICE / SUM10 / READY | 12160 / 16 / 16 / 16 |
| DECISION / MISO / ticks perdidos | 16 / 16 / 0 |

En la ejecución integrada Python esperaba una compra y una venta. El monitor
acabó con `error_code=00`; las salidas lógicas fueron `LED=0001`, actividad del
Espino únicamente.

## Implementación FPGA

Yosys 0.70+176 y nextpnr-ice40 0.11.1-68-g1daf1f5c sintetizaron y ubicaron el
diseño para HX1K/VQ100, seed 1 y reloj pedido de 25 MHz.

| Recurso/medición | Resultado |
|---|---:|
| LUT4 | 995 |
| Logic Cells | 1165/1280 (91%) |
| BRAM | 9/16 |
| Fmax final | 42,04 MHz |
| Timing a 25 MHz | PASS |
| Archivo `.bin` | Generado después de simulación y P&R correctos |

Ruta del binario: `build/demo_autonoma_debug.bin`.

SHA-256: `127A4ADE357B0C0D2C802C8E044BC3FBC95B60ECF2AE8ADA4854DB7C80564D59`.

No se programó la Go Board. La confirmación del código físico requiere que se
programe manualmente este archivo exacto; `VERIFY OK` de una imagen anterior no
permite inferir qué condición disparó D3 en esta variante.
