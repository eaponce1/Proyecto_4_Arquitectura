from pathlib import Path
import sys,subprocess,json,hashlib,zipfile,shutil
root=Path.cwd();out=root/'proyecto4/alternativas/atm_adaptativa/resultados/referencia';out.mkdir(parents=True,exist_ok=True)
paths=[*sorted((root/'rtl').rglob('*.v')),*sorted((root/'sw').glob('*')),*sorted((root/'tb').rglob('*.sv')),
 root/'competition.bin',root/'competition.sha256',root/'goboard_trader.pcf',root/'Makefile',root/'tools/trader.py',
 root/'build/trader/validacion.json',root/'proyecto4/resultados/validacion_oficial/tb_proyecto_4_profesor.sv',
 *sorted((root/'docs/evidencia_fisica').glob('*'))]
paths=[p for p in paths if p.is_file()]
hashes={p.relative_to(root).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
backup=root/'respaldos/atm_referencia_07d0dd95.zip';backup.parent.mkdir(exist_ok=True)
if not backup.exists():
 with zipfile.ZipFile(backup,'w',zipfile.ZIP_DEFLATED) as z:
  for p in paths:z.write(p,p.relative_to(root).as_posix())
manifest=out/'fuentes_activos_antes.json'
if manifest.exists():assert json.loads(manifest.read_text())==hashes,'La referencia activa cambio; no sobrescribir el respaldo'
else:manifest.write_text(json.dumps(hashes,indent=2))
versions={}
for tool,args in [('python',['--version']),('iverilog',['-V']),('vvp',['-V']),('yosys',['-V']),('nextpnr-ice40',['--version'])]:
 path=shutil.which(tool);p=subprocess.run([path,*args],capture_output=True,text=True,encoding='utf-8',errors='replace')
 versions[tool]=dict(path=path,version=(p.stdout+p.stderr).strip(),sha256_ejecutable=hashlib.sha256(Path(path).read_bytes()).hexdigest())
for tool in ['icepack','icebox_vlog']:
 path=shutil.which(tool);versions[tool]=dict(path=path,sha256_ejecutable=hashlib.sha256(Path(path).read_bytes()).hexdigest())
(out/'herramientas.json').write_text(json.dumps(versions,indent=2))
print('PASS rama',subprocess.check_output(['git','branch','--show-current'],text=True).strip(),'HEAD',subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),'activos preservados',len(hashes),flush=True)
sys.path.insert(0,str(root/'tools'));import trader
trader.verify();trader.OUT=out/'icarus';trader.OUT.mkdir(exist_ok=True)
results=trader.test();(out/'pruebas_actuales.json').write_text(json.dumps(results,indent=2))
assert all(hashlib.sha256((root/p).read_bytes()).hexdigest()==h for p,h in hashes.items())
print('PASS pruebas de referencia y activos sin cambios',flush=True)
