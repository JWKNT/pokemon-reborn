"""Execute the reviewed combined cart/boulder plan through normal controls."""
import json,subprocess,sys,os
from pathlib import Path
R=Path(__file__).resolve().parents[1];plan=json.loads((R/'work/191-south-combined-plan.json').read_text())['actions'];start=int(sys.argv[1]) if len(sys.argv)>1 else 1
for i,step in enumerate(plan,1):
 if i<start:continue
 s=json.loads((R/'notes/navigation-state.json').read_text());label=f'South191-{i}'
 if 'cart' in step:
  assert s['variables']['492']==1-step['after']
  cmd=['victory_hazard_interact.py','132',label]
 else:
  dx,dy={'left':(-1,0),'right':(1,0),'up':(0,-1),'down':(0,1)}[step['direction']]
  assert s['positions']['784']['75']==[step['box_to'][0]-dx,step['box_to'][1]-dy]
  cmd=['victory_hazard_boulder.py','75',step['direction'],label]
 subprocess.run([sys.executable,str(R/'scripts'/cmd[0]),*cmd[1:]],check=True,env=dict(os.environ,REBORN_FAST_KEYS='1'))
 s=json.loads((R/'notes/navigation-state.json').read_text())
 if 'cart' in step:assert s['variables']['492']==step['after']
 else:assert s['positions']['784']['75']==step['box_to']
 print('SOUTH STEP VERIFIED',i,step,flush=True)
assert s['switches']['1121'];print('SOUTH PLATE ACTIVE',flush=True)
