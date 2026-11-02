"""Read-only paired surface/Dive planner; emits ordinary controls, never edits game data."""
from surface_readonly import ROOT,route,tag,WATER
import json,sys,subprocess,heapq
import copy
# Optional planning-only state; never changes native game data or navigation notes.
planning=json.loads(open(sys.argv[6]).read()) if len(sys.argv)>6 else {}
def planning_arg(switches=None):
 out=copy.deepcopy(planning);out.setdefault('switches',{}).update(switches or {});return json.dumps(out)
mid,sx,sy,tx,ty=map(int,sys.argv[1:6]);meta=json.loads((ROOT/'work/fly-map-data.json').read_text());under=meta['maps'][str(mid)]['DiveMap']
v=json.loads(subprocess.check_output(['ruby',str(ROOT/'scripts/route_map.rb'),str(mid),str(sx),str(sy),planning_arg({'578':False})],stderr=subprocess.DEVNULL))
u=json.loads(subprocess.check_output(['ruby',str(ROOT/'scripts/route_map.rb'),str(under),'0','0',planning_arg()],stderr=subprocess.DEVNULL))
g0=route(v,None,True)
sv=json.loads(subprocess.check_output(['ruby',str(ROOT/'scripts/route_map.rb'),str(mid),str(sx),str(sy),planning_arg({'578':True})],stderr=subprocess.DEVNULL))
for i,t in enumerate(sv['terrain']['data']):
 if t in WATER:sv['passages']['data'][i]=0;sv['priorities']['data'][i]=0
g1=route(sv,None,True)
# Aegir's underwater passages connect separate chambers on the same map.
# Model their installed touch transfers instead of treating every door as a wall.
transfers={}
uv=copy.deepcopy(u)
for eid,event in u['events'].items():
 commands=event.get('list') or []
 destinations=[c['parameters'] for c in commands if c['code']==201]
 if event['trigger']==1 and len(destinations)==1 and destinations[0][:2]==[0,under]:
  transfers[(event['x'],event['y'])]=tuple(destinations[0][2:4])
  uv['events'].pop(eid)
# Underwater travel traverses water tiles using the normal diving vehicle.
for i,t in enumerate(uv['terrain']['data']):
 if t in WATER:uv['passages']['data'][i]=0;uv['priorities']['data'][i]=0
ug=route(uv,None,True)
start=(mid,sx,sy,tag(v,(sx,sy))in WATER);todo=[(0,start)];dist={start:0};prev={start:None};end=None
while todo:
 cost,p=heapq.heappop(todo)
 if cost!=dist[p]:continue
 layer,x,y,surf=p;pos=(x,y)
 if layer==mid and pos==(tx,ty):end=p;break
 choices=[]
 if layer==under:
  choices=[((under,*transfers.get(n,n),False),('door:'+k if n in transfers else k),1)for k,n in ug.get(pos,[])if not k.startswith('jump:')]
  for key,dx,dy in [('up',0,-1),('down',0,1),('left',-1,0),('right',1,0)]:
   front=(x+dx,y+dy)
   if front in transfers:choices.append(((under,*transfers[front],False),'door:'+key,1))
  if tag(v,pos)==5:choices.append(((mid,x,y,True),'surface',8))
 else:
  edges=list((g1 if surf else g0).get(pos,[]))
  if not surf:edges.extend((k,n)for k,n in g1.get(pos,[])if tag(v,n)in WATER and tag(v,pos)not in WATER)
  for key,n in edges:
   if surf and key.startswith('jump:'):continue
   mode=tag(v,n)in WATER;extra=1
   if not surf and mode:key='surf:'+key;extra=8
   elif surf and not mode:
    if abs(n[0]-x)+abs(n[1]-y)!=1:continue
    key='land:'+key
   choices.append(((mid,*n,mode),key,extra))
  if surf and tag(v,pos)==5:choices.append(((under,x,y,False),'dive',8))
 for np,k,e in choices:
  nc=cost+e
  if nc<dist.get(np,float('inf')):dist[np]=nc;prev[np]=(p,k);heapq.heappush(todo,(nc,np))
if not end:
 print('REACHABLE', {layer:sum(p[0]==layer for p in dist) for layer in [mid,under]}, 'start',start,'goal surface neighbors',g1.get((tx,ty)), 'under doors',transfers)
 raise SystemExit('No paired Dive route')
steps=[]
while prev[end]:old,k=prev[end];steps.append({'from':old,'to':end,'key':k});end=old
steps.reverse();path=ROOT/'work'/f'dive-route-{mid}.json';path.write_text(json.dumps(steps,indent=2));print('PLAN',len(steps),'steps',path)
for s in steps:
 if s['key']in['dive','surface']:print(s)
