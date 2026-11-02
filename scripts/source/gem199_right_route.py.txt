"""Source-reviewed normal Ruby/Amethyst key route with fresh save checkpoints."""
import subprocess,sys,os
from pathlib import Path
R=Path(__file__).resolve().parents[1]
env=dict(os.environ,REBORN_FAST_KEYS='1',REBORN_ROUTE_CHUNK='112',REBORN_COORD_CACHE='1')
def run(*a):subprocess.run([sys.executable,str(R/'scripts'/a[0]),*map(str,a[1:])],check=True,env=env)
steps=[('victory_gem_cliff_event.py',791,7,'enter'),('checkpoint.py','Ruby199-entry'),('victory_gem_cliff_event.py',799,38,'talk'),('dialog.py','--story-burst','--limit=12'),('checkpoint.py','Ruby199-key'),('victory_gem_cliff_event.py',799,40,'item'),('victory_gem_cliff_event.py',799,3,'enter'),('checkpoint.py','Amethyst199-entry'),('victory_gem_cliff_event.py',802,38,'item'),('victory_gem_cliff_event.py',802,39,'item'),('victory_gem_cliff_event.py',802,36,'talk'),('dialog.py','--story-burst','--limit=12'),('checkpoint.py','Amethyst199-key'),('victory_gem_cliff_event.py',802,1,'enter'),('checkpoint.py','Gem199-right-return')]
start=int(sys.argv[1])if len(sys.argv)>1 else 1
for i,s in enumerate(steps,1):
 if i>=start:run(*s);print('RIGHT GEM ROUTE STEP',i,'DONE',flush=True)
