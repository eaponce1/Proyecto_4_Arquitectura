"""Comprueba artefactos finales y evidencias completas sin volver a sintetizar."""
from estrategia import *
from validar_rtl import signature
import hashlib
import zipfile
import subprocess

def main():
    out=HERE/'resultados';build=HERE/'build'
    sig=signature()
    meta=json.loads((build/'resultados.json').read_text())
    assert hashlib.sha256((build/'competition.bin').read_bytes()).hexdigest()==meta['sha256_bin']
    assert hashlib.sha256((HERE/'trade.hex').read_bytes()).hexdigest()==meta['sha256_hex']
    for line in (HERE/'SHA256_entrega.txt').read_text().splitlines():
        h,name=line.split('  ',1)
        name=name.replace(chr(92),'/')
        assert hashlib.sha256((HERE/name).read_bytes()).hexdigest()==h,name
    assert list(build.rglob('*.bin'))==[build/'competition.bin']
    interp=json.loads((out/'equivalencia_rv32e.json').read_text())
    full=json.loads((out/'equivalencia_verilator.json').read_text())
    stress=json.loads((out/'equivalencia_rtl.json').read_text())
    banks=json.loads((out/'bancos_oficiales.json').read_text())
    assert interp['hex_sha256']==full['sha256_hex']==meta['sha256_hex']
    assert interp['asm_sha256']==hashlib.sha256((HERE/'trade.s').read_bytes()).hexdigest()
    assert full['fuentes']==sig and all(r['fuentes']==sig for r in stress+banks)
    assert len(full['series'])==8 and sum(r['ticks'] for r in full['series'])==160000
    assert sum(r['ticks'] for r in interp['series'] if r['ticks']==20000)==160000
    for row in full['series']:
        log=(HERE/row['log'].replace(chr(92),'/')).read_text()
        assert 'PASS 20000 MISO frente a Python' in log and 'Salida=0' in log
        with (build/'verilator'/f"{row['serie']}.csv").open(newline='') as f:
            assert sum(1 for _ in csv.DictReader(f))==20000
    assert len(stress)==10
    for r in stress:
        assert r['discrepancias']==0 and r['margen_ciclos']>0
        log=(HERE/r['log'].replace(chr(92),'/')).read_text()
        assert f"PASS {r['ticks']} MISO frente a Python" in log and 'Salida=0' in log
    assert {r['periodo_ns'] for r in stress}>={100000,1000000,10000000}
    assert len(banks)==2 and all(r['tests']=='4/4' for r in banks)
    assert meta['lc']<=1280 and meta['bram']<=16
    assert all(c['achieved']>=c['constraint'] for c in meta['clocks'].values())
    assert len(meta['netlist'])==2
    for r in meta['netlist']:
        assert r['ticks']==48 and r['discrepancias']==0
        log=(HERE/r['log'].replace(chr(92),'/')).read_text();assert 'PASS 48 MISO frente a Python' in log and 'Salida=0' in log
    assert (build/'competition.bin').stat().st_size==32220
    assert 'OK' in (out/'invariantes.log').read_text() and 'Salida=0' in (out/'invariantes.log').read_text()
    prior=[];archived=0;from_git=0
    archive_dir=HERE.parents[2].parent/'ARCHIVO_HISTORICO'
    archive=None
    try:
        for line in (out/'SHA256_previos.txt').read_text().splitlines():
            h,name=line.split('  ',1)
            name=name.replace(chr(92),'/')
            original=HERE.parents[2]/name
            if original.exists():
                assert hashlib.sha256(original.read_bytes()).hexdigest()==h,name
            else:
                if archive is None and (archive_dir/'verificacion_respaldo.json').exists():
                    archive_meta=json.loads((archive_dir/'verificacion_respaldo.json').read_text())
                    path=archive_dir/archive_meta['archivo']
                    assert hashlib.sha256(path.read_bytes()).hexdigest()==archive_meta['sha256_zip']
                    archive=zipfile.ZipFile(path)
                if archive is not None:
                    entry=HERE.parents[2].name+'/'+Path(name).as_posix()
                    data=archive.read(entry);archived+=1
                else:
                    root=HERE.parents[2]
                    ref='66eede4c46e211c02dc5ef22de18f86e22e775c5'
                    result=subprocess.run(['git','-c','safe.directory='+root.as_posix(),'-C',str(root),
                        'show',ref+':'+Path(name).as_posix()],capture_output=True)
                    assert result.returncode==0,'La auditoria historica requiere clon Git completo o ARCHIVO_HISTORICO: '+name
                    data=result.stdout;from_git+=1
                assert hashlib.sha256(data).hexdigest()==h,name
            prior.append(name)
    finally:
        if archive is not None:archive.close()
    evidence=dict(estado='PASS_DIGITAL',bin_sha256=meta['sha256_bin'],hex_sha256=meta['sha256_hex'],
       bin_bytes=32220,series_completas=8,ticks_rv32e=160000,ticks_rtl_verilator=160000,
       ticks_icarus_estres=sum(r['ticks'] for r in stress),ticks_icarus_bancos=4000,
       ticks_netlist=96,artefactos_historicos_preservados=len(prior),historicos_en_zip=archived,historicos_en_git=from_git,
       prueba_fisica='PENDIENTE',superioridad_financiera_independiente='NO_DEMOSTRADA')
    (out/'auditoria_entrega.json').write_text(json.dumps(evidence,indent=2))
    print(json.dumps(evidence,indent=2))

if __name__=='__main__':main()
