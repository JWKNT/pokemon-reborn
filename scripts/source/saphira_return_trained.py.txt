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
for mid,eid in [(772,8),(414,50),(768,81),(768,110),(776,5),(776,45),(776,53),(777,5),(777,45),(777,37),(778,5)]:
 run('eventq',mid,eid,'enter')
run('eventq',778,18,'talk')
run('heal')
run('checkpoint','Saphira-return-trained-ready')
