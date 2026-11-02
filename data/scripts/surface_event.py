"""Reach a simple inspected event using the ice/surf path model and ordinary UI."""
from surface_plan import *
from locate import locate
# Four adjacent targets share the same map and save-derived navigation state.
# Cache only these pure graphs within this single event-planning invocation.
import surface_plan as _surface_module
_uncached_route = _surface_module.route
_event_graphs = {}
def _event_route(v, goal, return_graph=False):
 if not return_graph:return _uncached_route(v,goal,return_graph)
 key=repr(v)
 if key not in _event_graphs:_event_graphs[key]=_uncached_route(v,goal,return_graph)
 return _event_graphs[key]
_surface_module.route = _event_route
mid,eid=int(sys.argv[1]),int(sys.argv[2]);kind=sys.argv[3];assert kind in ['talk','item','enter']
m,x,y=locate(mid);assert m==mid
v=json.loads(subprocess.check_output(['ruby',str(ROOT/'scripts/route_map.rb'),str(mid),str(x),str(y)],stderr=subprocess.DEVNULL));e=v['events'][str(eid)];choices=[]
assert not any(c['code'] in [103,104] for c in e.get('list')or[])
for dx,dy,key in [(0,1,'up'),(0,-1,'down'),(1,0,'left'),(-1,0,'right')]:
 goal=(e['x']+dx,e['y']+dy)
 if any((ee['x'],ee['y'])==goal and any(c['code']==201 for c in ee.get('list')or[])for ee in v['events'].values()):continue
 try:r=surface_plan(v,goal);choices.append((sum(1 if ':'not in z['key']else 2 for z in r),goal,key))
 except ValueError:pass
assert choices,'No ice/surface approach'
_,goal,key=min(choices);print('SURFACE EVENT',eid,kind,goal,key,flush=True)
subprocess.run([sys.executable,str(ROOT/'scripts/surface_walk.py'),str(mid),*map(str,goal)]+(['--hold-straights'] if '--hold-straights' in sys.argv else []),check=True)
if kind=='enter':
 assert any(c['code']==201 for c in e.get('list')or[]),'Not a transfer'
 act(key+':.12','wait:2');print(read(),flush=True)
elif kind=='talk':act(key+':.12','wait:.15','c','wait:1');print(read(),flush=True)
else:
 act(key+':.03','wait:.3','c','wait:.8');t=read();print(t,flush=True)
 if not any(z in t.lower()for z in ['found','obtained','put the','put away']):raise SystemExit('Item acquisition review')
 act('x:2.5','wait:.5');print(read(),flush=True)
 subprocess.run([sys.executable,str(ROOT/'scripts/mark_event.py'),str(mid),str(eid)],check=True)
