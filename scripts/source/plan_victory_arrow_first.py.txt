"""Offline search for a normal path through the main-room boulder maze."""
import ast,json,heapq,re,time,sys,subprocess
from pathlib import Path
from collections import deque
ROOT=Path(__file__).resolve().parents[1]
tree=ast.parse((ROOT/'scripts/nav.py').read_text());ns=dict(ROOT=ROOT,json=json,heapq=heapq,re=re)
exec(compile(ast.Module(body=[x for x in tree.body if isinstance(x,ast.FunctionDef) and x.name=='route'],type_ignores=[]),'nav.py','exec'),ns)
startpos=(29,32);goal=(48,53);bounds=(27,70,31,56)
v=json.loads((ROOT/'work/196-arrow-static.json').read_text());ids=['58','59','60','61','62','63']
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
 if goal in rr:
  out=dict(map=787,player_start=list(startpos),goal_player=list(goal),initial=dict(zip(ids,initial)),pushes=plan,states=len(seen),seconds=time.time()-start)
  (ROOT/'work/196-arrow-first-boulders-plan.json').write_text(json.dumps(out,indent=2));print('FOUND',len(plan),len(seen),time.time()-start,flush=True);break
 if len(seen)>100000:raise SystemExit('Search bound')
 for j,b in enumerate(boxes):
  if b is None:continue
  if j>=4:
   for dx,dy,k in [(0,1,'down'),(-1,0,'left'),(1,0,'right'),(0,-1,'up')]:
    before=(b[0]-dx,b[1]-dy)
    if before in rr:
     nxt=list(boxes);nxt[j]=None;q.append((before,tuple(nxt),plan+[dict(event=int(ids[j]),kind='smash',**{'from':list(before)},direction=k)]));break
   continue
  for dx,dy,k in [(0,1,'down'),(-1,0,'left'),(1,0,'right'),(0,-1,'up')]:
   before=(b[0]-dx,b[1]-dy);after=(b[0]+dx,b[1]+dy)
   if before not in rr or after in bs or after in box_blocks or (k,after) not in bg.get(b,[]):continue
   nxt=list(boxes);nxt[j]=after
   q.append((before,tuple(nxt),plan+[dict(event=int(ids[j]),**{'from':list(before)},direction=k,box_to=list(after))]))
else:raise SystemExit('No solution')
