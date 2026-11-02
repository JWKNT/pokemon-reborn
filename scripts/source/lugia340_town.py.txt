"""Return via verified outdoor Fly point and heal after the completed Lugia quest."""
import os,subprocess,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1]
os.environ.update(REBORN_FAST_KEYS='1',REBORN_COORD_CACHE='1',REBORN_ROUTE_CHUNK='84')
def run(s,*a):
 print('LUGIA RETURN',s,*a,flush=True)
 subprocess.run([sys.executable,str(R/'scripts'/f'{s}.py'),*map(str,a)],check=True)
run('fly_to',519,'--carrier','Zapdos','--origin',688)
run('eventq',519,116,'enter');run('eventq',38,3,'talk');run('heal')
run('checkpoint','Lugia340-Healed')
