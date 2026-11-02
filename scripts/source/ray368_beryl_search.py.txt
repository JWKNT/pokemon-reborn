"""Beryl PC loop; catch eligibility extends into adjacent connected map544.

Unlike Opal, Ray can enter544 while player history is525/159. All positions
below are visible marker pixels or normal coordinates, never hidden roamer data.
"""
from play import *
from ray368_marker import marker
from locate import locate
for i in range(24):
 assert 'Reborn Region' in read(),'Map expected'
 # Move the visible selection box off Beryl; it otherwise covers Ray's head.
 act('right','wait:.2','right','wait:.3');read()
 m=marker();print('PUBLIC MARKER',m,flush=True)
 if tuple(m['grid']) == (1,8):
  print('CONNECTED BERYL MARKER: stop for grass route',flush=True);break
 if (ROOT/'work/stop-ray-search').exists():
  (ROOT/'work/stop-ray-search').unlink();print('STOP ON MAP',flush=True);break
 for _ in range(5):
  act('x','wait:1.2');t=read()
  if not any(s in t for s in ['Reborn Region','Field Notes','Quit Game']):break
 else:raise SystemExit('Map close review')
 p=locate();assert p==(525,21,23),p
 act('up:.12','wait:2');assert locate()==(159,10,10)
 act('down:.12','wait:2');assert locate()==(525,21,23)
 act('wait:.8','x','wait:1.2','c','wait:1.2')
 assert 'Field Notes' in read()
 act('down','wait:.15','down','wait:.15','down','wait:.15','c','wait:1')
else:print('Bounded search finished; map remains open',flush=True)
