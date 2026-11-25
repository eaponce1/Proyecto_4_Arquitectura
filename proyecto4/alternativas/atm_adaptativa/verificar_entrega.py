"""Verifica evidencia, puerta NO-GO y preservación de la imagen física anterior."""
from pathlib import Path
import csv,gzip,hashlib,json
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2];OUT=HERE/'resultados'

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    saved=json.loads((OUT/'referencia/fuentes_activos_antes.json').read_text())
    for path,value in saved.items():assert sha(ROOT/path)==value,path
    decision=json.loads((OUT/'decision.json').read_text())
    assert decision['estado']=='NO-GO' and not all(decision['puertas'].values())
    early=json.loads((HERE/'congelacion_antes_de_test.json').read_text())
    assert early['indice']==decision['seleccion'] and early['config']==decision['config']
    assert early['sha256_protocolo']==sha(HERE/'PROTOCOLO.json')==decision['protocolo_sha256']
    for p in (HERE/'trade.s',HERE/'trade.hex',HERE/'competition.bin',HERE/'build/competition.bin'):
        assert not p.exists(),'No publicar firmware ATM tras NO-GO: '+str(p)
    with gzip.open(OUT/'decisiones_tick.csv.gz','rt',encoding='utf-8',newline='') as stream:
        rows=list(csv.DictReader(stream))
    assert len(rows)==160000
    assert sum(int(r['comision']) for r in rows)==3295
    with (OUT/'combinaciones_tres_rondas.csv').open(newline='') as stream:combo=list(csv.DictReader(stream))
    assert sum(r['tipo']=='distintas' for r in combo)==56*7
    assert sum(r['tipo']=='con_repeticion' for r in combo)==120*7
    with (OUT/'grilla_completa.csv').open(newline='') as stream:grid=list(csv.DictReader(stream))
    assert len(grid)==191*8*4 and {int(r['config']) for r in grid}==set(range(191))
    report=json.loads((OUT/'validacion_modelo.json').read_text())
    assert report['ticks']==160000 and report['discrepancias']==0
    for line in (HERE/'SHA256_entrega.txt').read_text().splitlines():
        digest,path=line.split('  ',1);assert sha(HERE/path)==digest,path
    print('PASS evidencia y activos preservados; ATM permanece NO-GO; no hay BIN nuevo')

if __name__=='__main__':main()
