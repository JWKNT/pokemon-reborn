"""Read-only ordinary Surf/Dive planner across the four connected lake maps."""
from surface_readonly import route,tag,WATER
import json,heapq,copy,sys
from pathlib import Path
root=Path(__file__).resolve().parents[1]
vs={m:json.loads((root/f'work/lake{m}.json').read_text()) for m in [567,565,553,547]}
ground={m:route(v,None,True)for m,v in vs.items()};surf={}
for m in [567,565]:
 v=copy.deepcopy(vs[m])
 for i,t in enumerate(v['terrain']['data']):
  if t in WATER:v['passages']['data'][i]=0;v['priorities']['data'][i]=0
 surf[m]=route(v,None,True)
pair={567:553,565:547};reverse={v:k for k,v in pair.items()}
def choices(p):
 m,x,y,water=p;pos=(x,y);under=m in reverse
 graph=ground[m] if under or not water else surf[m]
 edges=list(graph.get(pos,[]))
 if not under and not water:
  edges.extend((k,n)for k,n in surf[m].get(pos,[])if tag(vs[m],n)in WATER and tag(vs[m],pos)not in WATER)
 for k,n in edges:
  if k.startswith('jump:'):continue
  nw=False if under else tag(vs[m],n)in WATER
  action=('surf:' if not under and not water and nw else '')+k
  yield (m,*n,nw),action,8 if action.startswith('surf:') else 1
 other=reverse.get(m,pair.get(m));surface=other if under else m
 if tag(vs[surface],pos)==5 and pos in ground[other] if not under else tag(vs[surface],pos)==5:
  yield (other,x,y,under),'surface'if under else'dive',8
 # These pairs share exactly the south/north boundary at x offset55.
 for north,south in [(567,565),(553,547)]:
  if m==north and y==67 and 55<=x<130:dest=(south,x-55,0);key='down'
  elif m==south and y==0:dest=(north,x+55,67);key='up'
  else:continue
  dm,dx,dy=dest;dg=ground[dm]if under or not water else surf[dm]
  if (dx,dy)in dg:yield(*dest,water),'connect:'+key,1
m,x,y,tm,tx,ty=map(int,sys.argv[1:]);start=(m,x,y,m in surf and tag(vs[m],(x,y))in WATER)
q=[(0,start)];dist={start:0};prev={start:None};end=None
while q:
 d,p=heapq.heappop(q)
 if d!=dist[p]:continue
 if p[:3]==(tm,tx,ty):end=p;break
 for n,k,c in choices(p):
  nd=d+c
  if nd<dist.get(n,float('inf')):dist[n]=nd;prev[n]=(p,k);heapq.heappush(q,(nd,n))
assert end,'No lake route'
steps=[]
while prev[end]:
 p,k=prev[end];steps.append({'from':p,'to':end,'key':k});end=p
steps.reverse();out=root/'work/lake-route-planned.json';out.write_text(json.dumps(steps,indent=2))
print('PLAN',len(steps),'steps',out)
for i,s in enumerate(steps):
 if s['key']in['dive','surface']or s['key'].startswith('connect:'):print(i,s)
