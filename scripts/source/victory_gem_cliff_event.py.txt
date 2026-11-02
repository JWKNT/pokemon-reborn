"""Approach reviewed Victory Road events through ordinary two-step Rock Climbs."""
from nav import *
from locate import locate
import copy
os.environ.setdefault("REBORN_COORD_CACHE","1")
route_env=dict(os.environ,REBORN_FAST_KEYS="1",REBORN_ROUTE_CHUNK="112")
mid,eid=int(sys.argv[1]),int(sys.argv[2]);kind=sys.argv[3]if len(sys.argv)>3 else'talk'
allowed={785:{145},810:set(range(4,17)),806:set(range(6,32))|set(range(67,75)),809:{19,20,21,22,23,42,43,44,45},805:{40,41,62,63,67,68,69,74,75,82,83},808:set(range(4,14)),807:{4,5,6,7,8,9,13},803:set(range(6,72)),812:{56,58,59,60,61,62,63,64,65,66,67,88,106,107,108,109,110,120},813:set(range(25,56))|{57,68,76,77,80,81,82,83},794:set(range(24,41))|{44,45,46,66},787:set(range(25,39))|set(range(46,50))|{55,57,68},792:set(range(9,14))|set(range(19,22))|set(range(25,55))|set(range(68,76))|set(range(79,86)),802:set(range(8,16)),799:set(range(8,18)),790:set(range(16,28))|{43},791:set(range(14,27))|set(range(35,39))|{41,42},800:set(range(8,18))|{39,41,42,43,44},801:set(range(8,15))|{39}}[mid]
forced_stand=tuple(map(int,sys.argv[4:6])) if len(sys.argv)>=6 else None
dirs=[('up',0,-1),('down',0,1),('left',-1,0),('right',1,0)]
def plan(v):
 target=v['events'][str(eid)];graph=route(v,None,True)
 def can_stand(p):
  # A one-tile landing can have no ordinary walking edges: its only exit is
  # the same Rock Climb. Check the tile itself, not graph.get(p).
  x,y=p;w,h=v['width'],v['height']
  if not (0<=x<w and 0<=y<h):return False
  pas=v['passages']['data'];pri=v['priorities']['data'];data=v['data']['data']
  for e in v['events'].values():
   if (e['x'],e['y'])!=p or e['through']:continue
   if e['character']:return False
   z=e['tile_id']
   if z>=0:
    if pas[z]&15==15:return False
    if pri[z]==0:return True
  for layer in [2,1,0]:
   z=data[x+w*y+w*h*layer]
   if pas[z]&15==15:return False
   if pri[z]==0:return True
  return True
 goals=[forced_stand] if forced_stand else [(target['x']+dx,target['y']+dy)for _,dx,dy in dirs]
 cliffs=[]
 for k in allowed:
  e=v['events'].get(str(k))
  if not e or 'Kernel.pbRockClimb'not in str(e['list']):continue
  rr=[c['parameters'][1]['list']for c in e['list']if c['code']==209 and c['parameters'][0]==-1]
  assert len(rr)==1,k
  moves=[c['code']for c in rr[0] if 1<=c['code']<=14]
  assert (2<=len(moves)<=25 and all(c==12 for c in moves)) or (moves[0]==moves[-1]==12 and 1<=len(moves[1:-1])<=5 and len(set(moves[1:-1]))==1 and moves[1]in[5,6,7,8]),(k,moves)
  meaningful=[c for c in e['list'] if c['code']!=0]
  forbidden=set()
  if meaningful and meaningful[0]['code']==111 and meaningful[0]['parameters'][:2]==[6,-1] and meaningful[1]['code']==411:forbidden.add(meaningful[0]['parameters'][2])
  for direction,dx,dy in dirs:
   if {'down':2,'left':4,'right':6,'up':8}[direction] in forbidden:continue
   a=(e['x']-dx,e['y']-dy);px,py=a;fx,fy=dx,dy
   for code in moves:
    if code==12:mx,my=fx,fy
    else:
     mx,my={5:(-1,1),6:(1,1),7:(-1,-1),8:(1,-1)}[code]
     # RPG XP diagonal movement turns an opposing facing toward travel.
     if fx==-mx:fx=mx
     if fy==-my:fy=my
    px+=mx;py+=my
   b=(px,py)
   if can_stand(a) and can_stand(b):cliffs.append((k,a,b,direction))
 todo=[(0,tuple(v['position']),[])];seen=set()
 while todo:
  cost,pos,steps=heapq.heappop(todo)
  if pos in seen:continue
  seen.add(pos)
  # Build walking reachability once for each cliff landing. Rebuilding the
  # entire tile graph for every candidate made large rooms unnecessarily slow.
  reach={pos:0};walk=[pos]
  for cell in walk:
   for _,nxt in graph.get(cell,[]):
    if nxt not in reach:reach[nxt]=reach[cell]+1;walk.append(nxt)
  if any(goal in reach for goal in goals):return steps
  for k,a,b,direction in cliffs:
   if b in seen or a not in reach:continue
   heapq.heappush(todo,(cost+reach[a]+10,b,steps+[(k,a,b,direction)]))
 raise SystemExit('No route even through reviewed straight cliffs')
for attempt in range(25):
 m,x,y=locate(mid);assert m==mid
 v=json.loads(subprocess.check_output(['ruby',str(ROOT/'scripts/route_map.rb'),str(mid),str(x),str(y)],stderr=subprocess.DEVNULL));steps=plan(v)
 if not steps:
  if forced_stand:
   subprocess.run([sys.executable,str(ROOT/'scripts/q.py'),f'{mid},{forced_stand[0]},{forced_stand[1]}'],check=True,env=route_env)
   if kind!='approach':subprocess.run([sys.executable,str(ROOT/'scripts/eventq.py'),str(mid),str(eid),kind],check=True)
  elif kind=='approach':
   target=v['events'][str(eid)];options=[]
   for _,dx,dy in dirs:
    dest=(target['x']+dx,target['y']+dy)
    try:options.append((len(route(v,dest)),dest))
    except ValueError:pass
   _,dest=min(options)
   subprocess.run([sys.executable,str(ROOT/'scripts/q.py'),f'{mid},{dest[0]},{dest[1]}'],check=True,env=route_env)
  else:subprocess.run([sys.executable,str(ROOT/'scripts/eventq.py'),str(mid),str(eid),kind],check=True)
  break
 k,a,b,direction=steps[0];print('NORMAL CLIFF',k,a,b,direction,flush=True)
 p=ROOT/'work/nw-cliff-route.json';p.write_text(json.dumps([[mid,x,y,*a,[]]]))
 subprocess.run([sys.executable,str(ROOT/'scripts/queue_route.py'),str(p),'--from-verified'],check=True,env=route_env)
 act(direction+':.18','c','wait:1')
 rr=snap();text=' '.join(v['text'] for v in rr).lower()
 if re.search(r'\bhp\b|\bfight\b|\bwild\b|pp:',text):raise SystemExit('Unexpected battle during cliff')
 if any(v['y']>.72 and len(v['text'])>10 for v in rr):subprocess.run([sys.executable,str(ROOT/'scripts/dialog.py'),'--yes','--limit=10'],check=True)
 actual=locate(mid);assert actual==(mid,*b),('Climb landing differs',actual,b)
else:raise SystemExit('Cliff route exceeded twenty-four transitions')
