"""Normal reviewed transfers back through the cleared tournament."""
import subprocess,sys,os
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
os.environ['REBORN_COORD_CACHE']='1'
os.environ['REBORN_FAST_KEYS']='1'
def run(s,*a):
 print('STAGE',s,*a,flush=True)
 subprocess.run([sys.executable,str(ROOT/'scripts'/(s+'.py')),*map(str,a)],check=True,cwd=ROOT)
for mid,eid in [(777,36),(777,8),(777,1),(776,51),(776,7),(776,1)]:run('eventq',mid,eid,'enter')
run('checkpoint','Saphira163-tournament-main-lobby')
