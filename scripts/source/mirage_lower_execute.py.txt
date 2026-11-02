"""Execute an offline lower-tower plan with normal inputs and saved group checks."""
import json,sys,subprocess,os,time
from pathlib import Path
R=Path(__file__).resolve().parents[1];p=json.load(open(sys.argv[1]));start=int(sys.argv[2]) if len(sys.argv)>2 else 0;steps=p['steps'];i=start
os.environ.setdefault('REBORN_FAST_KEYS','1');os.environ.setdefault('REBORN_COORD_CACHE','1');os.environ.setdefault('REBORN_ROUTE_CHUNK','84')
def run(s,*a):subprocess.run([sys.executable,str(R/'scripts'/f'{s}.py'),*map(str,a)],check=True)
while i<len(steps):
 s=steps[i];print('LOWER PLAN STEP',i,s,flush=True);label=f'Mirage{p.get("session",338)}-Room{p["room"]}-{p.get("label_tag","Ice")}-Step{i}'
 if s['kind']=='push':
  j=i+1
  while j<len(steps) and j-i<12 and steps[j-1]['after']==[steps[j-1]['before'][0]+({'left':-1,'right':1}.get(s['direction'],0)),steps[j-1]['before'][1]+({'up':-1,'down':1}.get(s['direction'],0))] and steps[j]['kind']=='push' and steps[j]['event']==s['event'] and steps[j]['direction']==s['direction']:j+=1
  n=json.load(open(R/'notes/navigation-state.json'));pos=n['positions'][str(s['map'])][str(s['event'])];assert pos==s['before'],('Stale push plan',pos,s)
  run('mirage_ladder_push',s['map'],s['event'],s['direction'],j-i,label)
 else:
  run('q',f'{s["map"]},{s["stand"][0]},{s["stand"][1]}')
  if s['kind']=='mirror':run('mirage_lower_shift',s['map'],s['event']);run('checkpoint',label)
  else:
   run('eventq',s['map'],s['event'],'enter')
   # A legitimate saved checkpoint verifies each dynamic stair destination.
   run('checkpoint',label)
   v=json.load(open(R/'notes'/f'{label}-status.json'));assert v['map']==s['map'] and v['position']==s['arrival'],('Unexpected ladder arrival',v['map'],v['position'],s)
  j=i+1
 with open(R/f'work/338-room{p["room"]}-execution.jsonl','a') as f:f.write(json.dumps(dict(epoch=time.time(),step=i,next_step=j,checkpoint=label))+'\n')
 i=j
run('q',f'{p.get("goal_map",881)},{p["goal"][0]},{p["goal"][1]}');run('checkpoint',f'Mirage{p.get("session",338)}-Room{p["room"]}Solved')
print('ROOM SOLVED',p['room'],flush=True)
