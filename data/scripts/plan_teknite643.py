"""Offline multi-boulder route search for the installed Teknite ridge."""
import json,copy,sys
from collections import deque
from route_readonly import route,ROOT
v=json.loads((ROOT/'work/223-map643.json').read_text())
ids=['1','2','3','4'];initial=tuple((v['events'][i]['x'],v['events'][i]['y']) for i in ids)
for i in ids:v['events'].pop(i)
g=route(v,None,True)
def flood(p,boxes):
 blocked=set(boxes);seen={p};q=deque([p])
 while q:
  for key,n in g.get(q.popleft(),[]):
   if n not in blocked and n not in seen:seen.add(n);q.append(n)
 return seen
start=(37,21);goal=(8,19);todo=deque([(start,initial,[])]);visited=set()
while todo:
 p,boxes,steps=todo.popleft();reach=flood(p,boxes);state=(min(reach),boxes)
 if state in visited:continue
 visited.add(state)
 if goal in reach:
  result={'map':643,'start':start,'goal':goal,'initial':dict(zip(ids,initial)),'pushes':steps,'states':len(visited)}
  print(json.dumps(result,indent=2));(ROOT/'work/223-teknite643-boulder-plan.json').write_text(json.dumps(result,indent=2)+'\n');break
 assert len(visited)<20000,'Search bound'
 for i,b in enumerate(boxes):
  if b==(-1,-1):continue
  for dx,dy,key in [(0,1,'down'),(-1,0,'left'),(1,0,'right'),(0,-1,'up')]:
   before=(b[0]-dx,b[1]-dy);after=(b[0]+dx,b[1]+dy)
   if before not in reach or after in boxes:continue
   drop=ids[i]=='2' and key=='down'
   if not drop and (key,after) not in g.get(b,[]):continue
   nxt=list(boxes);nxt[i]=(-1,-1) if drop else after
   todo.append((before,tuple(nxt),steps+[{'event':int(ids[i]),'from':before,'direction':key,'box_from':b,'box_to':None if drop else after,'erased_drop':drop}]))
else:raise SystemExit('No reviewed push route')
