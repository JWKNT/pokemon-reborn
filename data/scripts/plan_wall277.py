"""Offline multi-boulder route search using installed tiles and frozen saved evidence."""
import ast,heapq,json,re,subprocess,os
from pathlib import Path
from collections import deque
R=Path(__file__).resolve().parents[1]
os.environ['REBORN_FROZEN_SAVE']=str(R/'backups/Aster-Postgame308-Tier6.rxdata')
tree=ast.parse((R/'scripts/nav.py').read_text());ns=dict(ROOT=R,json=json,heapq=heapq,re=re)
exec(compile(ast.Module(body=[x for x in tree.body if isinstance(x,ast.FunctionDef) and x.name=='route'],type_ignores=[]),'nav.py','exec'),ns)
v=json.loads(subprocess.check_output(['ruby',str(R/'scripts/route_map.rb'),'277','13','7'],stderr=subprocess.DEVNULL))
boxes={int(k):(e['x'],e['y']) for k,e in v['events'].items() if e['name']=='Boulder'}
for k in list(v['events']):
 if v['events'][k]['name']=='Boulder':del v['events'][k]
g=ns['route'](v,None,True);dirs=[(0,1,'down'),(-1,0,'left'),(1,0,'right'),(0,-1,'up')]
def reach(p,b):
 q=deque([p]);seen={p}
 while q:
  for k,n in g.get(q.popleft(),[]):
   if n not in b and n not in seen:seen.add(n);q.append(n)
 return seen
p=(13,7);plan=[]
for goal in [(24,14),(10,14),(17,19),(13,7)]:
 initial=frozenset(boxes.values());q=[(0,0,0,p,initial,[])];seen=set();serial=0
 while q:
  if len(q)>6000:q=heapq.nsmallest(2000,q);heapq.heapify(q)
  _,cost,_,pos,b,moves=heapq.heappop(q);r=reach(pos,b);key=(min(r),b)
  if key in seen:continue
  seen.add(key)
  if goal in r:
   print('GOAL',goal,'states',len(seen),'pushes',len(moves),flush=True)
   for before,after,d in moves:
    eid=next(k for k,v in boxes.items() if v==before);boxes[eid]=after;plan.append(dict(event=eid,before=before,after=after,direction=d))
   plan.append(dict(walk=goal));p=goal;break
  if len(seen)>30000:raise SystemExit('Bound exceeded')
  for bx,by in b:
   for dx,dy,d in dirs:
    back=(bx-dx,by-dy);dest=(bx+dx,by+dy)
    if back not in r or dest in b or (d,dest) not in g.get((bx,by),[]):continue
    nb=(b-{(bx,by)})|{dest};serial+=1
    # Prefer pushing along a short geometric approach while retaining alternatives.
    heuristic=min(abs(x-goal[0])+abs(y-goal[1]) for x,y in reach(back,nb))
    heapq.heappush(q,(cost+1+heuristic*6,cost+1,serial,back,nb,moves+[((bx,by),dest,d)]))
 else:raise SystemExit('No path')
(R/'work/308-wall277-plan.json').write_text(json.dumps(plan,indent=2))
print(json.dumps(plan),flush=True)
