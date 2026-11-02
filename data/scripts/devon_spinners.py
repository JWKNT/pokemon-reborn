"""Plan the installed rotating Devon pads, then execute verified native inputs.
Reads public map events. Only navigation notes are written; never game data.
"""
from nav import ROOT,route,act,read,snap
from locate import locate
import argparse,json,subprocess,heapq,copy,re
from devon_terrain import terrain_conveyors

p=argparse.ArgumentParser();p.add_argument('--go',action='store_true');p.add_argument('--from',dest='origin',nargs=2,type=int,default=[4,4]);p.add_argument('--goal',nargs=2,type=int,default=[15,3]);p.add_argument('--map',dest='mid',type=int,choices=[630,629,631],default=630);p.add_argument('--planning-overrides',type=json.loads);p.add_argument('--monitor',type=int,help='Route to an accessible side of a source-inspected monitor');p.add_argument('--activate',action='store_true');p.add_argument('--allow-damage',action='store_true',help='Reviewed native electrical damage, with a large routing penalty; heal normally before battles');p.add_argument('--forced-per-check',type=int,choices=[1,2,3],default=3,help='Queue up to three inspected forced steps, retaining their waits, before one coordinate proof');a=p.parse_args()
assert not(a.go and a.planning_overrides)
assert not a.activate or(a.go and a.monitor)
switch_ids={630:[750,751,752],629:[757,758,759,760],631:list(range(769,776))}[a.mid]
switch_base=switch_ids[0]
path=ROOT/'notes/navigation-state.json';state=json.loads(path.read_text())
initial_switches=state.get('switches',{})|((a.planning_overrides or {}).get('switches',{}))
color=(a.planning_overrides or {}).get('variables',{}).get('342',state['variables']['342']);mask=sum(1<<i for i,sw in enumerate(switch_ids) if initial_switches.get(str(sw),False))
if a.go:
 m,x,y=locate(a.mid);assert m==a.mid
else:x,y=a.origin
graphs={};pads={};models={};physicalgraphs={};conveyors={};damage_tiles={};through_conveyors={}
move={1:(0,1),2:(-1,0),3:(1,0),4:(0,-1),5:(-1,1),6:(1,1),7:(-1,-1),8:(1,-1)}
def ensure(mm,c):
 if (mm,c)in models:return
 extra=copy.deepcopy(a.planning_overrides or {});extra.setdefault('variables',{})['342']=c;extra.setdefault('switches',{}).update({str(sw):bool(mm&(1<<i)) for i,sw in enumerate(switch_ids)})
 v=json.loads(subprocess.check_output(['ruby',str(ROOT/'scripts/route_map.rb'),str(a.mid),str(x),str(y),json.dumps(extra)],stderr=subprocess.DEVNULL))
 models[(mm,c)]=v;pads[(mm,c)]={};conveyors[(mm,c)]=terrain_conveyors(v);through_conveyors[(mm,c)]=set()
 damage_tiles[(mm,c)]={(e['x'],e['y'])for e in v['events'].values()if any('pbFieldDamage'in str(z['parameters'])for z in e['list'])}
 if a.allow_damage:
  for e in v['events'].values():e['list']=[z for z in e['list']if 'pbFieldDamage'not in str(z['parameters'])]
 for eid,e in v['events'].items():
  routes=[z['parameters'][1] for z in e['list'] if z['code']==209 and z['parameters'][0]==-1]
  if not routes:continue
  if all(all(z['code']in[0,29,31,32,35,36]for z in r['list'])for r in routes):continue
  changes=[z['parameters'] for z in e['list'] if z['code']==122 and z['parameters'][:4]==[343,343,0,0]]
  if e['trigger']==1 and len(routes)==1 and len(changes)==1:
   codes=[z['code'] for z in routes[0]['list']]
   assert all(z in [0,1,2,3,4,5,6,7,8,29,31,32,44] for z in codes),'Unreviewed spinner route'
   assert [z['parameters'] for z in e['list'] if z['code']==121]==[[776,776,0]]
   sw=changes[0][4]+switch_base-1;assert sw in switch_ids
   pads[(mm,c)][(e['x'],e['y'])]=(int(eid),[move[z] for z in codes if z in move],sw)
  elif e['trigger']==1 and len(routes)==1 and routes[0]['skippable']:
   codes=[z['code'] for z in routes[0]['list']];moving=[z for z in codes if z in move]
   if len(moving)==1 and moving[0] in [1,2,3,4] and all(z in [0,1,2,3,4,29,31,32,35,36] for z in codes):
    conveyors[(mm,c)][(e['x'],e['y'])]={1:'down',2:'left',3:'right',4:'up'}[moving[0]]

   else:e['through']=False;e['character']='REVIEWED_BLOCK'
  else:e['through']=False;e['character']='REVIEWED_BLOCK'
 graphs[(mm,c)]=route(v,None,True)
 physical=copy.deepcopy(v)
 for e in physical['events'].values():
  if any('pbFieldDamage' in str(z['parameters']) for z in e['list']):
   e['through']=True;e['character']='';e['list']=[z for z in e['list'] if 'pbFieldDamage' not in str(z['parameters'])]
 physicalgraphs[(mm,c)]=route(physical,None,True)
start=(x,y,color,mask);goal=tuple(a.goal);goals={goal};faces={}
ensure(mask,color)
if a.monitor:
 ev=models[(mask,color)]['events'][str(a.monitor)];ex,ey=ev['x'],ev['y']
 faces={(ex,ey+1):'up',(ex,ey-1):'down',(ex+1,ey):'left',(ex-1,ey):'right'};goals=set(faces)
 if a.activate:
  assert not any(c['code']in[101,102,201,301]for c in ev['list'])
  changes=[c['parameters']for c in ev['list']if c['code']==121]
  assert len(changes)==2 and changes[0][0]==changes[0][1]==changes[1][0]==changes[1][1] and [c[2]for c in changes]==[1,0]
  monitor_switch=changes[0][0]
q=[(0,start)];dist={start:0};prev={start:None};end=None
while q:
 cost,n=heapq.heappop(q)
 if cost!=dist[n]:continue
 if n[:2]in goals:end=n;goal=n[:2];break
 ensure(n[3],n[2])
 xx,yy,c,mm=n;choices=[('a',(xx,yy,c%3+1,mm),2,None,0)]
 for key,np in graphs[(mm,c)].get((xx,yy),[]):
  nm=mm;pad=None;forced=0;seen=set();valid=True;damage= int(np in damage_tiles[(nm,c)])
  while True:
   ensure(nm,c)
   if np not in pads[(nm,c)] and np not in conveyors[(nm,c)]:break
   if (*np,nm) in seen:valid=False;break
   seen.add((*np,nm))
   if np in pads[(nm,c)]:
    pad=pads[(nm,c)][np];eid,moves,sw=pad
    for dx,dy in moves:
     np=(np[0]+dx,np[1]+dy);forced+=1
     damage+=int(np in damage_tiles[(nm,c)])
     if np not in graphs[(nm,c)]:valid=False;break
    if not valid:break
    nm^=1<<(sw-switch_base)
   else:
    ck=conveyors[(nm,c)][np]
    ends=[p for k,p in graphs[(nm,c)].get(np,[]) if k==ck]
    if not ends:
     if any(k==ck for k,p in physicalgraphs[(nm,c)].get(np,[])):valid=False
     break
    np=ends[0];forced+=1;damage+=int(np in damage_tiles[(nm,c)])
  if not valid:continue
  choices.append((key,(*np,c,nm),1+forced*.2+2000*damage,pad,forced))
 for key,np,extra,pad,forced in choices:
  nc=cost+extra
  if nc<dist.get(np,float('inf')):dist[np]=nc;prev[np]=(n,key,pad,forced);heapq.heappush(q,(nc,np))
if end is None:
 (ROOT/'work'/f'devon-{a.mid}-unreachable-debug.json').write_text(json.dumps({'start':start,'goals':list(goals),'states':[list(n)for n in dist],'graph':{str(k):v for k,v in graphs[(mask,color)].items()},'pads':{str(k):v for k,v in pads[(mask,color)].items()},'conveyors':{str(k):v for k,v in conveyors[(mask,color)].items()}}))
 raise SystemExit('No safe installed-spinner route')
steps=[]
while prev[end]:
 old,key,pad,forced=prev[end];steps.append({'from':list(old),'to':list(end),'key':key,'pad':pad,'forced':forced});end=old
steps.reverse();print(json.dumps(steps),flush=True)
if not a.go:raise SystemExit(0)
i=0
while i<len(steps):
 chunk=[]
 while i<len(steps) and len(chunk)<16:
  z=steps[i];chunk.append(z);i+=1
  if sum(bool(z['forced'])for z in chunk)>=a.forced_per_check:break
 seq=[]
 for z in chunk:
  seq.append(z['key']+':.12')
  if z['key']=='a':seq.append('wait:.3')
  if z['forced']:seq.append('wait:'+str(min(6,max(2,z['forced']*.22))))
 act(*seq,'wait:.5');t=read();print(t,flush=True)
 assert not re.search(r'\bhp\b|\bfight\b',t,re.I)
 expected=chunk[-1]['to'];actual=locate(a.mid)
 assert actual==(a.mid,*expected[:2]),f'Spinner mismatch {actual}, expected{expected}'
 v=json.loads(path.read_text());v['variables']['342']=expected[2]
 v.setdefault('switches',{}).update({str(sw):bool(expected[3]&(1<<j)) for j,sw in enumerate(switch_ids)});path.write_text(json.dumps(v))
print('DEVON SPINNER ROUTE VERIFIED',goal,flush=True)
if a.activate:
 act(faces[goal]+':.12','c','wait:.5');print(read(),flush=True)
 assert locate(a.mid)==(a.mid,*goal)
 v=json.loads(path.read_text());v.setdefault('switches',{})[str(monitor_switch)]=not v.get('switches',{}).get(str(monitor_switch),False);path.write_text(json.dumps(v))
 print('DEVON MONITOR VERIFIED',a.monitor,monitor_switch,v['switches'][str(monitor_switch)],flush=True)
