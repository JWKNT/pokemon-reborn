"""Reach explosives and deliver the cart through the normal rail controls."""
import subprocess,sys,os,json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def run(*a):subprocess.run([sys.executable,str(R/'scripts'/a[0]),*map(str,a[1:])],check=True,env=dict(os.environ,REBORN_FAST_KEYS='1',REBORN_ROUTE_CHUNK='112',REBORN_COORD_CACHE='1'))
steps=[('rail_cart198.py',29,'Rail198-c-cart29-bottom'),('victory_rail_cliff_event.py',790,46,'talk'),('dialog.py','--story-burst','--limit=90'),('checkpoint.py','Rail198-explosives-loaded'),('victory_rail_cliff_event.py',790,42,'approach'),('rail_cart198.py',42,'Rail198-explosives-left'),('rail_lever198.py',35,0,'Rail198-D-off'),('victory_rail_cliff_event.py',790,29,'approach'),('rail_cart198.py',29,'Rail198-c-cart29-top'),('rail_cart198.py',42,'Rail198-blast')]
start=int(sys.argv[1])if len(sys.argv)>1 else 1
for i,a in enumerate(steps,1):
 if i<start:continue
 run(*a);print('RAIL PHASE C STEP',i,'DONE',flush=True)
assert json.loads((R/'notes/navigation-state.json').read_text())['switches']['1166']
