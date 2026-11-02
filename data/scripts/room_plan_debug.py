"""Plan reviewed, choice-free transfers across disconnected interior rooms.
This reads installed maps and the saved/observed navigation snapshot only.
It prints a plan; it never issues game input.
"""
import argparse,copy,heapq,json,subprocess
from route_readonly import ROOT,route
p=argparse.ArgumentParser();p.add_argument('--maps',required=True);p.add_argument('--start',required=True);p.add_argument('--goal',required=True,help='map,event');p.add_argument('--output');a=p.parse_args()
allowed=list(map(int,a.maps.split(',')));start=tuple(map(int,a.start.split(',')));gm,ge=map(int,a.goal.split(','));assert start[0] in allowed and gm in allowed
models={m:json.loads(subprocess.check_output(['ruby',str(ROOT/'scripts/route_map.rb'),str(m),'0','0'],stderr=subprocess.DEVNULL)) for m in allowed}
def sides(v,e,kind):
 required={c['parameters'][2] for c in e['list'] or [] if c['code']==111 and len(c['parameters'])>=3 and c['parameters'][:2]==[6,-1]}
 result=[]
 for dx,dy,direction in [(0,1,8),(0,-1,2),(1,0,4),(-1,0,6)]:
  if required and direction not in required:continue
  point=(e['x']+dx,e['y']+dy)
  try:result.append((len(route(v,point)),point))
  except ValueError:pass
 return result
dist={start:0};queue=[(0,start)];previous={};finish=None
while queue:
 cost,node=heapq.heappop(queue)
 if cost!=dist[node]:continue
 m,x,y=node;v=dict(models[m],position=[x,y])
 if m==gm:
  ss=sides(v,v['events'][str(ge)],'talk')
  if ss:finish=(node,min(ss));break
 for eid,e in v['events'].items():
  cs=e['list'] or []
  dests={tuple(c['parameters'][1:4]) for c in cs if c['code']==201 and c['parameters'][0]==0}
  if len(dests)!=1:continue
  dest=next(iter(dests))
  if dest[0] not in allowed:continue
  if any(c['code'] in [102,103,104,301] or any(s in str(c['parameters']) for s in ['pbTrainerBattle','pbDoubleTrainerBattle','pbWildBattle']) for c in cs):continue
  ss=sides(v,e,'enter')
  if not ss:continue
  extra,_=min(ss);nc=cost+extra+15
  if nc<dist.get(dest,float('inf')):
   dist[dest]=nc;previous[dest]=(node,{'map':m,'event':int(eid),'kind':'enter','arrival':list(dest)})
   heapq.heappush(queue,(nc,dest))
assert finish,('No reviewed room passage found',list(dist))
node,approach=finish;steps=[]
while node!=start:node,step=previous[node];steps.append(step)
steps.reverse();result={'start':list(start),'transfers':steps,'goal':{'map':gm,'event':ge,'approach':list(approach[1])},'source':'Installed maps and read-only saved/observed navigation notes'}
print(json.dumps(result,indent=2))
if a.output:open(a.output,'w').write(json.dumps(result,indent=2)+'\n')
