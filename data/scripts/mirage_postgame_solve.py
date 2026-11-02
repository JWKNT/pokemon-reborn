"""Offline linked-block puzzle planning from installed map geometry only."""
import json,sys
from collections import deque
from route_readonly import route,ROOT
v=json.load(open(sys.argv[1]));pe,se=map(int,sys.argv[2:4]);start=tuple(map(int,sys.argv[4:6]));out=sys.argv[6]
a=v['events'].pop(str(pe));b=v['events'].pop(str(se));blocked={(e['x'],e['y']) for e in v['events'].values() if not e['through']};v['position']=[-1,-1];g=route(v,None,True)
p=(a['x'],a['y']);o=(b['x'],b['y']);goals=[c['parameters'][3] for c in a['list'] if c['code']==111 and c['parameters'][:2] in [[1,47],[1,48]]];goal=(tuple(goals[:2]),tuple(goals[2:4]));dirs=[('up',0,-1),('down',0,1),('left',-1,0),('right',1,0)]
def reach(start,p,o):
 seen={start};todo=[start]
 for x in todo:
  for _,n in g.get(x,[]):
   if n not in seen and n not in [p,o]:seen.add(n);todo.append(n)
 return seen
q=deque([((p,o,start),[])]);seen=set();solution=None
while q:
 (p,o,player),path=q.popleft()
 if (p,o)==goal:solution=path;break
 accessible=reach(player,p,o);key=(p,o,min(accessible))
 if key in seen:continue
 seen.add(key)
 assert len(seen)<300000,'Bound reached'
 for actor in ([0,1] if '--both' in sys.argv else [0]):
  first,second=(p,o) if actor==0 else (o,p)
  for k,dx,dy in dirs:
   before=(first[0]-dx,first[1]-dy)
   if before not in accessible:continue
   fn=next((n for kk,n in g.get(first,[]) if kk==k and n!=second and n not in blocked),first)
   sn=next((n for kk,n in g.get(second,[]) if kk==k and n!=fn and n not in blocked),second)
   if (fn,sn)==(first,second):continue
   pn,on=(fn,sn) if actor==0 else (sn,fn)
   step={'event':pe if actor==0 else se,'partner':se if actor==0 else pe,'direction':k,'primary_before':first,'primary_after':fn,'secondary_before':second,'secondary_after':sn,'stand':before}
   q.append(((pn,on,before),path+[step]))

assert solution,(len(seen),'No solution')
r={'map':v['map'],'event':pe,'partner':se,'goals':goals,'states':len(seen),'steps':solution};open(out,'w').write(json.dumps(r,indent=2)+'\n');print('Solved',pe,len(solution),'pushes',len(seen),'states')
