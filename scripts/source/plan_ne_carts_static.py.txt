"""Offline NE minecart and boulder model from installed public puzzle source."""
import ast,json,heapq,re,subprocess,copy,pickle
from pathlib import Path
from collections import deque
from static_cart_model import cart_transition
R=Path(__file__).resolve().parents[1];ns=dict(ROOT=R,json=json,heapq=heapq,re=re)
t=ast.parse((R/'scripts/nav.py').read_text());f=next(n for n in t.body if isinstance(n,ast.FunctionDef)and n.name=='route');exec(compile(ast.Module(body=[f],type_ignores=[]),'route','exec'),ns)
bn=dict(ROOT=R,json=json,heapq=heapq,re=re);exec(ast.unparse(f).replace('graph = {}','jumps = {}; graph = {}').replace('native_jump = terrain(n) == 1','native_jump = False'),bn)
ids=[133,140,141];vs=[493,494,495];positions=[{0:(103,29),1:(99,23)},{0:(116,32),1:(106,29),2:(109,21)},{0:(105,19),1:(94,17),2:(96,20)}];commands=[json.loads((R/f'work/192-ne-cart{i}.json').read_text())['pages'][1]['list']for i in ids]
graphs=[];bgraphs=[]
for mask in range(8):
 ex={'switches':{str(1123+i):bool(mask&(1<<i))for i in range(3)}};v=json.loads(subprocess.check_output(['ruby',str(R/'scripts/route_map.rb'),'784','114','32',json.dumps(ex)],stderr=subprocess.DEVNULL));events=copy.deepcopy(v['events'])
 for i in ids+[135]:v['events'].pop(str(i),None)
 graphs.append(ns['route'](v,None,True));bgraphs.append(bn['route'](v,None,True))
q=deque([((114,32),0,(0,0,0),(103,23),[])]);seen=set()
while q:
 p,mask,states,box,plan=q.popleft();g=graphs[mask];cartpos=[positions[i][s]for i,s in enumerate(states)];blocked=set(cartpos+[box]);rr={p};qq=deque([p])
 while qq:
  for k,n in g.get(qq.popleft(),[]):
   if n not in blocked and n not in rr:rr.add(n);qq.append(n)
 key=(min(rr),mask,states,box)
 if key in seen:continue
 seen.add(key)
 if len(seen)>10000:raise SystemExit('Limit')
 adjacent=lambda xy:sorted(rr.intersection({(xy[0]+dx,xy[1]+dy)for dx,dy in [(0,1),(0,-1),(1,0),(-1,0)]}))
 for j,eid in [(0,134),(2,136)]:
  e=events[str(eid)]
  for a in adjacent((e['x'],e['y'])):q.append((a,mask^(1<<j),states,box,plan+[dict(lever=eid,after=not bool(mask&(1<<j)),approach=a)]))
 before=(box[0]-1,box[1]);after=(box[0]+1,box[1])
 if box[0]<106 and before in rr and after not in blocked and ('right',after)in bgraphs[mask].get(box,[]):
  nm=mask|2 if after==(106,23)else mask;q.append((before,nm,states,after,plan+[dict(event=135,direction='right',box_to=after)]))
 for i,eid in enumerate(ids):
  sw={1123+j:bool(mask&(1<<j))for j in range(3)};new,xy,face=cart_transition(commands[i],vs[i],states[i],sw,cartpos[i],True)
  if new==states[i]:continue
  assert positions[i][new]==xy,(eid,states[i],mask,new,xy)
  for a in adjacent(cartpos[i]):
   dest=a if eid==141 else (xy[0]+face[0],xy[1]+face[1])
   pp=plan+[dict(cart=eid,before=states[i],after=new,approach=a,cart_to=xy,player_to=dest)]
   if eid==141 and new==2:
    out=dict(initial_player=[114,32],actions=pp,states=len(seen));(R/'work/192-ne-cart-plan.json').write_text(json.dumps(out,indent=2));print('FOUND',len(pp),'actions',len(seen),'states');raise SystemExit(0)
   newstates=list(states);newstates[i]=new;q.append((dest,mask,tuple(newstates),box,pp))
raise SystemExit('NO SOLUTION '+str(len(seen)))
