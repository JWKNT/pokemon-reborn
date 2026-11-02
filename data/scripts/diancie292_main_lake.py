"""Normal Dive passage from western pond to main lake, followed by quest entrance."""
import os,sys,subprocess
from pathlib import Path
R=Path(__file__).resolve().parents[1]
os.environ.update(REBORN_FAST_KEYS='1',REBORN_COORD_CACHE='1',REBORN_ROUTE_CHUNK='84')
def run(n,*a):
 print('MAIN LAKE',n,*a,flush=True)
 subprocess.run([sys.executable,str(R/'scripts'/f'{n}.py'),*map(str,a)],check=True)
if '--underwater' not in sys.argv:
 run('surface_walk',850,35,59)
 run('waterfall_step',850,35,59,'down',850,35,62)
 run('surface_walk',850,26,65)
 run('dive_transition',850,26,65,851)
run('underwater_walk',851,23,61)
run('eventq',851,3,'enter')
run('underwater_walk',851,43,13)
run('eventq',851,7,'enter')
run('underwater_walk',851,68,107)
run('dive_transition',851,68,107,850)
run('surface_walk',850,62,107)
run('eventq',850,57,'enter')
run('checkpoint','Diancie292-MainLake')
run('q','850,58,42')
run('play','down:.12','wait:5')
run('diancie292_depths_entry')
