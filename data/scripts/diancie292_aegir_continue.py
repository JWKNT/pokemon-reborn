"""Continue verified lower waterfall arrival through Aegir and Dive entrance."""
import os,sys,subprocess
from pathlib import Path
R=Path(__file__).resolve().parents[1]
os.environ.update(REBORN_FAST_KEYS='1',REBORN_COORD_CACHE='1',REBORN_ROUTE_CHUNK='84')
def run(n,*a):
 print('AEGIR CONTINUE',n,*a,flush=True)
 subprocess.run([sys.executable,str(R/'scripts'/f'{n}.py'),*map(str,a)],check=True)
run('surface_walk',852,4,95)
run('eventq',852,3,'enter')
run('checkpoint','Diancie292-Aegir')
run('aegir_event',849,54,'enter')
run('diancie292_depths_entry')
