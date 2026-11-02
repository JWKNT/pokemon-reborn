"""Normal UI route to restored Seventh Street psychologist."""
import subprocess,sys,os
from pathlib import Path
R=Path(__file__).resolve().parents[1]
os.environ['REBORN_COORD_CACHE']='1'
os.environ.pop('REBORN_FAST_KEYS',None)
def run(s,*a):
 print('STAGE',s,*a,flush=True)
 env=dict(os.environ)
 if s in ['q','eventq']:env.update(REBORN_FAST_KEYS='1',REBORN_ROUTE_CHUNK='112')
 subprocess.run([sys.executable,str(R/'scripts'/(s+'.py')),*map(str,a)],check=True,cwd=R,env=env)
if '--arrived' not in sys.argv:run('fly_to',524,'--carrier','Tranquill')
run('eventq',524,30,'enter')
run('eventq',168,8,'enter')
run('eventq',168,18,'talk')
run('choose_dialog','7th Street|Lapis Ward','7th Street')
run('dialog','--limit=5')
run('checkpoint','Prep203-Seventh-elevator')
run('eventq',168,11,'enter')
run('eventq',168,15,'enter')
run('eventq',324,4,'enter')
run('eventq',326,3,'talk')
run('choose_dialog','Yes|No','Yes')
