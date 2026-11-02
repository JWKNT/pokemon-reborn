"""Remaining first-room crystal order, followed by the normal north exit."""
import os,subprocess,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1]
os.environ.update(REBORN_FAST_KEYS='1',REBORN_COORD_CACHE='1',REBORN_ROUTE_CHUNK='84')
def run(n,*a):
 print('CORE UPPER',n,*a,flush=True);subprocess.run([sys.executable,str(R/'scripts'/f'{n}.py'),*map(str,a)],check=True)
for eid,name,choice in [(34,'Cold8',True),(121,'Blue9',False),(32,'Hot9',True),(61,'Red10',False),(34,'Cold10',True),(8,'Blue11',False),(32,'Hot11',True),(48,'Rock12',True),(34,'Cold12',True),(120,'Crystal13',False)]:
 run('surface_event',870,eid,'talk')
 run('dialog',*(['--yes']if choice else []),'--limit',30,'--story-burst')
 run('checkpoint','Heatran295-'+name)
run('surface_event',870,101,'enter')
run('dialog','--limit',100,'--story-burst')
run('checkpoint','Heatran295-UpperCore')
