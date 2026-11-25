"""Casos frontera financieros y causalidad observacional."""
import unittest
from estrategia import *

class Invariantes(unittest.TestCase):
    def test_fills_frontera(self):
        self.assertEqual(fill(10000,0,0x7f,255),(50,39,39,5))
        self.assertEqual(fill(4,0,0x7f,100),(4,0,0,0))
        self.assertEqual(fill(0,1,0xbf,100),(95,0,1,5))
        self.assertEqual(fill(0,1,0xbf,1),(0,1,0,0))
        self.assertEqual(fill(100,0,0xff,100),(100,0,0,0))
        self.assertEqual(fill(100,0,0x40,100),(100,0,0,0))

    def test_dominio_entero(self):
        for cash in (0,4,5,99,100,104,105,9995,10000,100000):
            for shares in (0,1,63,64,166,255):
                for price in range(100,256):
                    for order in (0,0x41,0x7f,0x81,0xbf,0xff):
                        c,s,q,f=fill(cash,shares,order,price)
                        self.assertGreaterEqual(c,0);self.assertGreaterEqual(s,0)
                        self.assertLessEqual(q,63)
                        self.assertIn(f,(0,5))
                        self.assertEqual(c+s*price,cash+shares*price-f)

    def test_causalidad_y_reinicio(self):
        p=load(HERE/'datos/practica_meta_2022.csv')[:1024]
        _,a=run(p+[100]*128,frozen(),True)
        _,b=run(p+[255]*128,frozen(),True)
        self.assertEqual(a[:1024],b[:1024])
        self.assertEqual(run(p,frozen(),True),run(p,frozen(),True))
        # The decision generated after final tick is never booked as a fill.
        m,r=run([100],frozen(),True)
        self.assertEqual((m['ordenes'],m['comisiones'],r[0]['miso'],r[0]['decision']),(0,0,0,0x7f))

if __name__=='__main__':unittest.main(verbosity=2)
