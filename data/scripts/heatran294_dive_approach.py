"""Reviewed connected-map route from lower ice to Ametrine Core's underwater door."""
import os,subprocess,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1]
os.environ.update(REBORN_FAST_KEYS='1',REBORN_COORD_CACHE='1',REBORN_ROUTE_CHUNK='84')
def run(n,*a):
 print('CORE APPROACH',n,*a,flush=True);subprocess.run([sys.executable,str(R/'scripts'/f'{n}.py'),*map(str,a)],check=True)
run('surface_walk',433,27,0)
run('play','up:.12','wait:1')
run('surface_walk',387,16,35)
run('play','down:.12','wait:1')
run('surface_walk',433,22,19)
run('play','down:.12','wait:1')
run('surface_walk',434,22,2)
run('dive_transition',434,22,2,436)
run('q','436,22,0,up:.12,wait:1','435,22,0,up:.12,wait:1','400,54,17,down:.12,wait:2')
run('checkpoint','Heatran294-UnderwaterDoor')
