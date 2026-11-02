"""Read-only BFS over installed ice geometry and published puzzle rules."""
import json
from collections import deque
from pathlib import Path
from route_readonly import route
R=Path(__file__).resolve().parents[1]
v=json.loads((R/'work/250-rock-plan-map.json').read_text());v['position']=[31,27]
v['events']['87']={'x':30,'y':24,'character':'trchar169','through':False,'tile_id':0,'trigger':0,'list':[],'name':'Danielle'}
graph=route(v,None,True);w,h=v['width'],v['height'];data=v['data']['data'];tags=v['terrain']['data']
def ice(p):
 return next((tags[data[p[0]+w*p[1]+w*h*z]] for z in [2,1,0] if tags[data[p[0]+w*p[1]+w*h*z]] not in [0,13]),0)==12
cracks=[(25,20),(24,21),(25,22),(26,23),(25,24)]
order=['left','right','left','up','right'];start=((22,23),8);q=deque([start]);prev={start:None}
while q:
 state=q.popleft();p,mask=state
 if mask==31:break
 for k,n in graph.get(p,[]):
  if k.startswith('jump:'):continue
  newmask=mask;trail=[];valid=True
  while True:
   if not (22<=n[0]<=35 and 18<=n[1]<=28):valid=False;break
   trail.append(n)
   if n in cracks:
    bit=1<<cracks.index(n)
    if newmask&bit or k!=order[newmask.bit_count()]:valid=False;break
    newmask|=bit
    # Installed crack event forces MoveForward before sliding resumes.
    nxt=next((b for a,b in graph.get(n,[]) if a==k),None)
    if nxt is None:valid=False;break
    n=nxt;continue
   if not ice(n):break
   nxt=next((b for a,b in graph.get(n,[]) if a==k),None)
   if nxt is None:break
   n=nxt
  if not valid:continue
  dest=(n,newmask)
  if dest not in prev:prev[dest]=(state,k,trail);q.append(dest)
else:raise SystemExit('No ice solution')
steps=[]
while prev[state]:
 before,k,trail=prev[state];steps.append({'start':before[0],'key':k,'end':state[0],'mask':state[1],'trail':trail});state=before
steps.reverse();(R/'work/250-ice-plan.json').write_text(json.dumps(steps,indent=2)+'\n');print(json.dumps(steps))
