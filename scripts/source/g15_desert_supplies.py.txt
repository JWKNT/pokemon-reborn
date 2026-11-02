"""Reviewed foot/train departure and main-route desert pickups, no runtime edits."""
from play import *
from locate import locate
def r(s,*a):subprocess.run([sys.executable,str(ROOT/'scripts'/(s+'.py')),*map(str,a)],check=True)
def note(variables=None,switches=None):
 p=ROOT/'notes/navigation-state.json';v=json.loads(p.read_text())
 for group,values in [('variables',variables),('switches',switches)]:
  if values:v[group].update({str(k):val for k,val in values.items()})
 p.write_text(json.dumps(v))
m,x,y=locate();assert m==694
note({360:1},switches={827:True,829:False})
r('use_field_item','Super Repel');r('eventq',m,34,'item');note(switches={813:True})
if m==694:r('eventq',m,89,'item');r('mark_event',m,89)
elif m==705:r('eventq',m,95,'item');r('mark_event',m,95)
else:raise SystemExit('Alternate layout lacks planned seed: inspect legitimate pickup route')
r('eventq',m,26,'item');r('mark_event',m,26)
r('checkpoint','Desert-castle-supplies-ready')
r('city_enter',m,687);r('eventq',687,15,'enter')
r('room_plan','--maps','664,663','--start','664,52,44','--goal','663,22','--output','work/g15-scrap-entry-room-plan.json')
print('DESERT SUPPLIES + SCRAP CAR ENTRY COMPLETE',flush=True)
