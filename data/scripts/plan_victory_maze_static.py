"""Offline search for a normal path through the main-room boulder maze."""
import ast,json,heapq,re,time,sys
from pathlib import Path
from collections import deque
ROOT=Path(__file__).resolve().parents[1]
tree=ast.parse((ROOT/'scripts/nav.py').read_text());ns=dict(ROOT=ROOT,json=json,heapq=heapq,re=re)
exec(compile(ast.Module(body=[x for x in tree.body if isinstance(x,ast.FunctionDef) and x.name=='route'],type_ignores=[]),'nav.py','exec'),ns)
entry='--entry' in sys.argv
startpos=(53,14) if entry else (55,32);goal=(55,32) if entry else (57,42)
bounds=(45,64,14,33) if entry else (50,61,32,45)
v=json.loads((ROOT/'work/189-map784-next.json').read_text());ids=[i for i,e in v['events'].items() if i!='80' and e['name']=='Boulder' and 50<=e['x']<=59 and 33<=e['y']<=42]
if entry:ids=['69','70']
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
 p,boxes,plan=q.popleft();bs=set(boxes);rr=reach(p,bs);key=(min(rr),boxes)
 if key in seen:continue
 seen.add(key)
 if goal in rr:
  out=dict(map=784,player_start=list(startpos),goal_player=list(goal),initial=dict(zip(ids,initial)),pushes=plan,states=len(seen),seconds=time.time()-start)
  (ROOT/('work/189-main-entry-plan.json' if entry else 'work/189-main-maze-plan.json')).write_text(json.dumps(out,indent=2));print('FOUND',len(plan),len(seen),time.time()-start,flush=True);break
 if len(seen)>100000:raise SystemExit('Search bound')
 for j,b in enumerate(boxes):
  for dx,dy,k in [(0,1,'down'),(-1,0,'left'),(1,0,'right'),(0,-1,'up')]:
   before=(b[0]-dx,b[1]-dy);after=(b[0]+dx,b[1]+dy)
   if before not in rr or after in bs or after in box_blocks or (k,after) not in bg.get(b,[]):continue
   nxt=list(boxes);nxt[j]=after
   q.append((before,tuple(nxt),plan+[dict(event=int(ids[j]),**{'from':list(before)},direction=k,box_to=list(after))]))
else:raise SystemExit('No solution')
