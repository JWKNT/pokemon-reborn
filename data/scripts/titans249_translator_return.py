"""Save the inspected Amaria conversation and return to Reborn via normal controls."""
import os,sys,subprocess
from pathlib import Path
R=Path(__file__).resolve().parents[1]
os.environ.update(REBORN_FAST_KEYS='1',REBORN_COORD_CACHE='1',REBORN_ROUTE_CHUNK='84')
def run(s,*a):
 print('TITANS',s,*a,flush=True);subprocess.run([sys.executable,str(R/'scripts'/f'{s}.py'),*map(str,a)],check=True)
run('checkpoint','Postgame249-Amaria')
run('city_enter',825,636)
run('city_enter',636,360)
run('fly_to',526,'--carrier','Zapdos')
run('checkpoint','Postgame249-Coral')
