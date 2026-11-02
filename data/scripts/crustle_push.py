"""Push an observed sleeping Crustle in one batch; verify player displacement."""
from nav import *
from locate import locate
m,eid=int(sys.argv[1]),int(sys.argv[2]);direction=sys.argv[3];count=int(sys.argv[4]);assert 1<=count<=20
v=json.loads(subprocess.check_output(['ruby',str(ROOT/'scripts/route_map.rb'),str(m),'0','0'],stderr=subprocess.DEVNULL));e=v['events'][str(eid)];x,y=e['x'],e['y']
assert 'pbPushThisBoulder' in str(e['list'])
dx,dy={'up':(0,-1),'down':(0,1),'left':(-1,0),'right':(1,0)}[direction]
if m in [358,360]:
 ground=json.loads((ROOT/'notes/navigation-state.json').read_text()).get('switches',{}).get('410',False)
 subprocess.run([sys.executable,str(ROOT/'scripts/layer_walk.py'),str(m),str(x-dx),str(y-dy),str(int(ground))],check=True)
else:
 subprocess.run([sys.executable,str(ROOT/'scripts/q.py'),f'{m},{x-dx},{y-dy}'],check=True)
# Installed Route2 cliff scripts move farther than an ordinary push.
cliffs={(360,198,40,88,'down'):2,(360,198,39,95,'down'):2,(360,123,27,84,'down'):2,(360,123,25,88,'down'):3,(360,137,44,87,'down'):4}
cx,cy=x,y
for j in range(count):
 expected=(cx-dx,cy-dy)
 distance=cliffs.get((m,eid,cx,cy,direction),1)
 if distance>1:assert j==count-1,'Split a sequence at each cliff'
 cx+=dx*distance;cy+=dy*distance
seq=[direction,'c','wait:0.6']
for _ in range(count-1):seq += [direction,'c','wait:0.6']
act(*seq);t=read();print(t,flush=True)
if any(label in t.lower() for label in ['bishop','knight','rook','queen']):raise SystemExit('PROMOTION REVIEW')
mm,xx,yy=locate(m)
assert mm==m and (xx,yy)==expected,((mm,xx,yy),expected)
p=ROOT/'notes/navigation-state.json';s=json.loads(p.read_text());s.setdefault('positions',{}).setdefault(str(m),{})[str(eid)]=[cx,cy];p.write_text(json.dumps(s))
print('PUSH POSITION VERIFIED',eid,s['positions'][str(m)][str(eid)],flush=True)
