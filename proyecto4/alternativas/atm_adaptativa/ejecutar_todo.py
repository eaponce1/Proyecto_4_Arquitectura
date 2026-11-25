"""Un comando; la puerta financiera no se omite ni programa la placa."""
from pathlib import Path
import argparse,hashlib,json,os,shutil,subprocess,sys
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2];OUT=HERE/'resultados'

def step(name,args,cwd=ROOT):
    p=subprocess.run([str(a) for a in args],cwd=cwd,capture_output=True,text=True,encoding='utf-8',errors='replace')
    (OUT/(name+'.log')).write_text(p.stdout+p.stderr+f'\nSalida={p.returncode}\n',encoding='utf-8')
    print(p.stdout[-2500:],end='',flush=True)
    if p.returncode:raise RuntimeError(name+': '+p.stderr[-1800:])

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--sin-rtl-referencia',action='store_true')
    parser.add_argument('--sin-pdf',action='store_true');args=parser.parse_args();OUT.mkdir(exist_ok=True)
    def py(name):return [sys.executable,'-X','utf8','-B',HERE/(name+'.py')]
    if not args.sin_rtl_referencia:step('auditoria_inicial',py('auditoria_inicial'))
    step('invariantes',py('test_invariantes'))
    step('backtest',py('backtest'))
    step('seleccion_referencia',py('reproducir_seleccion_referencia'))
    step('modelo',py('validar_modelo'))
    decision=json.loads((OUT/'decision.json').read_text())
    if decision['estado']!='NO-GO':raise RuntimeError('GO cuantitativo requiere implementar y validar firmware antes de entregar; no hay aprobacion automatica')
    step('informe',py('generar_informe'))
    if not args.sin_pdf:
        if os.name=='nt':cmd=['wsl','-d','Ubuntu','--cd',str(HERE),'--','bash','compilar_informe.sh']
        else:cmd=['bash','compilar_informe.sh']
        step('pdf',cmd,HERE)
    files=[p for p in HERE.rglob('*') if p.is_file() and p.name!='SHA256_entrega.txt'
        and not any(part in ('build','__pycache__','.matplotlib','informe_build') for part in p.relative_to(HERE).parts)
        and p.name!='decisiones_tick.csv' and p.suffix not in ('.vvp','.pyc')]
    (HERE/'SHA256_entrega.txt').write_text(''.join(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+p.relative_to(HERE).as_posix()+'\n' for p in sorted(files)),encoding='utf-8')
    step('verificacion',py('verificar_entrega'))
    # El log de verificación se crea tras el manifiesto: excluirlo de la firma recursiva.
    manifest=HERE/'SHA256_entrega.txt'
    manifest.write_text(''.join(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+p.relative_to(HERE).as_posix()+'\n' for p in sorted(files) if p.name!='verificacion.log'),encoding='utf-8')
    print('RESULTADO FINAL: NO-GO. Firmware y BIN activos conservados.')

if __name__=='__main__':main()
