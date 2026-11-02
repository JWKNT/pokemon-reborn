"""Retired experiment: two-area history prevents Rayquaza entering Opal.

Preserved for the recorded attempt history. Use ray368_beryl_search.py instead,
whose target544 is connected to player525 but never enters player area history.
"""
raise SystemExit('Retired: Hall/Opal loop excludes its own target from roaming choices')
from play import *
from ray368_marker import marker
from locate import locate
def run(name,*args):subprocess.run([sys.executable,str(ROOT/'scripts'/name),*map(str,args)],check=True)
for i in range(24):
 assert 'Reborn Region' in read(),'Map expected'
 m=marker();print('PUBLIC MARKER',m,flush=True)
 # Opal Ward itself: restored city wards use transfers, not connected maps.
 if tuple(m['grid']) == (7,14):
  print('OPAL MARKER: stop for grass route',flush=True);break
 for _ in range(5):
  act('x','wait:1.2')
  t=read()
  if not any(s in t for s in ['Reborn Region','Field Notes','Quit Game']):break
 else:raise SystemExit('Map close review')
 p=locate();assert p in [(519,34,46),(519,35,46)],p
 act('up:.12','wait:2')
 assert locate()==(38,15,28)
 act('down:.12','wait:2')
 p=locate();assert p in [(519,34,46),(519,35,46)],p
 act('x','wait:.4','c','wait:.8')
 assert 'Field Notes' in read() and 'Region Map' in read()
 act('down','wait:.15','down','wait:.15','down','wait:.15','c','wait:1')
else:print('Bounded search finished; map remains open',flush=True)
