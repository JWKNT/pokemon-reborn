"""Previously verified New World portal and Aegir waterfall route, no battle interaction."""
import os,sys,subprocess
from pathlib import Path
R=Path(__file__).resolve().parents[1]
os.environ.update(REBORN_FAST_KEYS='1',REBORN_COORD_CACHE='1',REBORN_ROUTE_CHUNK='84')
def run(s,*a):
 print('AMARIA ISLAND',s,*a,flush=True);subprocess.run([sys.executable,str(R/'scripts'/f'{s}.py'),*map(str,a)],check=True)
run('settle_arrival',883)
run('surface_event',883,9,'enter')
run('settle_arrival',850)
run('surface_walk',850,46,21)
run('play','down:.12','down:.12','down:.12','down:.12','down:.12')
run('surface_walk',850,48,27)
run('waterfall_step',850,48,27,'down',850,48,30)
run('surface_walk',850,54,51)
run('checkpoint','Amaria343-Retry')
