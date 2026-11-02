"""Read-only mountain path model: walking, surfing, landing, and ice slides."""
from nav import *
import copy
WATER={5,6,7,9}
def tag(v,p):
 w,h=v['width'],v['height'];x,y=p
 if not (0<=x<w and 0<=y<h):return -1
 return next((v['terrain']['data'][v['data']['data'][x+w*y+w*h*z]] for z in [2,1,0] if v['terrain']['data'][v['data']['data'][x+w*y+w*h*z]] not in [0,13]),0)
def surface_plan(v,goal):
 g0=route(v,None,True);sv=copy.deepcopy(v)
 for i,t in enumerate(v['terrain']['data']):
  if t in WATER:sv['passages']['data'][i]=0;sv['priorities']['data'][i]=0
 g1=route(sv,None,True);graphs={False:g0,True:g1}
 # route(..., return_graph=True) returns unweighted adjacency, so carry the
 # ordinary planner's trainer sight-line penalty into this surface search.
 hazards=set()
 for e in v['events'].values():
  match=re.search(r'Trainer\((\d+)\)',e.get('name',''))
  if not match or not any(k in str(e.get('list',[])) for k in ['pbTrainerBattle','pbDoubleTrainerBattle']):continue
  direction=e.get('direction',0)
  if direction not in [2,4,6,8]:continue
  dx,dy={2:(0,1),4:(-1,0),6:(1,0),8:(0,-1)}[direction]
  hazards.update((e['x']+dx*i,e['y']+dy*i) for i in range(1,int(match[1])+1))
 start=(*v['position'],tag(v,tuple(v['position'])) in WATER)
 q=[(0,start)];dist={start:0};prev={start:None};end=None
 while q:
  cost,p=heapq.heappop(q)
  if cost!=dist[p]:continue
  if p[:2]==goal:end=p;break
  pos=p[:2];surf=p[2]
  choices=list(graphs[surf].get(pos,[]))
  if not surf:
   choices.extend((k,n) for k,n in g1.get(pos,[]) if tag(v,n) in WATER and tag(v,pos) not in WATER)
  for key,n in choices:
   # Ground touch-jump events can skip their forced movement while Surfing.
   # Do not treat those event jumps as traversable water edges (Fiore679).
   if surf and key.startswith('jump:'):continue
   mode=tag(v,n) in WATER;extra=1
   if not surf and mode:key='surf:'+key;extra=8
   elif surf and not mode:
    # A walking graph can hop a ledge over two tiles. A Surf exit must
    # reach the adjacent shore; that artificial jump cannot disembark.
    if abs(n[0]-pos[0])+abs(n[1]-pos[1])!=1:continue
    key='land:'+key
   elif not mode and tag(v,n)==12 and not key.startswith('jump:'):
    direction=key;walkgraph=g0
    while tag(v,n)==12:
     farther=next((nn for kk,nn in walkgraph.get(n,[]) if kk==direction),None)
     if farther is None:break
     n=farther;extra+=1
    key='slide:'+direction
   np=(*n,mode);nc=cost+extra+(500 if n in hazards else 0)
   if nc<dist.get(np,float('inf')):
    dist[np]=nc;prev[np]=(p,key);heapq.heappush(q,(nc,np))
 if end is None:raise ValueError('No mountain surface route')
 steps=[]
 while prev[end]:
  old,k=prev[end];steps.append({'from':old,'to':end,'key':k});end=old
 return steps[::-1]
if __name__=='__main__':
 mid,sx,sy,tx,ty=map(int,sys.argv[1:6])
 v=json.loads(subprocess.check_output(['ruby',str(ROOT/'scripts/route_map.rb'),str(mid),str(sx),str(sy)],stderr=subprocess.DEVNULL))
 r=surface_plan(v,(tx,ty));print(json.dumps(r,indent=2))
