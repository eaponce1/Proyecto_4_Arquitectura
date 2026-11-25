# ATM — informe cuantitativo

**Dictamen: NO-GO. No reemplazar la imagen activa.**

Se investigaron 191 configuraciones, incluidas las perdedoras, y se
seleccionó la número 4 exclusivamente en los primeros 12.000 ticks
de cada serie. El protocolo se fijó antes de ejecutar la grilla. No se usaron
series secretas ni se descargaron datos externos. Los datos son de desarrollo
conocidos; LOCO, LOSO y walk-forward son validación interna.

## Diseño y criterios

ATM combina momentum rápido/lento, estados ALCISTA/LATERAL/BAJISTA, confirmación
de revisiones y gestión de exposición. La grilla compara señales de momentum,
medias, híbrida, persistencia, ruptura y pendiente; exposiciones 25/50/75/90/100 %
y dinámica; stops fijos/de volatilidad, permanencia, reserva, compras progresivas
y liquidación total/parcial. Todas las configuraciones están en PROTOCOLO.json.
Las variantes sin volatilidad son controles descriptivos; co-varían otros
parámetros del perfil y no permiten atribuir causalidad a un solo factor.

La elegida usa fast=16, slow=64, revisión=8, entrada delta rápido >=4 con delta
lento >=0 confirmado dos revisiones; salida delta rápido <=-4 y lento <=0, o
stop desde entrada/pico. Distancia de stop=min(40,max(12,4*max(1,volatilidad))).
Volatilidad es la media redondeada hacia arriba de 16 cambios absolutos de precio.
En lateralidad conserva la exposición anterior; en alcista busca 100 %, en
bajista 0 %. Mínimo 4 acciones por compra/rebalanceo y permanencia mínima de
16 ticks, salvo stop. El filtro de costo usa movimiento histórico por cantidad
>=10; es un proxy y no una estimación demostrada de rentabilidad esperada.

El ranking y las once puertas están congelados. Se exige >=6/8 ventajas,
mejor mediana monetaria y relativa, no empeorar la peor ventaja ni DD/comisiones,
LOCO>=5/8, LOSO>=6/8, WF>=14/24 y no empeorar victorias/peor ventaja de las 56
ternas. La elección no se repite mirando el test. Ninguna de las 155 variantes
elegibles cumplió simultáneamente las seis puertas descriptivas de serie completa;
ese cribado posterior se publica pero no se usa para seleccionar otra política.

## Contabilidad y referencias

Caja 10.000, inventario cero, comisión 5 por fill positivo, máximo 63, sin deuda
ni corto. Se ejecuta la orden anterior antes de decidir. La última decisión no
se liquida ficticiamente. Mantener teórico compra idealmente al inicio; mantener
SPI debe emitir y completar sus órdenes mediante el mismo protocolo. No son
referencias idénticas. La contabilidad ATM se cotejó con una implementación
anterior independiente en 160.000 ticks: cero discrepancias.

| Política | Patrimonio medio | Ventajas/8 | Peor final | DD máximo % | Comisión media |
|---|---:|---:|---:|---:|---:|
No_operar | 10.000 | 6 | 10.000 | 0,00 | 0
Mantener_teorico | 9.679 | 0 | 8.315 | 60,73 | 5
Mantener_SPI | 9.687 | 2 | 8.315 | 60,73 | 9
Momentum32 | 12.725 | 6 | 8.615 | 61,11 | 271
Tendencia_lenta | 10.971 | 5 | 8.540 | 50,55 | 119
SMA10 | 5.467 | 0 | 4.577 | 54,47 | 4.833
Agresiva | 9.558 | 4 | 4.531 | 63,86 | 76
Candidata_anterior | 10.234 | 6 | 8.284 | 30,34 | 106
ATM | 11.814 | 5 | 7.717 | 49,38 | 412

## Ocho series y operaciones ATM

| Serie | Momentum32 | ATM | Mantener | Ventaja ATM | Compras | Ventas | Comisión | DD % |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
AMD enero | 19.312 | 13.356 | 8.315 | 5.041 | 65 | 63 | 640 | 30,56
AMD mayo | 11.490 | 9.227 | 9.647 | -420 | 34 | 34 | 340 | 36,04
Apple 2022 | 12.528 | 12.740 | 11.063 | 1.677 | 46 | 46 | 460 | 31,65
Apple 2023 | 13.555 | 10.175 | 10.371 | -196 | 46 | 46 | 460 | 36,85
Meta 2022 | 13.700 | 16.366 | 9.695 | 6.671 | 37 | 37 | 370 | 17,46
Netflix 2022 | 8.615 | 10.816 | 9.179 | 1.637 | 42 | 42 | 420 | 36,46
Netflix 2023 | 8.929 | 7.717 | 9.170 | -1.453 | 31 | 30 | 305 | 49,38
Tesla 2022 | 13.671 | 14.115 | 9.995 | 4.120 | 30 | 30 | 300 | 29,34

Los CSV incluyen caja, inventario, tiempo invertido y exposición por tick.
Hay 160.000 filas en decisiones_tick.csv.gz y todas las operaciones en operaciones.csv.

## Folds y tres rondas

| Procedimiento | Momentum32 histórico | ATM |
|---|---:|---:|
| LOCO | 5/8 | 6/8 |
| LOSO | 6/8 | 5/8 |
| Walk-forward | 14/24 | 14/24 |

Las selecciones históricas LOCO/LOSO se comprobaron con su matriz completa;
las tres selecciones WF se recalcularon usando solo prefijos. Los resultados
históricos se reejecutaron, no se sustituyeron por los del entrenamiento.
En ATM, cada fold vuelve a elegir en su entrenamiento; LOCO excluye todas las
series de una empresa. WF reinicia cartera e indicadores en cada ventana test,
como en la referencia: no representa una única cartera continua por veinte mil ticks.

| Política | Ternas positivas/56 | Peor suma de patrimonios | Peor ventaja monetaria | Ventaja media |
|---|---:|---:|---:|---:|
Momentum32 | 56 | 29.034 | 660 | 9.137
ATM | 52 | 27.119 | -2.069 | 6.404
Tendencia_lenta | 52 | 27.154 | -2.859 | 3.875
SMA10 | 0 | 14.543 | -14.848 | -12.638
Mantener_SPI | 31 | 26.688 | -90 | 22
No_operar | 44 | 30.000 | -1.429 | 962
Mantener_teorico | 0 | 26.664 | 0 | 0

Se publican además 120 ternas con repetición por política. Las permutaciones de
una terna no cambian la suma y no se cuentan como evidencia adicional. El objetivo
de suma de tres patrimonios sigue la instrucción de investigación del usuario;
estas combinaciones no son resultados oficiales de competencia ni determinan su nota.

## Por qué es NO-GO

ATM logra 5/8 frente a 6/8; su mediana relativa es
16,50 % frente a 24,90 %.
Su peor ventaja es -15,85 % frente a
-6,14 %. Reduce DD máximo a
49,38 %, pero aumenta la comisión media a
411,88. La mayor protección no compensa los fallos
de rentabilidad y consistencia exigidos. Los perdedores y el mejor caso están
identificados en resultados_por_empresa.csv. Los nueve estreses sintéticos se
publican por separado; no se atribuyen fechas o empresas a esas secuencias.

## Assembly, RTL, timing y BIN

**No ejecutados para ATM por NO-GO cuantitativo.** No se generaron trade.s,
trade.hex ni BIN de ATM; no se reutilizó el HEX anterior como si fuera nuevo.
No hay ciclos, CPI, LUT4, BRAM, Fmax ni 4/4 del profesor atribuibles a ATM.
Las pruebas originales de referencia Icarus se repitieron y permanecen en
resultados/referencia/; no son pruebas RTL de ATM. Los testbenches oficiales y
sus cuatro criterios permanecen intactos.

La versión activa conserva 1260/1280 LC, 9/16 BRAM, Fmax de 50,19 MHz y reloj
de procesamiento de 12,5 MHz. Su máximo observado de decisión es 321 ciclos,
25,68 us. Estas cifras son de la referencia, no mediciones de la candidata.
BIN activo SHA-256: 5e1579caef1f8de2813b6cf50bb17c505e77b3a534787447d27660eaad63a606.
No hay hash de BIN ATM porque no existe una imagen aprobada.

## Reproducción y programación

Desde la raíz del repositorio:

```powershell
python -X utf8 -B proyecto4/alternativas/atm_adaptativa/ejecutar_todo.py
```

El ejecutor reproduce la investigación, los controles y el informe. Conserva
el fallo financiero como NO-GO. Para programar manualmente la última versión
físicamente confirmada, seguir usando el programar.ps1 de la raíz; no programa ATM.
No se ejecutó iceprog en esta investigación. No se hereda a ATM la confirmación
de compras/ventas de la imagen activa. No se aportaron patrimonios oficiales
de tres rondas ni una nueva prueba física ATM.

## Conclusión

La familia y la grilla exploradas no justifican sustituir Momentum32. La mejora
aislada del drawdown y del fold LOCO no cumple el conjunto de puertas fijadas.
Este NO-GO no demuestra que toda estrategia adaptativa sea inferior; limita la
conclusión a estas configuraciones, reglas de selección y datos conocidos.
Se preservan los resultados fallidos para revisión y se mantiene el BIN funcional.
