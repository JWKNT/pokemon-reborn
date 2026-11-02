"""Offline static route planning only; no input or game state writes."""
import ast,json,subprocess,heapq,re
from pathlib import Path
from collections import deque
R=Path(__file__).resolve().parents[1];env={'ROOT':R,'json':json,'deque':deque,'heapq':heapq,'re':re}
for file in ['nav.py','victory_gem_cliff_event.py']:
 t=ast.parse((R/'scripts'/file).read_text());exec(compile(ast.Module(body=[x for x in t.body if isinstance(x,ast.FunctionDef)],type_ignores=[]),file,'exec'),env)
env.update(allowed=set(range(6,32))|set(range(67,75)),dirs=[('up',0,-1),('down',0,1),('left',-1,0),('right',1,0)])
r=env['route'];out=[]
for stage,a,eid,goal in [(3,(20,30),59,(36,33)),(4,(36,33),61,(56,38)),(5,(56,38),62,(27,48)),(6,(27,48),63,(16,63)),(7,(16,63),64,(51,60)),(8,(51,60),3,None)]:
 ov={'variables':{'520':stage},'switches':{'410':False,**{str(1245+i):i<stage-3 for i in range(5)}}}
 v=json.loads(subprocess.check_output(['ruby',str(R/'scripts/route_map.rb'),'806',*map(str,a),json.dumps(ov)],stderr=subprocess.DEVNULL));(R/'work'/f'amethyst-stage-{stage}-map.json').write_text(json.dumps(v));env.update(eid=eid,forced_stand=goal);steps=env['plan'](v);parts=[]
 for k,b,c,d in steps:
  parts.append({'walk':r(v,b),'start':v['position'],'end':b});parts.append({'cliff':k,'direction':d,'start':b,'end':c});v['position']=c
 e=v['events'][str(eid)]
 if goal is None:
  choices=[]
  for d,dx,dy in env['dirs']:
   b=(e['x']-dx,e['y']-dy)
   try:choices.append((len(r(v,b)),b,d))
   except ValueError:pass
  _,goal,d=min(choices)
 parts.append({'walk':r(v,goal),'start':v['position'],'end':goal})
 if stage==8:parts.append({'exit':d})
 out.append({'stage':stage,'target':(e['x'],e['y']),'goal':goal,'parts':parts})
p=R/'work/amethyst-route-plan.json';p.write_text(json.dumps(out,indent=2));print([(x['stage'],x['goal'],sum(len(z.get('walk',[])) for z in x['parts'])) for x in out])
