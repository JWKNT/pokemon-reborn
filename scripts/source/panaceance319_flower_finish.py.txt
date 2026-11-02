"""Finish the verified southwest orb route after its full camera animation."""
from play import *
def run(s,*a):subprocess.run([sys.executable,str(ROOT/'scripts'/(s+'.py')),*map(str,a)],check=True)
ids=['1763','1770','1771']
for i,(x,y,s)in enumerate([(7,130,2),(18,133,1),(36,131,2)],8):
 q=ROOT/'work/319-sw-finish-route.json';q.write_text(json.dumps([[879,0,0,x,y,[]]]));run('queue_route',q);act('wait:2')
 tag=f'Idyll319-flowerMushroom{i}';run('checkpoint',tag);v=json.loads((ROOT/f'notes/{tag}-navigation.json').read_text())['switches'];assert v.get('1773')and all(bool(v.get(k))==(j==s)for j,k in enumerate(ids))
run('eventq',879,180,'item');run('checkpoint','Idyll319-Gracidea4')
