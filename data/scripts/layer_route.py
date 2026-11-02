"""Read-only Route 2 planner that tracks switch410 across stairs and jumps."""
from nav import *
import copy
DIR={'up':(0,-1,8),'down':(0,1,2),'left':(-1,0,4),'right':(1,0,6)}
def effect(event,direction,ground):
 active={-1:True};conditions={}
 for c in event.get('list',[]) or []:
  code,a,indent=c['code'],c['parameters'],c['indent']
  if code==111:
   if a[:2]==[6,-1]:ok=a[2]==direction
   elif a[:2]==[0,410]:ok=ground==(a[2]==0)
   else:ok=False
   conditions[indent]=ok;active[indent]=active.get(indent-1,True) and ok
  elif code==411:active[indent]=active.get(indent-1,True) and not conditions.get(indent,False)
  elif code==412:active.pop(indent,None)
  elif code==121 and a[:2]==[410,410] and active.get(indent-1,True):ground=a[2]==0
 return ground
CACHE={}
def plan(mid,x,y,ground,tx,ty,target_ground=None,hypothetical_state=None):
 st=copy.deepcopy(hypothetical_state) if hypothetical_state is not None else json.loads((ROOT/"notes/navigation-state.json").read_text())
 st.get("switches",{}).pop("410",None)
 cachekey=(mid,json.dumps(st,sort_keys=True))
 maps={};graphs={}
 for s in [False,True]:
  if (cachekey,s) in CACHE:
   maps[s],graphs[s]=CACHE[(cachekey,s)];continue
  arg=json.dumps({'switches':{**st.get('switches',{}),'410':s},'variables':st.get('variables',{})})
  v=json.loads(subprocess.check_output(['ruby',str(ROOT/'scripts/route_map.rb'),str(mid),str(x),str(y),arg],stderr=subprocess.DEVNULL))
  if hypothetical_state is not None:
   for eid,xy in st.get('positions',{}).get(str(mid),{}).items():
    if eid in v['events']:v['events'][eid]['x'],v['events'][eid]['y']=xy
  maps[s]=v;graphs[s]=route(v,None,True);CACHE[(cachekey,s)]=(v,graphs[s])
 start=(x,y,ground);todo=[(0,start)];dist={start:0};prev={start:None};final=None
 while todo:
  cost,p=heapq.heappop(todo)
  if cost!=dist[p]:continue
  if p[:2]==(tx,ty) and (target_ground is None or p[2]==target_ground):final=p;break
  px,py,s=p
  for key,(nx,ny) in graphs[s].get((px,py),[]):
   k=key.removeprefix('jump:');dx,dy,d=DIR[k];new=s
   points=[(px+dx,py+dy),(nx,ny)] if key.startswith('jump:') else [(nx,ny)]
   for point in dict.fromkeys(points):
    for e in maps[s]['events'].values():
     if e['trigger']==1 and (e['x'],e['y'])==point:new=effect(e,d,new)
   n=(nx,ny,new);nc=cost+(2 if key.startswith('jump:') else 1)
   if nc<dist.get(n,float('inf')):dist[n]=nc;prev[n]=(p,key,action_jump(maps[s],p[:2],key));heapq.heappush(todo,(nc,n))
 if final is None:raise ValueError('No layered route')
 out=[];p=final
 while prev[p]:old,key,activate=prev[p];out.append({'from':old,'key':key,'to':p,'action_jump':activate});p=old
 return out[::-1]
if __name__=='__main__':
 mid,x,y,ground,tx,ty=map(int,sys.argv[1:7]);r=plan(mid,x,y,bool(ground),tx,ty)
 print(json.dumps(r));(ROOT/'work/layer-route.json').write_text(json.dumps(r,indent=2))
