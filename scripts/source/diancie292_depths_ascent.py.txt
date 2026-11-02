"""Source-reviewed ascent across normal waterfall underpasses to Cain's earrings."""
import os,sys,subprocess
from pathlib import Path
R=Path(__file__).resolve().parents[1]
os.environ.update(REBORN_FAST_KEYS='1',REBORN_COORD_CACHE='1',REBORN_ROUTE_CHUNK='84')
def run(n,*a):
 print('DEPTHS ASCENT',n,*a,flush=True)
 subprocess.run([sys.executable,str(R/'scripts'/f'{n}.py'),*map(str,a)],check=True)
run('surface_walk',860,48,107)
for eid in [10,14,21,23,1]:run('eventq',860,eid,'enter')
run('eventq',865,4,'talk')
run('linear_dialog',865,4,'--source-page',0,'--burst')
run('checkpoint','Diancie292-Earrings')
