"""Invariantes de contabilidad, causalidad y regímenes; no evalúa rentabilidad."""
from dataclasses import replace
import json,random,unittest
from pathlib import Path
from estrategia_atm import Config,Policy,population
from simulador_atm import execute,run
from baselines import active

class Invariants(unittest.TestCase):
    def test_independent_accounting_against_active_reference(self):
        for cash in (0,4,5,6,104,10000):
            for shares in (0,1,63,100):
                for p in (1,100,255):
                    for byte in range(256):
                        self.assertEqual(execute(cash,shares,byte,p),active.fill(cash,shares,byte,p))

    def test_future_cannot_change_prefix(self):
        rng=random.Random(1701);prefix=[rng.randrange(100,256) for _ in range(300)]
        for cfg in population():
            _,a=run(prefix+[100]*20,Policy(cfg),True)
            _,b=run(prefix+[255]*20,Policy(cfg),True)
            self.assertEqual(a[:300],b[:300])

    def test_causal_price_and_partial_fill(self):
        class Buy:
            def decide(self,p,cash,shares):return 127
        m,rows=run([100,255],Buy(),True)
        self.assertEqual(rows[0]['miso'],0)
        self.assertEqual(rows[1]['fill'],39)
        self.assertEqual(m['caja'],50)
        self.assertEqual(m['comisiones'],5)

    def test_up_down_and_sideways(self):
        cfg=replace(Config(),review=4,entry=2,confirm=1,min_hold=0)
        m,rows=run([100]*80+[220]*80+[100]*80,Policy(cfg),True)
        self.assertGreater(m['compras'],0);self.assertGreater(m['ventas'],0)
        self.assertEqual({r['regimen'] for r in rows},{'ALCISTA','LATERAL','BAJISTA'})
        self.assertEqual(m['acciones'],0)

    def test_reset_starts_fresh(self):
        p=[100]*80+[220]*80+[100]*80
        self.assertEqual(run(p,Policy(Config()),True),run(p,Policy(Config()),True))

if __name__=='__main__':unittest.main(verbosity=2)
