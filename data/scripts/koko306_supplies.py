"""Collect Protect and approach the public Ability Capsule offer normally."""
import os,sys,subprocess
from pathlib import Path
R=Path(__file__).resolve().parents[1]
os.environ.update(REBORN_FAST_KEYS='1',REBORN_COORD_CACHE='1',REBORN_ROUTE_CHUNK='112')
def run(n,*a):
 print('KOKO SUPPLIES',n,*a,flush=True)
 subprocess.run([sys.executable,str(R/'scripts'/f'{n}.py'),*map(str,a)],check=True)
run('city_enter',38,519);run('fly_to',527,'--carrier','Zapdos')
run('eventq',527,87,'enter');run('eventq',826,10,'item');run('overworld')
run('teach_machine','TM17','Excadrill','Protect',1)
run('city_enter',826,527);run('fly_to',355,'--carrier','Zapdos')
run('eventq',355,98,'item');run('overworld')
run('eventq',355,89,'talk')
