"""Reviewed train approach and PP supplies along the northern desert route."""
import subprocess,sys,os
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def run(s,*a):
 print('DESERT',s,*a,flush=True)
 env=dict(os.environ,REBORN_COORD_CACHE='1')
 if s in ['q','eventq','city_enter']:env.update(REBORN_FAST_KEYS='1',REBORN_ROUTE_CHUNK='84')
 subprocess.run([sys.executable,str(R/'scripts'/f'{s}.py'),*map(str,a)],check=True,env=env)
if '--desert-only' not in sys.argv:
 run('league222_errands','cave-moves')
 run('league222_errands','station')
run('settle_arrival',694)
run('eventq',694,49,'item')
run('eventq',694,71,'item')
run('city_enter',694,687)
run('eventq',687,9,'item')
run('eventq',687,1,'enter')
run('checkpoint','League223-TekniteEntrance')
