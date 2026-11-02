from play import *
from nav import route
from locate import locate
import heapq
mid,x,y=locate(234)
if mid!=234:raise SystemExit('Wrong map')
base=json.loads((ROOT/'notes/navigation-state.json').read_text());stage=base['variables']['145'];cache={}
for s in range(9):
 cache[s]=json.loads(subprocess.check_output(['ruby',str(ROOT/'scripts/route_map.rb'),'234','0','0',json.dumps({'variables':{'145':s}})],stderr=subprocess.DEVNULL))
q=[(0,stage,x,y,[])];seen=set();plan=None
while q:
 cost,s,x,y,steps=heapq.heappop(q)
 if (s,x,y) in seen:continue
 seen.add((s,x,y));v=cache[s];v['position']=[x,y];reach=route(v,None)
 if (9,27) in reach:plan=steps+[(s,9,27,None)];break
 for e in v['events'].values():
  for c in e['list']:
   a=c['parameters']
   if c['code']==122 and a[:4]==[145,145,0,0] and a[4]!=s and (e['x'],e['y']) in reach:
    heapq.heappush(q,(cost+reach[(e['x'],e['y'])],a[4],e['x'],e['y'],steps+[(s,e['x'],e['y'],a[4])]))
print('FOREST EXIT PLAN',plan,flush=True)
if not plan:raise SystemExit('No exit plan')
for stage,x,y,nextstage in plan:
 rc=subprocess.call([sys.executable,str(ROOT/'scripts/q.py'),f'234,{x},{y}'])
 if rc:raise SystemExit(rc)
 if nextstage is not None:
  p=ROOT/'notes/navigation-state.json';v=json.loads(p.read_text());v['variables']['145']=nextstage;p.write_text(json.dumps(v))
act('left','wait:2');print(read())
