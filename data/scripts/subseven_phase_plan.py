"""Offline shortest paths for installed Subseven wall-walking puzzle.
Reads installed assets and last saved navigation only; outputs a reviewable plan.
No input, imports of input helpers, or game/save modifications.
"""
import json,subprocess,sys,heapq,re
from pathlib import Path
R=Path(__file__).resolve().parents[1]
sx,sy,tx,ty=map(int,sys.argv[1:5])
v=json.loads(subprocess.check_output(['ruby',str(R/'scripts/route_map.rb'),'871',str(sx),str(sy)],stderr=subprocess.DEVNULL))
w,h=v['width'],v['height'];data=v['data']['data'];pas=v['passages']['data'];pri=v['priorities']['data'];events=v['events']
blocked={(e['x'],e['y']) for e in events.values() if not e['through'] and e['character']}
transfers={(e['x'],e['y']) for e in events.values() if any(c['code']==201 for c in e['list'] or []) and e['trigger'] in [1,2]}
tiles={(e['x'],e['y']):e['tile_id'] for e in events.values() if not e['through'] and e['tile_id']>=0}
def ok(x,y,d):
 if not(0<=x<w and 0<=y<h):return False
 bit=1<<(d//2-1)
 ts=([tiles[x,y]] if (x,y) in tiles else [])+[data[x+w*y+w*h*z] for z in [2,1,0]]
 for t in ts:
  if pas[t]&bit or pas[t]&15==15:return False
  if pri[t]==0:return True
 return True
statues={}
for eid,e in events.items():
 cs=e['list'] or []
 # Lower interaction tile has no facing restriction or origin adjustment.
 if any(c['code']==111 and c['parameters'][:2]==[6,-1] for c in cs):continue
 if any(c['code']==122 and c['parameters'][:2]==[629,629] for c in cs) and any(c['code']==209 and c['parameters'][0]==-1 and any(z['code']==37 for z in c['parameters'][1]['list']) for c in cs):statues[eid]=(e['x'],e['y'])
doorways={}
for eid,e in events.items():
 cs=e["list"] or [];ds=[tuple(c["parameters"][1:4]) for c in cs if c["code"]==201 and c["parameters"][0]==0]
 if e["trigger"] in [1,2] and ds and len(set(ds))==1 and ds[0][0]==871 and not any(c["code"] in [102,103,104,301] or any(t in str(c["parameters"]) for t in ["pbTrainerBattle","pbDoubleTrainerBattle","pbWildBattle"]) for c in cs):doorways[eid]=(e,ds[0][1:])
hazards=set()
for e in events.values():
 match=re.search(r'Trainer\((\d+)\)',e.get('name',''))
 if not match or not any(k in str(e.get('list',[])) for k in ['pbTrainerBattle','pbDoubleTrainerBattle']):continue
 dx,dy={2:(0,1),4:(-1,0),6:(1,0),8:(0,-1)}.get(e.get('direction'),(0,0))
 for n in range(1,int(match[1])+1):hazards.add((e['x']+dx*n,e['y']+dy*n))
starts=(sx,sy,-1,-1);q=[(0,starts)];dist={starts:0};prev={};end=None
while q:
 cost,state=heapq.heappop(q)
 if cost!=dist[state]:continue
 x,y,ax,ay=state
 if (x,y)==(tx,ty):end=state;break
 opts=[]
 for k,dx,dy,d in [('up',0,-1,8),('down',0,1,2),('left',-1,0,4),('right',1,0,6)]:
  nx,ny=x+dx,y+dy
  if not(0<=nx<w and 0<=ny<h)or(nx,ny)in transfers:continue
  if ax>=0:
   na=(ax,ay) if abs(nx-ax)+abs(ny-ay)<=8 else (-1,-1)
   opts.append(((nx,ny,*na),['phase',k,nx,ny,ax,ay],1))
  elif (nx,ny)not in blocked and ok(x,y,d)and ok(nx,ny,10-d):opts.append(((nx,ny,-1,-1),['walk',k,nx,ny],1))
 for eid,(ex,ey)in statues.items():
  if abs(ex-x)+abs(ey-y)==1 and (ax,ay)!=(ex,ey):opts.append(((x,y,ex,ey),['statue',int(eid),x,y],5))
 for eid,(e,dest) in doorways.items():
  if ax>=0 or abs(e['x']-x)+abs(e['y']-y)!=1:continue
  facing=6 if e['x']>x else 4 if e['x']<x else 2 if e['y']>y else 8
  required={c['parameters'][2] for c in e['list'] if c['code']==111 and c['parameters'][:2]==[6,-1]}
  if required and facing not in required:continue
  opts.append(((*dest,-1,-1),['transfer',int(eid),*dest],4))
 for nxt,action,weight in opts:
  nc=cost+weight+(500 if nxt[:2] in hazards else 0)
  if nc<dist.get(nxt,10**9):dist[nxt]=nc;prev[nxt]=(state,action);heapq.heappush(q,(nc,nxt))
assert end,'No path under installed radius rule'
actions=[];cur=end
while cur!=starts:cur,a=prev[cur];actions.append(a)
actions.reverse();result=dict(start=[sx,sy],goal=[tx,ty],cost=dist[end],states=len(dist),actions=actions)
print(json.dumps(result,indent=2))
