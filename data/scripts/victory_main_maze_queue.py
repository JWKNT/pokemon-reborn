"""Execute the reviewed static maze solution, verifying every normal push/save."""
import json,subprocess,sys,os
from pathlib import Path
R=Path(__file__).resolve().parents[1]
planfile=Path(sys.argv[2]) if len(sys.argv)>2 else R/'work/189-main-maze-plan.json'
prefix=sys.argv[3] if len(sys.argv)>3 else 'Maze190'
p=json.loads(planfile.read_text())['pushes']+[dict(event=80,direction='left',box_to=[55,42])]
start=int(sys.argv[1]) if len(sys.argv)>1 else 1
for i,step in enumerate(p,1):
 if i<start:continue
 state=json.loads((R/'notes/navigation-state.json').read_text())
 dx,dy={'left':(-1,0),'right':(1,0),'up':(0,-1),'down':(0,1)}[step['direction']]
 assert state['positions']['784'][str(step['event'])]==[step['box_to'][0]-dx,step['box_to'][1]-dy],('Unexpected box before step',i)
 subprocess.run([sys.executable,str(R/'scripts/victory_hazard_boulder.py'),str(step['event']),step['direction'],f'{prefix}-{i}'],check=True,env=dict(os.environ,REBORN_FAST_KEYS='1'))
print('MAIN MAZE COMPLETE',flush=True)
