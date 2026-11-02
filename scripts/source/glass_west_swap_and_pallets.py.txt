"""Reviewed normal western companion swap, then three gated pallet motions."""
from play import *
from locate import locate
from glass_positions import refresh
assert locate(732)==(732,18,31)
act('left:.12','wait:.3','c','wait:2')
print(read(),flush=True)
subprocess.run([sys.executable,str(ROOT/'scripts/checkpoint.py'),'Glass-west-companions-ready'],check=True)
v=json.loads((ROOT/'notes/navigation-state.json').read_text())
assert v['switches'].get('947') and not v['switches'].get('946'), 'Normal swap not confirmed'
assert v['variables']['404']<=19, 'Blue not in western corridor'
(ROOT/'notes/navigation-state.json').write_text(json.dumps(refresh(v,json.loads((ROOT/'work/story-map-732-events.json').read_text()))))
for core,direction in [(97,'down'),(147,'right'),(157,'right')]:
 subprocess.run([sys.executable,str(ROOT/'scripts/glass_pallet.py'),str(core),direction],check=True)
print('WEST STAGING AND FIRST UPPER PALLETS COMPLETE',flush=True)
