"""Open the initial Heatran route with normal Rock Smash and story dialogue."""
import os,subprocess,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1]
os.environ.update(REBORN_FAST_KEYS='1',REBORN_COORD_CACHE='1',REBORN_ROUTE_CHUNK='84')
def run(n,*a):
 print('CORE OPEN',n,*a,flush=True);subprocess.run([sys.executable,str(R/'scripts'/f'{n}.py'),*map(str,a)],check=True)
for eid,save in [(47,'Heatran294-FirstRock'),(24,'Heatran294-CenterRock')]:
 run('surface_event',870,eid,'talk')
 run('dialog','--yes','--limit',12,'--story-burst')
 run('checkpoint',save)
run('surface_event',870,27,'talk')
run('dialog','--limit',100,'--story-burst')
run('checkpoint','Heatran294-Brothers')
