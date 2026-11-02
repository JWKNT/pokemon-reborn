"""Follow a source-derived mushroom plan; verify every change with ordinary saves."""
from play import *
def run(s,*a):subprocess.run([sys.executable,str(ROOT/'scripts'/(s+'.py')),*map(str,a)],check=True)
def go(x,y):
 q=ROOT/'work/318-mushroom-route.json';q.write_text(json.dumps([[878,0,0,x,y,[]]]));run('queue_route',q)
go(38,105);run('checkpoint','Idyll318-SWEntry')
nav=json.loads((ROOT/'notes/Idyll318-SWEntry-navigation.json').read_text());sw=nav['switches'];assert sw.get('1772') is True and not sw.get('1773',False)
ids=['1763','1770','1771'];active=[i for i,k in enumerate(ids)if sw.get(k)]
assert len(active)<=1
run('idyll_mushroom_plan',38,105,active[0]if active else 3,'shaymin')
plan=json.loads((ROOT/'work/318-mushroom-plan.json').read_text())
changes=[s for s in plan['steps']if s['from'][2:]!=s['to'][2:]]
for i,step in enumerate(changes,1):
 if step['key']=='orb':run('eventq',878,175,'talk')
 else:go(*step['to'][:2])
 act('wait:2');name=f'Idyll318-Mushroom{i}';run('checkpoint',name)
 nav=json.loads((ROOT/'notes'/f'{name}-navigation.json').read_text());sw=nav['switches'];expected=step['to'][2]
 assert all(bool(sw.get(k))==(j==expected)for j,k in enumerate(ids)),f'Mushroom change {i} differs from plan'
 assert bool(sw.get('1773'))==step['to'][3]
 print('VERIFIED MUSHROOM',i,step['to'],flush=True)
run('eventq',878,180,'talk');run('linear_dialog',878,180,'--source-page',0);run('checkpoint','Idyll318-Shaymin5')
