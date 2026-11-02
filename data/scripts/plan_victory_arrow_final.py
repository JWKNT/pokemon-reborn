"""Offline search for a normal path through the main-room boulder maze."""
import ast,json,heapq,re,time,sys,subprocess
from pathlib import Path
from collections import deque
ROOT=Path(__file__).resolve().parents[1]
tree=ast.parse((ROOT/'scripts/nav.py').read_text());ns=dict(ROOT=ROOT,json=json,heapq=heapq,re=re)
exec(compile(ast.Module(body=[x for x in tree.body if isinstance(x,ast.FunctionDef) and x.name=='route'],type_ignores=[]),'nav.py','exec'),ns)
startpos=(48,52);goal=(48,65);bounds=(27,70,31,78)
v=json.loads((ROOT/'work/197-arrow-switch-off-planning.json').read_text());ids=['69','73','74']
v['events']['65'].update(x=48,y=53)
for e in ['62','63','64']:v['events'].pop(e,None)
for e,xy in {'58':(62,44),'59':(68,47),'60':(64,52),'61':(60,52)}.items():v['events'][e].update(x=xy[0],y=xy[1])
initial=tuple((v['events'][i]['x'],v['events'][i]['y']) for i in ids)
for i in ids:v['events'].pop(i)
v['position']=list(startpos);g=ns['route'](v,None,True)
# Boulders use Game_Character movement, without player stair/ledge triggers.
source=ast.unparse(next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='route'))
source=source.replace('graph = {}', 'jumps = {}; graph = {}').replace('native_jump = terrain(n) == 1','native_jump = False')
boxns=dict(ROOT=ROOT,json=json,heapq=heapq,re=re);exec(compile(source,'static-box-route','exec'),boxns);bg=boxns['route'](v,None,True)
g={p:[(k,n) for k,n in edges if bounds[0]<=n[0]<=bounds[1] and bounds[2]<=n[1]<=bounds[3]] for p,edges in g.items() if bounds[0]<=p[0]<=bounds[1] and bounds[2]<=p[1]<=bounds[3]}
box_blocks={(e['x'],e['y']) for e in v['events'].values() if not e['through']}
def reach(p,bs):
 q=deque([p]);seen={p}
 while q:
  for k,n in g.get(q.popleft(),[]):
   if n not in bs and n not in seen:seen.add(n);q.append(n)
 return seen
q=deque([(startpos,initial,[])]);seen=set();start=time.time()
while q:
 p,boxes,plan=q.popleft();bs={b for b in boxes if b is not None};rr=reach(p,bs);key=(min(rr),boxes)
 if key in seen:continue
 seen.add(key)
 if boxes[2]==goal:
  out=dict(map=787,player_start=list(startpos),goal_player=list(goal),initial=dict(zip(ids,initial)),pushes=plan,states=len(seen),seconds=time.time()-start)
  (ROOT/'work/197-arrow-final-boulders-plan.json').write_text(json.dumps(out,indent=2));print('FOUND',len(plan),len(seen),time.time()-start,flush=True);break
 if len(seen)>100000:raise SystemExit('Search bound')
 for j,b in enumerate(boxes):
  if b is None:continue
  if False:
   for dx,dy,k in [(0,1,'down'),(-1,0,'left'),(1,0,'right'),(0,-1,'up')]:
    before=(b[0]-dx,b[1]-dy)
    if before in rr:
     nxt=list(boxes);nxt[j]=None;q.append((before,tuple(nxt),plan+[dict(event=int(ids[j]),kind='smash',**{'from':list(before)},direction=k)]));break
   continue
  for dx,dy,k in [(0,1,'down'),(-1,0,'left'),(1,0,'right'),(0,-1,'up')]:
   before=(b[0]-dx,b[1]-dy);after=(b[0]+dx,b[1]+dy)
   if before not in rr or after in bs or after in box_blocks or (k,after) not in bg.get(b,[]):continue
   nxt=list(boxes);nxt[j]=after
   q.append((b,tuple(nxt),plan+[dict(event=int(ids[j]),**{'from':list(before)},direction=k,box_to=list(after))]))
else:raise SystemExit('No solution')
