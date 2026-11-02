"""Execute reviewed Panaceance mushroom transitions through normal controls."""
from play import *
def run(s,*a):subprocess.run([sys.executable,str(ROOT/'scripts'/(s+'.py')),*map(str,a)],check=True)
def go(x,y):
 q=ROOT/'work/319-mushroom-route.json';q.write_text(json.dumps([[879,0,0,x,y,[]]]));run('queue_route',q)
target=sys.argv[1]
go(38,105);run('checkpoint',f'Idyll319-{target}Entry')
v=json.loads((ROOT/f'notes/Idyll319-{target}Entry-navigation.json').read_text())['switches'];ids=['1763','1770','1771'];active=[i for i,k in enumerate(ids)if v.get(k)];assert len(active)<=1
run('panaceance_mushroom_plan',38,105,active[0]if active else 3,int(bool(v.get('1773'))),target)
plan=json.loads((ROOT/'work/319-mushroom-plan.json').read_text())
for i,st in enumerate([a for a in plan['steps']if a['before'][2:]!=a['after'][2:]],1):
 if st['key']=='orb':
  run('eventq',879,207,'talk');act('wait:10')
 else:go(*st['after'][:2])
 act('wait:2');tag=f'Idyll319-{target}Mushroom{i}';run('checkpoint',tag)
 v=json.loads((ROOT/f'notes/{tag}-navigation.json').read_text())['switches'];assert all(bool(v.get(k))==(j==st['after'][2])for j,k in enumerate(ids));assert bool(v.get('1773'))==st['after'][3]
 print('VERIFIED',st['after'],flush=True)
if target=='flower':
 run('eventq',879,180,'item');run('checkpoint','Idyll319-Gracidea4')
