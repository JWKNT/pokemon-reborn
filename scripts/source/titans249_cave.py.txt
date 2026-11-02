"""Collect useful cave pickups and enter the Titans portal via normal UI."""
import os,sys,subprocess
from pathlib import Path
R=Path(__file__).resolve().parents[1]
os.environ.update(REBORN_FAST_KEYS='1',REBORN_COORD_CACHE='1',REBORN_ROUTE_CHUNK='84')
def run(s,*a):
 print('TITANS',s,*a,flush=True);subprocess.run([sys.executable,str(R/'scripts'/f'{s}.py'),*map(str,a)],check=True)
for e in [10,7,11]:run('eventq',636,e,'item')
run('eventq',636,9,'enter')
run('play','wait:3')
run('checkpoint','Postgame249-TitansPortal')
