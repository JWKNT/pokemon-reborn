"""Return with the collected Good Rod and prepare an owned Thief user."""
import os,subprocess,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1]
E=dict(os.environ,REBORN_FAST_KEYS='1',REBORN_COORD_CACHE='1',REBORN_ROUTE_CHUNK='84')
def run(s,*a):
 print('FISH PREP',s,*a,flush=True)
 subprocess.run([sys.executable,str(R/'scripts'/f'{s}.py'),*map(str,a)],env=E,check=True)
run('eventq',242,8,'enter')
run('settle_arrival',271)
run('fly_to',519,'--carrier','Zapdos')
run('city_enter',519,38)
run('q','38,9,20,up:.12,c,wait:1')
run('pc_open_reviewed')
run('pc_exchange_named',23,5,'Arcanine','Aegislash')
run('take_held','Arcanine','Charcoal')
run('teach_machine','TM46','Arcanine','Thief',0,'--single-step')
run('checkpoint','Postgame247-FishingPrep')
