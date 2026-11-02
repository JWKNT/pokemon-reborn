"""Plan normal WTC trash pushes from installed tiles, without any game writes/input."""
import sys,json,subprocess,heapq,itertools
from collections import deque
from layer_route import ROOT,plan,route,effect,DIR

def solve(mid,sx,sy,ground,goals,limit=25000):
 ids=list(goals);v=json.loads(subprocess.check_output(['ruby',str(ROOT/'scripts/route_map.rb'),str(mid),str(sx),str(sy),json.dumps({'switches':{'410':True}})],stderr=subprocess.DEVNULL))
 initial=tuple((v['events'][i]['x'],v['events'][i]['y'])for i in ids)
 target=tuple(tuple(goals[i])for i in ids)
 for i in ids:v['events'].pop(i)
 graph=route(v,None,True)
 floor={}
 for p,edges in graph.items():
  for k,n in edges:
   d=DIR[k.removeprefix('jump:')][2];new=True
   for e in v['events'].values():
    if e['trigger']==1 and (e['x'],e['y'])==n:new=effect(e,d,new)
   if not new or k.startswith('jump:'):continue
   floor.setdefault(p,[]).append((k,n))
 def reach(pos,boxes):
  blocked=set(boxes);seen={pos};todo=[pos]
  for p in todo:
   for k,n in floor.get(p,[]):
    if n not in blocked and n not in seen:seen.add(n);todo.append(n)
  return seen
 if ground:start=(sx,sy)
 else:
  options=[]
  for x,y in initial:
   for dx,dy,d in DIR.values():
    p=(x-dx,y-dy)
    try:steps=plan(mid,sx,sy,ground,*p,True);options.append((len(steps),p))
    except ValueError:pass
  if not options:raise ValueError('No initial floor access')
  start=min(options)[1]
 def h(boxes):return sum(abs(x-tx)+abs(y-ty)for(x,y),(tx,ty)in zip(boxes,target))
 serial=itertools.count();q=[(h(initial),0,next(serial),start,initial,[])];seen={};expanded=0
 while q:
  _,cost,_,pos,boxes,pushes=heapq.heappop(q);r=reach(pos,boxes);key=(min(r),boxes)
  if cost>=seen.get(key,float('inf')):continue
  seen[key]=cost;expanded+=1
  if boxes==target:return {'map':mid,'initial':dict(zip(ids,initial)),'goals':goals,'pushes':pushes,'states':expanded}
  if expanded>limit:raise ValueError('Push planning bound exceeded')
  for i,(x,y)in enumerate(boxes):
   for k,(dx,dy,d)in DIR.items():
    before=(x-dx,y-dy);after=(x+dx,y+dy)
    if before not in r or after in boxes or (k,after)not in floor.get((x,y),[]):continue
    new=list(boxes);new[i]=after;new=tuple(new);c=cost+1
    action={'event':int(ids[i]),'direction':k,'box_to':list(after)}
    heapq.heappush(q,(c+h(new),c,next(serial),(x,y),new,pushes+[action]))
 raise ValueError('No normal push solution')
if __name__=='__main__':
 mid,sx,sy,g=map(int,sys.argv[1:5]);print(json.dumps(solve(mid,sx,sy,bool(g),json.loads(sys.argv[5])),indent=2))
