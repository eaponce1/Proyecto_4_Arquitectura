"""Auditoría documental y de integridad; no asigna una nota ni certifica la defensa."""
from pathlib import Path
import csv, hashlib, json, re, unicodedata

ROOT=Path(__file__).resolve().parents[1]
AUTHORS=['Cristian Acevedo','Guillermo Arriaza','Eduardo Ponce']

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def norm(s):
    return ' '.join(''.join(c for c in unicodedata.normalize('NFKD',s) if not unicodedata.combining(c)).split()).lower()

def main():
    folder=ROOT/'docs/informe';build=folder/'build'
    text=(build/'informe_extraido.txt').read_text(encoding='utf-8')
    audit=(build/'auditoria_extraida.txt').read_text(encoding='utf-8')
    normalized=norm(text)
    for name in AUTHORS:assert norm(name) in normalized,name
    for term in ['Conclusiones','Amdahl','roofline','CPI máximo','Tiempo medio','VERIFY OK']:
        assert norm(term) in normalized,term
    assert 'no permite acreditar toda la entrega' in norm(audit)
    assert 'tres rondas' in norm(audit) and 'defensa' in norm(audit)
    for name in ['informe_final','auditoria_entrega']:
        log=(build/(name+'.log')).read_text(encoding='utf-8',errors='replace')
        assert 'Overfull' not in log, f'Revisar cajas desbordadas en {name}'
        assert 'undefined references' not in log.lower()
    validation=json.loads((ROOT/'build/trader/validacion.json').read_text())
    for path,h in validation['fuentes'].items():assert sha(ROOT/path)==h,path
    assert sha(ROOT/'competition.bin')==validation['sha256_bin']
    assert sha(ROOT/'sw/trade.hex')==validation['sha256_hex']
    assert validation['politica']=='tendencia_lenta_128_5pct'
    assert validation['prueba_fisica']=='PENDIENTE_NUEVA_IMAGEN'
    with (ROOT/'proyecto4/alternativas/tendencia_lenta/resultados/comparacion_final.csv').open(encoding='utf-8',newline='') as f:
        rows=list(csv.DictReader(f))
    assert len(rows)==8 and sum(int(r['ventaja'])>0 for r in rows)==5
    full=json.loads((ROOT/'build/trader/equivalencia_verilator.json').read_text())
    assert sum(s['ticks'] for s in full['series'])==160000
    assert all(s['discrepancias']==0 for s in full['series'])
    for path,h in full['fuentes'].items():assert sha(ROOT/path)==h,path
    historical=json.loads((ROOT/'docs/evidencia_codisenio/procedencia.json').read_text())
    assert sum(t['ticks'] for t in historical['trazas'])==60000
    for name,item in historical['archivos'].items():assert sha(ROOT/'docs/evidencia_codisenio'/name)==item['sha256']
    times=json.loads((ROOT/'docs/evidencia_informe/metricas_finales.json').read_text())
    assert sum(s['ticks'] for s in times['series'])==160000
    def pages(name):return int(re.search(r'Pages:\s*(\d+)',(build/name).read_text())[1])
    report=dict(fecha='2026-11-25',integrantes=AUTHORS,
        dictamen='CUMPLIMIENTO_DOCUMENTAL_AMPLIO_CON_PENDIENTES; ENTREGA_INTEGRAL_NO_ACREDITADA',
        enunciado=dict(ruta='docs/referencia/enunciado_proyecto4.pdf',sha256=sha(ROOT/'docs/referencia/enunciado_proyecto4.pdf'),paginas_rubrica=[3,4,5]),
        informe=dict(ruta='docs/INFORME_FINAL.pdf',sha256=sha(ROOT/'docs/INFORME_FINAL.pdf'),paginas=pages('pdfinfo.txt')),
        auditoria=dict(ruta='docs/AUDITORIA_ENTREGA.pdf',sha256=sha(ROOT/'docs/AUDITORIA_ENTREGA.pdf'),paginas=pages('auditoria_pdfinfo.txt')),
        comprobaciones=dict(autores_y_secciones=True,sin_desbordes=True,firmas_bin_y_fuentes=True,
            ticks_rtl=160000,ventajas_conocidas='5/8',filas_codisenio_cotejadas=60000,metricas_finales_resumidas=160000),
        prueba_fisica=dict(estado='PENDIENTE_NUEVA_IMAGEN',alcance='El registro previo corresponde a Momentum32 5e1579ca, no a tendencia lenta',
            evidencia='docs/evidencia_fisica/registro_20261125.md',sha256=sha(ROOT/'docs/evidencia_fisica/registro_20261125.md'),
            resultados_tres_rondas='NO_APORTADOS'),
        pendientes=['Programacion y prueba fisica del nuevo BIN de tendencia lenta',
            'Ocho series completas a 1 ms y 10 ms; actualmente integracion de 396 ticks por cadencia larga',
            'Patrimonio/referencia/posicion de las tres rondas oficiales',
            'Acreditacion de defensa y entrega original dentro del plazo',
            'Perfil regional y comparacion de hardware bajo la politica final'])
    (ROOT/'docs/AUDITORIA_ENTREGA.json').write_text(json.dumps(report,indent=2,ensure_ascii=False),encoding='utf-8')
    compilation=dict(pdf_sha256=report['informe']['sha256'],paginas=report['informe']['paginas'],
        auditoria_pdf_sha256=report['auditoria']['sha256'],paginas_auditoria=report['auditoria']['paginas'],
        compilador='pdfLaTeX / pdfTeX 1.40.25, TeX Live 2023',pasadas=3,pasadas_auditoria=2,
        revisado='Autores, conclusiones, metricas, evidencia fisica, roofline y auditoria; sin cajas desbordadas',
        fuentes={p.relative_to(ROOT).as_posix():sha(p) for p in sorted([*folder.glob('*.tex'),*folder.glob('figuras/*.png'),folder/'compilar.sh'])},
        prueba_fisica='PENDIENTE_NUEVA_IMAGEN; EVIDENCIA PREVIA SOLO MOMENTUM32')
    (folder/'compilacion.json').write_text(json.dumps(compilation,indent=2),encoding='utf-8')
    print('PASS integridad y lectura PDF:',report['informe']['paginas'],'paginas; auditoria',report['auditoria']['paginas'],'paginas')
    print('DICTAMEN: faltan resultados oficiales, defensa/plazo y perfil de hardware de la politica final')

if __name__=='__main__':main()
