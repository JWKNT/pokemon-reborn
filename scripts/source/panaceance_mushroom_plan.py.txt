"""Read-only ordinary-movement plan for Panaceance mushroom puzzle."""
import ast,heapq,json,re,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
node=next(n for n in ast.parse((ROOT/'scripts/nav.py').read_text()).body if isinstance(n,ast.FunctionDef)and n.name=='route')
exec(compile(ast.Module(body=[node],type_ignores=[]),'nav-route','exec'))
ids=['1763','1770','1771']
def build():
 grids={}
 for s in range(4):
  for o in [False,True]:
   sw={k:i==s for i,k in enumerate(ids)};sw['1773']=o
   v=json.loads(subprocess.check_output(['ruby',str(ROOT/'scripts/route_map.rb'),'879','0','0',json.dumps({'switches':sw})],stderr=subprocess.DEVNULL))
   triggers={}
   for e in v['events'].values():
    changes=[c['parameters']for c in e['list']if c['code']==121 and str(c['parameters'][0])in ids and c['parameters'][2]==0]
    if e['trigger']==1 and changes:triggers[e['x'],e['y']]=ids.index(str(changes[-1][0]))
   grids[s,o]=route(v,None,True),triggers
 return grids
if __name__=='__main__':
 x,y,s=map(int,sys.argv[1:4]);o=bool(int(sys.argv[4]));target=sys.argv[5]
 grids=build();start=x,y,s,o;q=[(0,start)];dist={start:0};prev={start:None};goal=None
 while q:
  cost,u=heapq.heappop(q)
  if cost!=dist[u]:continue
  x,y,s,o=u
  if target=='blue'and s==1 or target=='red'and s==0 or target=='purple'and s==2 or target=='flower'and o and abs(x-43)+abs(y-134)==1:goal=u;break
  graph,tr=grids[s,o];edges=[]
  for key,p in graph.get((x,y),[]):
   if 0<=p[0]<=65 and 80<=p[1]<=145:edges.append(((*p,tr.get(p,s),o),key))
  if not o and abs(x-17)+abs(y-119)==1:edges.append(((x,y,s,True),'orb'))
  for v,k in edges:
   n=cost+1
   if n<dist.get(v,float('inf')):dist[v]=n;prev[v]=u,k;heapq.heappush(q,(n,v))
 if goal is None:raise SystemExit('No route; explored '+str(len(dist)))
 steps=[];u=goal
 while prev[u]:p,k=prev[u];steps.append(dict(before=p,after=u,key=k));u=p
 steps.reverse();result=dict(start=start,goal=goal,steps=steps)
 (ROOT/'work/319-mushroom-plan.json').write_text(json.dumps(result,indent=2))
 print(json.dumps(dict(steps=len(steps),goal=goal,changes=[a for a in steps if a['before'][2:]!=a['after'][2:]])))
