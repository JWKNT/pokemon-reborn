"""Continuous normal walking and immediate interaction at the first cart/levers.

Only source-reviewed map784 cart74, levers114/116 and RockClimbs56/120 are allowed. Avoid the
destination coordinate pause that lets an icicle knock Aster out of reach.
The caller verifies resulting puzzle state at a legitimate normal save.
"""
from nav import *
from locate import locate

eid=int(sys.argv[1]);assert eid in [56,74,114,116,120]
mid,sx,sy=locate(784);assert mid==784
v=json.loads(subprocess.check_output(['ruby',str(ROOT/'scripts/route_map.rb'),'784',str(sx),str(sy)],stderr=subprocess.DEVNULL))
e=v['events'][str(eid)];options=[]
for dx,dy,k in [(0,1,'up'),(0,-1,'down'),(1,0,'left'),(-1,0,'right')]:
 p=(e['x']+dx,e['y']+dy)
 try:options.append((len(route(v,p)),p,k,route(v,p)))
 except ValueError:pass
if not options:raise SystemExit('No cart/lever approach')
_,goal,facing,path=min(options);assert len(path)<=100
graph=route(v,None,True);cursor=(sx,sy);seq=[]
for k in path:
 target=next(p for kk,p in graph[cursor] if kk==k)
 if k.startswith('jump:'):
  seq += [k[5:]+':.12','wait:'+str(max(.9,.2*(abs(target[0]-cursor[0])+abs(target[1]-cursor[1]))))]
 else:seq.append(k+':.12')
 cursor=target
assert cursor==goal
seq += [facing+':.3','c','wait:'+('10' if eid==74 else '1')]
print('CONTINUOUS CART ACTION',eid,[sx,sy],goal,len(path),flush=True)
start=time.time();act(*seq);print(read(),flush=True)
with (ROOT/'notes/victory-cart-actions.jsonl').open('a') as f:
 f.write(json.dumps({'start_epoch':start,'end_epoch':time.time(),'event':eid,'from':[sx,sy],'planned_approach':goal,'path':path,'verification':'Pending normal save puzzle flags'})+'\n')
