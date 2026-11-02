"""Offline combined normal-cart and boulder plan for the southeast approach."""
import ast,json,heapq,re,subprocess,copy
from pathlib import Path
from collections import deque
R=Path(__file__).resolve().parents[1];ns=dict(ROOT=R,json=json,heapq=heapq,re=re)
t=ast.parse((R/'scripts/nav.py').read_text());fun=next(n for n in t.body if isinstance(n,ast.FunctionDef) and n.name=='route');exec(compile(ast.Module(body=[fun],type_ignores=[]),'route','exec'),ns)
source=ast.unparse(fun).replace('graph = {}','jumps = {}; graph = {}').replace('native_jump = terrain(n) == 1','native_jump = False');bn=dict(ROOT=R,json=json,heapq=heapq,re=re);exec(source,bn)
v=json.loads(subprocess.check_output(['ruby',str(R/'scripts/route_map.rb'),'784','110','52'],stderr=subprocess.DEVNULL));v['events'].pop('75');graphs=[];bgraphs=[]
for cart in [(95,61),(109,52)]:
 vv=copy.deepcopy(v);vv['events']['132'].update(x=cart[0],y=cart[1]);graphs.append(ns['route'](vv,None,True));bgraphs.append(bn['route'](vv,None,True))
blocks={(e['x'],e['y'])for i,e in v['events'].items() if not e['through'] and i!='132'}
def reach(p,b,g):
 q=deque([p]);r={p}
 while q:
  for k,n in g.get(q.popleft(),[]):
   if n!=b and n not in r:r.add(n);q.append(n)
 return r
q=deque([((110,52),(111,61),1,[])]);seen=set()
while q:
 p,b,c,plan=q.popleft();g=graphs[c];rr=reach(p,b,g);key=(min(rr),b,c)
 if key in seen:continue
 seen.add(key)
 if b==(103,54):
  out=dict(start_player=[110,52],start_box=[111,61],start_cart=1,actions=plan,states=len(seen));(R/'work/191-south-combined-plan.json').write_text(json.dumps(out,indent=2));print('FOUND',len(plan),'actions',len(seen));break
 boarding=[(95,62),(110,52)][c]
 if boarding in rr:q.append(([(95,62),(110,52)][1-c],b,1-c,plan+[dict(cart=132,after=1-c)]))
 for dx,dy,k in [(0,1,'down'),(-1,0,'left'),(1,0,'right'),(0,-1,'up')]:
  before=(b[0]-dx,b[1]-dy);after=(b[0]+dx,b[1]+dy)
  if before in rr and after not in blocks and (k,after) in bgraphs[c].get(b,[]):q.append((before,after,c,plan+[dict(event=75,direction=k,box_to=list(after))]))
else:print('NO SOLUTION',len(seen))
