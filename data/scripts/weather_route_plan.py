"""Read-only cross-map route proposal from exported installed map geometry."""
import json,heapq,itertools
from pathlib import Path
from route_readonly import route
R=Path(__file__).resolve().parents[1]
maps={m:json.loads((R/f'work/252-map{m}.json').read_text()) for m in (836,837)}
def solve(start,goal):
 serial=itertools.count();q=[(0,next(serial),start,[])];seen=set()
 while q:
  cost,_,node,steps=heapq.heappop(q)
  if node in seen:continue
  seen.add(node);mid,x,y=node;v=dict(maps[mid],position=[x,y])
  if mid==goal[0]:
   options=[]
   for dx,dy in [(0,1),(0,-1),(1,0),(-1,0)]:
    near=(goal[1]+dx,goal[2]+dy)
    try: options.append((len(route(v,near)),near))
    except ValueError:pass
   if options:
    length,near=min(options);return cost+length,steps+[{'map':mid,'from':[x,y],'goal':near,'orb':goal[1:],'tiles':length}]
  reach=route(v,None)
  for eid,e in v['events'].items():
   transfers=[c['parameters'][1:4] for c in e['list'] if c['code']==201 and c['parameters'][0]==0 and c['parameters'][1] in maps]
   if len(transfers)!=1:continue
   if not any((e['x']+dx,e['y']+dy) in reach for dx,dy in [(1,0),(-1,0),(0,1),(0,-1)]):continue
   near=[(reach[(e['x']+dx,e['y']+dy)],(e['x']+dx,e['y']+dy)) for dx,dy in [(1,0),(-1,0),(0,1),(0,-1)] if (e['x']+dx,e['y']+dy) in reach]
   _,ap=min(near);r=route(v,ap)
   dest=tuple(transfers[0]);step={'map':mid,'from':[x,y],'event':int(eid),'goal':[e['x'],e['y']],'tiles':len(r),'destination':list(dest)}
   if dest not in seen:heapq.heappush(q,(cost+len(r)+5,next(serial),dest,steps+[step]))
 return None
if __name__=='__main__':
 result=[]
 for start in [(836,59,95),(836,10,41),(836,176,51)]:
  for goal in [(837,25,58),(837,39,61),(837,57,58)]:
   answer=solve(start,goal)
   if answer:result.append({'start':start,'goal':goal,'solution':answer});print(result[-1],flush=True)
 (R/'work/252-weather-route-proposals.json').write_text(json.dumps(result,indent=2)+'\n')
