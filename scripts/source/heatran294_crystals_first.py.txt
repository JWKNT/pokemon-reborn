"""Validated first three crystals and temperature changes via ordinary UI."""
import os,subprocess,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1]
os.environ.update(REBORN_FAST_KEYS='1',REBORN_COORD_CACHE='1',REBORN_ROUTE_CHUNK='84')
def run(n,*a):
 print('CORE CRYSTALS',n,*a,flush=True);subprocess.run([sys.executable,str(R/'scripts'/f'{n}.py'),*map(str,a)],check=True)
run('checkpoint','Heatran294-BrothersReady')
for eid,name,choice in [(103,'Blue2',False),(32,'Hot2',True),(29,'Red3',False),(34,'Cold3',True),(123,'Blue4',False)]:
 run('surface_event',870,eid,'talk')
 run('dialog',*(['--yes']if choice else []),'--limit',30,'--story-burst')
 run('checkpoint','Heatran294-'+name)
run('teach_machine','TMX4','Swampert','Strength',0,'--single-step')
run('checkpoint','Heatran294-StrengthReady')
