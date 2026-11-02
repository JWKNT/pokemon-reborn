"""Travel to reviewed low-level fishing shore after Good Rod registration."""
import os,subprocess,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1]
E=dict(os.environ,REBORN_FAST_KEYS='1',REBORN_COORD_CACHE='1',REBORN_ROUTE_CHUNK='84')
def run(s,*a):
 print('FISHING',s,*a,flush=True)
 subprocess.run([sys.executable,str(R/'scripts'/f'{s}.py'),*map(str,a)],env=E,check=True)
run('party_lead','Arcanine')
run('city_enter',38,519)
run('fly_to',232,'--carrier','Zapdos')
run('q','232,16,20,down:.12')
run('checkpoint','Postgame247-FishingShore')
