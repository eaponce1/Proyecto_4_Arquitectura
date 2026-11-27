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
    for term in ['Conclusiones','Amdahl','roofline','CPI máximo','Tiempo medio','VERIFY OK','Repetición directa del ZIP de práctica']:
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
    assert validation['prueba_fisica']=='REPROGRAMACION_REPORTADA_POR_USUARIO'
    physical_path=ROOT/'docs/evidencia_fisica/reprogramacion_tendencia_lenta.json'
    physical=json.loads(physical_path.read_text(encoding='utf-8'))
    assert physical['sha256_bin_local']==validation['sha256_bin']
    campaign=json.loads((ROOT/'resultados_simulacion/testbench_todas_acciones/resumen.json').read_text(encoding='utf-8'))
    assert len(campaign['resultados'])==78 and sum(r['ticks'] for r in campaign['resultados'])==1557620
    assert all(r['estado']=='PASS' and r['discrepancias']==0 for r in campaign['resultados'])
    assert campaign['sha256_bin']==validation['sha256_bin']
    direct=json.loads((ROOT/'resultados_simulacion/testbench_zip_practica/resumen.json').read_text(encoding='utf-8'))
    assert direct['sha256_bin']==validation['sha256_bin'] and direct['ticks']==160000 and len(direct['resultados'])==8
    assert all(r['estado']=='PASS' for r in direct['resultados']) and direct['zip_sha256'] in normalized.replace(' ','')
    assert '1 557 620' in normalized or '1557620' in normalized.replace(' ','')
    with (ROOT/'proyecto4/alternativas/tendencia_lenta/resultados/comparacion_final.csv').open(encoding='utf-8',newline='') as f:
        rows=list(csv.DictReader(f))
    assert len(rows)==8 and sum(int(r['ventaja'])>0 for r in rows)==5
    full=json.loads((ROOT/'build/trader/equivalencia_verilator.json').read_text())
    assert sum(s['ticks'] for s in full['series'])==160000
    assert all(s['discrepancias']==0 for s in full['series'])
    for path,h in full['fuentes'].items():assert sha(ROOT/path)==h,path
    final=json.loads((ROOT/'docs/evidencia_codisenio_final/auditoria.json').read_text())
    assert final['estado']=='PASS' and final['ticks']==640000
    flash=json.loads((ROOT/'docs/evidencia_fisica/verificacion_flash_lenta_20261127T004337Z.json').read_text())
    assert flash['resultado']=='VERIFY OK' and flash['sha256_bin_referencia']==validation['sha256_bin']
    assert norm('Co-diseño con la política final de tendencia lenta') in normalized
    assert '640 000' in normalized or '640000' in normalized.replace(' ','')
    historical=json.loads((ROOT/'docs/evidencia_codisenio/procedencia.json').read_text())
    assert sum(t['ticks'] for t in historical['trazas'])==60000
    for name,item in historical['archivos'].items():assert sha(ROOT/'docs/evidencia_codisenio'/name)==item['sha256']
    times=json.loads((ROOT/'docs/evidencia_informe/metricas_finales.json').read_text())
    assert sum(s['ticks'] for s in times['series'])==160000
    def pages(name):return int(re.search(r'Pages:\s*(\d+)',(build/name).read_text())[1])
    report=dict(fecha='2026-11-27',integrantes=AUTHORS,
        dictamen='TRES_APARTADOS_TECNICOS_DOCUMENTADOS_Y_VERIFICADOS; ENTREGA_INTEGRAL_NO_ACREDITADA',
        enunciado=dict(ruta='docs/referencia/enunciado_proyecto4.pdf',sha256=sha(ROOT/'docs/referencia/enunciado_proyecto4.pdf'),paginas_rubrica=[3,4,5]),
        informe=dict(ruta='docs/INFORME_FINAL.pdf',sha256=sha(ROOT/'docs/INFORME_FINAL.pdf'),paginas=pages('pdfinfo.txt')),
        auditoria=dict(ruta='docs/AUDITORIA_ENTREGA.pdf',sha256=sha(ROOT/'docs/AUDITORIA_ENTREGA.pdf'),paginas=pages('auditoria_pdfinfo.txt')),
        comprobaciones=dict(autores_y_secciones=True,sin_desbordes=True,firmas_bin_y_fuentes=True,
            ticks_rtl=1557620,escenarios=78,repeticion_zip=dict(ticks=160000,series=8,compras=98,ventas=92,zip_sha256=direct['zip_sha256'],datos_nuevos=False),ventajas_conocidas='5/8',ventajas_adicionales=['16/35 proporcional','18/35 afin'],filas_codisenio_final=640000,variantes_finales=4,filas_codisenio_historico=60000,metricas_finales_resumidas=160000),
        prueba_fisica=dict(estado='FLASH_VERIFY_OK; SPI_MAESTRA_PENDIENTE_SOLO_D1',alcance=flash['alcance'],comparacion_flash='docs/evidencia_fisica/verificacion_flash_lenta_20261127T004337Z.json',incidente='docs/evidencia_fisica/incidente_maestra_solo_d1.json',
            evidencia=physical_path.relative_to(ROOT).as_posix(),sha256=sha(physical_path),
            resultados_tres_rondas='NO_APORTADOS'),
        pendientes=['Traza fisica de la maestra asociada a la reprogramacion reportada',
            'Ocho series completas a 1 ms y 10 ms si se exige esa extension; actualmente integracion de 396 ticks por cadencia larga',
            'Patrimonio/referencia/posicion de las tres rondas oficiales',
            'Acreditacion de defensa y entrega original dentro del plazo',
            'Recepcion SPI fisica de la maestra: usuario reporto solo D1'])
    (ROOT/'docs/AUDITORIA_ENTREGA.json').write_text(json.dumps(report,indent=2,ensure_ascii=False),encoding='utf-8')
    compilation=dict(pdf_sha256=report['informe']['sha256'],paginas=report['informe']['paginas'],
        auditoria_pdf_sha256=report['auditoria']['sha256'],paginas_auditoria=report['auditoria']['paginas'],
        compilador='pdfLaTeX / pdfTeX 1.40.25, TeX Live 2023',pasadas=3,pasadas_auditoria=2,
        revisado='Autores, conclusiones, metricas, evidencia fisica, roofline y auditoria; sin cajas desbordadas',
        fuentes={p.relative_to(ROOT).as_posix():sha(p) for p in sorted([*folder.glob('*.tex'),*folder.glob('figuras/*.png'),folder/'compilar.sh'])},
        prueba_fisica='FLASH_VERIFY_OK; SPI_MAESTRA_PENDIENTE; RESULTADOS FINANCIEROS DE CAMPANA RTL')
    (ROOT/'docs/INFORME_FINAL.sha256').write_text(report['informe']['sha256']+'  INFORME_FINAL.pdf\n',encoding='ascii')
    (folder/'compilacion.json').write_text(json.dumps(compilation,indent=2),encoding='utf-8')
    print('PASS integridad y lectura PDF:',report['informe']['paginas'],'paginas; auditoria',report['auditoria']['paginas'],'paginas')
    print('DICTAMEN: tres apartados tecnicos documentados; faltan SPI fisico, resultados oficiales y defensa/plazo')

if __name__=='__main__':main()
