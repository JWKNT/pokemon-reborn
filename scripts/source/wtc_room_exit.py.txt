"""Use a reviewed WTC connection, including Surf on purified water."""
from play import *
from locate import locate
from layer_route import plan
from surface_plan import surface_plan

mid,desired=map(int,sys.argv[1:3])
selected_event=int(sys.argv[sys.argv.index('--event')+1])if '--event' in sys.argv else None
actual=locate(mid);assert actual[0]==mid
v=json.loads(subprocess.check_output(['ruby',str(ROOT/'scripts/route_map.rb'),str(mid),*map(str,actual[1:])],stderr=subprocess.DEVNULL))
s=json.loads((ROOT/'notes/navigation-state.json').read_text())
# Restored entry hall also requires ordinary Surf across purified water.
surface=mid==467 or 497<=mid<=505
choices=[]
for eid,e in v['events'].items():
 if selected_event is not None and int(eid)!=selected_event:continue
 cs=e['list']or[]
 dest={tuple(c['parameters'][1:4])for c in cs if c['code']==201 and c['parameters'][0]==0}
 if len(dest)!=1 or next(iter(dest))[0]!=desired:continue
 if any(c['code']in[101,102,103,104,355,655,301]for c in cs):continue
 for dx,dy,key in [(0,1,'up'),(0,-1,'down'),(1,0,'left'),(-1,0,'right')]:
  goal=(e['x']+dx,e['y']+dy)
  if any((ee['x'],ee['y'])==goal and any(c['code']==201 for c in ee['list']or[])for ee in v['events'].values()):continue
  try:
   r=surface_plan(v,goal)if surface else plan(mid,*actual[1:],s['switches'].get('410',False),*goal,False)
   choices.append((len(r),int(eid),goal,key,next(iter(dest))))
  except ValueError:pass
assert choices,'No verified room connection'
_,eid,goal,key,dest=min(choices)
print('WTC ROOM CONNECTION',mid,eid,dest,'via',goal,key,flush=True)
if surface:
 subprocess.run([sys.executable,str(ROOT/'scripts/surface_walk.py'),str(mid),*map(str,goal)],check=True)
else:
 subprocess.run([sys.executable,str(ROOT/'scripts/layer_walk.py'),str(mid),*map(str,goal),str(int(s['switches'].get('410',False))),'0'],check=True)
act(key+':.12','wait:2')
assert locate(desired)==dest,'Room transfer needs review'
p=ROOT/'notes/navigation-state.json';s=json.loads(p.read_text());s.get('positions',{}).pop(str(desired),None);p.write_text(json.dumps(s))
print('WTC CONNECTION VERIFIED',dest,flush=True)
