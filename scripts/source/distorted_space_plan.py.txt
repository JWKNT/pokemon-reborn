"""Offline Dijkstra model of installed Malamar flips and radius-eight statues.
Reads only installed assets and frozen navigation; never controls or modifies game.
"""
import json,subprocess,sys,heapq,ast,re
from pathlib import Path
R=Path(__file__).resolve().parents[1];ROOT=R
fn=next(n for n in ast.parse((R/'scripts/nav.py').read_text()).body if isinstance(n,ast.FunctionDef)and n.name=='route')
exec(compile(ast.Module(body=[fn],type_ignores=[]),'pure-route','exec'))
mid,sx,sy,tx,ty=map(int,sys.argv[1:6]);lo,hi=map(int,sys.argv[6:8])
maps={i:json.loads(subprocess.check_output(['ruby',str(R/'scripts/route_map.rb'),str(i),str(sx),str(sy)],stderr=subprocess.DEVNULL))for i in [890,891]}
models={};graphs={m:route(v,None,True)for m,v in maps.items()}
for m,v in maps.items():
 w,h=v['width'],v['height'];events=v['events'];data=v['data']['data'];pas=v['passages']['data'];pri=v['priorities']['data']
 blocked={(e['x'],e['y'])for e in events.values()if not e['through']and e['character']}
 transfers={(e['x'],e['y'])for e in events.values()if any(c['code']==201 for c in e['list']or[])and e['trigger']in[1,2]}
 tiles={(e['x'],e['y']):e['tile_id']for e in events.values()if not e['through']and e['tile_id']>=0}
 allowed={}
 for y in range(lo,hi+1):
  for x in range(w):
   for d in [2,4,6,8]:
    bit=1<<(d//2-1);good=True
    ts=([tiles[x,y]]if(x,y)in tiles else[])+[data[x+w*y+w*h*z]for z in[2,1,0]]
    for t in ts:
     if pas[t]&bit or pas[t]&15==15:good=False;break
     if pri[t]==0:break
    allowed[x,y,d]=good
 statues={};mal={}
 for eid,e in events.items():
  cs=e['list']or[]
  if any(c['code']==117 and c['parameters']==[78]for c in cs):mal[int(eid)]=(e['x'],e['y'])
  # Upper interaction tiles activate only when faced upward from below.
  if any(c['code']==122 and c['parameters'][:2]==[629,629]for c in cs)and any(c['code']==209 and c['parameters'][0]==-1 and any(z['code']==37 for z in c['parameters'][1]['list'])for c in cs):statues[int(eid)]=(e['x'],e['y'],any(c['code']==111 and c['parameters'][:2]==[6,-1]for c in cs))
 models[m]=(allowed,blocked,transfers,statues,mal)
start=(mid,sx,sy,-1,-1);q=[(0,start)];dist={start:0};prev={};end=None
while q:
 cost,state=heapq.heappop(q)
 if cost!=dist[state]:continue
 m,x,y,ax,ay=state
 if(x,y)==(tx,ty):end=state;break
 allowed,blocked,transfers,statues,mal=models[m];opts=[]
 for k,dx,dy,d in [('up',0,-1,8),('down',0,1,2),('left',-1,0,4),('right',1,0,6)]:
  nx,ny=x+dx,y+dy
  if not(0<=nx<w and lo<=ny<=hi)or(nx,ny)in transfers:continue
  if ax>=0:
   na=(ax,ay)if abs(nx-ax)+abs(ny-ay)<=8 else(-1,-1)
   opts.append(((m,nx,ny,*na),['phase',m,k,nx,ny,ax,ay],1))
 if ax<0:
  for k,(nx,ny)in graphs[m].get((x,y),[]):
   if lo<=ny<=hi and(nx,ny)not in transfers:opts.append(((m,nx,ny,-1,-1),['walk',m,k,nx,ny],1))
 for eid,(ex,ey,upper)in statues.items():
  if abs(ex-x)+abs(ey-y)==1 and(ax,ay)!=(ex,ey)and(not upper or(x,y)==(ex,ey+1))and(ax<0 or abs(2*x-ex-ax)+abs(2*y-ey-ay)<=8):opts.append(((m,x,y,ex,ey),['statue',m,eid,x,y,ex,ey],6))
 for eid,(ex,ey)in mal.items():
  if abs(ex-x)+abs(ey-y)==1 and(ax<0 or abs(2*x-ex-ax)+abs(2*y-ey-ay)<=8):opts.append(((1781-m,x,y,ax,ay),['malamar',m,eid,x,y,ax,ay],10))
 for nxt,action,weight in opts:
  nc=cost+weight
  if nc<dist.get(nxt,10**9):dist[nxt]=nc;prev[nxt]=(state,action);heapq.heappush(q,(nc,nxt))
assert end,('No route found',len(dist),sorted(set((m,x,y)for m,x,y,ax,ay in dist if abs(x-tx)+abs(y-ty)<8)))
actions=[];cur=end
while cur!=start:cur,a=prev[cur];actions.append(a)
actions.reverse();print(json.dumps(dict(start=start,end=end,cost=dist[end],states=len(dist),actions=actions),indent=2))
