"""Reviewed direct train route to the desert, via normal controls."""
import os,subprocess,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1]
env=dict(os.environ,REBORN_FAST_KEYS='1',REBORN_COORD_CACHE='1',REBORN_ROUTE_CHUNK='84')
def run(s,*a):
 print('STATION',s,*a,flush=True)
 subprocess.run([sys.executable,str(R/'scripts'/f'{s}.py'),*map(str,a)],check=True,env=env)
run('city_enter',530,591)
run('eventq',591,6,'talk')
run('choose_dialog','Yes|No','Yes')
run('linear_dialog',591,6,'--active','--past-choice')
run('checkpoint','Postgame243-TrainTicket')
run('eventq',591,19,'enter')
run('play','wait:14')
run('settle_arrival',694)
