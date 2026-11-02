"""Finish room870 after crystal event8 (guide11), using corrected event mapping."""
import os,subprocess,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1]
os.environ.update(REBORN_FAST_KEYS='1',REBORN_COORD_CACHE='1')
def run(n,*a):
 print('CORE FINISH',n,*a,flush=True);subprocess.run([sys.executable,str(R/'scripts'/f'{n}.py'),*map(str,a)],check=True)
for eid,name,choice in [(32,'Hot11',True),(48,'Rock12',True),(34,'Cold12',True),(120,'FinalCrystal',False)]:
 run('surface_event',870,eid,'talk');run('dialog',*(['--yes']if choice else []),'--limit',30,'--story-burst');run('checkpoint','Heatran295-'+name)
run('surface_event',870,101,'enter')
run('dialog','--limit',100,'--story-burst')
run('checkpoint','Heatran295-UpperCore')
