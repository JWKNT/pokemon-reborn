"""Read-only transfer/route search using installed maps and frozen own progress."""
import json,subprocess,sys,heapq
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent))
from route_readonly import route
R=Path(__file__).resolve().parents[1]
cache={}
def load(mid):
 if mid not in cache:cache[mid]=json.loads(subprocess.check_output(['ruby',str(R/'scripts/route_map.rb'),str(mid),'0','0'],stderr=subprocess.DEVNULL))
 return cache[mid]
start=(404,15,13);goal=(409,19,7);q=[(0,start,[])];seen=set()
while q:
 cost,node,path=heapq.heappop(q)
 if node in seen:continue
 seen.add(node);mid,x,y=node;v=dict(load(mid));v['position']=[x,y]
 if mid==goal[0]:
  opts=[]
  for target in [(15,26)]:
   try:steps=route(v,target);opts.append((len(steps),target,steps))
   except ValueError:pass
  if opts:
   n,target,steps=min(opts);print(json.dumps({'cost':cost+n,'path':path,'last':[mid,*target],'last_steps':steps},indent=2));break
 for eid,e in v['events'].items():
  for c in e['list'] or []:
   if c['code']!=201 or c['parameters'][0]!=0:continue
   dst=tuple(c['parameters'][1:4])
   if dst[0] not in range(404,412) or dst in seen:continue
   opts=[]
   for dx,dy,d in [(0,1,'up'),(0,-1,'down'),(1,0,'left'),(-1,0,'right')]:
    try:steps=route(v,(e['x']+dx,e['y']+dy));opts.append((len(steps),[e['x']+dx,e['y']+dy],d))
    except ValueError:pass
   if opts:
    n,p,d=min(opts);heapq.heappush(q,(cost+n+1,dst,path+[{'map':mid,'event':int(eid),'approach':p,'direction':d,'destination':dst}]))
else:print('VISITED',sorted(seen));raise SystemExit('No route')
