"""Normal-controls continuation after the visibly completed stalactite scene.
Stops on every unexpected encounter, dialogue choice, or landing.
"""
import subprocess,sys,os
from pathlib import Path
R=Path(__file__).resolve().parents[1]
env=dict(os.environ,REBORN_FAST_KEYS='1',REBORN_ROUTE_CHUNK='112',REBORN_COORD_CACHE='1')
steps=[('checkpoint','Road201-stalactite-dropped'),('victory_gem_cliff_event',813,7,'enter'),('checkpoint','Charous201-lower-entry'),('victory_gem_cliff_event',794,7,'enter'),('dialog','--story-burst','--limit=85'),('checkpoint','Road201-final-chambers-entry')]
start=int(sys.argv[1])if len(sys.argv)>1 else 1
for i,a in enumerate(steps,1):
 if i<start:continue
 subprocess.run([sys.executable,str(R/'scripts'/f'{a[0]}.py'),*map(str,a[1:])],check=True,env=env)
 print('LOWER CHAROUS STEP',i,'DONE',flush=True)
