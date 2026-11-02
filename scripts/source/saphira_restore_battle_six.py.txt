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
run('mart_exit')
run('eventq',38,6,'enter')
run('fly_to',414,'--carrier','Tranquill')
run('eventq',414,22,'enter')
run('eventq',772,7,'talk')
run('pc_open_reviewed')
run('pc_exchange_named',12,5,'Excadrill','Tranquill')
run('train_candy_one','Excadrill',5,'XL')
run('checkpoint','Saphira-six-trained')
