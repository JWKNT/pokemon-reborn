"""Source-only proposed post-Solaris paths. Reads fixed map assets/frozen128 evidence, writes work proposals only. Never imports executable input entry points or reads a live save. Special edges are installed763 bridge/Waterfall events; paths are not authorized blind input queues."""
import sys,json,copy,heapq,re
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import nav,surface_plan as sp
nav.ROOT=Path('/private/tmp/source-planner-no-state');sp.ROOT=nav.ROOT
R=Path(__file__).resolve().parent.parent
F=json.load(open(R/'notes/Void-Hypno-won-128-navigation.json'))
raw=json.load(open(R/'work/post-solaris-map-grids-static.json'))
F['variables']['391']=54;F['switches']['988']=True;F['switches']['989']=True;F['switches']['999']=False
F['self_switches']['763,48,A']=True
D={'up':(0,-1),'down':(0,1),'left':(-1,0),'right':(1,0)}
def model(mid,pos,ama=False):
 v=copy.deepcopy(raw[str(mid)]);v['position']=list(pos);v['mounted']=False;events={}
 for eid,e in v['events'].items():
  for p in e['pages'][::-1]:
   c=p['condition'];ss=F['self_switches'].copy()
   if ama:ss['763,134,A']=True
   if c['switch1_valid'] and not F['switches'].get(str(c['switch1_id'])):continue
   if c['switch2_valid'] and not F['switches'].get(str(c['switch2_id'])):continue
   if c['variable_valid'] and F['variables'].get(str(c['variable_id']),0)<c['variable_value']:continue
   if c['self_switch_valid'] and not ss.get(f'{mid},{eid},{c["self_switch_ch"]}'):continue
   q={'x':e['x'],'y':e['y'],'name':e['name'],'through':p['through'],'character':p['graphic']['character_name'],'tile_id':p['graphic']['tile_id'],'trigger':p['trigger'],'move_type':p['move_type'],'direction':p['graphic']['direction'],'list':p['list']}
   events[eid]=q;break
 v['events']=events
 # Make every remaining trainer sight tile an absolute barrier.
 for e in list(events.values()):
  if 'Trainer(' in e['name'] and 'pbTrainerBattle' in str(e['list']):
   n=int(re.search(r'Trainer\((\d+)\)',e['name'])[1]);dx,dy={2:(0,1),4:(-1,0),6:(1,0),8:(0,-1)}[e['direction']]
   for i in range(1,n+1):events[f'hazard{len(events)}']={'x':e['x']+i*dx,'y':e['y']+i*dy,'name':'STATIC_HAZARD','through':False,'character':'BLOCK','tile_id':0,'trigger':0,'list':[]}
 return v

def planner(start,goal,ama=False):
 v=model(763,start[1:3],ama);u=model(741,(0,0),ama)
 g0=nav.route(v,None,True)
 # 763E128-131: impassable bank touch routes force six normal walking tiles.
 for y in (46,47):
  g0.setdefault((57,y),[]).append(('bridge:right',(63,y)))
  g0.setdefault((63,y),[]).append(('bridge:left',(57,y)))
 sv=copy.deepcopy(v)
 for i,t in enumerate(sv['terrain']['data']):
  if t in sp.WATER:sv['passages']['data'][i]=0;sv['priorities']['data'][i]=0
 g1=nav.route(sv,None,True);ug=nav.route(u,None,True)
 todo=[(0,start)];dist={start:0};prev={start:None};end=None
 while todo:
  cost,p=heapq.heappop(todo)
  if cost!=dist[p]:continue
  layer,x,y,surf=p;pos=(x,y)
  if p[:3]==goal:end=p;break
  choices=[]
  if layer==741:
   choices=[((741,*n,False),k,1)for k,n in ug.get(pos,[])if not k.startswith('jump:')]
   if sp.tag(v,pos)==5:choices.append(((763,x,y,True),'surface',8))
  else:
   edges=list((g1 if surf else g0).get(pos,[]))
   if not surf:edges.extend((k,n)for k,n in g1.get(pos,[])if sp.tag(v,n)in sp.WATER and sp.tag(v,pos)not in sp.WATER)
   for key,n in edges:
    if surf and key.startswith('jump:'):continue
    mode=sp.tag(v,n)in sp.WATER;extra=1
    if sp.tag(v,n)==8:continue # all waterfall transitions explicitly modeled below
    if not surf and mode:key='surf:'+key;extra=8
    elif surf and not mode:
     if abs(n[0]-x)+abs(n[1]-y)!=1:continue
     key='land:'+key
    choices.append(((763,*n,mode),key,extra))
   if surf and sp.tag(v,pos)==5:choices.append(((741,x,y,False),'dive',8))
   if surf:
    for key in ('up','down'):
     dx,dy=D[key];n=(x+dx,y+dy)
     if sp.tag(v,n)not in (8,9):continue
     while sp.tag(v,n)in (8,9):n=(n[0]+dx,n[1]+dy)
     if sp.tag(v,n)in sp.WATER:choices.append(((763,*n,True),'waterfall:'+key,8+abs(n[1]-y)))
  for np,k,e in choices:
   nc=cost+e
   if nc<dist.get(np,float('inf')):dist[np]=nc;prev[np]=(p,k);heapq.heappush(todo,(nc,np))
 if end is None:return None
 steps=[]
 while prev[end]:old,k=prev[end];steps.append({'from':old,'to':end,'key':k});end=old
 return steps[::-1]
if __name__=='__main__':
 paths={}
 for ama in (False,True):
  for sy in (52,53):
   r=planner((763,46,sy,False),(741,46,43),ama)
   k=f'start46_{sy}_AmaDefeated{ama}';paths[k]=r
   print(k,len(r)if r else None)
   if r:
    print([s for s in r if ':'in s['key']or s['key']in ('dive','surface')])
    print('last',r[-12:])
 (R/'work/post-solaris-water-route-proposed.json').write_text(json.dumps({'source_only':True,'baseline':'Void-Hypno-won-128-navigation','hypothetical_flags':{'391':54,'988':True,'989':True,'999':False,'763,48,A':True},'paths':paths},indent=2)+'\n')
 F['variables']['391']=56;F['switches']['989']=False
 ret=planner((741,46,43,False),(763,59,61),False)
 assert ret,'No source return route'
 (R/'work/post-solaris-water-return-proposed.json').write_text(json.dumps({'source_only':True,'hypothetical_flags':{'391':56,'989':False},'steps':ret},indent=2)+'\n')
 print('return',len(ret))
