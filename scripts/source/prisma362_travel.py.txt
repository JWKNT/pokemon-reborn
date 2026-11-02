"""Recorded normal travel along reviewed installed Beryl cave transfers."""
import os,subprocess,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1]
os.environ.update(REBORN_FAST_KEYS='1',REBORN_COORD_CACHE='1',REBORN_ROUTE_STEP_PAUSE='.10',REBORN_ROUTE_CHUNK='56')
def run(n,*a):
 print('PRISMA TRAVEL',n,*a,flush=True)
 subprocess.run([sys.executable,str(R/'scripts'/f'{n}.py'),*map(str,a)],check=True)
run('eventq',38,6,'enter')
run('fly_to',525,'--carrier','Zapdos')
run('connected_walk',525,551,15,12)
run('connected_walk',551,552,20,8)
run('eventq',552,29,'smash')
run('eventq',552,30,'smash')
run('connected_walk',552,551,5,7)
run('eventq',551,16,'smash')
run('eventq',551,15,'enter')
run('eventq',184,2,'enter')
run('eventq',185,12,'enter')
run('checkpoint','Prisma362-Entry')
