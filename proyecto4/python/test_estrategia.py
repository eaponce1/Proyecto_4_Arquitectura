"""Pruebas unitarias de reglas, causalidad y desfase de una transaccion SPI."""

import unittest

from estrategia import (
    Accion, Decision, MANTENER, estrategia_trading, estrategia_sma_umbral,
    estrategia_tendencia_confirmada, estrategia_sma_umbral_cooldown,
)
from functools import partial
from simulador import ejecutar_decision, leer_precios, simular_estrategia


class ReglasDeEjecucionTests(unittest.TestCase):
    def test_compra(self):
        r = ejecutar_decision(1000, 0, Decision(Accion.COMPRAR, 2), 100)
        self.assertEqual((r.caja, r.acciones, r.cantidad_ejecutada), (795, 2, 2))

    def test_venta(self):
        r = ejecutar_decision(100, 3, Decision(Accion.VENDER, 2), 50)
        self.assertEqual((r.caja, r.acciones, r.cantidad_ejecutada), (195, 1, 2))

    def test_venta_se_limita_a_acciones_disponibles(self):
        r = ejecutar_decision(100, 2, Decision(Accion.VENDER, 63), 10)
        self.assertEqual((r.caja, r.acciones, r.cantidad_ejecutada), (115, 0, 2))

    def test_mantener(self):
        r = ejecutar_decision(500, 4, MANTENER, 100)
        self.assertEqual((r.caja, r.acciones, r.cantidad_ejecutada, r.comision), (500, 4, 0, 0))

    def test_caja_insuficiente_no_genera_deuda(self):
        r = ejecutar_decision(14, 0, Decision(Accion.COMPRAR, 1), 10)
        self.assertEqual((r.caja, r.acciones, r.cantidad_ejecutada, r.comision), (14, 0, 0, 0))

    def test_compra_se_reduce_a_maximo_asequible(self):
        r = ejecutar_decision(105, 0, Decision(Accion.COMPRAR, 63), 10)
        self.assertEqual((r.caja, r.acciones, r.cantidad_ejecutada), (0, 10, 10))

    def test_venta_sin_acciones_no_se_ejecuta(self):
        r = ejecutar_decision(100, 0, Decision(Accion.VENDER, 63), 10)
        self.assertEqual((r.caja, r.acciones, r.cantidad_ejecutada, r.comision), (100, 0, 0, 0))

    def test_cantidad_maxima_63(self):
        r = ejecutar_decision(10000, 0, Decision(Accion.COMPRAR, 63), 100)
        self.assertEqual((r.caja, r.acciones, r.cantidad_ejecutada), (3695, 63, 63))
        with self.assertRaises(ValueError):
            Decision(Accion.COMPRAR, 64)

    def test_comision_fija_por_orden_ejecutada(self):
        r = ejecutar_decision(1000, 0, Decision(Accion.COMPRAR, 1), 100)
        self.assertEqual(r.comision, 5)
        r2 = ejecutar_decision(r.caja, r.acciones, Decision(Accion.VENDER, 1), 100)
        self.assertEqual(r2.comision, 5)
        self.assertEqual(r2.caja, 990)


class CausalidadTests(unittest.TestCase):
    def test_desfase_spi_ejecuta_al_tick_siguiente(self):
        precios = [100, 200]

        def comprar_despues_del_precio(historial, acciones):
            return Decision(Accion.COMPRAR, 1) if len(historial) == 1 else MANTENER

        r = simular_estrategia(precios, "lag", comprar_despues_del_precio)
        self.assertEqual(r.decisiones[0]["decision_recibida"], MANTENER.byte)
        self.assertEqual(r.decisiones[0]["decision_siguiente"], Decision(Accion.COMPRAR, 1).byte)
        self.assertEqual(r.decisiones[0]["cantidad_ejecutada"], 0)
        self.assertEqual(r.decisiones[1]["cantidad_ejecutada"], 1)
        self.assertEqual(r.decisiones[1]["precio"], 200)

    def test_no_consulta_informacion_futura(self):
        base = [100, 101, 102, 103, 104, 105, 106, 107, 108, 109]
        con_futuro_alto = base + [255] * 20
        con_futuro_bajo = base + [1] * 20
        politicas = [
            estrategia_trading,
            partial(estrategia_sma_umbral, umbral=2),
            partial(estrategia_tendencia_confirmada),
            partial(estrategia_sma_umbral_cooldown, umbral=2, cooldown=5),
        ]
        for indice, politica in enumerate(politicas):
            a = simular_estrategia(con_futuro_alto, f"a{indice}", politica)
            b = simular_estrategia(con_futuro_bajo, f"b{indice}", politica)
            for tick in range(len(base)):
                self.assertEqual(
                    a.decisiones[tick]["decision_siguiente"],
                    b.decisiones[tick]["decision_siguiente"],
                    f"la variante {indice} consulto un tick futuro {tick}",
                )

    def test_lectura_de_serie_completa(self):
        precios = leer_precios()
        self.assertEqual(len(precios), 20000)
        self.assertEqual((min(precios), max(precios)), (100, 255))

    def test_senal_compra_y_venta_de_sma_momentum(self):
        subida = list(range(100, 110))
        bajada = list(range(110, 100, -1))
        self.assertEqual(estrategia_trading(subida, 0).accion, Accion.COMPRAR)
        self.assertEqual(estrategia_trading(bajada, 2).accion, Accion.VENDER)
        self.assertEqual(estrategia_trading(bajada, 0), MANTENER)

    def test_variante_a_exige_umbral_de_momentum(self):
        subida = list(range(100, 110))  # momentum de tres ticks = 3
        self.assertEqual(estrategia_sma_umbral(subida, 0, umbral=2).accion, Accion.COMPRAR)
        self.assertEqual(estrategia_sma_umbral(subida, 0, umbral=4), MANTENER)

    def test_variante_b_confirma_dos_tendencias_y_evitar_reentrar(self):
        subida = list(range(100, 111))
        compra = estrategia_tendencia_confirmada(subida, 0, cantidad=4)
        self.assertEqual(compra, Decision(Accion.COMPRAR, 4))
        self.assertEqual(estrategia_tendencia_confirmada(subida, 4, cantidad=4), MANTENER)

    def test_variante_c_cooldown_se_cuenta_desde_fill(self):
        subida = list(range(100, 110))
        self.assertEqual(
            estrategia_sma_umbral_cooldown(subida, 0, tick=12, ultimo_tick_operacion=9),
            MANTENER,
        )
        self.assertEqual(
            estrategia_sma_umbral_cooldown(subida, 0, tick=14, ultimo_tick_operacion=9).accion,
            Accion.COMPRAR,
        )


if __name__ == "__main__":
    unittest.main()
