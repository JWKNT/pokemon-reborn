"""Plan and execute safe Devon floor crossings with the actual radio color.
Reads public map pages. Writes only navigation notes after observed normal inputs.
Conveyor/spinner events are excluded until their movement has been reviewed.
"""
from nav import *
from locate import locate,capture_ready
import copy,argparse
from devon_terrain import terrain_conveyors
p=argparse.ArgumentParser();p.add_argument('map',type=int);p.add_argument('x',type=int);p.add_argument('y',type=int);p.add_argument('--color',type=int,choices=[1,2,3]);p.add_argument('--go',action='store_true');p.add_argument('--from',dest='origin',nargs=2,type=int);p.add_argument('--conveyors',action='store_true',help='Follow inspected single-cardinal conveyor chains; spinners remain blocked');p.add_argument('--planning-overrides',type=json.loads,help='Read-only hypothetical state for dry route planning');a=p.parse_args()
assert not (a.go and a.planning_overrides),'Hypothetical overrides are only for read-only plans'
statepath=ROOT/'notes/navigation-state.json';state=json.loads(statepath.read_text());color=a.color or state['variables'].get('342');assert color in [1,2,3]
if a.go:m,x,y=locate(a.map);assert m==a.map
else:
 m=a.map;x,y=a.origin or (12,10)
models={};graphs={};physicalgraphs={};hazards={};arrows={}
for c in [1,2,3]:
 extra=copy.deepcopy(a.planning_overrides or {});extra.setdefault('variables',{})['342']=c
 v=json.loads(subprocess.check_output(['ruby',str(ROOT/'scripts/route_map.rb'),str(m),str(x),str(y),json.dumps(extra)],stderr=subprocess.DEVNULL));models[c]=v
 arrows[c]=terrain_conveyors(v) if a.conveyors else {}
 for i,e in v['events'].items():
  cs=e['list'];danger=any('pbFieldDamage' in str(z['parameters'])for z in cs)
  routes=[z['parameters'][1] for z in cs if z['code']==209 and z['parameters'][0]==-1]
  forced=bool(routes)
  reviewed=False
  if routes and all(all(z['code']in[0,29,31,32,35,36]for z in r['list'])for r in routes):
   reviewed=True  # Native animation/speed restoration, no forced movement.
  if a.conveyors and e['trigger']==1 and len(routes)==1:
   moves=[z['code'] for z in routes[0]['list'] if z['code'] in range(1,9)]
   if len(moves)==1 and moves[0] in [1,2,3,4] and all(z['code'] in [0,1,2,3,4,29,31,32,35,36] for z in routes[0]['list']):
    arrows[c][(e['x'],e['y'])]={1:'down',2:'left',3:'right',4:'up'}[moves[0]]
    reviewed=True
  if danger or (forced and not reviewed):e['through']=False;e['character']='REVIEWED_BLOCK'
 physical=copy.deepcopy(v)
 for e in physical['events'].values():
  if any('pbFieldDamage' in str(z['parameters'])for z in e['list']):
   e['through']=True;e['character']=''
   e['list']=[z for z in e['list'] if 'pbFieldDamage' not in str(z['parameters'])]
 physicalgraphs[c]=route(physical,None,True)
 graphs[c]=route(v,None,True)
 # The raw graph intentionally contains trainer sight lines. Prefer routes
 # around those lines when controlling the electrical floor puzzle.
 hazards[c]=set()
 for e in v['events'].values():
  sight=re.search(r'Trainer\((\d+)\)',e.get('name',''))
  if not sight or not any('pbTrainerBattle' in str(z['parameters']) for z in e['list']):continue
  dx,dy={2:(0,1),4:(-1,0),6:(1,0),8:(0,-1)}.get(e['direction'],(0,0))
  hazards[c].update((e['x']+dx*n,e['y']+dy*n) for n in range(1,int(sight[1])+1))
def follow(n,c):
 seen=set();hops=0;visited=[]
 while n in arrows[c]:
  if n in seen:raise ValueError('Conveyor cycle')
  seen.add(n);visited.append(n)
  key=arrows[c][n];ends=[p for k,p in graphs[c].get(n,[]) if k==key]
  if not ends:
   # These inspected routes are skippable: a conveyor against a wall ends
   # with the player on that tile. Electrical hazards remain blocked.
   if n not in graphs[c] or any(k==key for k,_ in physicalgraphs[c].get(n,[])):raise ValueError('Conveyor landing unsafe')
   return n,hops,visited
  if len(ends)!=1:raise ValueError('Ambiguous conveyor landing')
  n=ends[0];hops+=1
 visited.append(n)
 return n,hops,visited
start=(x,y,color);goal=(a.x,a.y);q=[(0,start)];dist={start:0};prev={start:None};end=None
while q:
 cost,node=heapq.heappop(q)
 if cost!=dist[node]:continue
 if node[:2]==goal:end=node;break
 xx,yy,c=node
 choices=[]
 for key,np in graphs[c].get((xx,yy),[]):
  try:np,hops,visited=follow(np,c)
  except ValueError:continue
  choices.append((('conveyor:'+key) if hops else key,(*np,c),1+hops*.2+(500 if any(p in hazards[c] for p in visited) else 0)))
 choices.append(('a',(xx,yy,c%3+1),2))
 for key,np,extra in choices:
  nc=cost+extra
  if nc<dist.get(np,float('inf')):dist[np]=nc;prev[np]=(node,key);heapq.heappush(q,(nc,np))
if end is None:raise SystemExit('No safe route without an unreviewed conveyor')
steps=[]
while prev[end]:
 old,key=prev[end];steps.append({'from':list(old),'to':list(end),'key':key});end=old
steps.reverse();print(json.dumps(steps),flush=True)
if not a.go:raise SystemExit(0)
# Twelve reviewed edges fit in the capture guard's freshness window. Radio
# changes settle before the next queued step; verify each whole short crossing.
idx=0
while idx<len(steps):
 chunk=[]
 while idx<len(steps) and len(chunk)<16:
  s=steps[idx]
  chunk.append(s);idx+=1
  if tuple(s['to'][:2]) in hazards[s['to'][2]] or s['key'].startswith('conveyor:'):break
 expected=tuple(chunk[-1]['to']);seq=[]
 for z in chunk:
  seq.append(z['key'].removeprefix('conveyor:')+':.12')
  if z['key']=='a':seq.append('wait:.25')
  if z['key'].startswith('conveyor:'):seq.append('wait:2')
 act(*seq,'wait:.7');t=read();print(t,flush=True)
 if any(z['key']=='a' for z in chunk):
  state=json.loads(statepath.read_text());state['variables']['342']=expected[2];statepath.write_text(json.dumps(state))
 if re.search(r'\bhp\b|\bfight\b',t,re.I) or any(z['y']>.72 and len(z['text'])>18 for z in snap()):raise SystemExit('Devon crossing interrupted')
 actual=locate(m)
 if actual!=(m,*expected[:2]):raise SystemExit(f'Devon coordinate mismatch: expected {expected}, actual {actual}')
print('DEVON SAFE CROSSING VERIFIED',m,*goal,expected[2] if steps else color,flush=True)
