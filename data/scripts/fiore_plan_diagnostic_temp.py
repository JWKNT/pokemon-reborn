"""Read-only Fiore maze planner: walking, Surf, Dive and reviewed room portals."""
import argparse,copy,heapq,json,subprocess
from surface_readonly import ROOT,route,tag,WATER
p=argparse.ArgumentParser();p.add_argument('--start',required=True);p.add_argument('--goal',required=True);p.add_argument('--output',required=True);p.add_argument('--variables',type=json.loads,default={});a=p.parse_args()
start3=tuple(map(int,a.start.split(',')));goal=tuple(map(int,a.goal.split(',')))
maps={m:json.loads(subprocess.check_output(['ruby',str(ROOT/'scripts/route_map.rb'),str(m),'0','0',json.dumps({'variables':a.variables})],stderr=subprocess.DEVNULL)) for m in range(678,684)}
surface={678:681,679:682};under={u:s for s,u in surface.items()};graphs={};portals={};water=set(WATER)|{8}
for m,v in maps.items():
 graphs[m,False]=route(v,None,True)
 if m in surface:
  vv=copy.deepcopy(v)
  for i,t in enumerate(v['terrain']['data']):
   if t in water:vv['passages']['data'][i]=0;vv['priorities']['data'][i]=0
  graphs[m,True]=route(vv,None,True)
 for eid,e in v['events'].items():
  cs=e['list'] or [];ds={tuple(c['parameters'][1:4])for c in cs if c['code']==201 and c['parameters'][0]==0}
  if len(ds)!=1 or any(c['code']in[102,103,104,301]or any(z in str(c['parameters'])for z in ['pbTrainerBattle','pbDoubleTrainerBattle','pbWildBattle'])for c in cs):continue
  dest=next(iter(ds))
  if dest[0]not in maps:continue
  required={c['parameters'][2] for c in cs if c['code']==111 and c['parameters'][:2]==[6,-1]}
  for dx,dy,k,d in [(0,1,'up',8),(0,-1,'down',2),(1,0,'left',4),(-1,0,'right',6)]:
   if required and d not in required:continue
   xy=(e['x']+dx,e['y']+dy)
   portals.setdefault((m,*xy),[]).append((dest,{'kind':'portal','map':m,'event':int(eid),'arrival':list(dest)}))
start=(*start3,start3[0]in surface and tag(maps[start3[0]],start3[1:])in water)
q=[(0,start)];dist={start:0};prev={start:None};end=None
while q:
 cost,n=heapq.heappop(q)
 if cost!=dist[n]:continue
 m,x,y,surf=n;xy=(x,y);v=maps[m]
 if n[:3]==goal:end=n;break
 moves=[]
 candidates=list(graphs[m,surf].get(xy,[]))
 if m in surface and not surf:
  candidates.extend((k,z)for k,z in graphs[m,True].get(xy,[])if tag(v,z)in water and tag(v,xy)not in water)
 for k,z in candidates:
  if surf and k.startswith('jump:'):continue
  ns=m in surface and tag(v,z)in water;detail={'kind':'walk','map':m,'target':list(z)};extra=1
  if m in surface and tag(v,z)==8:continue
  if m in surface and not surf and ns:extra=8
  if m in surface and surf and not ns and abs(z[0]-x)+abs(z[1]-y)!=1:continue
  if m in surface and surf and k=='down'and tag(v,z)==9:
   zx,zy=z
   while tag(v,(zx,zy))in[8,9]:zy+=1
   z=(zx,zy);detail={'kind':'waterfall','map':m,'direction':'down','from':list(xy),'arrival':[m,*z]};extra=8
  moves.append(((m,*z,ns),detail,extra))
 if m in surface and surf and tag(v,(x,y-1))==8:
  yy=y-1
  while tag(v,(x,yy))in[8,9]:yy-=1
  moves.append(((m,x,yy,True),{'kind':'waterfall','map':m,'direction':'up','from':[x,y],'arrival':[m,x,yy]},8))
 if m in surface and surf and tag(v,xy)==5:
  um=surface[m]
  if xy in graphs[um,False]:moves.append(((um,x,y,False),{'kind':'dive','from':[m,x,y],'arrival':[um,x,y]},8))
 if m in under and tag(maps[under[m]],xy)==5:
  sm=under[m];moves.append(((sm,x,y,True),{'kind':'dive','from':[m,x,y],'arrival':[sm,x,y]},8))
 for dest,detail in portals.get(n[:3],[]):
  if xy not in graphs[m,surf]:continue
  dm,dx,dy=dest;mode=dm in surface and tag(maps[dm],(dx,dy))in water
  moves.append(((*dest,mode),detail,12))
 for nn,d,e in moves:
  nc=cost+e
  if nc<dist.get(nn,float('inf')):dist[nn]=nc;prev[nn]=(n,d);heapq.heappush(q,(nc,nn))

if not end:
 print('NEAREST',sorted([(abs(n[1]-goal[1])+abs(n[2]-goal[2]),n) for n in dist if n[0]==goal[0]])[:20]);raise SystemExit(1)
steps=[]
while prev[end]:old,d=prev[end];steps.append(d);end=old
steps.reverse();segments=[]
for d in steps:
 if d['kind']=='walk'and segments and segments[-1]['kind']=='walk'and segments[-1]['map']==d['map']:segments[-1]=d
 else:segments.append(d)
result={'start':list(start3),'goal':list(goal),'segments':segments,'source':'Installed maps/metadata and observed navigation state; no game mutation'}
open(a.output,'w').write(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
