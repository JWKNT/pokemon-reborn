"""Reviewed foot/train departure and main-route desert pickups, no runtime edits."""
from play import *
from locate import locate
def r(s,*a):subprocess.run([sys.executable,str(ROOT/'scripts'/(s+'.py')),*map(str,a)],check=True)
def note(variables=None,switches=None):
 p=ROOT/'notes/navigation-state.json';v=json.loads(p.read_text())
 for group,values in [('variables',variables),('switches',switches)]:
  if values:v[group].update({str(k):val for k,val in values.items()})
 p.write_text(json.dumps(v))
act('x','wait:.7');m,x,y=locate();assert m==694
r('eventq',m,89,'item');r('mark_event',m,89)
r('eventq',m,26,'item');r('mark_event',m,26)
r('checkpoint','Desert-castle-supplies-ready')
