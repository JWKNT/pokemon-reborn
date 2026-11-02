"""Normal-controls SE basement sequence, guarded by real saves after actions."""
import os,sys,json,subprocess
from pathlib import Path
R=Path(__file__).resolve().parents[1];env=dict(os.environ,REBORN_FAST_KEYS='1',REBORN_COORD_CACHE='1');plan=json.loads((R/'work/191-se-solution.json').read_text())['actions'];start=int(sys.argv[1])if len(sys.argv)>1 else 1
switches={'48':'1127','51':'1128','60':'1129','61':'1130','62':'1131'}
def run(name,*args):subprocess.run([sys.executable,str(R/'scripts'/name),*map(str,args)],check=True,env=env)
for i,step in enumerate(plan,1):
 if i<start:continue
 s=json.loads((R/'notes/navigation-state.json').read_text());run('overworld.py')
 if 'lever' in step:
  eid=str(step['lever']);assert s['switches'][switches[eid]]!=step['after']
  run('eventq.py',786,eid,'talk')
 elif 'event' in step:run('victory_boulder_push.py',786,step['event'],step['direction'],1)
 else:raise SystemExit('Unreviewed action')
 run('checkpoint.py',f'SE191-{i}');run('party_open.py');s=json.loads((R/'notes/navigation-state.json').read_text())
 if 'lever' in step:assert s['switches'][switches[eid]]==step['after'],('Lever did not change',i)
 else:assert s['positions']['786'][str(step['event'])]==step['box_to']
 print('SE ACTION VERIFIED',i,step,flush=True)
