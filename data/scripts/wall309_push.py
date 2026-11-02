"""One planned ordinary Strength push on Wasteland Wall, verified by quicksave."""
from nav import *
eid=int(sys.argv[1]);key=sys.argv[2];label=sys.argv[3]
assert key in ['up','down','left','right']
v=json.loads(subprocess.check_output(['ruby',str(ROOT/'scripts/route_map.rb'),'277','0','0'],stderr=subprocess.DEVNULL));e=v['events'][str(eid)]
assert e['name']=='Boulder' and 'pbPushThisBoulder' in str(e['list'])
dx,dy={'up':(0,-1),'down':(0,1),'left':(-1,0),'right':(1,0)}[key];x,y=e['x'],e['y']
subprocess.run([sys.executable,str(ROOT/'scripts/q.py'),f'277,{x-dx},{y-dy}'],check=True)
act(key+':.12','wait:.7')
subprocess.run([sys.executable,str(ROOT/'scripts/checkpoint.py'),label],check=True)
n=json.loads((ROOT/'notes/navigation-state.json').read_text());expected=[x+dx,y+dy]
assert n['positions']['277'][str(eid)]==expected,(n['positions']['277'][str(eid)],expected)
print('NORMAL PUSH VERIFIED',eid,expected,flush=True)
