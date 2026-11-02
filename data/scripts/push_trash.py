"""Push one reviewed WTC trash pile, verifying movement before updating notes."""
from play import *
from locate import locate
mid,eid=int(sys.argv[1]),int(sys.argv[2]);key=sys.argv[3];count=int(sys.argv[4])
assert mid in range(468,479) and 1<=count<=6
dx,dy={'up':(0,-1),'down':(0,1),'left':(-1,0),'right':(1,0)}[key]
m,x,y=locate(mid);assert m==mid
v=json.loads(subprocess.check_output(['ruby',str(ROOT/'scripts/route_map.rb'),str(mid),str(x),str(y)],stderr=subprocess.DEVNULL))
e=v['events'][str(eid)];assert e['name']=='block'
assert any(c['code']==209 and c['parameters'][0]==0 and any(z['code']==11 for z in c['parameters'][1]['list'])for c in e['list'])
start=(e['x']-dx,e['y']-dy)
statefile=ROOT/'notes/navigation-state.json';s=json.loads(statefile.read_text())
subprocess.run([sys.executable,str(ROOT/'scripts/layer_walk.py'),str(mid),str(start[0]),str(start[1]),str(int(s['switches'].get('410',False))),'1'],check=True)
s=json.loads(statefile.read_text());assert s['switches']['410'],'Trash can only be pushed from the floor'
act(key+':.12')
for _ in range(count):
 act('c','wait:.5',key+':.12','wait:.3')
 t=read().lower();print(t,flush=True)
 if len(t.splitlines())>3 or any(z in t for z in ['fight','yes','no\n','hp']):raise SystemExit('Trash interaction needs review')
actual=locate(mid);expected=(mid,start[0]+dx*count,start[1]+dy*count)
assert actual==expected,('Push displacement needs review',actual,expected)
s=json.loads(statefile.read_text());s.setdefault('positions',{}).setdefault(str(mid),{})[str(eid)]=[e['x']+dx*count,e['y']+dy*count]
statefile.write_text(json.dumps(s))
print('TRASH PUSH VERIFIED',eid,count,actual,flush=True)
