"""Fetch west Glaceon and activate the reviewed upper-left bridge normally."""
from play import *
from locate import locate
from glass_positions import refresh

def run(s,*a):subprocess.run([sys.executable,str(ROOT/'scripts'/(s+'.py')),*map(str,a)],check=True)
def mirror(ss=None,vv=None):
 p=ROOT/'notes/navigation-state.json';v=json.loads(p.read_text());v['switches'].update(ss or {});v['variables'].update(vv or {});p.write_text(json.dumps(refresh(v,json.loads((ROOT/'work/story-map-732-events.json').read_text()))))
p=ROOT/'notes/route-next.json';p.write_text(json.dumps([[732,41,26,18,31,[]]]));run('queue_route',p)
# Waiting Glaceon is19,31; Espeon will become its actual previous player square.
assert locate(732)==(732,18,31)
act('right:.12','wait:.3','c','wait:2');print(read(),flush=True)
run('checkpoint','Glass-Blue-west-rejoined')
v=json.loads((ROOT/'notes/navigation-state.json').read_text());assert v['switches'].get('946') and not v['switches'].get('947')
run('layer_walk',732,35,15,1,1)
run('eventq',732,84,'talk');run('linear_dialog',732,84,'--active')
mirror(vv={'402':60})
run('eventq',732,95,'item');run('eventq',732,62,'talk');run('linear_dialog',732,62,'--active');mirror(ss=None)
# Descend to the clear central holding square; the companion trails one tile.
p.write_text(json.dumps([[732,0,0,41,22,[]],[732,0,0,41,23,[]]]));run('queue_route',p)
print('BLUE AT41,22; PLAYER41,23. INSPECT BEFORE WAIT',flush=True)
