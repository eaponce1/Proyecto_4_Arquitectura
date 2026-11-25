# Demo autónoma – variante de diagnóstico

Esta carpeta contiene una variante independiente para diagnosticar las tres
causas que antes se agrupaban en D3. No modifica `demo_autonoma`, MMIO SMA10,
Espino, SPI Slave, SMA10 ni el firmware original. Usa esos RTL/firmware como
dependencias y añade un top y un monitor de errores propios.

## LEDs

| LED Go Board | Señal | Significado |
|---|---|---|
| D1 | `o_LED[0]` | El Espino inició fetch |
| D2 | `o_LED[1]` | Bit 0 del primer código de error |
| D3 | `o_LED[2]` | Error general: `error_code != 0` |
| D4 | `o_LED[3]` | Bit 1 del primer código de error |

Los errores son sticky hasta reset. Captura el primero que aparece; si más de
una condición está activa en el mismo ciclo, la prioridad es 1, luego 2 y luego
3.

| Código | D2 | D4 | Condición |
|---:|---|---|---|
| 01 | encendido | apagado | Llega precio nuevo con `price_pending=1` |
| 10 | apagado | encendido | DECISION escrita sin leer PRICE en ese tick |
| 11 | encendido | encendido | DECISION escrita cuando ya había 16 decisiones |
| 00 | apagado | apagado | Sin error |

D3 siempre indica que existe un código distinto de cero. En una ejecución
correcta final, D1 queda encendido y D2/D3/D4 apagados. D4 ya no indica
finalización; se reutiliza para el bit alto del código.

## Pruebas reproducibles

Desde la raíz `pochoco_soc-main`:

```powershell
powershell -ExecutionPolicy Bypass -File proyecto4/pruebas_fisicas/demo_autonoma_debug/ejecutar_pruebas.ps1
powershell -ExecutionPolicy Bypass -File proyecto4/pruebas_fisicas/demo_autonoma_debug/sintetizar.ps1
```

El testbench unitario inyecta cada evento por separado y comprueba que un evento
posterior no sobrescriba el primero. El test integrado envía 16 precios y
compara escrituras DECISION y respuestas MISO tick a tick con la referencia
Python `estrategia_reversion_media`.

## Resultados medidos

Validación del 22-11-2026:

- Monitor de errores: PASS para condiciones 1, 2, 3, retención del primer
  error y estado normal sin error.
- Integración: PASS, 16/16 ticks, STATUS=12160, PRICE=16, SUM10=16, READY=16,
  DECISION=16, MISO=16, una compra, una venta y cero ticks perdidos.
- Yosys: 995 LUT4.
- nextpnr HX1K/VQ100: 1165/1280 LC, 9/16 BRAM, Fmax final 42,04 MHz; PASS a
  25 MHz.
- Bitstream independiente: `build/demo_autonoma_debug.bin`.

SHA-256 del binario: `127A4ADE357B0C0D2C802C8E044BC3FBC95B60ECF2AE8ADA4854DB7C80564D59`.
El bitstream no se ha programado automáticamente.
