"""Offline Sokoban plan from installed map and frozen owned navigation evidence.
Extracts the pure route function without importing input-owning modules.
"""
import ast,json,heapq,re,sys,subprocess
from pathlib import Path
from collections import deque
ROOT=Path(__file__).resolve().parents[1]
tree=ast.parse((ROOT/'scripts/nav.py').read_text());ns=dict(ROOT=ROOT,json=json,heapq=heapq,re=re)
exec(compile(ast.Module(body=[x for x in tree.body if isinstance(x,ast.FunctionDef) and x.name=='route'],type_ignores=[]),'nav.py','exec'),ns)
m,eid,sx,sy,bx,by,gx,gy=map(int,sys.argv[1:9]);eid=str(eid)
v=json.loads(subprocess.check_output(['ruby',str(ROOT/'scripts/route_map.rb'),str(m),str(sx),str(sy)],stderr=subprocess.DEVNULL))
v['events'].pop(eid);g=ns['route'](v,None,True)
source=ast.unparse(next(x for x in tree.body if isinstance(x,ast.FunctionDef) and x.name=='route')).replace('graph = {}','jumps = {}; graph = {}').replace('native_jump = terrain(n) == 1','native_jump = False')
boxns=dict(ROOT=ROOT,json=json,heapq=heapq,re=re);exec(source,boxns);bg=boxns['route'](v,None,True)
box_blocks={(e['x'],e['y']) for e in v['events'].values() if not e['through']}
def reachable(p,b):
 q=deque([p]);seen={p}
 while q:
  for k,n in g.get(q.popleft(),[]):
   if n!=b and n not in seen:seen.add(n);q.append(n)
 return seen
q=deque([((sx,sy),(bx,by),[])]);seen=set()
while q:
 p,b,plan=q.popleft();reach=reachable(p,b);key=(min(reach),b)
 if key in seen:continue
 seen.add(key)
 if b==(gx,gy):
  print(json.dumps(dict(map=m,initial={eid:[bx,by]},goals={eid:[gx,gy]},pushes=plan,states=len(seen)),indent=2));break
 if len(seen)>10000:raise SystemExit('Search limit')
 for dx,dy,k in [(0,1,'down'),(-1,0,'left'),(1,0,'right'),(0,-1,'up')]:
  before=(b[0]-dx,b[1]-dy);after=(b[0]+dx,b[1]+dy)
  if before not in reach or after in box_blocks or (k,after) not in bg.get(b,[]):continue
  # The player remains on the pushing side; it can walk into the vacated tile next.
  q.append((before,after,plan+[dict(event=int(eid),**{'from':list(before)},direction=k,box_to=list(after))]))
else:
 print('No solution; states',len(seen),'boxes',sorted(set(b for p,b in seen)),file=sys.stderr);raise SystemExit(1)
