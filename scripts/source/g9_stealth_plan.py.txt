"""Read-only conservative route analysis of installed Sanctum guard patterns."""
import json,sys,re
from pathlib import Path
from nav import route
root=Path(__file__).resolve().parents[1];v=json.loads((root/'work/g9-stealth-map.json').read_text());events=json.loads((root/'work/g9-stealth-guards.json').read_text());static=set();dynamic=set()
for i in range(15,30):
 e=events[str(i)];p=e['pages'][0];x,y=e['x'],e['y'];d=p['graphic']['direction'];states=[(x,y,d)];moves=p['move_route']['list']
 for c in moves:
  code=c['code']
  if code in [1,2,3,4]:
   dx,dy,d={1:(0,1,2),2:(-1,0,4),3:(1,0,6),4:(0,-1,8)}[code];x+=dx;y+=dy
  if code in [16,17,18,19]:d={16:2,17:4,18:6,19:8}[code]
  states.append((x,y,d))
 target=dynamic if p['move_type']==3 else static
 for x,y,d in states:
  target.add((x,y));dx,dy={2:(0,1),4:(-1,0),6:(1,0),8:(0,-1)}[d]
  for n in range(1,7 if i==28 else 6):target.add((x+dx*n,y+dy*n))
(root/'work/g9-stealth-danger.json').write_text(json.dumps({'static':sorted(static),'dynamic':sorted(dynamic)},indent=2))
for mode,cells in [('static',static),('all',static|dynamic)]:
 vv=json.loads(json.dumps(v))
 for i,(x,y) in enumerate(cells):vv['events']['danger'+str(i)]={'x':x,'y':y,'through':False,'character':'guardvision','tile_id':0,'list':[],'name':'GuardVision','trigger':0,'direction':2}
 for start,goal in [([24,38],(48,20)),([48,20],(25,1))]:
  vv['position']=start
  try:print(mode,start,goal,route(vv,goal))
  except ValueError:print(mode,start,goal,'NO CONSERVATIVELY SAFE PATH')
