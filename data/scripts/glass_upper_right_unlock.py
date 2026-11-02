"""Reviewed right bridge, safe companion parking and atrium opening; no door entry."""
from play import *
from locate import locate
from glass_positions import refresh

def run(s,*a):subprocess.run([sys.executable,str(ROOT/'scripts'/(s+'.py')),*map(str,a)],check=True)
def mirror(ss=None,vv=None):
 p=ROOT/'notes/navigation-state.json';v=json.loads(p.read_text());v['switches'].update(ss or {});v['variables'].update(vv or {});p.write_text(json.dumps(refresh(v,json.loads((ROOT/'work/story-map-732-events.json').read_text()))))
def walk(*targets):
 p=ROOT/'notes/route-next.json';p.write_text(json.dumps([[732,0,0,x,y,[]]for x,y in targets]));run('queue_route',p)
if '--blue-park-facing-ready' not in sys.argv:
 run('eventq',732,63,'talk');run('checkpoint','Glass-upper-Blue-rejoined')
 v=json.loads((ROOT/'notes/navigation-state.json').read_text());assert v['switches'].get('946') and not v['switches'].get('947')
 walk((42,15));run('eventq',732,85,'talk');run('linear_dialog',732,85,'--active');mirror(vv={'403':60})
 walk((42,11),(43,11),(42,11));run('glass_companion_wait','Glaceon',43,11,'right')
else:run('glass_companion_wait','Glaceon',43,11,'right','--facing-ready')
walk((42,15));act('right:.12','wait:.3','c','wait:2');print(read(),flush=True)
run('checkpoint','Glass-upper-Espeon-carried')
v=json.loads((ROOT/'notes/navigation-state.json').read_text());assert v['switches'].get('947') and not v['switches'].get('946');assert (v['variables']['404'],v['variables']['405'])==(43,11)
for core,direction in [(170,'right'),(165,'left')]:run('glass_pallet',core,direction)
run('eventq',732,174,'talk');run('linear_dialog',732,174,'--active');mirror(ss={'958':True})
for core,direction in [(157,'left'),(153,'up'),(157,'right'),(165,'right')]:run('glass_pallet',core,direction)
# Stay away from38/39,8, which starts the uninterrupted gauntlet.
run('checkpoint','Glass-atrium-open-before-prep')
v=json.loads((ROOT/'notes/navigation-state.json').read_text());assert v['switches'].get('958') and v['variables']['420']==2
print('ATRIUM OPEN; PREPARE TEAM BEFORE ENTERING DOOR',flush=True)
