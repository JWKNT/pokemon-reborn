"""Read-only shortest route through unconditional, same-map touch teleporters.
Print safe_steps waypoints; never sends input or changes game/save data.
"""
from nav import route
import json,sys,subprocess,heapq
mid,sx,sy,gx,gy=map(int,sys.argv[1:6]);goal=(gx,gy)
v=json.loads(subprocess.check_output(['ruby','scripts/route_map.rb',str(mid),str(sx),str(sy)],stderr=subprocess.DEVNULL))
warps=[]
for eid,e in v['events'].items():
 c=e['list'] or [];ts=[x['parameters'] for x in c if x['code']==201]
 if e['trigger'] not in [1,2] or len(ts)!=1 or any(x['code']==111 for x in c):continue
 a=ts[0]
 if a[0]!=0 or a[1]!=mid:continue
 warps.append(((e['x'],e['y']),tuple(a[2:4]),eid))
start=(sx,sy);q=[(0,start,[])];best={start:0}
while q:
 cost,pos,steps=heapq.heappop(q)
 if cost!=best[pos]:continue
 vv=dict(v,position=list(pos))
 try:
  p=route(vv,goal)
  # A reachable final walk may not be globally shortest, but is a valid reviewed route.
  print(json.dumps(steps+[['q',f'{mid},{gx},{gy}']],indent=2));break
 except ValueError:pass
 for tile,dest,eid in warps:
  if tile==pos:continue
  try:p=route(vv,tile)
  except ValueError:continue
  if not p or p[-1].startswith('jump:'):continue
  k=p[-1];dx,dy={'left':(-1,0),'right':(1,0),'up':(0,-1),'down':(0,1)}[k]
  before=(tile[0]-dx,tile[1]-dy);nc=cost+len(p)+2
  if nc<best.get(dest,10**9):
   best[dest]=nc;heapq.heappush(q,(nc,dest,steps+[['q',f'{mid},{before[0]},{before[1]},{k},wait:2']]))
else:raise SystemExit('No safe warp route found')
