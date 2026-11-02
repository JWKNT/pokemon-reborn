"""Continue inspected second Core crystal sequence through normal UI."""
import os,subprocess,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1]
os.environ.update(REBORN_FAST_KEYS='1',REBORN_COORD_CACHE='1')
def run(n,*a):
 print('CORE SECOND',n,*a,flush=True);subprocess.run([sys.executable,str(R/'scripts'/f'{n}.py'),*map(str,a)],check=True)
for eid,name,choice in [(6,'SecondCold2',True),(54,'SecondBlue4',False),(55,'SecondBlue5',False),(9,'SecondHot3',True),(17,'SecondRock6',True),(34,'SecondRed7',False)]:
 run('surface_event',872,eid,'talk')
 run('dialog',*(['--yes']if choice else []),'--limit',30,'--story-burst')
 run('checkpoint','Heatran296-'+name)
