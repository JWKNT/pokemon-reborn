"""Operate a reviewed Railnet lever through UI; update navigation model only."""
from play import *
eid,target=map(int,sys.argv[1:3]);assert eid in [17,26,46,57,66,86,117,135,144] and target in [1,2]
for n in range(3):
 v=json.loads(subprocess.check_output(['ruby',str(ROOT/'scripts/route_map.rb'),'228','1','3'],stderr=subprocess.DEVNULL))
 assignments=[c['parameters'] for c in v['events'][str(eid)]['list'] if c['code']==122]
 assert len(assignments)==1
 a=assignments[0];assert a[0]==a[1] and a[2:4]==[0,0]
 if n==0:subprocess.run([sys.executable,str(ROOT/'scripts/eventq.py'),'228',str(eid),'talk'],check=True)
 else:act('c','wait:1.0');print(read(),flush=True)
 statepath=ROOT/'notes/navigation-state.json';state=json.loads(statepath.read_text());state.setdefault('variables',{})[str(a[0])]=a[4];statepath.write_text(json.dumps(state))
 print('LEVER',eid,'planned state',a[4],'target',target,flush=True)
 if a[4]==target:break
else:raise SystemExit('Lever cycle review')
