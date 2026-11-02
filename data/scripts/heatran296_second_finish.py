"""Final cold crystal; stop before final-room entry for observed planning."""
import os,subprocess,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1]
os.environ.update(REBORN_FAST_KEYS='1',REBORN_COORD_CACHE='1')
def run(n,*a):
 print('CORE FINAL',n,*a,flush=True);subprocess.run([sys.executable,str(R/'scripts'/f'{n}.py'),*map(str,a)],check=True)
for eid,name,choice in [(6,'SecondCold3',True),(56,'SecondBlue8',False)]:
 run('surface_event',872,eid,'talk')
 run('dialog',*(['--yes']if choice else []),'--limit',30,'--story-burst')
 run('checkpoint','Heatran296-'+name)
