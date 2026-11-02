"""One source-reviewed map784 push without a destination inspection pause.

The frozen normal save supplies the boulder position. Walking and pushing form
one continuous key queue so icicles cannot strike during a destination pause.
A fresh normal save must confirm the exact boulder outcome before any next push.
"""
from nav import *
from hazard_position import party_position
E=int(sys.argv[1]);key=sys.argv[2];assert E in [69,70,71,72,73,75,79,80,135,*range(82,105)]
dx,dy={'up':(0,-1),'down':(0,1),'left':(-1,0),'right':(1,0)}[key]
m,sx,sy=party_position();assert m==784
v=json.loads(subprocess.check_output(['ruby',str(ROOT/'scripts/route_map.rb'),'784',str(sx),str(sy)],stderr=subprocess.DEVNULL));e=v['events'][str(E)];assert e['name']=='Boulder' and 'pbPushThisBoulder' in str(e['list'])
other_boxes={i:[ev['x'],ev['y']] for i,ev in v['events'].items() if ev['name']=='Boulder' and i!=str(E)}
count=int(sys.argv[4]) if len(sys.argv)>4 else 1
assert 1<=count<=10
before=(e['x']-dx,e['y']-dy);expected=[e['x']+count*dx,e['y']+count*dy]
wall_burst=len(sys.argv)>4
if wall_burst:
 import ast
 assert E==73, 'Only source-reviewed SW boulder permits wall bursts'
 tree=ast.parse((ROOT/'scripts/nav.py').read_text());fun=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='route')
 pure=ast.unparse(fun).replace('graph = {}','jumps = {}; graph = {}').replace('native_jump = terrain(n) == 1','native_jump = False')
 boxns=dict(ROOT=ROOT,json=json,heapq=heapq,re=re);exec(pure,boxns)
 vv=json.loads(json.dumps(v));vv['events'].pop(str(E));bg=boxns['route'](vv,None,True)
 assert not any(k==key for k,n in bg.get(tuple(expected),[])), 'No physical wall at planned stop'
 blocked={(ev['x'],ev['y']) for ev in vv['events'].values() if not ev['through']}
 cursor=(e['x'],e['y'])
 for _ in range(count):
  dest=(cursor[0]+dx,cursor[1]+dy);assert (key,dest) in bg.get(cursor,[]) and dest not in blocked
  cursor=dest

p=route(v,before);assert len(p)<=110;g=route(v,None,True);cursor=(sx,sy);seq=[]
for k in p:
 target=next(n for kk,n in g[cursor] if kk==k)
 if k.startswith('jump:'):seq += [k[5:]+':.12','wait:'+str(max(.9,.2*(abs(target[0]-cursor[0])+abs(target[1]-cursor[1]))))]
 else:seq += [k+':.12']
 cursor=target
assert cursor==before
seq += ['wait:.3',key+':'+str(count*.65+.7 if wall_burst else .2),'wait:1.0'];print('BOULDER APPROACH',E,(sx,sy),before,p,expected,flush=True);act('x','wait:.8','x','wait:.2',*seq)
label=sys.argv[3];assert re.fullmatch(r'[A-Za-z0-9-]+',label)
subprocess.run([sys.executable,str(ROOT/'scripts/checkpoint.py'),label],check=True)
subprocess.run([sys.executable,str(ROOT/'scripts/party_open.py')],check=True)
s=json.loads((ROOT/'notes/navigation-state.json').read_text());assert s['positions']['784'][str(E)]==expected,('Push differs; inspect before retrying',s['positions']['784'][str(E)],expected)
print('HAZARD PUSH VERIFIED',E,expected,flush=True)

assert all(s['positions']['784'][i]==p for i,p in other_boxes.items()),'Another boulder moved: review entire current maze before continuing'
