"""Reviewed surfacing and entry; stop at Cal's first conversation."""
import os,subprocess,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1]
os.environ.update(REBORN_FAST_KEYS='1',REBORN_COORD_CACHE='1',REBORN_ROUTE_CHUNK='84')
def run(n,*a):
 print('CORE ENTRY',n,*a,flush=True);subprocess.run([sys.executable,str(R/'scripts'/f'{n}.py'),*map(str,a)],check=True)
run('q','401,16,17')
run('dive_transition',401,16,17,388)
run('surface_event',388,4,'enter')
run('checkpoint','Heatran294-CoreEntry')
run('surface_event',870,3,'talk')
run('dialog','--limit',35,'--story-burst')
run('checkpoint','Heatran294-Cal')
