"""Normal PC exchange, teach owned Rock Climb, then return to cave approach."""
import os,sys,subprocess
from pathlib import Path
R=Path(__file__).resolve().parents[1]
os.environ.update(REBORN_FAST_KEYS='1',REBORN_COORD_CACHE='1',REBORN_ROUTE_CHUNK='112')
def run(n,*a):
 print('LELE CLIMBER',n,*a,flush=True)
 subprocess.run([sys.executable,str(R/'scripts'/f'{n}.py'),*map(str,a)],check=True)
run('fly_to',519,'--carrier','Zapdos');run('city_enter',519,38)
run('eventq',38,4,'talk');run('pc_open_reviewed')
run('pc_exchange_named',25,4,'Swampert','Cresselia','--box',2)
run('teach_machine','TMX9','Swampert','Rock Climb',3,'--single-step')
run('checkpoint','Lele303-Climber')
run('city_enter',38,519);run('fly_to',814,'--carrier','Zapdos')
run('eventq',814,16,'enter');run('city_enter',798,796)
run('city_enter',796,791);run('city_enter',791,810)
run('q','810,30,23,down:.12,c,wait:1')
print('CHECK ROCK CLIMB CAPTION BEFORE ADVANCING.',flush=True)
