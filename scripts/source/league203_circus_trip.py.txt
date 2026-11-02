"""Leave the psychologist by normal verified transfers."""
import subprocess,sys,os
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def run(s,*a):
 print('STAGE',s,*a,flush=True)
 env=dict(os.environ,REBORN_COORD_CACHE='1')
 env.pop('REBORN_FAST_KEYS',None)
 if s in ['q','eventq']:env['REBORN_FAST_KEYS']='1'
 subprocess.run([sys.executable,str(R/'scripts'/(s+'.py')),*map(str,a)],check=True,cwd=R,env=env)
run('eventq',326,1,'enter')
run('eventq',324,1,'enter')
run('eventq',168,12,'enter')
run('eventq',168,18,'talk')
run('choose_dialog','7th Street|Lapis Ward','Lapis Ward')
run('dialog','--limit=5')
run('checkpoint','Prep203-Seventh-exit')
run('eventq',168,11,'enter')
run('eventq',168,2,'enter')
run('fly_to',355,'--carrier','Tranquill')
run('eventq',355,118,'talk')
run('heal')
run('checkpoint','Prep203-Circus-ready')
run('league202_candy_rounds',1,3,'Prep203-Circus-ready')
