import unittest

from estrategia_referencia import CANDIDATA, crear_politica, senal_hibrida
from backtest import medir_periodica, preparar
from estrategia import Accion, Decision, MANTENER
from simulador import ejecutar_decision, leer_precios, simular_estrategia


class ReferenciaTests(unittest.TestCase):
    def test_objetivo_y_confirmacion(self):
        self.assertEqual(senal_hibrida(7, 0, 10000, 0, CANDIDATA), MANTENER)
        self.assertEqual(senal_hibrida(8, -1, 10000, 0, CANDIDATA), MANTENER)
        self.assertEqual(senal_hibrida(8, 0, 10000, 0, CANDIDATA), Decision(Accion.COMPRAR, 32))
        self.assertEqual(senal_hibrida(16, 0, 10000, 0, CANDIDATA), Decision(Accion.COMPRAR, 37))
        self.assertEqual(senal_hibrida(16, 0, 20000, 0, CANDIDATA), Decision(Accion.COMPRAR, 63))
        self.assertEqual(senal_hibrida(16, 0, 10000, 32, CANDIDATA), MANTENER)
        self.assertEqual(senal_hibrida(-1, 1, 5000, 32, CANDIDATA), MANTENER)
        self.assertEqual(senal_hibrida(-1, 0, 5000, 32, CANDIDATA), Decision(Accion.VENDER, 32))
        self.assertEqual(senal_hibrida(-8, 1, 5000, 32, CANDIDATA), Decision(Accion.VENDER, 32))

    def test_reserva_en_compra_maxima_y_venta_minima(self):
        for cantidad in range(1, 64):
            caja = 510 + 255*cantidad
            plan = senal_hibrida(16, 0, caja, 0, CANDIDATA)
            self.assertEqual(plan, Decision(Accion.COMPRAR, cantidad))
            fill = ejecutar_decision(caja, 0, plan, 255)
            self.assertEqual((fill.caja, fill.acciones), (505, cantidad))
            venta = ejecutar_decision(fill.caja, fill.acciones, Decision(Accion.VENDER, cantidad), 1)
            self.assertGreaterEqual(venta.caja, 500)
            self.assertEqual(venta.acciones, 0)

    def test_desfase_y_causalidad(self):
        precios = leer_precios()[:2000]
        corta = simular_estrategia(precios[:1000], "Corta", crear_politica())
        larga = simular_estrategia(precios, "Larga", crear_politica())
        self.assertEqual(corta.decisiones, larga.decisiones[:1000])
        self.assertEqual(larga.decisiones[0]["decision_recibida"], 0)
        self.assertEqual(larga.decisiones[385]["decision_recibida"], 0x60)
        self.assertEqual(larga.decisiones[1025]["decision_recibida"], 0xA0)
        for anterior, actual in zip(larga.decisiones, larga.decisiones[1:]):
            self.assertEqual(anterior["decision_siguiente"], actual["decision_recibida"])
            self.assertGreaterEqual(actual["caja"], 500)
            self.assertTrue(0 <= actual["acciones"] <= 63)

    def test_medicion_de_calibracion_coincide_con_simulador(self):
        precios = leer_precios()[:12000]
        r = simular_estrategia(precios, "Desarrollo", crear_politica())
        m = r.metricas
        self.assertEqual(medir_periodica(preparar(precios), CANDIDATA),
                         (m.patrimonio_final, m.perdida_maxima, m.ordenes))


if __name__ == "__main__":
    unittest.main()
