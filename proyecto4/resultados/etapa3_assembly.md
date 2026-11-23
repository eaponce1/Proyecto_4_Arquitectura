# Etapa 3 — implementación Assembly RV32E de SMA10

## Estado

Se implementó `proyecto4/sw/trade.s` y se generó `proyecto4/sw/trade.hex` con el assembler original del Proyecto 2. La imagen contiene 89 instrucciones/palabras, por debajo de la palabra RAM 500 reservada para historial. No se modificaron RTL, Espino Core, ALU, assembler ni el testbench original del Proyecto 4.

## Algoritmo Python auditado

La referencia exacta está en `python/enfoques_finales.py`, función `estrategia_reversion_media`. Con al menos diez precios, calcula `S=sum(últimos 10)` y compara `10*p` con los umbrales enteros:

- Sin acciones: comprar 16 si `10*p <= S-10`; de lo contrario mantener.
- Con acciones: vender `min(16, acciones)` si `10*p >= S+10`; de lo contrario mantener.
- En calentamiento, con menos de diez muestras: mantener.

El parámetro 10 es el margen fijo que define esa implementación. No se sustituyó por otro margen ni se adelantó información. El byte es `0x50` para comprar 16, `0x80 + q` para vender q, y `0x00` para mantener. El firmware actual reproduce la referencia Python tick a tick.

## SPI, memoria y registros

Las direcciones se tomaron del RTL `rtl/pochoco_spi_slave.v`: base `0x80010000`; STATUS `+0` (bit 0 indica precio nuevo), PRICE `+4` (leerlo limpia la bandera) y DECISION `+8`. El SoC se configura con SPI habilitado (`EnableSpi=1`) en la prueba RTL dedicada.

El historial circular usa diez palabras en RAM, bytes 2000–2036 (índices de palabra 500–509); byte 2040 es el centinela exclusivo. La imagen debe seguir ocupando menos de 500 palabras. Registros RV32E asignados:

| Registro | Uso |
|---|---|
| x1 | Base MMIO SPI |
| x2 | STATUS temporal |
| x3 | precio actual |
| x4 | decisión pendiente / byte transmitido |
| x5 | acciones mantenidas localmente |
| x6 | número de muestras válidas, saturado en 10 |
| x7 | puntero circular de escritura |
| x8 | puntero de suma SMA |
| x9 | contador de multiplicación por sumas / cantidad asequible |
| x10 | suma de diez precios |
| x11 | cantidad / temporal |
| x12 | `10*p` / fee temporal |
| x13 | temporales y presupuesto de compra |
| x14 | fin del buffer (2040) |
| x15 | caja local, inicializada a 10.000 |

El ciclo sondea STATUS hasta bit 0, lee PRICE, aplica localmente al portfolio la decisión recibida (la FPGA ya la ejecutó al precio actual), añade el precio al anillo, calcula la nueva decisión con el historial actualizado y escribe DECISION para la siguiente transacción. Así se conserva el desfase SPI. SMA10 se compara sin dividir: `10*p` se forma como `8*p + 2*p` mediante sumas. La compra aplica el máximo asequible mediante restas repetidas y limita la solicitud a 16. La venta usa la cantidad disponible codificada en la decisión pendiente.

Las instrucciones emitidas y empleadas son `lui`, `addi`, `lw`, `sw`, `andi`, `add`, `sub`, `beq`, `bne`, `bge` y `jal`; no hay shifts, MUL, DIV ni pseudoinstrucciones. El programa actualiza su contabilidad local para reproducir fills parciales y la condición de comisión de la venta.

## Ciclos y riesgos

Estimación inicial, no medida: aproximadamente 100–300 instrucciones por precio (≈235–705 ciclos con CPI 2,35), sin contar espera de STATUS. El número depende de la cantidad de sumas para compras/ventas y del CPI real. No se ha medido el tiempo RTL ni certificado que se procese cada tick a 0,1 ms.

Riesgos que quedan: si el firmware no observa un tick, su caja/acciones locales dejan de reflejar la contabilidad maestra; la prueba RTL integrada cubre una serie corta, no los 20.000 ticks; el rango de ciclos es aproximado y no modela latencias reales de memoria/MMIO. El historial y el código no deben solaparse al cambiar la imagen.

## Validación ejecutada

| Validación | Resultado real |
|---|---|
| Ensamblado por `sw/assembler.py` | Aprobado; 89 palabras |
| HEX contra Python, secuencia completa de 20.000 ticks | Aprobado; decisión recibida y decisión siguiente coinciden en cada tick |
| HEX contra Python, caso sintético de fills parciales | Aprobado |
| Integración RTL/Icarus con SPI y serie sintética de 30 ticks | Aprobado; MISO/decisiones comparadas con Python; prueba ejecutada como parte de la suite |
| Suite Python Proyecto 4 | Aprobado: 32 pruebas |
| Suite Python Proyecto 2 | Aprobado: 11 pruebas |
| Regresión `tests/run_tests.py` Proyecto 2 | Falla en `periph_tb` con `debounced buttons`; el banco espera una polaridad de botones que no coincide con la inversión activa-baja del RTL. El core sí pasa antes del fallo. No se modificó ese RTL ni su banco. |

La equivalencia completa demostrada es de ejecución funcional/instrucción del HEX frente a Python, no de simulación RTL ciclo a ciclo durante los 20.000 ticks. El test de integración RTL verifica SPI con una entrada sintética corta. Tampoco se midieron ciclos en hardware ni se programó la Go Board.

## Comandos

Desde `pochoco_soc-main`:

```powershell
python sw/assembler.py proyecto4/sw/trade.s -o proyecto4/sw/trade.hex
python -B -m unittest discover -s proyecto4/python -v
python -B -m unittest discover -s tests -v
python -B tests/run_tests.py
```

La prueba integrada requiere `iverilog` y `vvp` disponibles en PATH. El comando heredado `tests/run_tests.py` termina en el fallo conocido de `periph_tb`.
