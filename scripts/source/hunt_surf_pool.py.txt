"""Hunt reviewed153 pool using short reversible sweeps; stop at wanted wild or unknown UI."""
from play import *
from locate import locate
import difflib
assert locate(153)in[(153,18,44),(153,19,44),(153,20,44)]
subprocess.run([sys.executable,str(ROOT/'scripts/surface_walk.py'),'153','19','44'],check=True);targets=['lombre','ludicolo']
for i in range(100):
 t=read();low=t.lower();print('POOL',i,t.replace('\n',' | '),flush=True)
 if any(n in low for n in targets):print('TARGET FOUND',flush=True);break
 if 'repel' in low:
  subprocess.run([sys.executable,str(ROOT/'scripts/renew_repel.py'),'--cancel'],check=True);continue
 if any(s in low for s in ['fight','hp','wild','safely','escape']):
  subprocess.run([sys.executable,str(ROOT/'scripts/flee.py')],check=True);continue
 if len(t.splitlines())>3:raise SystemExit('Unknown pool dialogue')
 act(*(['right:.12','left:.12']*8))
else:raise SystemExit('Hunt iteration limit')
