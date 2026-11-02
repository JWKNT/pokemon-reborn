"""Reviewed third-floor green crystal, smash and field-change encounter."""
import subprocess,sys,os
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def run(s,*a):
 print('GREEN',s,*a,flush=True)
 subprocess.run([sys.executable,str(R/'scripts'/f'{s}.py'),*map(str,a)],check=True,env=dict(os.environ,REBORN_COORD_CACHE='1',REBORN_FAST_KEYS='1',REBORN_ROUTE_CHUNK='84'))
run('teknite_walk',648,8,'talk');run('linear_dialog',648,8,'--source-page',0,'--burst');run('checkpoint','League223-Green3F')
run('teknite_walk',648,9,'smash');run('checkpoint','League223-Rock3F')
# Event9's reachable south side is22,20; horizontal corridor17..27 has no events.
run('q','648,22,20');run('hunt_target','Aron,Lairon,Boldore,Gigalith,Dugtrio,Sandslash,Heatmor,Durant,Turtonator','--dense-horizontal');run('battle_ready')
