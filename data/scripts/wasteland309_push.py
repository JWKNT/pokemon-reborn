"""One planned ordinary Strength push on Wasteland Wall, verified by quicksave."""
from nav import *
mid=int(sys.argv[1]);eid=int(sys.argv[2]);key=sys.argv[3];count=int(sys.argv[4]);label=sys.argv[5];assert mid in [275,276,277,279] and 1<=count<=20
assert key in ['up','down','left','right']
v=json.loads(subprocess.check_output(['ruby',str(ROOT/'scripts/route_map.rb'),str(mid),'0','0'],stderr=subprocess.DEVNULL));e=v['events'][str(eid)]
assert e['name']=='Boulder' and 'pbPushThisBoulder' in str(e['list'])
dx,dy={'up':(0,-1),'down':(0,1),'left':(-1,0),'right':(1,0)}[key];x,y=e['x'],e['y']
subprocess.run([sys.executable,str(ROOT/'scripts/q.py'),f'{mid},{x-dx},{y-dy}'],check=True)
seq=[]
for i in range(count):
 seq += [key+':.12','wait:.65']
 if i<count-1:seq += [key+':.12','wait:.25']
act(*seq)
subprocess.run([sys.executable,str(ROOT/'scripts/checkpoint.py'),label],check=True)
n=json.loads((ROOT/'notes/navigation-state.json').read_text());expected=[x+count*dx,y+count*dy]
assert n['positions'][str(mid)][str(eid)]==expected,(n['positions'][str(mid)][str(eid)],expected)
print('NORMAL PUSH VERIFIED',eid,expected,flush=True)
