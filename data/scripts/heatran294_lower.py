"""Source-reviewed normal Rock Climb and connected ice-map approach."""
from play import *
from locate import locate
def run(n,*a):subprocess.run([sys.executable,str(ROOT/'scripts'/f'{n}.py'),*map(str,a)],check=True)
run('surface_event',387,32,'talk')
t=read();assert 'yes' in t.lower() and 'no' in t.lower(),t
run('choose_dialog','Yes|No','Yes');act('c','wait:5')
print('CLIMB LANDING',locate(),flush=True)
run('play','down:.12','wait:1')
run('checkpoint','Heatran294-LowerIce')
