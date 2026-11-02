"""Normal controls to collect optional Prison Bottle, then approach main descent."""
import os,sys,subprocess
from pathlib import Path
R=Path(__file__).resolve().parents[1]
os.environ.update(REBORN_FAST_KEYS='1',REBORN_COORD_CACHE='1',REBORN_ROUTE_CHUNK='84')
def run(n,*a):
 print('DEPTHS BOTTLE',n,*a,flush=True)
 subprocess.run([sys.executable,str(R/'scripts'/f'{n}.py'),*map(str,a)],check=True)
run('surface_walk',860,33,27)
run('waterfall_step',860,33,27,'up',860,33,14)
run('surface_walk',860,35,14)
run('eventq',860,144,'item')
run('surface_walk',860,33,14)
run('waterfall_step',860,33,14,'down',860,33,27)
run('surface_walk',860,24,31)
run('play','down:.12','c','wait:2')
