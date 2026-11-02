"""Offline search of mirrored movable ladders using installed map collision data."""
import json,sys,copy
from collections import deque
from route_readonly import route
from surface_readonly import surface_plan
room=int(sys.argv[1]);out=sys.argv[2]
initial=json.loads(sys.argv[3]) if len(sys.argv)>3 else None
cfg={2:dict(offset=31,ladder=[66,67],blocks=[35,36],bounds=(10,33,67,115),start=(17,84),block=(14,80),goal=(15,69)),3:dict(offset=30,ladder=[79,80],blocks=[40,41],bounds=(9,37,138,186),start=(36,154),block=(27,153),goal=(35,139))}[room]
maps={m:json.load(open(f'work/{(initial or {}).get("map_session",338)}-map{m}.json')) for m in [881,882]};graphs={};mirrors={};blockers={};off=cfg['offset'];dirs=[('up',0,-1),('down',0,1),('left',-1,0),('right',1,0)]
x0,x1,y0,y1=cfg['bounds'];inside=lambda p:x0<=p[0]<=x1 and y0<=p[1]<=y1
for m,v in maps.items():
 v=copy.deepcopy(v)
 for e in cfg['ladder'] if m==881 else cfg['blocks']:v['events'].pop(str(e))
 mirrors[m]=[(int(k),(e['x'],e['y'])) for k,e in v['events'].items() if e['name']=='Glass' and inside((e['x'],e['y'])) and any(c['code']==201 for c in e['list'])]
 blockers[m]={(e['x'],e['y']) for e in v['events'].values() if not e['through']}
 v['position']=[-1,-1];v['ignore_ice']=True;g=route(v,None,True);graphs[m]={p:[(d,n) for d,n in edges if inside(n)] for p,edges in g.items() if inside(p)}
def ice(p):
 v=maps[882];w,h=v['width'],v['height']
 for z in [2,1,0]:
  tag=v['terrain']['data'][v['data']['data'][p[0]+w*p[1]+w*h*z]]
  if tag and tag!=13:return tag==12
 return False
def reach(m,p,a):
 blocks={a,(a[0],a[1]+off)};seen={p};todo=[p]
 for u in todo:
  for d,n in graphs[m].get(u,[]):
   if n in blocks:continue
   if m==882:
    while ice(n):
     nn=next((nn for dd,nn in graphs[m].get(n,[]) if dd==d and nn not in blocks),None)
     if nn is None:break
     n=nn
   if n not in seen:seen.add(n);todo.append(n)
 return seen
initial=json.loads(sys.argv[3]) if len(sys.argv)>3 else dict(map=881,player=cfg['start'],block=cfg['block'])
q=deque([(initial['map'],tuple(initial['player']),tuple(initial['block']),[])]);seen=set();solution=None
while q:
 m,p,a,path=q.popleft();r=reach(m,p,a);key=(m,a,min(r))
 if key in seen:continue
 seen.add(key)
 if initial.get('goal_block') and list(a)==initial['goal_block']:solution=path;break
 if m==initial.get('goal_map',881):
  if tuple(initial.get('goal',cfg['goal'])) in r:solution=path;break
  if initial.get('surf_goal'):
   vv=copy.deepcopy(maps[m]);vv['position']=p
   for layer,eid in enumerate(cfg['blocks']):vv['events'][str(eid)]['x'],vv['events'][str(eid)]['y']=a[0],a[1]+off*layer
   try:tail=surface_plan(vv,tuple(initial['goal']))
   except ValueError:pass
   else:solution=path+[dict(kind='surface',map=m,start=p,steps=tail,block=a)];break
 assert len(seen)<150000,'Search bound'
 for eid,e in mirrors[m]:
  for d,dx,dy in dirs:
   s=(e[0]-dx,e[1]-dy)
   if s in r and s in graphs[1763-m]:q.append((1763-m,s,a,path+[dict(kind='mirror',map=m,event=eid,stand=s,block=a)]));break
 for layer in [0,1]:
  b=(a[0],a[1]+off*layer)
  if m==881:
   for d,dx,dy in dirs:
    s=(b[0]-dx,b[1]-dy)
    if s in r and (d,b) in graphs[m].get(s,[]):
     dest=(a[0],a[1]+off*(1-layer));q.append((m,dest,a,path+[dict(kind='ladder',map=m,event=cfg['ladder'][layer],stand=s,arrival=dest,block=a)]));break
  else:
   for d,dx,dy in dirs:
    s=(b[0]-dx,b[1]-dy);dest=(b[0]+dx,b[1]+dy)
    if s in r and (d,dest) in graphs[m].get(b,[]) and dest not in blockers[m]:
     while ice(dest):
      nn=(dest[0]+dx,dest[1]+dy)
      if (d,nn) not in graphs[m].get(dest,[]) or nn in blockers[m]:break
      dest=nn
     na=(dest[0],dest[1]-off*layer);q.append((m,s,na,path+[dict(kind='push',map=m,event=cfg['blocks'][layer],direction=d,stand=s,before=b,after=dest,block=na)]))
assert solution,('No solution',len(seen))
json.dump(dict(room=room,states=len(seen),steps=solution,goal=initial.get('goal',cfg['goal']),goal_map=initial.get('goal_map',881),session=initial.get('session',338)),open(out,'w'),indent=2)
print('SOLVED',room,len(seen),'states',len(solution),'actions')
for s in solution:print(s)
