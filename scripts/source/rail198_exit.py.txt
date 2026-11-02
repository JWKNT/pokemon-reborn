"""Exit the completed final rail puzzle through its normally blasted tunnel."""
import json,subprocess,sys,os
from pathlib import Path
R=Path(__file__).resolve().parents[1]
n=json.loads((R/'notes/navigation-state.json').read_text());assert n['switches']['1166']
steps=[('rail_cart198.py',41,'Rail198-exit-cart41-right'),('rail_lever198.py',33,1,'Rail198-exit-A-on'),('rail_cart198.py',41,'Rail198-exit-cart41-upperright'),('eventq.py',790,7,'enter'),('dialog.py','--story-burst','--limit=90'),('checkpoint.py','Gem198-entry')]
start=int(sys.argv[1])if len(sys.argv)>1 else 1
for i,a in enumerate(steps,1):
 if i<start:continue
 subprocess.run([sys.executable,str(R/'scripts'/a[0]),*map(str,a[1:])],check=True,env=dict(os.environ,REBORN_FAST_KEYS='1',REBORN_ROUTE_CHUNK='112',REBORN_COORD_CACHE='1'))
 print('RAIL EXIT STEP',i,'DONE',flush=True)
