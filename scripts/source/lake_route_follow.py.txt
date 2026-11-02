"""Follow a reviewed static lake plan with ordinary inputs and verified transfers."""
from play import *
from locate import locate
steps=json.loads(pathlib.Path(sys.argv[1]).read_text());assert steps
assert locate(steps[0]['from'][0])==tuple(steps[0]['from'][:3]),'Plan start changed'
def travel(p):
 m,x,y=p[:3]
 if m in [567,565,538]:cmd=['surface_walk.py',str(m),str(x),str(y),'--hold-straights']
 elif m in [553,547,558]:cmd=['q.py',f'{m},{x},{y}']
 else:raise ValueError('Unreviewed lake map')
 env=os.environ.copy();env['REBORN_ROUTE_HELD']='1'
 subprocess.run([sys.executable,str(ROOT/'scripts'/cmd[0]),*cmd[1:]],env=env,check=True)
for s in steps:
 k=s['key']
 if k not in ['surface','dive']and not k.startswith('connect:'):continue
 travel(s['from']);m,x,y=s['from'][:3];dest=s['to']
 if k.startswith('connect:'):
  act(k.split(':')[1]+':.12','wait:1.2');actual=locate(dest[0])
  assert actual==tuple(dest[:3]),f'Connection review: {actual}, expected {dest[:3]}'
 else:subprocess.run([sys.executable,str(ROOT/'scripts/dive_transition.py'),str(m),str(x),str(y),str(dest[0])],check=True)
travel(steps[-1]['to']);print('LAKE PLAN COMPLETE',steps[-1]['to'],flush=True)
