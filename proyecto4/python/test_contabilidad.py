"""Pruebas matematicas de saldo, comisiones, FIFO, patrimonio y drawdown."""

import unittest

from estrategia import Accion, Decision, MANTENER, estrategia_trading
from metricas import calcular_metricas
from simulador import leer_precios, simular_estrategia


class AuditoriaContableTests(unittest.TestCase):
    def test_drawdown_absoluto_puede_superar_capital_inicial(self):
        # Equity no negativa en ningun punto; cae desde un peak ganado de 10 254.
        m = calcular_metricas([10000, 10254, 102], 102, 0, 0, 0)
        self.assertEqual(m.perdida_maxima, 10152)
        self.assertAlmostEqual(m.drawdown_maximo_pct, 10152 * 100 / 10254)
        self.assertGreater(m.perdida_maxima, 10000)

    def test_drawdown_reportado_se_reproduce_sobre_la_serie_y_no_hay_saldo_negativo(self):
        resultado = simular_estrategia(
            leer_precios(), "SMA original", estrategia_trading
        )
        self.assertEqual(resultado.metricas.perdida_maxima, 10152)
        self.assertEqual(min(resultado.cajas), 0)
        self.assertEqual(min(resultado.posiciones), 0)
        self.assertEqual(min(resultado.patrimonios), 102)
        self.assertEqual(resultado.metricas.comisiones, resultado.metricas.ordenes * 5)

    def test_patrimonio_es_caja_mas_acciones_por_precio_en_cada_tick(self):
        def politica(historial, acciones):
            if len(historial) == 1:
                return Decision(Accion.COMPRAR, 2)
            if len(historial) == 2:
                return Decision(Accion.VENDER, 1)
            return MANTENER

        resultado = simular_estrategia([100, 120, 80], "contabilidad", politica)
        for row in resultado.decisiones:
            self.assertEqual(
                row["patrimonio"], row["caja"] + row["acciones"] * row["precio"]
            )
            self.assertGreaterEqual(row["caja"], 0)
            self.assertGreaterEqual(row["acciones"], 0)
        self.assertEqual(resultado.patrimonios, [10000, 9995, 9910])

    def test_comision_solo_se_cobra_por_orden_ejecutada(self):
        def politica(historial, acciones):
            return Decision(Accion.VENDER, 63) if len(historial) == 1 else MANTENER

        resultado = simular_estrategia([100, 100], "sin fills", politica)
        self.assertEqual(resultado.metricas.ordenes, 0)
        self.assertEqual(resultado.metricas.comisiones, 0)
        self.assertEqual(resultado.compras + resultado.ventas, 0)

    def test_comisiones_ordenes_y_fills_coinciden(self):
        def politica(historial, acciones):
            if len(historial) == 1:
                return Decision(Accion.COMPRAR, 2)
            if len(historial) == 2:
                return Decision(Accion.VENDER, 1)
            return MANTENER

        resultado = simular_estrategia([100, 120, 80], "fees", politica)
        self.assertEqual(resultado.metricas.ordenes, 2)
        self.assertEqual(resultado.metricas.comisiones, 10)
        self.assertEqual(resultado.compras, 1)
        self.assertEqual(resultado.ventas, 1)
        self.assertEqual(resultado.compras + resultado.ventas, resultado.metricas.ordenes)

    def test_fees_de_compra_y_venta_incluidos_en_pnl_fifo(self):
        def politica(historial, acciones):
            if len(historial) == 1:
                return Decision(Accion.COMPRAR, 2)
            if len(historial) == 2:
                return Decision(Accion.VENDER, 1)
            return MANTENER

        resultado = simular_estrategia([100, 120, 80], "fifo", politica)
        # Compra de 2 a 120 cuesta 245 (incluye 5 de comision). Una unidad
        # vendida tiene base FIFO 122.50; venta neta 75: perdida 47.50.
        self.assertEqual(resultado.ganancia_perdida_cierres, [-47.5])
        self.assertEqual(resultado.operaciones[-1]["ganancia_perdida_realizada"], -47.5)

    def test_decision_calculada_en_tick_previo_se_ejecuta_al_precio_actual(self):
        def politica(historial, acciones):
            return Decision(Accion.COMPRAR, 1) if len(historial) == 1 else MANTENER

        resultado = simular_estrategia([100, 200], "desfase", politica)
        compra = resultado.operaciones[0]
        self.assertEqual(compra["tick_calculo_decision"], 0)
        self.assertEqual(compra["precio_al_calcular"], 100)
        self.assertEqual(compra["tick_ejecucion"], 1)
        self.assertEqual(compra["precio_ejecucion"], 200)


if __name__ == "__main__":
    unittest.main()
