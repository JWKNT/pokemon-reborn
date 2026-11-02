"""Shop at the verified critical capture vendor, then travel to east Route1."""
import os,sys,subprocess,json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
os.environ.update(REBORN_FAST_KEYS='1',REBORN_COORD_CACHE='1',REBORN_ROUTE_CHUNK='84')
def run(s,*a):
 print('DEPART',s,*a,flush=True);subprocess.run([sys.executable,str(R/'scripts'/f'{s}.py'),*map(str,a)],check=True)
run('city_enter',520,369)
run('eventq',369,1,'talk')
