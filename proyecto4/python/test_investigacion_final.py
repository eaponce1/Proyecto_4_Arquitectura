"""Pruebas de causalidad, límites y contabilidad de los enfoques finales."""

import unittest

from enfoques_finales import (
    estrategia_momentum_umbral,
    estrategia_reversion_media,
    estrategia_tendencia_persistente,
)
from estrategia import Accion, Decision, MANTENER
from simulador import simular_estrategia


class EnfoquesFinalesTests(unittest.TestCase):
    def test_cantidad_por_orden_no_supera_63(self):
        subida = list(range(100, 110))
        self.assertLessEqual(estrategia_momentum_umbral(subida, 0).cantidad, 63)
        self.assertLessEqual(estrategia_reversion_media([110] * 9 + [100], 0).cantidad, 63)
        persistente = list(range(100, 112))
        self.assertLessEqual(estrategia_tendencia_persistente(persistente, 0).cantidad, 63)

    def test_momentum_umbral_y_estado_plano_largo(self):
        subida = [100, 100, 100, 100, 101]
        buy = estrategia_momentum_umbral(subida, 0)
        self.assertEqual(buy, Decision(Accion.COMPRAR, 16))
        self.assertEqual(estrategia_momentum_umbral(subida, 16), MANTENER)
        bajada = [110, 110, 110, 110, 109]
        self.assertEqual(estrategia_momentum_umbral(bajada, 16), Decision(Accion.VENDER, 16))

    def test_reversion_sma10_entra_bajo_y_sale_sobre(self):
        abajo = [110] * 9 + [99]
        arriba = [100] * 9 + [111]
        self.assertEqual(estrategia_reversion_media(abajo, 0), Decision(Accion.COMPRAR, 16))
        self.assertEqual(estrategia_reversion_media(arriba, 16), Decision(Accion.VENDER, 16))
        self.assertEqual(estrategia_reversion_media(arriba, 0), MANTENER)

    def test_tendencia_requiere_dos_cierres_y_mantiene_hasta_reversion(self):
        subida = list(range(100, 112))
        buy = estrategia_tendencia_persistente(subida, 0)
        self.assertEqual(buy, Decision(Accion.COMPRAR, 16))
        self.assertEqual(estrategia_tendencia_persistente(subida, 16), MANTENER)
        bajada = list(range(120, 108, -1))
        self.assertEqual(estrategia_tendencia_persistente(bajada, 16), Decision(Accion.VENDER, 16))

    def test_no_consulta_precios_futuros(self):
        prefijo = [100, 101, 100, 102, 101, 104, 103, 105, 106, 105, 108, 109]
        futuros_a = prefijo + [255] * 20
        futuros_b = prefijo + [1] * 20
        for politica in (estrategia_momentum_umbral, estrategia_reversion_media,
                         estrategia_tendencia_persistente):
            a = simular_estrategia(futuros_a, "a", politica)
            b = simular_estrategia(futuros_b, "b", politica)
            for tick in range(len(prefijo)):
                self.assertEqual(a.decisiones[tick]["decision_siguiente"], b.decisiones[tick]["decision_siguiente"])

    def test_desfase_y_limites_contables(self):
        prices = [100, 101, 102, 103, 104, 105]
        result = simular_estrategia(prices, "momentum", estrategia_momentum_umbral)
        for tick, row in enumerate(result.decisiones):
            self.assertEqual(row["patrimonio"], row["caja"] + row["acciones"] * prices[tick])
            self.assertGreaterEqual(row["caja"], 0)
            self.assertGreaterEqual(row["acciones"], 0)
            if tick:
                self.assertEqual(row["decision_calculo_tick"], tick - 1)
                self.assertEqual(row["decision_recibida"], result.decisiones[tick-1]["decision_siguiente"])


if __name__ == "__main__":
    unittest.main()
