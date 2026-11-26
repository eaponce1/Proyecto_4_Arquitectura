"""Pruebas de bordes financieros, causalidad y ventanas de la politica importada."""
from modelo_lento import Policy,fill,run,synth

def main():
    # Umbral exacto en ambas direcciones, y un punto por debajo de la suma requerida.
    for up,end,expected in [(True,105,True),(True,104,False),(False,95,False),(False,96,True)]:
        p=Policy();p.inside=not up
        for _ in range(129):p.decide(100,10000,0)
        for _ in range(128):p.decide(end,10000,0)
        assert p.inside==expected,(up,end)
    # Cada revision mueve el ancla: aumentos sucesivos menores al 5% no se acumulan.
    p=Policy()
    for price in [100,104,108,112]:
        for _ in range(128):p.decide(price,10000,0)
    assert not p.inside
    _,rows=run(synth()['integracion_cadencias'],trace=True)
    assert all(r['miso']==0 for r in rows[:257])
    assert [(r['tick'],r['miso']) for r in rows if r['miso']]==[(257,0x7f),(258,0x64),(385,0xbf),(386,0xa4)]
    assert rows[-1]['patrimonio']==9980 and rows[-1]['comisiones_acum']==20
    p=Policy();p.inside=True
    assert p.decide(100,705,1)==0 and p.decide(100,805,1)==72
    assert p.decide(100,105,0)==65
    for cash in [0,4,5,6,9999,10000]:
        for shares in [0,1,63,300]:
            for price in [1,5,100,255]:
                for order in range(256):
                    c,a,q,fee=fill(cash,shares,order,price)
                    assert c>=0 and a>=0 and q<=63
                    assert c+a*price==cash+shares*price-fee
                    assert fee==(5 if q else 0)
    for prices in synth().values():
        result,trace=run(prices,trace=True)
        for n in [1,min(128,len(prices)),len(prices)//2]:
            _,other=run(prices[:n]+[255 if prices[n-1]!=255 else 1]*20,trace=True)
            assert other[:n]==trace[:n]
        assert run(prices,trace=True)==(result,trace), 'Estado residual entre rondas'
    print('PASS umbrales, ancla movil, desfase SPI, lotes, contabilidad exhaustiva y causalidad')

if __name__=='__main__':main()
