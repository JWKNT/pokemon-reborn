"""Normal-controls Mega Ring errands, ending before any unreviewed battle."""
import subprocess,sys,os,json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def run(n,*a):
 e=dict(os.environ,REBORN_COORD_CACHE='1',REBORN_ROUTE_CHUNK='84')
 if n!='fly_to':e['REBORN_FAST_KEYS']='1'
 else:e.pop('REBORN_FAST_KEYS',None)
 print('STAGE',n,*a,flush=True);subprocess.run([sys.executable,str(R/'scripts'/f'{n}.py'),*map(str,a)],env=e,check=True)
run('party_pick','Tranquill','--single');run('fly_to',564,'--menu-open','--origin',271)
run('eventq',564,1,'enter');run('eventq',22,2,'enter');run('eventq',564,4,'enter')
run('eventq',23,16,'talk');run('linear_dialog',23,16,'--source-page',5,'--burst');run('checkpoint','League220-Headphones')
run('eventq',23,2,'enter');run('fly_to',523);run('eventq',523,3,'enter')
