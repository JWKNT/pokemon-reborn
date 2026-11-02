"""Normal reviewed climbing route after puzzle3; stops on encounters/dialogue."""
import subprocess,sys,os
from pathlib import Path
R=Path(__file__).resolve().parents[1]
env=dict(os.environ,REBORN_FAST_KEYS='1',REBORN_ROUTE_CHUNK='112',REBORN_COORD_CACHE='1')
steps=[('victory_gem_cliff_event',792,86,'item'),('victory_gem_cliff_event',792,6,'enter'),('checkpoint','Road200-high-entry'),('victory_gem_cliff_event',794,105,'item'),('victory_gem_cliff_event',794,5,'enter'),('dialog','--story-burst','--limit=85'),('checkpoint','Logic200-four-entry')]
start=int(sys.argv[1])if len(sys.argv)>1 else 1
for i,a in enumerate(steps,1):
 if i<start:continue
 subprocess.run([sys.executable,str(R/'scripts'/f'{a[0]}.py'),*map(str,a[1:])],check=True,env=env)
 print('CHAROUS EAST STEP',i,'DONE',flush=True)
