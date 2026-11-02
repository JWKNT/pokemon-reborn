"""Normal PC exchange and verified Fly for pre-Saphira preparation."""
import subprocess,sys,os
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
os.environ['REBORN_COORD_CACHE']='1'
def run(s,*a,fast=False):
 print('STAGE',s,*a,flush=True)
 env=dict(os.environ)
 if fast:env['REBORN_FAST_KEYS']='1'
 subprocess.run([sys.executable,str(ROOT/'scripts'/(s+'.py')),*map(str,a)],check=True,cwd=ROOT,env=env)
run('pc_open_reviewed')
run('pc_exchange_named',6,5,'Tranquill','Kricketune')
run('eventq',772,8,'enter',fast=True)
run('fly_to',355,'--carrier','Tranquill')
run('checkpoint','Saphira163-Circus-preparation')
