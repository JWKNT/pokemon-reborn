"""Push the rail-room boulder normally; verify its exact position from a normal save."""
from nav import *
import ast
key=sys.argv[1];count=int(sys.argv[2]);label=sys.argv[3];assert key in ['up','down','left','right'] and 1<=count<=4
v=json.loads(subprocess.check_output(['ruby',str(ROOT/'scripts/route_map.rb'),'790','0','0'],stderr=subprocess.DEVNULL));e=v['events']['31'];assert 'pbPushThisBoulder' in str(e['list']);dx,dy={'up':(0,-1),'down':(0,1),'left':(-1,0),'right':(1,0)}[key];x,y=e['x'],e['y'];expected=[x+count*dx,y+count*dy]
tree=ast.parse((ROOT/'scripts/nav.py').read_text());fun=next(n for n in tree.body if isinstance(n,ast.FunctionDef)and n.name=='route');ns=dict(ROOT=ROOT,json=json,heapq=heapq,re=re);exec(ast.unparse(fun).replace('graph = {}','jumps = {}; graph = {}').replace('native_jump = terrain(n) == 1','native_jump = False'),ns)
vv=json.loads(json.dumps(v));vv['events'].pop('31');g=ns['route'](vv,None,True);cursor=(x,y)
for _ in range(count):
 dest=cursor[0]+dx,cursor[1]+dy;assert (key,dest)in g.get(cursor,[]);cursor=dest
subprocess.run([sys.executable,str(ROOT/'scripts/q.py'),f'790,{x-dx},{y-dy}'],check=True)
seq=[]
for j in range(count):
 seq += [key+':.12','wait:.55']
 if j<count-1:seq += [key+':.12','wait:.2']
act(*seq)
subprocess.run([sys.executable,str(ROOT/'scripts/checkpoint.py'),label],check=True)
n=json.loads((ROOT/'notes/navigation-state.json').read_text());assert n['positions']['790']['31']==expected,(n['positions']['790']['31'],expected)
print('RAIL BOULDER VERIFIED',expected,flush=True)
