"""Offline switch/cart BFS; only normal reachable lever and cart interactions."""
import ast,json,heapq,re,subprocess,copy,pickle,sys
from pathlib import Path
from collections import deque
from static_cart_model import cart_transition
R=Path(__file__).resolve().parents[1];ns=dict(ROOT=R,json=json,heapq=heapq,re=re)
t=ast.parse((R/'scripts/nav.py').read_text());f=next(n for n in t.body if isinstance(n,ast.FunctionDef)and n.name=='route');exec(compile(ast.Module(body=[f],type_ignores=[]),'route','exec'),ns)
cs=json.loads((R/'work/191-sw-cart88.json').read_text())['pages'][1]['list'];positions={int(k):tuple(v)for k,v in json.loads((R/'work/191-sw-cart-positions.json').read_text()).items()};cache=R/'work/192-sw-entry-graphs.pkl'
if cache.exists():graphs,events=pickle.loads(cache.read_bytes())
else:
 graphs=[]
 for mask in range(128):
  extra={'switches':{str(1136+i):bool(mask&(1<<i))for i in range(7)}}
  v=json.loads(subprocess.check_output(['ruby',str(R/'scripts/route_map.rb'),'786','90','59',json.dumps(extra)],stderr=subprocess.DEVNULL));events=v['events'];v['events'].pop('88',None);g=ns['route'](v,None,True)
  inside=lambda p:50<=p[0]<=130 and 15<=p[1]<=78
  graphs.append({p:[(k,n)for k,n in edges if inside(n)]for p,edges in g.items()if inside(p)})
 cache.write_bytes(pickle.dumps((graphs,events)))
initialmask=int(sys.argv[1])if len(sys.argv)>1 else 0
levers=['70','72','74','76','79','80','82'];q=deque([((90,59),initialmask,0,[])]);seen=set()
while q:
 p,mask,state,plan=q.popleft();g=graphs[mask];cart=positions[state];rr={p};qq=deque([p])
 while qq:
  for k,n in g.get(qq.popleft(),[]):
   if n!=cart and n not in rr:rr.add(n);qq.append(n)
 key=(min(rr),mask,state)
 if key in seen:continue
 seen.add(key)
 adjacent=lambda xy:sorted(rr.intersection({(xy[0]+dx,xy[1]+dy)for dx,dy in [(0,1),(0,-1),(1,0),(-1,0)]}))
 for a in adjacent(cart):
  new,xy=cart_transition(cs,497,state,{1136+i:bool(mask&(1<<i))for i in range(7)},cart)
  if new==state:continue
  assert positions[new]==xy
  pp=plan+[dict(cart=88,before=state,after=new,approach=a,cart_to=xy)]
  if new==8:
   out=dict(initial_mask=initialmask,actions=pp,states=len(seen));(R/'work/191-sw-cart-solution.json').write_text(json.dumps(out,indent=2));print('FOUND',len(pp),'actions',len(seen),'states',flush=True);raise SystemExit(0)
  q.append((a,mask,new,pp))
 for i,eid in enumerate(levers):
  e=events[eid]
  for a in adjacent((e['x'],e['y'])):q.append((a,mask^(1<<i),state,plan+[dict(lever=int(eid),after=not bool(mask&(1<<i)),approach=a)]))
raise SystemExit('No solution '+str(len(seen)))
