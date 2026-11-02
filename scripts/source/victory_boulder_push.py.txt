"""Push one map786 Boulder by normal movement, with a verified landing.

Boulder events trigger on bump; C instead opens the Strength explanation.
Activate Strength first. The helper stops if movement differs from prediction.
"""
from nav import *
from locate import locate
m,eid=int(sys.argv[1]),int(sys.argv[2]);direction=sys.argv[3];count=int(sys.argv[4])
assert m==786 and eid in [40,41,63,64,100,116] and 1<=count<=20
v=json.loads(subprocess.check_output(['ruby',str(ROOT/'scripts/route_map.rb'),str(m),'0','0'],stderr=subprocess.DEVNULL));e=v['events'][str(eid)];x,y=e['x'],e['y']
assert e['name']=='Boulder' and 'pbPushThisBoulder' in str(e['list'])
dx,dy={'up':(0,-1),'down':(0,1),'left':(-1,0),'right':(1,0)}[direction]
subprocess.run([sys.executable,str(ROOT/'scripts/q.py'),f'{m},{x-dx},{y-dy}'],check=True)
seq=[]
for j in range(count):
 seq += [direction+':.12','wait:.55']
 if j<count-1:seq += [direction+':.12','wait:.2']
act(*seq);print(read(),flush=True)
actual=locate(m);expected=(m,x+(count-2)*dx,y+(count-2)*dy)
assert actual==expected,('Push displacement differs; inspect before retrying',actual,expected)
p=ROOT/'notes/navigation-state.json';s=json.loads(p.read_text());s.setdefault('positions',{}).setdefault(str(m),{})[str(eid)]=[x+count*dx,y+count*dy];p.write_text(json.dumps(s))
print('OBSERVED PUSH DISPLACEMENT',eid,s['positions'][str(m)][str(eid)],flush=True)
