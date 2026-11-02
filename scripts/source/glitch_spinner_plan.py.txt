"""Read-only routing for Rocket Hideout's installed forced-movement arrows."""
from nav import *
MOVE={1:(0,1),2:(-1,0),3:(1,0),4:(0,-1)}
def spinner_plan(v,goal):
 arrows={}
 for e in v['events'].values():
  cs=e.get('list')or[]
  routes=[c['parameters'][1]['list']for c in cs if c['code']==209 and c['parameters'][0]==-1]
  if e['trigger']!=1 or len(routes)!=1:continue
  codes=[m['code']for m in routes[0]]
  if not all(c in [0,1,2,3,4,31,32]for c in codes):continue
  moves=[MOVE[c]for c in codes if c in MOVE]
  if moves:arrows[(e['x'],e['y'])]=moves
 def follow(pos):
  seen=set();count=0
  while pos in arrows:
   if pos in seen:raise ValueError('Spinner cycle')
   seen.add(pos)
   for dx,dy in arrows[pos]:pos=(pos[0]+dx,pos[1]+dy);count+=1
  return pos,count
 g=route(v,None,True);start=tuple(v['position']);q=[(0,start)];dist={start:0};prev={start:None}
 while q:
  cost,p=heapq.heappop(q)
  if cost!=dist[p]:continue
  if p==goal:break
  for key,n in g.get(p,[]):
   try:end,hops=follow(n)
   except ValueError:continue
   if end not in g and end!=goal:continue
   nc=cost+1+hops*.2
   if nc<dist.get(end,float('inf')):
    dist[end]=nc;prev[end]=(p,'spin:'+key if hops else key,hops);heapq.heappush(q,(nc,end))
 if goal not in prev:raise ValueError('No spinner route')
 result=[];p=goal
 while prev[p]:
  old,k,hops=prev[p];result.append({'from':old,'to':p,'key':k,'forced_tiles':hops});p=old
 return result[::-1]
if __name__=='__main__':
 mid,sx,sy,tx,ty=map(int,sys.argv[1:]);assert mid==448
 v=json.loads(subprocess.check_output(['ruby',str(ROOT/'scripts/route_map.rb'),str(mid),str(sx),str(sy)],stderr=subprocess.DEVNULL))
 print(json.dumps(spinner_plan(v,(tx,ty)),indent=2))
