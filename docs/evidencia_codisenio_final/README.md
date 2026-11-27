# Co-diseño de la política final

Comparación nueva, a 12,5 MHz, SUM10/128 ticks/5%, mismas ocho series y cartera
causal. No se cambia el BIN activo. Las 32 trazas completas (640.000 ticks)
están en `trazas/`; no son 32 muestras financieras independientes.

| Variante | Ciclos medios | Máximo | LC | BRAM | Fmax SoC | Ruta |
|---|---:|---:|---:|---:|---:|---|
| Software incremental | 127,07279 | 303 | 1199 | 8 | 50,71 MHz | PASS |
| Custom-0 | 125,07309 | 303 | 1368 | 10 | No válido | No cabe |
| MMIO incremental activo | 83,97834 | 259 | 1219 | 9 | 50,67 MHz | PASS |
| MMIO barrido | 83,97834 | 259 | 1227 | 9 | 51,04 MHz | PASS |

Se conserva MMIO incremental: 1,51316× frente a software, kernel de 49,1006 a
6 ciclos, actualización inmediata y ocho LC menos que barrido. El barrido acaba
antes de que la CPU lea y por eso sus ciclos de extremo a extremo son iguales.
Custom-0 ahorra dos ciclos por kernel, pero excede la HX1K en 88 LC.

`equivalencia_perfil.json` liga trazas y fuentes; `hardware.json`, los resultados
de Yosys y nextpnr. `resumen.json` y `comparacion.csv` agregan métricas y Amdahl.
`implantacion/` conserva logs completos, netlists comprimidas, reportes de timing
y ASC de las tres implementaciones que caben. No hay ASC válido de Custom-0.
`unidades.json` y `unidades/` registran pruebas de instrucción y reinicio BRAM.
`auditoria.json` es el resultado del cotejo de todas las filas almacenadas.

El perfil marca PC de entrada/salida del kernel. Comprueba por tick que
RX + cartera + kernel + decisión = latencia total. En todas las variantes coteja
SUM10/READY en registros, además de MISO, DECISION y contabilidad del banco
estricto. La ventana incluye recepción completa a escritura DECISION, no espera
posterior. IC cuenta commits y CPI es ciclos/IC acumulados. Una operación útil
es un precio procesado hasta DECISION; la capacidad de servicio no equivale a
compras por segundo ni se probó como tasa máxima de entrada.

El roofline del informe usa techos arquitectónicos de 50 MB/s para LSU32 y
25 MB/s por puerto BRAM16, sin afirmar medición de ancho de banda o potencia.
El kernel software es incremental optimizado, no una base ingenua O(10).
El estudio histórico anterior queda en `../evidencia_codisenio/`.

Desde la raíz del repositorio, OSS CAD Suite en PATH y Ubuntu WSL con G++/make:

```powershell
python -B tools/preparar_codisenio_lento.py
python -B tools/banco_codisenio_lento.py
python -B tools/probar_unidades_codisenio.py
wsl -d Ubuntu -- bash tools/codisenio_lento_wsl.sh --fase smoke --sin-preparar
wsl -d Ubuntu -- bash tools/codisenio_lento_wsl.sh --fase simular --sin-preparar
python -B tools/medir_codisenio_lento.py --fase hardware --sin-preparar
python -B tools/resumir_codisenio_lento.py
python -B tools/graficar_codisenio_final.py
python -B tools/auditar_codisenio_final.py
```

La preparación debe terminar antes de simular o sintetizar. El flujo hardware
usa HX1K/VQ100, PCF activo, semilla 1 y restricción 25 MHz; no ejecuta iceprog.
Para auditar la evidencia publicada basta el último comando, sin WSL ni FPGA.
