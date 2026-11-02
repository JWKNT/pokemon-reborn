"""Normal portal exit, flight and Grand Hall healing after the completed capture."""
import os,sys,subprocess
from pathlib import Path
R=Path(__file__).resolve().parents[1]
os.environ.update(REBORN_FAST_KEYS='1',REBORN_COORD_CACHE='1',REBORN_ROUTE_CHUNK='84')
def run(s,*a):
 print('RETURN',s,*a,flush=True);subprocess.run([sys.executable,str(R/'scripts'/f'{s}.py'),*map(str,a)],check=True)
run('eventq',834,1,'enter')
run('play','wait:3')
run('fly_to',519,'--carrier','Zapdos')
run('city_enter',519,38)
run('q','38,5,22,up:.12')
run('heal')
run('checkpoint','Postgame248-Healed')
