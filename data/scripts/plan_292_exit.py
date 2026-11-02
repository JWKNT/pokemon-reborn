"""Read-only Dijkstra across surface walking/surf/ice and underwater Dive edges."""
from surface_readonly import ROOT,route,tag,WATER
import json,subprocess,heapq
import copy
v=json.loads(subprocess.check_output(['ruby',str(ROOT/'scripts/route_map.rb'),'375','40','12'],stderr=subprocess.DEVNULL));u=json.loads(subprocess.check_output(['ruby',str(ROOT/'scripts/route_map.rb'),'389','53','33'],stderr=subprocess.DEVNULL))
g0=route(v,None,True);sv=copy.deepcopy(v)
for i,t in enumerate(v['terrain']['data']):
 if t in WATER:sv['passages']['data'][i]=0;sv['priorities']['data'][i]=0
for i,t in enumerate(u['terrain']['data']):
 if t in WATER:u['passages']['data'][i]=0;u['priorities']['data'][i]=0
g1=route(sv,None,True);ug=route(u,None,True)
start=(1,53,33,True);goal=(0,40,12,False);q=[(0,start)];dist={start:0};prev={start:None}
while q:
 cost,p=heapq.heappop(q)
 if cost!=dist[p]:continue
 if p==goal:break
 layer,x,y,surf=p;pos=(x,y);choices=[]
 if layer:
  choices=[((1,*n,True),k,1)for k,n in ug.get(pos,[])]
  if tag(v,pos)==5:choices.append(((0,x,y,True),'surface',8))
 else:
  c=list((g1 if surf else g0).get(pos,[]))
  if not surf:c.extend((k,n)for k,n in g1.get(pos,[])if tag(v,n)in WATER and tag(v,pos)not in WATER)
  for key,n in c:
   if surf and key.startswith("jump:"):continue
   mode=tag(v,n)in WATER;extra=1
   if not surf and mode:key='surf:'+key;extra=8
   elif surf and not mode:
    if abs(n[0]-x)+abs(n[1]-y)!=1:continue
    key='land:'+key
   elif not mode and tag(v,n)==12 and not key.startswith('jump:'):
    direction=key
    while tag(v,n)==12:
     farther=next((nn for kk,nn in g0.get(n,[])if kk==direction),None)
     if farther is None:break
     n=farther;extra+=1
    key='slide:'+direction
   choices.append(((0,*n,mode),key,extra))
  if surf and tag(v,pos)==5:choices.append(((1,x,y,True),'dive',8))
 for np,k,e in choices:
  nc=cost+e
  if nc<dist.get(np,float('inf')):dist[np]=nc;prev[np]=(p,k);heapq.heappush(q,(nc,np))
else:raise SystemExit('No multilayer route')
steps=[];p=goal
while prev[p]:
 old,k=prev[p];steps.append({'from':old,'to':p,'key':k});p=old
steps.reverse();(ROOT/'work/292-exit375-plan.json').write_text(json.dumps(steps,indent=2))
print('PLAN',len(steps),'edges cost',dist[goal])
for s in steps:
 if s['key']in['dive','surface']:print(s)
