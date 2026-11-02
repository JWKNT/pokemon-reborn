from play import *
from collections import deque
import heapq
from itertools import groupby
from PIL import Image

def loadmap():
 raw=subprocess.check_output(['ruby',str(ROOT/'scripts/map_state.rb')],stderr=subprocess.DEVNULL);(ROOT/'notes/map-state.json').write_bytes(raw);return json.loads(raw)
def save():
 act('d','wait:0.4','c','wait:0.8','c','wait:0.3')
def route(v,goal):
 w,h=v['width'],v['height'];data=v['data']['data'];pas=v['passages']['data'];pri=v['priorities']['data']
 blocked={(e['x'],e['y']) for e in v['events'].values() if not e['through'] and e['character']}
 tile_events={(e['x'],e['y']):e['tile_id'] for e in v['events'].values() if not e['through'] and e['tile_id']>0}
 statefile=ROOT/'notes/navigation-state.json'
 if statefile.exists():blocked.update(map(tuple,json.loads(statefile.read_text()).get('avoid',{}).get(str(v['map']),[])))
 def ok(x,y,d):
  if x<0 or y<0 or x>=w or y>=h:return False
  bit=1<<(d//2-1)
  if (x,y) in tile_events:
   t=tile_events[(x,y)]
   if pas[t]&bit or pas[t]&15==15:return False
   if pri[t]==0:return True
  for z in [2,1,0]:
   t=data[x+w*y+w*h*z]
   if pas[t]&bit or pas[t]&15==15:return False
   if pri[t]==0:return True
  return True
 jumps={}
 for e in v['events'].values():
  cmds=e['list'] or []
  if not any(c['code']==250 and any(isinstance(a,dict) and a.get('name')=='jump' for a in c['parameters']) for c in cmds):continue
  direction=None
  for c in cmds:
   a=c['parameters']
   if c['code']==111 and len(a)>=3 and a[:2]==[6,-1]:direction=a[2]
   if c['code']==509 and direction and a[0].get('code')==14:
    dx,dy={2:(0,1),4:(-1,0),6:(1,0),8:(0,-1)}[direction]
    p=(e['x']-dx,e['y']-dy);jx,jy=a[0]['parameters'];jumps[(p,direction)]=(p[0]+jx,p[1]+jy)
 statefile=ROOT/'notes/navigation-state.json'
 if statefile.exists():
  for sx,sy,k,tx,ty in json.loads(statefile.read_text()).get('edges',{}).get(str(v['map']),[]):
   jumps[((sx,sy),{'down':2,'left':4,'right':6,'up':8}[k])]=(tx,ty)
 def cost(n):
  if 'terrain' not in v:return 1
  tags=v['terrain']['data']
  for z in [2,1,0]:
   tag=tags[data[n[0]+w*n[1]+w*h*z]]
   if tag and tag!=13:return 8 if tag in [2,10,11,14] else 1
  return 1
 start=tuple(v['position']);q=[(0,start)];dist={start:0};prev={start:None};dirs=[(0,1,2,'down'),(-1,0,4,'left'),(1,0,6,'right'),(0,-1,8,'up')]
 while q:
  distance,p=heapq.heappop(q)
  if distance!=dist[p]:continue
  if p==goal:break
  for dx,dy,d,k in dirs:
   n=(p[0]+dx,p[1]+dy)
   if (p,d) in jumps:
    n=jumps[(p,d)]
    nd=distance+cost(n)
    if n not in blocked and nd<dist.get(n,float('inf')):
     prev[n]=(p,'jump:'+k);dist[n]=nd;heapq.heappush(q,(nd,n))
    continue
   if n in blocked or not ok(*p,d) or not ok(*n,10-d):continue
   nd=distance+cost(n)
   if nd<dist.get(n,float('inf')):
    prev[n]=(p,k);dist[n]=nd;heapq.heappush(q,(nd,n))
 if goal is None:return dist
 if goal not in prev:raise ValueError('No path')
 out=[];p=goal
 while prev[p]:p,k=prev[p];out.append(k)
 return out[::-1]
if __name__=='__main__':
 v=loadmap();
 if '--from' in sys.argv:
  j=sys.argv.index('--from');v['position']=list(map(int,sys.argv[j+1:j+3]))
 goal=tuple(map(int,sys.argv[1:3]));path=route(v,goal);print('MAP',v['map'],v['position'],'to',goal,'PATH',path,flush=True)
 if '--go' in sys.argv:
  for key,g in groupby(path):
   n=len(list(g))
   if key.startswith('jump:'):
    for _ in range(n):act(key[5:],'wait:0.9')
   else:act(f'{key}:{n*.1+.02:.3f}')
   rr=snap();txt='\n'.join(a['text'] for a in rr)
   im=Image.open(STATE).convert('RGB');w,h=im.size
   crop=im.crop((int(w*.10),int(h*.74),int(w*.47),int(h*.87)))
   white=sum(1 for r,g,b in crop.getdata() if min(r,g,b)>225)/(crop.width*crop.height)
   if ('hp' in txt.lower() or 'wild ' in txt.lower() or 'fight' in txt.lower() or (white>.35 and any(a['y']>.73 for a in rr))):print('INTERRUPTED',txt,flush=True);sys.exit(2)
  print(read(),flush=True)
