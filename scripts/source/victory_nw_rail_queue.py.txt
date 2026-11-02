"""Normal-control implementation of the source-reviewed rock-loading puzzle.
Stop on routing/dialogue/save mismatch; never force through a blocked climb.
"""
import json,os,sys,subprocess
from pathlib import Path
R=Path(__file__).resolve().parents[1]
plan=json.loads((R/'work/193-nw-rail-guide-plan.json').read_text())
start=int(sys.argv[1])if len(sys.argv)>1 else 1
prefix=sys.argv[2]if len(sys.argv)>2 else 'NW193-rail'
env=dict(os.environ,REBORN_FAST_KEYS='1',REBORN_COORD_CACHE='1',REBORN_ROUTE_CHUNK='112')
def run(name,*args):subprocess.run([sys.executable,str(R/'scripts'/name),*map(str,args)],check=True,env=env)
def state():return json.loads((R/'notes/navigation-state.json').read_text())
s=state()
if start==1:
 for kind,values in plan['initial'].items():
  for key,value in values.items():assert s[kind][key]==value,(kind,key,s[kind][key],value)
for i,step in enumerate(plan['steps'],1):
 if i<start:continue
 s=state();run('overworld.py')
 if 'load'in step:
  assert s['variables']['499']==1 and not s['switches']['1148']
  run('victory_nw_cliff_event.py',786,97,'talk');run('dialog.py','--yes','--limit=8')
 elif 'lever'in step:
  assert s['switches'][str(step['switch'])]!=step['after']
  run('victory_nw_cliff_event.py',786,step['lever'],'talk');run('play.py','wait:3')
 else:
  var='498'if step['cart']==94 else'499';assert s['variables'][var]==step['before']
  run('victory_nw_cliff_event.py',786,step['cart'],'talk');run('play.py','wait:12')
 run('checkpoint.py',f'{prefix}-{i}');run('party_open.py');s=state()
 if 'load'in step:assert s['switches']['1148']
 elif 'lever'in step:assert s['switches'][str(step['switch'])]==step['after']
 else:
  assert s['variables'][var]==step['after']
  if 'cart_to'in step and 'pillar'not in step:assert s['positions']['786'][str(step['cart'])]==step['cart_to']
  if 'deposit'in step:assert s['switches'][str(step['deposit'])] and not s['switches']['1148']
  if 'pillar'in step:assert s['switches'][str(step['pillar'])]
 print('NW RAIL VERIFIED',i,step,flush=True)
print('NORTHWEST PILLAR COMPLETE',flush=True)
