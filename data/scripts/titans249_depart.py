"""Normal saved quest departure and flight to Celestinine Cascade."""
import os,sys,subprocess
from pathlib import Path
R=Path(__file__).resolve().parents[1]
os.environ.update(REBORN_FAST_KEYS='1',REBORN_COORD_CACHE='1',REBORN_ROUTE_CHUNK='84')
def run(s,*a):
 print('TITANS',s,*a,flush=True);subprocess.run([sys.executable,str(R/'scripts'/f'{s}.py'),*map(str,a)],check=True)
run('checkpoint','Postgame249-TitansAccepted')
run('city_enter',827,826)
run('city_enter',826,527)
run('fly_to',359,'--carrier','Zapdos')
run('checkpoint','Postgame249-Cascade')
