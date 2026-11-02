"""Execute the two NW boulder plans, verifying each ordinary push."""
import json,os,sys,subprocess
from pathlib import Path
R=Path(__file__).resolve().parents[1]
start=int(sys.argv[1])if len(sys.argv)>1 else 1
prefix=sys.argv[2]if len(sys.argv)>2 else 'NW193'
steps=sum([json.loads((R/f'work/192-nw-{part}-plan.json').read_text())['pushes']for part in ['upper','lower']],[])
groups={g['start']:g for g in json.loads((R/'work/194-nw-push-groups.json').read_text())}
i=start
while i<=len(steps):
 step=steps[i-1];g=groups.get(i);count=g['count']if g and g['wall_burst'] and g['count']>1 else 1
 s=json.loads((R/'notes/navigation-state.json').read_text());eid=step['event']
 dx,dy={'up':(0,-1),'down':(0,1),'left':(-1,0),'right':(1,0)}[step['direction']]
 assert s['positions']['784'][str(eid)]==[step['box_to'][0]-dx,step['box_to'][1]-dy],('Different current boulder',i)
 label=f'{prefix}-{i+count-1}'
 args=[str(eid),step['direction'],label]+([str(count)]if count>1 else[])
 subprocess.run([sys.executable,str(R/'scripts/hazard_retry.py'),'victory_hazard_boulder_fast.py',*args],check=True,env=dict(os.environ,REBORN_FAST_KEYS='1'))
 s=json.loads((R/'notes/navigation-state.json').read_text());assert s['positions']['784'][str(eid)]==steps[i+count-2]['box_to']
 print('NW MAIN PUSH VERIFIED',i,'through',i+count-1,flush=True)
 i+=count
assert s['switches']['1119'];print('NORTHWEST ACCESS OPEN',flush=True)
