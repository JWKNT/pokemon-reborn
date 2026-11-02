"""Offline breadth-first push planner for the two short Wasteland entrance rooms."""
import ast,json,heapq,re,subprocess
from pathlib import Path
from collections import deque
R=Path(__file__).resolve().parents[1];ns=dict(ROOT=R,json=json,heapq=heapq,re=re)
t=ast.parse((R/'scripts/nav.py').read_text());exec(compile(ast.Module(body=[x for x in t.body if isinstance(x,ast.FunctionDef)and x.name=='route'],type_ignores=[]),'nav.py','exec'),ns)
for mid,start,goal in [(275,(9,10),(17,13)),(276,(10,6),(20,15))]:
 v=json.load(open(R/f'work/309-map{mid}.json'));boxes={int(k):(e['x'],e['y'])for k,e in v['events'].items()if e['name']=='Boulder'}
 for k in list(v['events']):
  if v['events'][k]['name']=='Boulder':del v['events'][k]
 v['position']=list(start);g=ns['route'](v,None,True)
 def reach(p,b):
  q=deque([p]);s={p}
  while q:
   for _,n in g.get(q.popleft(),[]):
    if n not in b and n not in s:s.add(n);q.append(n)
  return s
 q=deque([(start,tuple(boxes.values()),[])]);seen=set();ids=list(boxes)
 while q:
  p,b,plan=q.popleft();rr=reach(p,b);key=(min(rr),b)
  if key in seen:continue
  seen.add(key)
  if goal in rr:
   print(mid,plan,flush=True);json.dump(plan,open(R/f'work/309-small-{mid}-plan.json','w'),indent=2);break
  for i,(x,y)in enumerate(b):
   for dx,dy,d in [(0,1,'down'),(0,-1,'up'),(-1,0,'left'),(1,0,'right')]:
    back=(x-dx,y-dy);to=(x+dx,y+dy)
    if back in rr and to not in b and (d,to)in g.get((x,y),[]):
     bb=list(b);bb[i]=to;q.append((back,tuple(bb),plan+[dict(event=ids[i],direction=d,before=[x,y],after=to)]))
 else:print('No route',mid,'states',len(seen),'start edges',g.get(start));print('reachable',sorted(reach(start,tuple(boxes.values()))))
