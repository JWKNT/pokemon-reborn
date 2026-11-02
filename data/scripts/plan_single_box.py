"""Offline shortest normal pushes from a public map; no UI imports."""
import ast,json,heapq,re,sys,copy
from pathlib import Path
from collections import deque
ROOT=Path(__file__).resolve().parents[1]
p,eid,gx,gy=sys.argv[1:5];eid=str(int(eid));goal=(int(gx),int(gy));v=json.loads(Path(p).read_text())
fun=next(n for n in ast.parse((ROOT/'scripts/nav.py').read_text()).body if isinstance(n,ast.FunctionDef)and n.name=='route');ns=dict(ROOT=ROOT,json=json,heapq=heapq,re=re);exec(ast.unparse(fun).replace('graph = {}','jumps = {}; graph = {}').replace('native_jump = terrain(n) == 1','native_jump = False'),ns);route=ns['route']
e=v['events'].pop(eid);box=(e['x'],e['y']);g=route(v,None,True);lo,hi=5,5
xmin,xmax,ymin,ymax=min(box[0],goal[0])-lo,max(box[0],goal[0])+hi,min(box[1],goal[1])-lo,max(box[1],goal[1])+hi
def reach(p,b):
 q=[p];r={p}
 for a in q:
  for _,d in g.get(a,[]):
   if d!=b and xmin<=d[0]<=xmax and ymin<=d[1]<=ymax and d not in r:r.add(d);q.append(d)
 return r
seeds=[(box[0]+dx,box[1]+dy)for dx,dy in [(1,0),(-1,0),(0,1),(0,-1)]if (box[0]+dx,box[1]+dy)in g]
q=deque((p,box,[])for p in seeds);seen=set()
while q:
 p,b,plan=q.popleft();r=reach(p,b);key=(min(r),b)
 if key in seen:continue
 seen.add(key)
 if b==goal:print(json.dumps({'event':eid,'goal':goal,'pushes':plan,'states':len(seen)},indent=2));break
 for k,dx,dy in [('right',1,0),('left',-1,0),('down',0,1),('up',0,-1)]:
  a=(b[0]-dx,b[1]-dy);d=(b[0]+dx,b[1]+dy)
  if a in r and (k,d)in g.get(b,[]) and xmin<=d[0]<=xmax and ymin<=d[1]<=ymax:q.append((b,d,plan+[{'key':k,'box_from':b,'box_to':d,'stand':a}]))
else:raise SystemExit('No ordinary push solution')
