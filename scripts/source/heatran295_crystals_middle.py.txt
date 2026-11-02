"""Source-reviewed crystal activations; each normal input sequence ends in a verified save."""
import os,subprocess,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1]
os.environ.update(REBORN_FAST_KEYS='1',REBORN_COORD_CACHE='1',REBORN_ROUTE_CHUNK='84')
def run(n,*a):
 print('CORE CRYSTALS',n,*a,flush=True);subprocess.run([sys.executable,str(R/'scripts'/f'{n}.py'),*map(str,a)],check=True)
for eid,name,choice in [(32,'Hot4',True),(21,'Red5',False),(34,'Cold5',True),(124,'Blue6',False),(122,'Blue7',False),(32,'Hot7',True),(60,'Red8',False)]:
 run('surface_event',870,eid,'talk')
 run('dialog',*(['--yes']if choice else []),'--limit',30,'--story-burst')
 run('checkpoint','Heatran295-'+name)
