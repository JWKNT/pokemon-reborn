"""Reviewed first-room Malamar path, using normal controls and public coordinates."""
import os
os.environ.update(REBORN_FAST_KEYS='1',REBORN_COORD_CACHE='1',REBORN_ROUTE_STEP_PAUSE='.10',REBORN_ROUTE_CHUNK='56')
from play import *
from locate import locate
steps=json.loads((ROOT/'work/360-room1-plan.json').read_text())[1:]
for s in steps:
 print('PUZZLE STEP',s,flush=True)
 subprocess.run([sys.executable,str(ROOT/'scripts/q.py'),','.join(map(str,[s['map'],*s['position']]))],check=True)
 if s['event']==7:
  subprocess.run([sys.executable,str(ROOT/'scripts/eventq.py'),str(s['map']),'7','enter'],check=True)
  break
 act(s['facing'],'c','wait:.6');t=read();print(t,flush=True)
 assert 'malamar' in t.lower(),'Expected Malamar text'
 act('c','wait:1.5');t=read();print(t,flush=True)
 if 'room inverted' in t.lower():act('c','wait:.5')
 elif len(t.splitlines())>2:raise SystemExit('Unexpected inversion dialogue')
 actual=locate();assert actual==(1781-s['map'],*s['position']),(actual,s)
 print('INVERSION VERIFIED',actual,flush=True)
