"""Offline shortest-push plan for one Citae Prisma mirror; planning state only."""
import sys,json,subprocess,heapq,itertools
from nav import route
from pathlib import Path
R=Path(__file__).resolve().parents[1]
eid,gx,gy=map(int,sys.argv[1:4]);assert eid in [72,73,74,75,95]
n=json.load(open(R/'notes/navigation-state.json'));pos=tuple(map(int,sys.argv[4:6])) if len(sys.argv)>5 else tuple(json.load(open(R/'work/last-native-position.json'))['position'][1:])
v=json.loads(subprocess.check_output(['ruby',str(R/'scripts/route_map.rb'),'896',*map(str,pos)],stderr=subprocess.DEVNULL));start=(v['events'][str(eid)]['x'],v['events'][str(eid)]['y'])
counter=itertools.count();q=[(0,next(counter),pos,start,[])];seen=set()
while q:
 cost,_,player,box,plan=heapq.heappop(q);vv=dict(v,events={k:dict(e) for k,e in v['events'].items()},position=list(player));vv['events'][str(eid)].update(x=box[0],y=box[1]);reach=route(vv,None);key=(min(reach),box)
 if key in seen:continue
 seen.add(key)
 if box==(gx,gy):print(json.dumps({'event':eid,'from':start,'to':[gx,gy],'states':len(seen),'pushes':plan},indent=2));break
 if len(seen)>1800:raise SystemExit('Search bound')
 for dx,dy,d in [(0,-1,'up'),(0,1,'down'),(-1,0,'left'),(1,0,'right')]:
  before=(box[0]-dx,box[1]-dy);after=(box[0]+dx,box[1]+dy)
  if not(17<=after[0]<=28 and 59<=after[1]<=68) or before not in reach:continue
  free=dict(vv,events=dict(vv['events']),position=list(box));free['events'].pop(str(eid))
  try:
   if route(free,after)!=[d]:continue
  except ValueError:continue
  heapq.heappush(q,(cost+1,next(counter),before,after,plan+[dict(direction=d,stand=before,after=after)]))
else:raise SystemExit('No legal push plan')
