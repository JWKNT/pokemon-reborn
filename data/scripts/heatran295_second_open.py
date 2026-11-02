"""Start room872 after its introductory scene has fully completed."""
import os,subprocess,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1]
os.environ.update(REBORN_FAST_KEYS='1',REBORN_COORD_CACHE='1',REBORN_ROUTE_CHUNK='84')
def run(n,*a):
 print('CORE SECOND',n,*a,flush=True);subprocess.run([sys.executable,str(R/'scripts'/f'{n}.py'),*map(str,a)],check=True)
for eid,name,choice in [(32,'SecondRed1',False),(6,'SecondCold1',True),(53,'SecondBlue2',False)]:
 run('surface_event',872,eid,'talk')
 run('dialog',*(['--yes']if choice else []),'--limit',30,'--story-burst')
 run('checkpoint','Heatran295-'+name)
# Stop for direct observation and source-based boulder approach.
