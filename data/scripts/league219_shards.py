"""Normal-controls follow-up shard route; caller verifies starting map179."""
import subprocess,sys,os
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def run(n,*a):
 e=dict(os.environ,REBORN_FAST_KEYS='1',REBORN_COORD_CACHE='1',REBORN_ROUTE_CHUNK='84')
 if n=='fly_to':e.pop('REBORN_FAST_KEYS',None)
 print('STAGE',n,*a,flush=True);subprocess.run([sys.executable,str(R/'scripts'/f'{n}.py'),*map(str,a)],env=e,check=True)
run('eventq',179,1,'enter');run('eventq',178,11,'smash');run('eventq',178,2,'enter');run('eventq',179,29,'item');run('checkpoint','League219-StairwayShards')
run('eventq',179,2,'enter');run('eventq',178,1,'enter');run('eventq',177,1,'enter')
