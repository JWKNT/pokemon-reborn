from play import *
from collections import deque
import heapq,re
from itertools import groupby
from PIL import Image

def action_jump(v,p,key):
 """Action-button trash jumps differ from automatic stairs and ledges."""
 if not key.startswith('jump:'):return False
 dx,dy={'up':(0,-1),'down':(0,1),'left':(-1,0),'right':(1,0)}[key[5:]]
 return any(e['trigger']==0 and (e['x'],e['y'])==(p[0]+dx,p[1]+dy)
  and any(c['code']==250 and any(isinstance(a,dict) and a.get('name')=='jump' for a in c['parameters']) for c in e.get('list',[]))
  for e in v['events'].values())

def loadmap():
 raw=subprocess.check_output(['ruby',str(ROOT/'scripts/map_state.rb')],stderr=subprocess.DEVNULL);(ROOT/'notes/map-state.json').write_bytes(raw);return json.loads(raw)
def save():
 act('d','wait:0.4','c','wait:0.8','c','wait:0.3')
def route(v,goal,return_graph=False):
 w,h=v['width'],v['height'];data=v['data']['data'];pas=v['passages']['data'];pri=v['priorities']['data']
 # Ametrine's cracked lava marker is a landing for ThroughOn touch jumps.
 # Verified normal UI map870: (136,36) right -> (138,36), event146.
 blocked={(e['x'],e['y']) for e in v['events'].values() if not e['through'] and e['character']
  and not (v['map'] in [870,872] and e['character']=='cracks1' and e['name'].startswith('Lavajump')
   and all(c['code']==0 for c in e.get('list') or []))}
 # Electrical panel pages change with the radio. Generic walking must never
 # cross a currently live tile; the Devon helper chooses a safe radio state.
 blocked.update((e['x'],e['y']) for e in v['events'].values()
  if any('pbFieldDamage' in str(c.get('parameters',[])) for c in (e.get('list') or [])))
 blocked.update((e['x'],e['y']) for e in v['events'].values() if any(c['code']==201 for c in (e['list'] or [])) and (e['x'],e['y'])!=goal and (e['x'],e['y'])!=tuple(v['position']))
 tile_events={(e['x'],e['y']):e['tile_id'] for e in v['events'].values() if not e['through'] and e['tile_id']>=0}
 statefile=ROOT/'notes/navigation-state.json'
 if statefile.exists():
  saved_plan=json.loads(statefile.read_text())
  blocked.update(map(tuple,saved_plan.get('avoid',{}).get(str(v['map']),[])))
  if v['map']==732:
   # Glass ladders leave companions behind. A route carrying a companion must
   # use the normal lift instead; walking the same coordinates is insufficient.
   following=[name for name,sw in [('Glaceon','946'),('Espeon','947')]
    if saved_plan.get('switches',{}).get(sw)]
   blocked.update((e['x'],e['y']) for e in v['events'].values()
    if e['trigger']==1 and any('pbRemoveDependency2("'+name+'")' in str(e.get('list',[])) for name in following))
 def ok(x,y,d):
  if x<0 or y<0 or x>=w or y>=h:return False
  bit=1<<(d//2-1) if d else 0
  if (x,y) in tile_events:
   t=tile_events[(x,y)]
   if pas[t]&bit or pas[t]&15==15:return False
   if pri[t]==0:return True
  for z in [2,1,0]:
   t=data[x+w*y+w*h*z]
   if pas[t]&bit or pas[t]&15==15:return False
   if pri[t]==0:return True
  return True
 jumps={};touch_stairs={}
 for e in v['events'].values():
  cmds=e['list'] or []
  if e['name']=='platjump':
   # These jumps require raised platforms. Evaluate only the installed
   # switch branches against our last ordinary saved navigation snapshot.
   switches=saved_plan.get('switches',{}) if statefile.exists() else {}
   branches={};enabled=[]
   for command in cmds:
    depth=command['indent'];code=command['code'];args=command['parameters']
    if code==411 and depth in branches:
     branches[depth]=not branches[depth];continue
    if code==412:
     branches.pop(depth,None);continue
    if code==111 and args[0]==0:
     branches[depth]=switches.get(str(args[1]),False)==(args[2]==0)
     continue
    if all(branches.values()):enabled.append(command)
   cmds=enabled
  if not any(c['code']==250 and any(isinstance(a,dict) and a.get('name')=='jump' for a in c['parameters']) for c in cmds):continue
  direction=None;totals={}
  for c in cmds:
   a=c['parameters']
   if c['code']==111 and len(a)>=3 and a[:2]==[6,-1]:direction=a[2]
   if c['code']==509 and direction and a[0].get('code')==14:
    dx,dy={2:(0,1),4:(-1,0),6:(1,0),8:(0,-1)}[direction]
    p=(e['x']-dx,e['y']-dy);jx,jy=a[0]['parameters'];old=totals.get(direction,(0,0));totals[direction]=(old[0]+jx,old[1]+jy)
    jumps[(p,direction)]=(p[0]+totals[direction][0],p[1]+totals[direction][1])
 # Idyll springy grass launches one fixed, installed jump after stepping on it.
 # Restrict this to the reviewed map and its transparent touch pads.
 if v['map']in [878,879]:
  for e in v['events'].values():
   cs=e['list'] or []
   if e['trigger']!=1 or not e['through'] or e['character']!={878:'springy_grass2',879:'springy_grass'}[v['map']]:continue
   if not any(c['code']==250 and 'PRSFX- Bounce' in str(c['parameters']) for c in cs):continue
   routes=[c['parameters'][1]['list'] for c in cs if c['code']==209 and c['parameters'][0]==-1]
   if len(routes)!=1 or any(c['code'] not in [0,14,24] for c in routes[0]):continue
   offsets=[c['parameters'] for c in routes[0] if c['code']==14]
   if len(offsets)!=1:continue
   jx,jy=offsets[0]
   for d,(dx,dy) in {2:(0,1),4:(-1,0),6:(1,0),8:(0,-1)}.items():
    before=(e['x']-dx,e['y']-dy)
    if ok(*before,d) and ok(e['x'],e['y'],10-d):
     jumps[(before,d)]=(e['x']+jx,e['y']+jy)
 # Diagonal stairs can trigger after entering a passable tile or when bumping
 # an impassable one. Preserve that distinction before the forced movement.
 for e in v['events'].values():
  if e['trigger']!=1:continue
  # A wrecked train enters and exits at the same side; its two move routes
  # are not a traversable stair. Treat the interaction tile as an obstacle.
  if v['map']==663 and any('engine seems to be wrecked' in str(c.get('parameters',[])).lower() for c in e.get('list') or []):
   blocked.add((e['x'],e['y']));continue
  # Helix's central ramp is created only after both gem grids are solved.
  if v['map']==887 and any(e is v['events'].get(str(i)) for i in [171,172,197,198]) and not saved_plan.get('switches',{}).get('1827',False):continue
  # The Victory Road forest underpasses hide the player during a straight
  # forced walk. Their active touch pages have no facing condition.
  if any(e is v['events'].get(str(i)) for i in ({849:range(58,70),850:range(87,105)}.get(v['map'],[]))):
   routes=[c['parameters'][1]['list'] for c in e['list'] or []
    if c['code']==209 and c['parameters'][0]==-1]
   if len(routes)==1 and all(m['code'] in [0,1,2,3,4,37,38,42] for m in routes[0]):
    moves=routes[0]
    if {37,38,42}.issubset({m['code'] for m in moves}):
     mx=sum({2:-1,3:1}.get(m['code'],0) for m in moves)
     my=sum({1:1,4:-1}.get(m['code'],0) for m in moves)
     for direction,(dx,dy) in {2:(0,1),4:(-1,0),6:(1,0),8:(0,-1)}.items():
      before=(e['x']-dx,e['y']-dy)
      enters=ok(*before,direction) and ok(e['x'],e['y'],10-direction)
      origin=(e['x'],e['y']) if enters else before
      jumps[(before,direction)]=(origin[0]+mx,origin[1]+my)
  # Glass rails use ThroughOn, MoveForward twice, ThroughOff without a
  # facing condition. This is normal player-touch movement, verified live
  # at map732 (70,44) -> (70,46). Only the currently active event page applies.
  forward_routes=[c['parameters'][1]['list'] for c in e['list'] or []
   if c['code']==209 and c['parameters'][0]==-1
   and [m['code'] for m in c['parameters'][1]['list']]==[37,12,12,38,0]]
  if v['map'] in [732,735] and forward_routes:
   for direction,(dx,dy) in {2:(0,1),4:(-1,0),6:(1,0),8:(0,-1)}.items():
    before=(e['x']-dx,e['y']-dy)
    enters=ok(*before,direction) and ok(e['x'],e['y'],10-direction)
    origin=(e['x'],e['y']) if enters else before
    jumps[(before,direction)]=(origin[0]+2*dx,origin[1]+2*dy)
  # Citae Prisma's eight bridge-edge events carry the player three tiles
  # forward, vertically below the bridge or horizontally onto the wing.
  # The installed routes are identical and have no facing restriction.
  if v['map']==896 and any(e is v['events'].get(str(i)) for i in range(23,31)):
   bridge_routes=[c['parameters'][1]['list'] for c in e['list'] or []
    if c['code']==209 and c['parameters'][0]==-1]
   if len(bridge_routes)==1 and [c['code'] for c in bridge_routes[0]]==[37,12,12,12,38,0]:
    for direction,(dx,dy) in {2:(0,1),4:(-1,0),6:(1,0),8:(0,-1)}.items():
     before=(e['x']-dx,e['y']-dy)
     enters=ok(*before,direction) and ok(e['x'],e['y'],10-direction)
     origin=(e['x'],e['y']) if enters else before
     jumps[(before,direction)]=(origin[0]+3*dx,origin[1]+3*dy)
  # Aegir Depths has normal horizontal touch passages behind waterfalls.
  # Installed events 860 use ThroughOn, six MoveForward steps, ThroughOff
  # with opacity changes. Model only the intended horizontal crossings.
  if v['map']==860 or (v['map']==511 and any(e is v['events'].get(str(i)) for i in range(37,41))):
   forward_count=3 if v['map']==511 else 6
   for command in e['list'] or []:
    if command['code']!=209 or command['parameters'][0]!=-1:continue
    moves=command['parameters'][1]['list'];codes=[m['code'] for m in moves]
    if codes.count(12)!=forward_count or 37 not in codes or 38 not in codes:continue
    if any(code not in [0,12,37,38,42] for code in codes):continue
    for direction,dx in [(4,-1),(6,1)]:
     before=(e['x']-dx,e['y'])
     enters=ok(*before,direction) and ok(e['x'],e['y'],10-direction)
     origin=(e['x'],e['y']) if enters else before
     jumps[(before,direction)]=(origin[0]+forward_count*dx,origin[1])
  # Byxbysion slides run an unconditional diagonal ThroughOn/Off route.
  # Unlike facing-gated stairs, these player-touch events have no code111.
  if v['map']==209 and not any(c['code']==111 for c in e['list'] or []):
   slide_routes=[c['parameters'][1]['list'] for c in e['list'] or [] if c['code']==209 and c['parameters'][0]==-1]
   if len(slide_routes)==1:
    moves=slide_routes[0];codes=[m['code'] for m in moves]
    if 37 in codes and 38 in codes and any(c in [5,6,7,8] for c in codes) and all(c in [0,5,6,7,8,29,31,32,37,38,44] for c in codes):
     mx=sum({5:-1,6:1,7:-1,8:1}.get(m['code'],0) for m in moves)
     my=sum({5:1,6:1,7:-1,8:-1}.get(m['code'],0) for m in moves)
     for direction,(dx,dy) in {2:(0,1),4:(-1,0),6:(1,0),8:(0,-1)}.items():
      before=(e['x']-dx,e['y']-dy)
      enters=ok(*before,direction) and ok(e['x'],e['y'],10-direction)
      origin=(e['x'],e['y']) if enters else before
      jumps[(before,direction)]=(origin[0]+mx,origin[1]+my)
  # Anna's Asylum has unconditional chain slides and short ladder passages.
  # Model the installed single player route, including its cardinal steps;
  # turn/speed/direction-lock commands do not change the destination.
  if v['map']==898 and not any(c['code']==111 for c in e['list'] or []):
   routes=[c['parameters'][1]['list'] for c in e['list'] or [] if c['code']==209 and c['parameters'][0]==-1]
   if len(routes)==1:
    moves=routes[0];codes=[m['code'] for m in moves]
    if 37 in codes and 38 in codes and all(c in [0,1,2,3,4,5,6,7,8,17,18,19,20,29,31,32,35,36,37,38] for c in codes):
     mx=sum({2:-1,3:1,5:-1,6:1,7:-1,8:1}.get(m['code'],0) for m in moves)
     my=sum({1:1,4:-1,5:1,6:1,7:-1,8:-1}.get(m['code'],0) for m in moves)
     for direction,(dx,dy) in {2:(0,1),4:(-1,0),6:(1,0),8:(0,-1)}.items():
      before=(e['x']-dx,e['y']-dy)
      enters=ok(*before,direction) and ok(e['x'],e['y'],10-direction)
      origin=(e['x'],e['y']) if enters else before
      jumps[(before,direction)]=(origin[0]+mx,origin[1]+my)
  diagonal=any(c['code']==209 and c['parameters'][0]==-1 and any(m['code'] in [5,6,7,8] for m in c['parameters'][1]['list']) for c in e['list'] or [])
  forced_ledge=any(c['code']==209 and c['parameters'][0]==-1 and
   any(m['code']==37 for m in c['parameters'][1]['list']) and
   any(m['code']==38 for m in c['parameters'][1]['list']) and
   any(m['code'] in [1,2,3,4] for m in c['parameters'][1]['list'])
   for c in e['list'] or [])
  if e['name']!='Stair' and not diagonal and not forced_ledge:continue
  direction=None
  for c in e['list'] or []:
   a=c['parameters']
   if c['code']==111 and len(a)>=3 and a[:2]==[6,-1]:direction=a[2]
   if c['code']==209 and direction and a[0]==-1:
    dx,dy={2:(0,1),4:(-1,0),6:(1,0),8:(0,-1)}[direction]
    before=(e['x']-dx,e['y']-dy)
    enters=ok(*before,direction) and ok(e['x'],e['y'],10-direction)
    tx,ty=(e['x'],e['y']) if enters else before
    for move in a[1]['list']:
     mx,my={1:(0,1),2:(-1,0),3:(1,0),4:(0,-1),5:(-1,1),6:(1,1),7:(-1,-1),8:(1,-1)}.get(move['code'],(0,0))
     tx+=mx;ty+=my
    # A later ThroughOff-only route must not erase the actual stair movement.
    if any(move['code'] in range(1,9) for move in a[1]['list']):
     jumps[((e['x']-dx,e['y']-dy),direction)]=(tx,ty)
     if not e['character'] and ok(e['x'],e['y'],0):
      ox,oy=(e['x'],e['y']) if enters else before
      touch_stairs[((e['x'],e['y']),direction)]=(e['x']+tx-ox,e['y']+ty-oy)
 # A forced diagonal landing can immediately activate the next touch stair.
 # Victory Road's descending sequence was observed from (36,14) to (31,18).
 # Keep the entire automatic chain in one edge, with a cycle guard.
 for edge,landing in list(jumps.items()):
  seen=set();direction=edge[1]
  while (landing,direction) in touch_stairs and landing not in seen:
   seen.add(landing);landing=touch_stairs[(landing,direction)]
  jumps[edge]=landing
 # Toybox pads launch an automatic chain across the intermediate pink balls.
 # Model the whole chain, not a walkable landing in empty space. Installed
 # endpoint pairs and the first (36,81)->(36,67) chain were reviewed in310.
 if v['map']==874:
  jumps={}
  for a,b in [(13,14),(15,16),(17,18),(19,20),(21,23),(22,32),(24,25),(27,26)]:
   ea,eb=v['events'][str(a)],v['events'][str(b)]
   assert ea['trigger']==eb['trigger']==1
   ax,ay,bx,by=ea['x'],ea['y'],eb['x'],eb['y']
   assert (ax==bx)!=(ay==by)
   dx=(bx>ax)-(bx<ax);dy=(by>ay)-(by<ay)
   d={(0,1):2,(-1,0):4,(1,0):6,(0,-1):8}[(dx,dy)]
   jumps[((ax-dx,ay-dy),d)]=(bx+dx,by+dy)
   jumps[((bx+dx,by+dy),10-d)]=(ax-dx,ay-dy)
 statefile=ROOT/'notes/navigation-state.json'
 if statefile.exists():
  for sx,sy,k,tx,ty in json.loads(statefile.read_text()).get('edges',{}).get(str(v['map']),[]):
   jumps[((sx,sy),{'down':2,'left':4,'right':6,'up':8}[k])]=(tx,ty)
 mounted=v.get('mounted',statefile.exists() and json.loads(statefile.read_text()).get('switches',{}).get('291',False))
 def terrain(n):
  if 'terrain' not in v or not (0<=n[0]<w and 0<=n[1]<h):return 0
  tags=v['terrain']['data']
  for z in [2,1,0]:
   tag=tags[data[n[0]+w*n[1]+w*h*z]]
   if tag and tag!=13:return tag
  return 0
 def landing_ok(n):
  if n in blocked or not (0<=n[0]<w and 0<=n[1]<h):return False
  if n in tile_events:
   t=tile_events[n]
   if pas[t]&15==15:return False
   if pri[t]==0:return True
  for z in [2,1,0]:
   t=data[n[0]+w*n[1]+w*h*z]
   if pas[t]&15==15:return False
   if pri[t]==0:return True
  return True
 hazards=set()
 for e in v['events'].values():
  match=re.search(r'Trainer\((\d+)\)',e.get('name',''))
  if not match or not any(k in str(e.get('list',[])) for k in ['pbTrainerBattle','pbDoubleTrainerBattle']):continue
  d=e.get('direction',0)
  if d not in [2,4,6,8]:continue
  dx,dy={2:(0,1),4:(-1,0),6:(1,0),8:(0,-1)}[d]
  x,y=e['x'],e['y']
  for _ in range(int(match[1])):
   nx,ny=x+dx,y+dy
   if not (0<=nx<w and 0<=ny<h):break
   hazards.add((nx,ny));x,y=nx,ny
 def cost(n):
  if 'terrain' not in v:return 1
  tags=v['terrain']['data']
  for z in [2,1,0]:
   tag=tags[data[n[0]+w*n[1]+w*h*z]]
   if tag and tag!=13:return 8 if tag in [2,10,11,14] else 1
  return 1
 graph={}
 start=tuple(v['position']);q=[(0,start)];dist={start:0};prev={start:None};dirs=[(0,1,2,'down'),(-1,0,4,'left'),(1,0,6,'right'),(0,-1,8,'up')]
 if return_graph:
  q=[(0,(x,y)) for y in range(h) for x in range(w)];heapq.heapify(q);dist={p:0 for _,p in q};prev={p:None for _,p in q}
 while q:
  distance,p=heapq.heappop(q)
  if distance!=dist[p]:continue
  if p==goal and not return_graph:break
  for dx,dy,d,k in dirs:
   n=(p[0]+dx,p[1]+dy)
   if (p,d) in jumps:
    n=jumps[(p,d)]
    if not (0<=n[0]<w and 0<=n[1]<h):continue
    nd=distance+cost(n)+(500 if n in hazards else 0)
    if n not in blocked:graph.setdefault(p,[]).append(('jump:'+k,n))
    if n not in blocked and nd<dist.get(n,float('inf')):
     prev[n]=(p,'jump:'+k);dist[n]=nd;heapq.heappush(q,(nd,n))
    continue
   if n in blocked or (mounted and terrain(n)==10) or not ok(*p,d) or not ok(*n,10-d):continue
   native_jump=terrain(n)==1
   if native_jump:
    n=(p[0]+2*dx,p[1]+2*dy)
    if not landing_ok(n) or (mounted and terrain(n)==10):continue
   # The lower Mirage dark strips use ordinary Ice terrain. One input
   # slides to the first non-ice tile or obstacle, including moved ladders.
   if v['map'] in [882,887] and not v.get('ignore_ice') and terrain(n)==12:
    native_jump=True
    for _ in range(w+h):
     if terrain(n)!=12:break
     nn=(n[0]+dx,n[1]+dy)
     if nn in blocked or not ok(*n,d) or not ok(*nn,10-d):break
     n=nn
   graph.setdefault(p,[]).append(('jump:'+k if native_jump else k,n))
   nd=distance+cost(n)+(500 if n in hazards else 0)
   if nd<dist.get(n,float('inf')):
    prev[n]=(p,'jump:'+k if native_jump else k);dist[n]=nd;heapq.heappush(q,(nd,n))
 if return_graph:return graph
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
