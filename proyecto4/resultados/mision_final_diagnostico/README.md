# Diagnóstico de cero órdenes en la FPGA

La última programación conocida grabó `trade_conservar.bin`, con SHA-256 `5F3C32E0AC266614B4B8FE825672255D7D29BF924CE51D3BB3E249516E052FC1`. La sesión de programación devolvió `VERIFY OK` y CDONE alto. En el reporte de la práctica Fila 5, JC arriba, la maestra mostró 20.000 ticks, 10 ms, PLACAS y cero órdenes. Cuando se consultó si hubo otra grabación entre ambos hechos, el usuario respondió «No lo sé».

**Causa reproducida:** la única escritura DECISION de `conservar.s` es `sw x0, 8(x1)`. Mientras Conservar está cargado, el hardware recibe cada precio y el procesador responde mantener. La ausencia de órdenes es el comportamiento previsto incluso con SPI funcional. Para atribuirle la práctica histórica de Fila 5 hace falta el hash del BIN de aquella sesión o el registro MISO y una serie conocida. Esta auditoría no leyó ni escribió la flash por USB.

## Evidencia disponible

- [Huellas comparadas](huellas_compiladas.csv). Se reensamblaron los HEX y se empaquetaron los ASC de cinco compilaciones. Cada comparación fue byte por byte. `competition.bin` histórico y `trade_mmio_base.bin` comparten bytes y huella. Conservar es una imagen diferente.
- [Simulación del propio BIN Conservar](bitstream_conservar_simulacion.log). `iceunpack` y `icebox_vlog` reconstruyeron la lógica del BIN y se comprobaron 70 MISO, todos `0x00`, en un vector de recuperación. LEDs `0111` correspondientes a instrucciones, precio recibido y PRICE leído sin decisión distinta de cero.
- [Resumen de A–F](resumen_escenarios.csv). 18 ejecuciones Icarus de 194 ticks completaron 3.492 transacciones. En los seis escenarios, Conservar mantuvo $10.000 y 0 órdenes. SMA10 base y Activo anterior compraron en el descenso, la caída y la recuperación y vendieron en la recuperación.
- Trazas completas en `base/`, `activo/` y `conservar/`, una carpeta por escenario con `ticks.csv`. El banco observa el precio recibido y la respuesta de STATUS, PRICE, SUM10 y READY. Coteja el byte DECISION, MISO y cartera interna de Espino en los modos activos.

## Contexto de las otras prácticas

Fila 7 con Apple mostró $10.000 y 0 órdenes, con precio final 124. Fila 2 con Tesla mostró $5.329 y la maestra contabilizó operaciones en su canal. Son ensayos distintos de Fila 5 y la serie de práctica del repositorio termina en 160. Se conservan sus registros anteriores.

## Repetir

Desde la raíz con Icarus, Python y las herramientas de IceStorm en PATH:

```powershell
$d = 'proyecto4/resultados/mision_final_diagnostico'
python -X utf8 -B "$d/diagnosticar.py"
python -X utf8 -B "$d/auditar_binarios.py"
powershell -NoProfile -ExecutionPolicy Bypass -File .\tb\ejecutar_tb_proyecto4.ps1
```

La ejecución de Windows de esta misión se realizó desde una copia aislada de la entrega y el banco `tb/` auditado. El registro previo y la repetición se conservan en archivos separados.

La repetición completó 2.000 ticks, 4/4 criterios y equivalencia Python con salida 0. El resultado fue $9.839, 109 órdenes, drawdown $396 y 253 ciclos de peor caso. [Log original repetido](windows_2000_repeticion/icarus.log) · [Decisiones](windows_2000_repeticion/decisiones.csv)

