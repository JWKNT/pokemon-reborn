"""Finish the known Core route; prepare team and stop at pre-boss tile."""
import os,subprocess,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1]
os.environ.update(REBORN_FAST_KEYS='1',REBORN_COORD_CACHE='1')
def run(n,*a):
 print('CORE EXIT',n,*a,flush=True);subprocess.run([sys.executable,str(R/'scripts'/f'{n}.py'),*map(str,a)],check=True)
run('surface_event',872,9,'talk');run('dialog','--yes','--limit',30,'--story-burst');run('checkpoint','Heatran296-SecondHotFinal')
run('surface_event',872,132,'enter');run('dialog','--limit',40,'--story-burst');run('checkpoint','Heatran296-BossRoom')
run('teach_machine','TM78','Swampert','Bulldoze',1,'--single-step')
run('give_held','Safety Goggles','Volcanion','--single-step');run('party_swap',0,2)
run('surface_walk',873,17,15);run('checkpoint','Heatran296-Entry')
