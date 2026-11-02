"""Approach reviewed Victory Road events through ordinary two-step Rock Climbs."""
from nav import *
from locate import locate
import copy
mid,eid=int(sys.argv[1]),int(sys.argv[2]);kind=sys.argv[3]if len(sys.argv)>3 else'talk'
assert mid==790
allowed=set(range(16,28))|{43}
dirs=[('up',0,-1),('down',0,1),('left',-1,0),('right',1,0)]
def plan(v):
 target=v['events'][str(eid)];graph=route(v,None,True)
 goals=[(target['x']+dx,target['y']+dy)for _,dx,dy in dirs]
 cliffs=[]
 for k in allowed:
  e=v['events'].get(str(k))
  if not e or 'Kernel.pbRockClimb'not in str(e['list']):continue
  rr=[c['parameters'][1]['list']for c in e['list']if c['code']==209 and c['parameters'][0]==-1]
  assert len(rr)==1 and not any(c['code']in range(1,12)for c in rr[0]),k
  count=[c['code']for c in rr[0]].count(12);assert count in [2,3]
  for direction,dx,dy in dirs:
   a=(e['x']-dx,e['y']-dy);b=(e['x']+(count-1)*dx,e['y']+(count-1)*dy)
   if graph.get(a)and graph.get(b):cliffs.append((k,a,b,direction))
 todo=[(0,tuple(v['position']),[])];seen=set()
 while todo:
  cost,pos,steps=heapq.heappop(todo)
  if pos in seen:continue
  seen.add(pos);vv=dict(v,position=list(pos))
  for goal in goals:
   try:route(vv,goal);return steps
   except ValueError:pass
  for k,a,b,direction in cliffs:
   if b in seen:continue
   try:path=route(vv,a)
   except ValueError:continue
   heapq.heappush(todo,(cost+len(path)+10,b,steps+[(k,a,b,direction)]))
 raise SystemExit('No route even through reviewed NW cliffs')
for attempt in range(7):
 m,x,y=locate(mid);assert m==mid
 v=json.loads(subprocess.check_output(['ruby',str(ROOT/'scripts/route_map.rb'),str(mid),str(x),str(y)],stderr=subprocess.DEVNULL));steps=plan(v)
 if not steps:
  if kind=='approach':
   target=v['events'][str(eid)];options=[]
   for _,dx,dy in dirs:
    dest=(target['x']+dx,target['y']+dy)
    try:options.append((len(route(v,dest)),dest))
    except ValueError:pass
   _,dest=min(options)
   subprocess.run([sys.executable,str(ROOT/'scripts/q.py'),f'{mid},{dest[0]},{dest[1]}'],check=True)
  else:subprocess.run([sys.executable,str(ROOT/'scripts/eventq.py'),str(mid),str(eid),kind],check=True)
  break
 k,a,b,direction=steps[0];print('NORMAL CLIFF',k,a,b,direction,flush=True)
 p=ROOT/'work/nw-cliff-route.json';p.write_text(json.dumps([[mid,x,y,*a,[]]]))
 subprocess.run([sys.executable,str(ROOT/'scripts/queue_route.py'),str(p),'--from-verified'],check=True)
 act(direction+':.18','c','wait:1')
 subprocess.run([sys.executable,str(ROOT/'scripts/dialog.py'),'--yes','--limit=10'],check=True)
 actual=locate(mid);assert actual==(mid,*b),('Climb landing differs',actual,b)
else:raise SystemExit('Cliff route exceeded six transitions')
