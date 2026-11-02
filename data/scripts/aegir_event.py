"""Reach an Aegir event with source-planned bridge levels and normal UI only."""
from layer_route import *
from locate import locate
mid,eid=int(sys.argv[1]),int(sys.argv[2]);kind=sys.argv[3]
assert mid in [849,850] and kind in ['talk','item','enter','smash']
m,x,y=locate(mid);assert m==mid
state=json.loads((ROOT/'notes/navigation-state.json').read_text())
ground=bool(state['switches']['410'])
v=json.loads(subprocess.check_output(['ruby',str(ROOT/'scripts/route_map.rb'),str(mid),str(x),str(y)],stderr=subprocess.DEVNULL))
e=v['events'][str(eid)];choices=[]
for dx,dy in [(0,1),(0,-1),(1,0),(-1,0)]:
 goal=(e['x']+dx,e['y']+dy)
 if any((ee['x'],ee['y'])==goal and any(c['code']==201 for c in ee.get('list')or[]) for ee in v['events'].values()):continue
 try:steps=plan(mid,x,y,ground,*goal);choices.append((len(steps),goal))
 except ValueError:pass
assert choices,'No layered approach to this Aegir event'
_,goal=min(choices)
print('AEGIR LAYER APPROACH',mid,eid,goal,ground,flush=True)
subprocess.run([sys.executable,str(ROOT/'scripts/layer_walk.py'),str(mid),*map(str,goal),str(int(ground)),'--hold-straights'],check=True)
subprocess.run([sys.executable,str(ROOT/'scripts/eventq.py'),str(mid),str(eid),kind],check=True)
