"""Offline SE rail planner from installed map, with normal pushes and levers."""
import ast,json,heapq,re,subprocess,copy,pickle
from pathlib import Path
from collections import deque
R=Path(__file__).resolve().parents[1];ns=dict(ROOT=R,json=json,heapq=heapq,re=re)
t=ast.parse((R/'scripts/nav.py').read_text());f=next(n for n in t.body if isinstance(n,ast.FunctionDef) and n.name=='route');exec(compile(ast.Module(body=[f],type_ignores=[]),'route','exec'),ns)
bn=dict(ROOT=R,json=json,heapq=heapq,re=re);exec(ast.unparse(f).replace('graph = {}','jumps = {}; graph = {}').replace('native_jump = terrain(n) == 1','native_jump = False'),bn)
cache=R/'work/191-se-graphs.pkl'
if cache.exists():graphs,bgraphs,events=pickle.loads(cache.read_bytes())
else:
 graphs=[];bgraphs=[]
 for mask in range(32):
  extra={'switches':{str(1127+i):bool(mask&(1<<i)) for i in range(5)}}
  v=json.loads(subprocess.check_output(['ruby',str(R/'scripts/route_map.rb'),'786','121','43',json.dumps(extra)],stderr=subprocess.DEVNULL));events=v['events']
  vv=copy.deepcopy(v)
  for i in ['63','64','116','65']:vv['events'].pop(i,None)
  graphs.append(ns['route'](vv,None,True));bgraphs.append(bn['route'](vv,None,True))
 cache.write_bytes(pickle.dumps((graphs,bgraphs,events)))
levers=['48','51','60','61','62'];boxids=['116','63','64'];initial=((121,43),14,((121,46),(106,50),(112,49)),False)
q=deque([(initial,[])]);seen=set();directions=[(0,-1,'up'),(-1,0,'left'),(0,1,'down')]
while q:
 (p,mask,boxes,smashed),plan=q.popleft();g=graphs[mask];blocked=set(boxes)|({(112,50)} if not smashed else set());rr={p};qq=deque([p])
 while qq:
  for k,n in g.get(qq.popleft(),[]):
   if n not in rr and n not in blocked:rr.add(n);qq.append(n)
 key=(min(rr),mask,boxes,smashed)
 if key in seen:continue
 seen.add(key)
 if len(seen)>100000:raise SystemExit('Limit')
 adjacent=lambda xy:sorted(rr.intersection({(xy[0]+dx,xy[1]+dy) for dx,dy in [(0,1),(0,-1),(1,0),(-1,0)]}))
 if mask==0 and adjacent((115,65)):
  out=dict(actions=plan,cart_approach=adjacent((115,65))[0],states=len(seen));(R/'work/191-se-solution.json').write_text(json.dumps(out,indent=2));print('FOUND',out,flush=True);break
 for i,eid in enumerate(levers):
  e=events[eid];aa=adjacent((e['x'],e['y']))
  for a in aa:q.append(((a,mask^(1<<i),boxes,smashed),plan+[dict(lever=int(eid),after=not bool(mask&(1<<i)),approach=a)]))
 if not smashed:
  for a in adjacent((112,50)):q.append(((a,mask,boxes,True),plan+[dict(smash=65,approach=a)]))
 for i,(b,(dx,dy,k)) in enumerate(zip(boxes,directions)):
  before=(b[0]-dx,b[1]-dy);after=(b[0]+dx,b[1]+dy)
  if before not in rr or after in blocked or (k,after) not in bgraphs[mask].get(b,[]):continue
  if i==0 and after[1]<44 or i==1 and after[0]<105 or i==2 and after[1]>51:continue
  if any(not e['through'] and (e['x'],e['y'])==after for ei,e in events.items() if ei not in boxids+['65']):continue
  new=list(boxes);new[i]=after
  q.append(((before,mask,tuple(new),smashed),plan+[dict(event=int(boxids[i]),direction=k,box_to=after)]))
else:print('NO SOLUTION',len(seen))
