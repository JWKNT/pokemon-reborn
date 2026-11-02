"""Reviewed companion swap and central pallet relayout; ordinary controls only."""
from play import *
from glass_positions import refresh

def run(s,*a):subprocess.run([sys.executable,str(ROOT/'scripts'/(s+'.py')),*map(str,a)],check=True)
run('eventq',732,65,'talk')
run('checkpoint','Glass-central-Espeon-rejoined')
v=json.loads((ROOT/'notes/navigation-state.json').read_text());assert v['switches'].get('947') and not v['switches'].get('946')
assert (v['variables']['404'],v['variables']['405'])==(41,22)
p=ROOT/'notes/navigation-state.json';p.write_text(json.dumps(refresh(v,json.loads((ROOT/'work/story-map-732-events.json').read_text()))))
for core,direction in [(157,'left'),(153,'down'),(157,'right')]:run('glass_pallet',core,direction)
p=ROOT/'notes/route-next.json';p.write_text(json.dumps([[732,0,0,43,15,[]],[732,0,0,43,16,[]]]));run('queue_route',p)
run('glass_companion_wait','Espeon',43,15,'up')
run('checkpoint','Glass-upper-Espeon-waiting')
v=json.loads((ROOT/'notes/navigation-state.json').read_text());assert not v['switches'].get('947') and (v['variables']['406'],v['variables']['407'])==(43,15)
print('UPPER RELAYOUT COMPLETE; ESPEON WAITING43,15',flush=True)
