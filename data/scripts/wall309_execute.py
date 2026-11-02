"""Execute the offline 23-push wall plan with checked normal controls and checkpoints."""
import json,subprocess,sys,os
from pathlib import Path
R=Path(__file__).resolve().parents[1]
os.environ.update(REBORN_FAST_KEYS='1',REBORN_COORD_CACHE='1',REBORN_ROUTE_CHUNK='112')
plan=json.loads((R/'work/308-wall277-plan.json').read_text())
start=int(sys.argv[1]) if len(sys.argv)>1 else 0
assert 0<=start<len(plan)
def run(n,*a):subprocess.run([sys.executable,str(R/'scripts'/f'{n}.py'),*map(str,a)],check=True)
for i,step in enumerate(plan[start:],start):
 print('WALL PLAN STEP',i,step,flush=True)
 if 'event' in step:
  state=json.loads((R/'notes/navigation-state.json').read_text());assert state['positions']['277'][str(step['event'])]==step['before']
  run('wall309_push',step['event'],step['direction'],f'Wasteland309-Push{i}')
 else:
  x,y=step['walk'];run('q',f'277,{x},{y}')
  canister={(24,14):(46,381),(10,14):(42,380),(17,19):(50,382)}.get((x,y))
  if canister:
   eid,sw=canister
   state=json.loads((R/'notes/navigation-state.json').read_text());assert not state['switches'][str(sw)]
   run('eventq',277,eid,'talk');run('checkpoint',f'Wasteland309-Canister{eid}')
   state=json.loads((R/'notes/navigation-state.json').read_text());assert state['switches'][str(sw)]
run('checkpoint','Wasteland309-ThreeCanisters')
state=json.loads((R/'notes/navigation-state.json').read_text());assert all(state['switches'][str(k)] for k in [380,381,382,383])
print('THREE CANISTERS VERIFIED',flush=True)
