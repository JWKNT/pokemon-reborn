"""Collect the ten inspected Underroot cells through normal UI, with public receipts."""
import os
os.environ.update(REBORN_FAST_KEYS='1',REBORN_COORD_CACHE='1',REBORN_ROUTE_CHUNK='56')
from nav import *
from locate import locate
journal=ROOT/'work/381-underroot-cells.json'
j=json.loads(journal.read_text()) if journal.exists() else {'done':[]}
assert not j.get('pending'),'Review interrupted collection before resuming'
for _ in range(10-len(j['done'])):
 mid,x,y=locate(153);assert mid==153
 v=json.loads(subprocess.check_output(['ruby',str(ROOT/'scripts/route_map.rb'),'153',str(x),str(y)],stderr=subprocess.DEVNULL))
 opts=[]
 for eid in range(134,144):
  if eid in j['done']:continue
  e=v['events'][str(eid)]
  assert any(c['code']==117 and c['parameters']==[62] for c in e['list']),('Cell not active',eid)
  for dx,dy in [(0,1),(0,-1),(1,0),(-1,0)]:
   try:opts.append((len(route(v,(e['x']+dx,e['y']+dy))),eid))
   except ValueError:pass
 assert opts,'No reachable remaining cell'
 _,eid=min(opts);j['pending']=eid;journal.write_text(json.dumps(j,indent=2)+'\n')
 subprocess.run([sys.executable,str(ROOT/'scripts/eventq.py'),'153',str(eid),'talk'],check=True)
 t=read();print(t,flush=True)
 assert 'captured' in t.lower() and 'cell' in t.lower(),'Expected public cell receipt'
 act('c','wait:.5');t=read();assert len(t.splitlines())<=3,'Cell completion review'
 p=ROOT/'notes/navigation-state.json';s=json.loads(p.read_text());s.setdefault('self_switches',{})[f'153,{eid},A']=True
 for var in ['590','591']:s['variables'][var]=s['variables'].get(var,0)+1
 p.write_text(json.dumps(s,indent=2)+'\n')
 j['done'].append(eid);j['pending']=None;journal.write_text(json.dumps(j,indent=2)+'\n')
 print('CELL COLLECTED',eid,'total this block',len(j['done']),flush=True)
subprocess.run([sys.executable,str(ROOT/'scripts/checkpoint.py'),'Underroot381-Cells'],check=True)
s=json.loads((ROOT/'notes/Underroot381-Cells-navigation.json').read_text());assert s['variables']['590']>=11
