"""Normal Charous climbing route. Stop for observed story before resuming."""
import subprocess,sys,os,json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
env=dict(os.environ,REBORN_FAST_KEYS='1',REBORN_ROUTE_CHUNK='112',REBORN_COORD_CACHE='1')
def run(*a):subprocess.run([sys.executable,str(R/'scripts'/a[0]),*map(str,a[1:])],check=True,env=env)
# The first climb starts Hardy/Radomus's scene; complete that separately.
steps=[('victory_gem_cliff_event.py',792,9,'approach'),('charous199_first_climb.py',),('dialog.py','--yes','--story-burst','--limit=85'),('checkpoint.py','Charous199-Hardy'),('victory_gem_cliff_event.py',792,27,'approach'),('q.py','792,31,11'),('dialog.py','--story-burst','--limit=90'),('checkpoint.py','Charous199-opened'),('victory_gem_cliff_event.py',792,3,'enter'),('dialog.py','--story-burst','--limit=90'),('checkpoint.py','Logic199-entry')]
start=int(sys.argv[1])if len(sys.argv)>1 else 1
for i,s in enumerate(steps,1):
 if i>=start:run(*s);print('CHAROUS STEP',i,'DONE',flush=True)
