> **Referencia de investigacion y validacion.** La imagen activa para programar se encuentra en la raiz del repositorio: [guia actual](../../../README.md). Este directorio conserva fuentes que necesitan los comparadores y bancos; sus builds y documentos completos anteriores estan en el [historial previo](https://github.com/eaponce1/Proyecto_4_Arquitectura/tree/66eede4c46e211c02dc5ef22de18f86e22e775c5/proyecto4/alternativas/mmio_sma10). Los comandos y resultados historicos de abajo no identifican el BIN vigente.

# Alternativa MMIO SMA10

El SoC recibe el byte al mismo evento `byte_done` ya usado por el SPI Slave.
La FPGA maestra mantiene intacto su protocolo y el registro DECISION; Espino
continúa leyendo PRICE, aplicando la contabilidad local y tomando la señal.

## Mapa de registros

La ventana SPI se selecciona en `pochoco_soc.v` cuando `data_addr[31]` y
`data_addr[16]` valen uno. `pochoco_spi_slave.v` calcula el registro como
`data_addr[7:2]`: STATUS=0, PRICE=1 y DECISION=2. Los offsets siguientes,
antes no asignados (lectura cero), se usan para SMA10:

| Dirección | Offset palabra | Acceso | Significado |
|---|---:|---|---|
| `0x8001000C` | 3 | lectura | suma de los últimos diez precios (bits 11:0) |
| `0x80010010` | 4 | lectura | READY en bit 0, tras diez precios |

El Assembly arma la base `0x80010000` con `lui x1, 0x80010`; por eso usa
`lw x10,12(x1)` y `lw x13,16(x1)`. Estos offsets se derivan de la decodificación
RTL existente, no sustituyen STATUS, PRICE o DECISION.

## Actualización

El periférico conserva diez bytes en una BRAM iCE40. Un puntero circular
selecciona el precio saliente. Antes de aceptar el siguiente precio, la lectura
síncrona de la BRAM deja disponible ese byte; `byte_done` suma el nuevo precio
y, una vez lleno el historial, resta el saliente. El resultado máximo es
2550, por lo que 12 bits bastan. El periférico no decide comprar ni vender.

## Pruebas

Desde la raíz `pochoco_soc-main`:

```powershell
python proyecto4/sw/assembler.py proyecto4/alternativas/mmio_sma10/sw/trade.s -o proyecto4/alternativas/mmio_sma10/sw/trade.hex
python proyecto4/alternativas/mmio_sma10/medir_mmio_sma10.py --ticks 20000
```

El testbench autónomo `tb/tb_sma10.sv` compara suma/READY en 20.000 entradas.
