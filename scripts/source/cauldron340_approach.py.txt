"""Travel toward Teknite through the ordinary train station."""
import os,subprocess,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1]
os.environ.update(REBORN_FAST_KEYS='1',REBORN_COORD_CACHE='1',REBORN_ROUTE_CHUNK='84')
def run(s,*a):
 print('CAULDRON',s,*a,flush=True);subprocess.run([sys.executable,str(R/'scripts'/f'{s}.py'),*map(str,a)],check=True)
run('eventq',38,6,'enter');run('fly_to',530,'--carrier','Zapdos','--origin',519);run('city_enter',530,591)
