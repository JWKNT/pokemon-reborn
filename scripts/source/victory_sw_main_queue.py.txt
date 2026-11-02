"""SW pressure-plate plan; wall-bounded runs and exact normal-save guards."""
import json,subprocess,sys,os
from pathlib import Path
R=Path(__file__).resolve().parents[1];plan=json.loads((R/'work/191-sw-main-plan.json').read_text())['pushes'];i=int(sys.argv[1])if len(sys.argv)>1 else 1
prefix=sys.argv[2]if len(sys.argv)>2 else 'SW192';groups=json.loads((R/'work/192-sw-push-groups.json').read_text())
while i<=len(plan):
 step=plan[i-1];s=json.loads((R/'notes/navigation-state.json').read_text());dx,dy={'left':(-1,0),'right':(1,0),'up':(0,-1),'down':(0,1)}[step['direction']]
 assert s['positions']['784']['73']==[step['box_to'][0]-dx,step['box_to'][1]-dy]
 group=next(g for g in groups if g['start']<=i<=g['end']);last=group['end']if group['wall_stop']else i;count=last-i+1;label=f'{prefix}-{last}'+('-wall'if group['wall_stop']else '')
 cmd=[sys.executable,str(R/'scripts/victory_hazard_boulder_fast.py'),'73',step['direction'],label]
 if group['wall_stop']:cmd.append(str(count))
 subprocess.run(cmd,check=True,env=dict(os.environ,REBORN_FAST_KEYS='1'))
 s=json.loads((R/'notes/navigation-state.json').read_text());assert s['positions']['784']['73']==plan[last-1]['box_to']
 print('SW PUSHES VERIFIED',i,last,plan[last-1],flush=True);i=last+1
assert s['switches']['1120'];print('SW PLATE ACTIVE',flush=True)
