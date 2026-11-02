"""Read-only route planner for installed Idyll mushroom switches; no game inputs."""
import ast,heapq,json,re,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
# Load only the pure route function, avoiding the UI module's input ownership.
module=ast.parse((ROOT/'scripts/nav.py').read_text())
node=next(n for n in module.body if isinstance(n,ast.FunctionDef) and n.name=='route')
exec(compile(ast.Module(body=[node],type_ignores=[]),'nav-route','exec'))
switch_ids=['1763','1770','1771']
def build():
 out={}
 for state in range(4):
  for orb in [False,True]:
   sw={k:i==state for i,k in enumerate(switch_ids)};sw['1773']=orb;sw['1772']=True # Plan for after the southeast orb is activated.
   v=json.loads(subprocess.check_output(['ruby',str(ROOT/'scripts/route_map.rb'),'878','0','0',json.dumps({'switches':sw})],stderr=subprocess.DEVNULL))
   graph=route(v,None,True)
   triggers={}
   for e in v['events'].values():
    changes=[c['parameters'] for c in e['list'] if c['code']==121]
    if e['trigger']!=1 or not changes:continue
    relevant=[a for a in changes if str(a[0])in switch_ids and a[2]==0]
    if relevant:triggers[(e['x'],e['y'])]=switch_ids.index(str(relevant[-1][0]))
   out[state,orb]=(graph,triggers)
 return out
if __name__=='__main__':
 start=tuple(map(int,sys.argv[1:3]));state=int(sys.argv[3]);target=sys.argv[4]
 grids=build();initial=(*start,state,False);q=[(0,initial)];dist={initial:0};prev={initial:None};goal=None
 while q:
  cost,u=heapq.heappop(q)
  if cost!=dist[u]:continue
  x,y,s,o=u
  if target=='orb' and o or target=='shaymin' and o and abs(x-44)+abs(y-134)==1:goal=u;break
  g,tr=grids[s,o];edges=[]
  for key,p in g.get((x,y),[]):
   if not(0<=p[0]<=65 and 90<=p[1]<=145):continue
   edges.append(((*p,tr.get(p,s),o),key))
  if not o and abs(x-26)+abs(y-130)==1:edges.append(((x,y,s,True),'orb'))
  for v,k in edges:
   n=cost+1
   if n<dist.get(v,float('inf')):dist[v]=n;prev[v]=(u,k);heapq.heappush(q,(n,v))
 if goal is None:
  print('reachable',len(dist),'states',sorted(set(u[2:]for u in dist)),'bounds',[(min(u[i]for u in dist),max(u[i]for u in dist))for i in [0,1]])
  raise SystemExit('No mushroom path')
 steps=[];u=goal
 while prev[u]:p,k=prev[u];steps.append({'from':p,'to':u,'key':k});u=p
 steps.reverse();out={'start':initial,'goal':goal,'steps':steps}
 (ROOT/'work/318-mushroom-plan.json').write_text(json.dumps(out,indent=2))
 print(json.dumps({'count':len(steps),'transitions':[x for x in steps if x['from'][2:]!=x['to'][2:]],'goal':goal}))
