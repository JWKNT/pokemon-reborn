"""Leave the club and use the established Ametrine Fly point and nurse."""
import os,subprocess,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1]
os.environ.update(REBORN_FAST_KEYS='1',REBORN_COORD_CACHE='1',REBORN_ROUTE_CHUNK='84')
def run(n,*a):
 print('HEATRAN TRIP',n,*a,flush=True);subprocess.run([sys.executable,str(R/'scripts'/f'{n}.py'),*map(str,a)],check=True)
run('eventq',827,39,'enter')
run('eventq',826,2,'enter')
run('fly_to',439,'--carrier','Zapdos')
run('checkpoint','Heatran294-Ametrine')
