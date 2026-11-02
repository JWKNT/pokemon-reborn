"""Read-only mirror-block solver, including access to each pushing side."""
import json,subprocess,sys
from collections import deque
from route_readonly import route,ROOT
specs=[(668,23,24,0),(670,53,1,1),(671,10,32,2),(672,49,1,3),(674,109,34,4),(673,92,8,5)]
results=[]
for mid,pe,se,stage in specs:
 v=json.loads(subprocess.check_output(['ruby',str(ROOT/'scripts/route_map.rb'),str(mid),'0','0',json.dumps({'variables':{'377':stage},'reset_positions':True})],stderr=subprocess.DEVNULL))
 a=v['events'].pop(str(pe));b=v['events'].pop(str(se));stone_blocked={(e['x'],e['y']) for e in v['events'].values() if not e['through']};v['position']=[-1,-1];g=route(v,None,True)
 pos=(a['x'],a['y']);other=(b['x'],b['y']);goals=[c['parameters'][3]for c in a['list']if c['code']==111 and c['parameters'][:2]in [[1,47],[1,48]]];goal=(tuple(goals[:2]),tuple(goals[2:]))
 dirs=[('up',0,-1),('down',0,1),('left',-1,0),('right',1,0)]
 def reach(start,p,o):
  seen={start};todo=[start]
  for x in todo:
   for _,n in g.get(x,[]):
    if n not in seen and n not in [p,o]:seen.add(n);todo.append(n)
  return seen
 roots=[(pos[0]-dx,pos[1]-dy) for k,dx,dy in dirs if any(kk==k and n==pos for kk,n in g.get((pos[0]-dx,pos[1]-dy),[]))]
 assert roots
 start=(pos,other,roots[0]);q=deque([(start,[])]);seen=set();solution=None
 while q:
  (p,o,player),path=q.popleft()
  if (p,o)==goal:solution=path;break
  accessible=reach(player,p,o);key=(p,o,min(accessible))
  if key in seen:continue
  seen.add(key)
  assert len(seen)<150000,'Bound reached'
  for k,dx,dy in dirs:
   before=(p[0]-dx,p[1]-dy)
   if before not in accessible:continue
   pn=next((n for kk,n in g.get(p,[])if kk==k and n!=o and n not in stone_blocked),p)
   on=next((n for kk,n in g.get(o,[])if kk==k and n!=pn and n not in stone_blocked),o)
   if (pn,on)==(p,o):continue
   step={'direction':k,'primary_before':p,'primary_after':pn,'secondary_before':o,'secondary_after':on,'stand':before}
   q.append(((pn,on,before),path+[step]))
 assert solution,(mid,len(seen),'No solution')
 r={'map':mid,'event':pe,'partner':se,'stage':stage,'goals':goals,'states':len(seen),'steps':solution};results.append(r)
 print(mid,len(solution),len(seen),flush=True)
 (ROOT/'work/243-mirage-solved.json').write_text(json.dumps(results,indent=2)+'\n')
