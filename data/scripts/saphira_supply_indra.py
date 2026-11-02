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
run('eventq',611,1,'enter')
run('fly_to',355,'--carrier','Tranquill')
run('eventq',355,118,'talk')
run('heal')
run('checkpoint','Saphira-before-Indra')
run('saphira_indra_candy')
run('checkpoint','Saphira-Indra-candies')
