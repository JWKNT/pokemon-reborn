"""Collect the missed Super Rod from the postgame Lost and Found."""
import os,subprocess,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1]
os.environ.update(REBORN_FAST_KEYS='1',REBORN_COORD_CACHE='1',REBORN_ROUTE_CHUNK='84')
def run(s,*a):
 print('ROD',s,*a,flush=True);subprocess.run([sys.executable,str(R/'scripts'/f'{s}.py'),*map(str,a)],check=True)
run('connected_walk',544,525);run('fly_to',519,'--carrier','Zapdos','--origin',525)
run('eventq',519,215,'enter');run('eventq',602,35,'item');run('checkpoint','Lugia340-SuperRod')
