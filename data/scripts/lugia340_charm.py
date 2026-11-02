"""Travel to the ordinary Beryl Library item after inspecting its installed event."""
import os,subprocess,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1]
os.environ.update(REBORN_FAST_KEYS='1',REBORN_COORD_CACHE='1',REBORN_ROUTE_CHUNK='84')
def run(s,*a):
 print('CHARM',s,*a,flush=True);subprocess.run([sys.executable,str(R/'scripts'/f'{s}.py'),*map(str,a)],check=True)
run('eventq',369,5,'enter');run('fly_to',525,'--carrier','Zapdos','--origin',520)
run('connected_walk',525,544,23,17);run('eventq',544,44,'enter');run('eventq',548,4,'enter');run('eventq',549,24,'item');run('checkpoint','Lugia340-AmethystCharm')
