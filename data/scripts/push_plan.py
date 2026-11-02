"""Read-only breadth-first plan for normal Strength pushes on a known map."""
import sys,subprocess,json,copy
from collections import deque
from nav import route
m,sx,sy,gx,gy=map(int,sys.argv[1:6]);ids=[a for a in sys.argv[6:] if not a.startswith('--')]
remove=[a.split('=',1)[1].split(',') for a in sys.argv if a.startswith('--remove=')]
v=json.loads(subprocess.check_output(['ruby','scripts/route_map.rb',str(m),str(sx),str(sy)],stderr=subprocess.DEVNULL))
for group in remove:
 for i in group:v['events'].pop(i,None)
initial=tuple((v['events'][i]['x'],v['events'][i]['y']) for i in ids)
q=deque([((sx,sy),initial,[])]);seen=set()
while q:
 pos,boxes,plan=q.popleft();vv=dict(v,events={k:dict(e) for k,e in v['events'].items()});vv['position']=list(pos)
 for i,p in zip(ids,boxes):vv['events'][i].update(x=p[0],y=p[1])
 reach=route(vv,None);key=(min(reach),boxes)
 if key in seen:continue
 seen.add(key)
 if (gx,gy) in reach:print(json.dumps({'map':m,'pushes':plan,'goal':[gx,gy],'states':len(seen)},indent=2));break
 if len(seen)>150:raise SystemExit('Search bound')
 for bi,(x,y) in enumerate(boxes):
  for dx,dy,k in [(0,1,'down'),(0,-1,'up'),(1,0,'right'),(-1,0,'left')]:
   before=(x-dx,y-dy);after=(x+dx,y+dy)
   if before not in reach:continue
   free=dict(vv,events=dict(vv['events']));free['position']=[x,y];free['events'].pop(ids[bi])
   try:
    if len(route(free,after))!=1:continue
   except ValueError:continue
   new=list(boxes);new[bi]=after
   q.append(((x,y),tuple(new),plan+[{'event':int(ids[bi]),'from':list(before),'direction':k,'box_to':list(after)}]))
else:raise SystemExit('No push solution with these obstacles')
