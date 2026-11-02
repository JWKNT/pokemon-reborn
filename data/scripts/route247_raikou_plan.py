"""Pure walking connectivity across installed Route 1 maps; no UI imports."""
from route_readonly import route,ROOT
import json,collections,sys
mids=[290,286,285,287,291,292,289,288]
maps={m:json.loads((ROOT/f'work/247-map{m}.json').read_text())for m in mids}
if '--mounted' in sys.argv:
 for v in maps.values():v['mounted']=True
graphs={m:route(v,None,True)for m,v in maps.items()}
conns=collections.defaultdict(list)
for a,ax,ay,b,bx,by in json.loads((ROOT/'work/map-connections-reviewed.json').read_text()):
 if a in maps and b in maps:
  conns[a].append((b,ax,ay,bx,by));conns[b].append((a,bx,by,ax,ay))
start=tuple(map(int,sys.argv[sys.argv.index('--start')+1].split(','))) if '--start' in sys.argv else ((286,23,26) if '--mounted' in sys.argv else (290,20,19));goal=(287,69,13)
queue=collections.deque([start]);prev={start:None};move={}
while queue:
 n=queue.popleft();mid,x,y=n;v=maps[mid]
 if n==goal:break
 opts=[((mid,*p),k)for k,p in graphs[mid].get((x,y),[])]
 for k,dx,dy in [('up',0,-1),('down',0,1),('left',-1,0),('right',1,0)]:
  if 0<=x+dx<v['width'] and 0<=y+dy<v['height']:continue
  for dest,ax,ay,bx,by in conns[mid]:
   tx,ty=x+dx-ax+bx,y+dy-ay+by
   if graphs[dest].get((tx,ty)):opts.append(((dest,tx,ty),k))
 for dst,k in opts:
  if dst not in prev:prev[dst]=n;move[dst]=k;queue.append(dst)
if goal not in prev:
 print('NO WALKING PATH',len(prev),'reachable maps',collections.Counter(m for m,x,y in prev))
else:
 seq=[];n=goal
 while prev[n] is not None:seq.append({'from':prev[n],'to':n,'key':move[n]});n=prev[n]
 seq.reverse();(ROOT/'work/247-raikou-walking-plan.json').write_text(json.dumps(seq,indent=2)+'\n')
 print('WALKING PATH',len(seq),'crossings',[v for v in seq if v['from'][0]!=v['to'][0]])
