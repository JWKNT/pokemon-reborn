"""Push an observed cardinal chess piece in one batch; verify player displacement."""
from nav import *
from locate import locate
m,eid=int(sys.argv[1]),int(sys.argv[2]);direction=sys.argv[3];count=int(sys.argv[4]);assert 1<=count<=8
v=json.loads(subprocess.check_output(['ruby',str(ROOT/'scripts/route_map.rb'),str(m),'0','0'],stderr=subprocess.DEVNULL));e=v['events'][str(eid)];x,y=e['x'],e['y']
assert 'pbPushThisObject' in str(e['list'])
dx,dy={'up':(0,-1),'down':(0,1),'left':(-1,0),'right':(1,0)}[direction]
subprocess.run([sys.executable,str(ROOT/'scripts/q.py'),f'{m},{x-dx},{y-dy}'],check=True)
seq=[direction,'c','wait:0.35']
for _ in range(count-1):seq += [direction,'c','wait:0.35']
act(*seq);t=read();print(t,flush=True)
if any(label in t.lower() for label in ['bishop','knight','rook','queen']):raise SystemExit('PROMOTION REVIEW')
mm,xx,yy=locate(m);expected=(x+(count-2)*dx,y+(count-2)*dy)
assert mm==m and (xx,yy)==expected,((mm,xx,yy),expected)
p=ROOT/'notes/navigation-state.json';s=json.loads(p.read_text());s.setdefault('positions',{}).setdefault(str(m),{})[str(eid)]=[x+count*dx,y+count*dy];p.write_text(json.dumps(s))
print('PUSH POSITION VERIFIED',eid,s['positions'][str(m)][str(eid)],flush=True)
