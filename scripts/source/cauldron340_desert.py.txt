"""Recorded northern desert approach, with verified field utility preparation."""
import os,subprocess,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1]
os.environ.update(REBORN_FAST_KEYS='1',REBORN_COORD_CACHE='1',REBORN_ROUTE_CHUNK='84')
def run(s,*a):
 print('CAULDRON DESERT',s,*a,flush=True);subprocess.run([sys.executable,str(R/'scripts'/f'{s}.py'),*map(str,a)],check=True)
run('field_repel','Max Repel');run('teach_machine','TMX9','Swampert','Rock Climb',0,'--single-step')
run('city_enter',704,687);run('eventq',687,1,'enter');run('checkpoint','Cauldron340-TekniteEntrance')
