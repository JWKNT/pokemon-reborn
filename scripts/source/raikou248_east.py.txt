"""Recorded route from ball shop to the eastern northern-woods Honey tree."""
import os,sys,subprocess
from pathlib import Path
R=Path(__file__).resolve().parents[1]
os.environ.update(REBORN_FAST_KEYS='1',REBORN_COORD_CACHE='1',REBORN_ROUTE_CHUNK='84')
def run(s,*a):
 print('RAIKOU ROUTE',s,*a,flush=True);subprocess.run([sys.executable,str(R/'scripts'/f'{s}.py'),*map(str,a)],check=True)
run('city_enter',369,520)
run('party_lead','Zapdos')
run('fly_to',292,'--carrier','Zapdos')
run('connected_walk',292,291)
run('connected_walk',291,287,69,13)
run('eventq',287,8,'enter')
run('forest_honey245',289,57,60,'Postgame248-NorthLog339','Heracross')
