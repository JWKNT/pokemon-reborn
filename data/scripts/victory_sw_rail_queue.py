"""Execute the source-planned SW rail puzzle using normal controls and saves."""
import os,sys,json,subprocess
from pathlib import Path
R=Path(__file__).resolve().parents[1];env=dict(os.environ,REBORN_FAST_KEYS='1',REBORN_COORD_CACHE='1',REBORN_ROUTE_CHUNK='112');plan=json.loads((R/'work/191-sw-cart-solution.json').read_text());start=int(sys.argv[1])if len(sys.argv)>1 else 1
switches={str(e):str(1136+i)for i,e in enumerate([70,72,74,76,79,80,82])}
def run(name,*args):subprocess.run([sys.executable,str(R/'scripts'/name),*map(str,args)],check=True,env=env)
s=json.loads((R/'notes/navigation-state.json').read_text())
if start==1:assert sum((1<<i)for i in range(7)if s['switches'][str(1136+i)])==plan['initial_mask'] and s['variables']['497']==0
for i,step in enumerate(plan['actions'],1):
 if i<start:continue
 s=json.loads((R/'notes/navigation-state.json').read_text());run('play.py','x','wait:.8','x','wait:.2')
 if 'lever' in step:
  eid=str(step['lever']);assert s['switches'][switches[eid]]!=step['after'];run('eventq.py',786,eid,'talk');run('play.py','wait:4')
 else:
  assert s['variables']['497']==step['before'];run('eventq.py',786,88,'talk');run('play.py','wait:12')
 run('checkpoint.py',f'SW192-rail-{i}');run('party_open.py');s=json.loads((R/'notes/navigation-state.json').read_text())
 if 'lever' in step:assert s['switches'][switches[eid]]==step['after']
 else:assert s['variables']['497']==step['after'] and s['positions']['786']['88']==step['cart_to']
 print('SW RAIL ACTION VERIFIED',i,step,flush=True)
assert s['switches']['1133'];print('SOUTHWEST PILLAR COMPLETE',flush=True)
