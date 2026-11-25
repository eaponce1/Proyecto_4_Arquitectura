# ATM adaptativa — NO-GO

Investigación aislada en `codex/atm-adaptativa`, desde `07d0dd95`. **No sustituye
el firmware ni el BIN de la raíz.** El resultado financiero no autorizó las fases
de Assembly, RTL ni síntesis; no hay un `competition.bin` de ATM para programar.

- [Informe cuantitativo](INFORME_CUANTITATIVO.md) y [PDF LaTeX](INFORME_CUANTITATIVO.pdf).
- [Protocolo previo](PROTOCOLO.json), 191 configuraciones, ranking y puertas congelados.
- [Decisión](resultados/decision.json), [matriz](resultados/matriz_aceptacion.csv) y
  [estado por fase](resultados/estado_fases.json).
- [Ocho series](resultados/resultados_por_empresa.csv), [LOCO/LOSO](resultados/resultados_leave_one_out.csv),
  [walk-forward](resultados/resultados_walk_forward.csv) y [ternas](resultados/combinaciones_tres_rondas.csv).
- `resultados/decisiones_tick.csv.gz`: 160.000 filas comprimidas sin pérdida.
  `backtest.py` regenera también el CSV abierto. `operaciones.csv` registra cada fill.
- `SHA256_entrega.txt`: firmas de fuentes y evidencia publicada.

ATM seleccionada obtiene 5/8 ventajas, mediana relativa 16,50 % y peor ventaja
-15,85 %. Momentum32 conserva 6/8, 24,90 % y -6,14 %. El DD de ATM baja a 49,38 %,
pero la comisión media aumenta a $411,88. LOCO 6/8, LOSO 5/8 y WF 14/24 son
validación interna; no acreditan superioridad en series secretas.

Desde la raíz del repositorio, con Python 3, Matplotlib, Icarus y Yosys:

```powershell
python -X utf8 -B proyecto4/alternativas/atm_adaptativa/ejecutar_todo.py
```

En Windows, el PDF requiere WSL Ubuntu con pdfLaTeX y poppler; en Linux,
`pdflatex`, `pdfinfo` y `pdftotext` en PATH. Las versiones exactas de referencia
están en `resultados/referencia/herramientas.json`. `--sin-pdf` permite repetir
solo la investigación. `--sin-rtl-referencia` reutiliza la evidencia de la
referencia ya ejecutada; no convierte sus pruebas en pruebas de ATM.

Para verificar lo recibido sin recalcular:

```powershell
python -X utf8 -B proyecto4/alternativas/atm_adaptativa/verificar_entrega.py
```

Las variantes conocidas se reejecutan con la misma contabilidad. El modelo lento
replica SUM10/128/5 % del ZIP analizado; no confundirlo con los otros parámetros
de investigación de ese ZIP. El benchmark teórico compra idealmente en tick 0;
el benchmark SPI respeta la orden pendiente y el máximo por byte.

Las pruebas originales del profesor y los archivos activos están protegidos por
hashes en `resultados/referencia/fuentes_activos_antes.json`. No se añadieron
bancos sustitutos del oficial. Por NO-GO no se ejecutó un banco con ATM ni se
inventaron ciclos, CPI o resultados de síntesis. La confirmación física anterior
pertenece al BIN activo, no a esta familia. Las firmas de los respaldos y las
versiones históricas siguen disponibles; no se eliminaron.

Para programar la Go Board, seguir usando **`programar.ps1` de la raíz**, que
verifica y programa la última imagen físicamente confirmada. No ejecutar un
`iceprog` apuntando a esta carpeta: no contiene una imagen nueva aprobada.

El PR se deja abierto para revisión; esta investigación no autoriza fusionar
ni reemplazar automáticamente la versión operativa.
