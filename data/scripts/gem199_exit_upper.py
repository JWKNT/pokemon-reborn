"""Open normal central shortcuts and follow upper rail-room path to Charous."""
import subprocess,sys,os,json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
env=dict(os.environ,REBORN_FAST_KEYS='1',REBORN_ROUTE_CHUNK='112',REBORN_COORD_CACHE='1')
def run(*a):subprocess.run([sys.executable,str(R/'scripts'/a[0]),*map(str,a[1:])],check=True,env=env)
steps=[('victory_gem_cliff_event.py',791,33,'talk'),('checkpoint.py','Gem199-shortcut-left'),('victory_gem_cliff_event.py',791,34,'talk'),('checkpoint.py','Gem199-shortcuts'),('victory_gem_cliff_event.py',791,3,'enter'),('checkpoint.py','Upper199-rail-entry'),('victory_gem_cliff_event.py',790,58,'item'),('victory_gem_cliff_event.py',790,57,'item'),('victory_gem_cliff_event.py',790,55,'item'),('victory_gem_cliff_event.py',790,62,'item'),('victory_gem_cliff_event.py',790,53,'enter'),('checkpoint.py','Upper199-arrow-entry'),('victory_gem_cliff_event.py',787,11,'enter'),('dialog.py','--story-burst','--limit=70'),('checkpoint.py','Charous199-entry')]
start=int(sys.argv[1])if len(sys.argv)>1 else 1
for i,s in enumerate(steps,1):
 if i>=start:run(*s);print('GEM EXIT STEP',i,'DONE',flush=True)
