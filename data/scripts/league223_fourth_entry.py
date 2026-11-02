"""Use the upper red crystal and enter Teknite4F normally."""
import subprocess,sys,os
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def run(s,*a):
 print('FOURTH ENTRY',s,*a,flush=True)
 subprocess.run([sys.executable,str(R/'scripts'/f'{s}.py'),*map(str,a)],check=True,env=dict(os.environ,REBORN_COORD_CACHE='1',REBORN_FAST_KEYS='1',REBORN_ROUTE_CHUNK='84'))
run('teknite_walk',648,7,'talk');run('linear_dialog',648,7,'--source-page',0,'--burst');run('checkpoint','League223-Red3F')
run('teknite_walk',648,17,'smash');run('checkpoint','League223-Wall3F')
run('teknite_walk',648,17,'enter');run('settle_arrival',641);run('checkpoint','League223-Teknite4F')
