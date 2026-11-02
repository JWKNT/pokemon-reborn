"""Reviewed ordinary cart/lever sequence through the first cargo load."""
import subprocess,sys,os,json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def run(*a):subprocess.run([sys.executable,str(R/'scripts'/a[0]),*map(str,a[1:])],check=True,env=dict(os.environ,REBORN_FAST_KEYS='1',REBORN_ROUTE_CHUNK='112',REBORN_COORD_CACHE='1'))
steps=[('rail_lever198.py',33,1,'Rail198-A-on'),('rail_cart198.py',41,'Rail198-cart41-upper'),('rail_lever198.py',34,1,'Rail198-B-on'),('rail_cart198.py',41,'Rail198-cart41-back'),('rail_lever198.py',33,0,'Rail198-A-off'),('rail_cart198.py',41,'Rail198-cart41-left-again'),('rail_cart198.py',29,'Rail198-cart29-bottom-again'),('rail_lever198.py',39,1,'Rail198-C-on'),('rail_cart198.py',29,'Rail198-cart29-top-again'),('rail_cart198.py',42,'Rail198-cart42-rocks'),('eventq.py',790,44,'talk'),('dialog.py','--yes','--limit=12'),('checkpoint.py','Rail198-rocks-loaded')]
start=int(sys.argv[1])if len(sys.argv)>1 else 1
for i,a in enumerate(steps,1):
 if i<start:continue
 run(*a);print('RAIL PHASE A STEP',i,'DONE',flush=True)
assert json.loads((R/'notes/navigation-state.json').read_text())['switches']['1164']
run('rail_cart198.py',42,'Rail198-rocks-cart-left')
