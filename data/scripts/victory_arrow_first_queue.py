"""Normal, guarded six-action corridor opening; starts in Party with Strength active."""
import os,sys,json,subprocess
from pathlib import Path
R=Path(__file__).resolve().parents[1];start=int(sys.argv[1])if len(sys.argv)>1 else 1
plan=json.loads((R/'work/196-arrow-first-boulders-plan.json').read_text())['pushes']
def run(*args):subprocess.run([sys.executable,str(R/'scripts'/args[0]),*map(str,args[1:])],check=True,env=dict(os.environ,REBORN_FAST_KEYS='1'))
for i,p in enumerate(plan,1):
 if i<start:continue
 e=p['event'];label=f'Arrow197-first-{i}'
 if p.get('kind')=='smash':run('victory_arrow_smash_fast.py',e,label)
 else:
  n=json.loads((R/'notes/navigation-state.json').read_text());dx,dy={'up':(0,-1),'down':(0,1),'left':(-1,0),'right':(1,0)}[p['direction']]
  assert n['positions']['787'][str(e)]==[p['box_to'][0]-dx,p['box_to'][1]-dy]
  run('arrow_retry.py','victory_arrow_boulder_fast.py',e,p['direction'],label)
  assert json.loads((R/'notes/navigation-state.json').read_text())['positions']['787'][str(e)]==p['box_to']
 print('ARROW ACTION VERIFIED',i,p,flush=True)
