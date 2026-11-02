"""Clear the fourth-floor crystal gate and prepare the final Earthquake."""
import subprocess,sys,os
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def run(s,*a):
 print('FOURTH CLEAR',s,*a,flush=True)
 subprocess.run([sys.executable,str(R/'scripts'/f'{s}.py'),*map(str,a)],check=True,env=dict(os.environ,REBORN_COORD_CACHE='1',REBORN_FAST_KEYS='1',REBORN_ROUTE_CHUNK='84'))
run('teknite_walk',650,7,'talk');run('linear_dialog',650,7,'--source-page',0,'--burst');run('checkpoint','League223-Key4F')
run('teknite_walk',650,8,'smash');run('checkpoint','League223-Rock4F')
run('teknite_point','650,27,33');run('hunt_target','Aron,Lairon,Boldore,Gigalith,Dugtrio,Sandslash,Heatmor,Durant,Turtonator','--dense-horizontal');run('battle_ready')
