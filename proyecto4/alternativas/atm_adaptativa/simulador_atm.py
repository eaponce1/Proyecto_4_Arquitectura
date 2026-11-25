"""Carga explícita para no confundir el simulador ATM con el histórico al usar spawn."""
from pathlib import Path
import importlib.util,sys
spec=importlib.util.spec_from_file_location('atm_broker_independiente',Path(__file__).with_name('simulador.py'))
module=importlib.util.module_from_spec(spec);sys.modules[spec.name]=module;spec.loader.exec_module(module)
run,rank,write,execute,benchmark=module.run,module.rank,module.write,module.execute,module.benchmark
