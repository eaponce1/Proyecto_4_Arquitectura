import json,collections,sys
cells=json.load(open(sys.argv[1]))['modules']['demo_autonoma_bus_detail_top']['cells']
def group(n):
 for g in ('u_soc.u_core','u_soc.u_ram','u_soc.u_spi','u_soc.u_sma10','u_soc','u_master','u_monitor','u_pc_probe'):
  if n.startswith(g+'.'): return g
 return 'top/shared'
for g,c in sorted((g,collections.Counter(v['type'] for n,v in cells.items() if group(n)==g)) for g in set(map(group,cells))):
 print(g,dict(c))
