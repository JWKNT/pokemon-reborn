"""Reviewed exterior metal plate, service entrance, Bennett choice and wakeup.
Route notes only mirror visibly completed source transitions; no game writes.
"""
from play import *
from locate import locate

def run(s,*a):subprocess.run([sys.executable,str(ROOT/'scripts'/(s+'.py')),*map(str,a)],check=True)
def stage(n):
 p=ROOT/'notes/navigation-state.json';v=json.loads(p.read_text());v['variables']['391']=n;p.write_text(json.dumps(v))
if '--bennett-active' not in sys.argv:
 run('eventq',731,3,'enter')
 run('eventq',715,70,'talk');run('linear_dialog',715,70,'--active','--burst');stage(7)
 # Installed plate event requires approach from west, facing right.
 run('eventq',715,72,'talk');run('linear_dialog',715,72,'--active','--burst','--world-settle',15);stage(9)
 run('eventq',715,83,'talk');run('linear_dialog',715,83,'--active','--burst');stage(10)
 run('eventq',715,63,'enter')
 run('eventq',733,1,'talk');run('linear_dialog',733,1,'--active','--burst');stage(12)
 run('eventq',733,6,'enter')
 # Walking to elevator landing starts the installed Bennett scene.
 p=ROOT/'notes/route-next.json';p.write_text(json.dumps([[733,0,0,28,40,[]]]))
 run('queue_route',p)
run('choose_dialog','To be stronger than anyone|To win Luna|To make things different|No','To make things different','--source',733,9)
run('linear_dialog',733,9,'--active','--past-choice','--world-settle',20);stage(13)
print('GLASS WAKEUP READY',locate(733),flush=True)
