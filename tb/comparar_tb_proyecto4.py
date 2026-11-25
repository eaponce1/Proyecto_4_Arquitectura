"""Valida los datos del banco y compara sus resultados con la referencia SMA10."""

import argparse
import csv
from pathlib import Path
import re
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "proyecto4" / "python"))
from enfoques_finales import estrategia_reversion_media
from simulador import leer_precios, simular_estrategia


def comparar(precios: list[int], csv_rtl: Path, log_icarus: Path) -> None:
    referencia = simular_estrategia(precios, "SMA10", estrategia_reversion_media)
    with csv_rtl.open(encoding="utf-8", newline="") as archivo:
        observado = list(csv.DictReader(archivo))
    if len(observado) != len(precios):
        raise ValueError(f"Esperados {len(precios)} ticks, Icarus registró {len(observado)}")

    campos = {
        "tick": "tick",
        "precio": "precio",
        "decision": "decision_recibida",
        "decision_escrita": "decision_siguiente",
        "caja": "caja",
        "acciones": "acciones",
        "patrimonio": "patrimonio",
    }
    latencias = []
    for rtl, python in zip(observado, referencia.decisiones, strict=True):
        for campo, campo_python in campos.items():
            dato = int(rtl[campo], 16 if campo.startswith("decision") else 10)
            esperado = python[campo_python]
            if dato != esperado:
                raise ValueError(f"Tick {python['tick']}, {campo}: RTL={dato}, Python={esperado}")
        latencias.append(int(rtl["ciclos"]))

    log = log_icarus.read_text(encoding="utf-8-sig")
    for etiqueta, esperado in {
        "Patrimonio final": referencia.metricas.patrimonio_final,
        "Ordenes ejecutadas": referencia.metricas.ordenes,
        "Perdida maxima": referencia.metricas.perdida_maxima,
    }.items():
        medicion = re.search(rf"^{etiqueta}:\s+(\d+)$", log, re.MULTILINE)
        if not medicion or int(medicion[1]) != esperado:
            raise ValueError(f"El log no coincide con Python para {etiqueta}={esperado}")

    latencia = re.search(
        r"^Peor caso precio->decision: (\d+) ciclos \(disponibles: (\d+)\)$",
        log, re.MULTILINE,
    )
    if not latencia or min(latencias) < 1 or max(latencias) != int(latencia[1]):
        raise ValueError("El peor caso no coincide con las latencias por tick")
    if max(latencias) >= int(latencia[2]):
        raise ValueError("El peor caso alcanza o supera el presupuesto de ciclos")

    print(f"PASS Python: {len(precios)} DECISION y {len(precios)} MISO, 0 diferencias")
    print(f"PASS Python: precio, caja, acciones y patrimonio en los {len(precios)} ticks")
    print(f"PASS Python: patrimonio {referencia.metricas.patrimonio_final}, "
          f"ordenes {referencia.metricas.ordenes}, drawdown {referencia.metricas.perdida_maxima}")
    print(f"PASS latencia: maximo de {max(latencias)} ciclos verificado en el CSV")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--serie", type=Path, required=True)
    parser.add_argument("--ticks", type=int, required=True)
    parser.add_argument("--resultado", type=Path)
    parser.add_argument("--log", type=Path)
    args = parser.parse_args()
    if (args.resultado is None) != (args.log is None):
        parser.error("--resultado y --log se proporcionan juntos")
    try:
        precios = leer_precios(args.serie)
        if not 1 <= args.ticks <= len(precios):
            raise ValueError(f"El número de ticks debe estar entre 1 y {len(precios)}")
        if args.resultado is None:
            print(f"PASS CSV: {len(precios)} precios consecutivos de {min(precios)} a {max(precios)}; "
                  f"se simularan los primeros {args.ticks}")
        else:
            comparar(precios[:args.ticks], args.resultado, args.log)
    except (OSError, ValueError, KeyError) as error:
        raise SystemExit(f"FAIL Python: {error}") from error


if __name__ == "__main__":
    main()
