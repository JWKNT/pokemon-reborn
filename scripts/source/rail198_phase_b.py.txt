"""Normal rail sequence delivering loose rocks to the blocked climbing route."""
import subprocess,sys,os,json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def run(*a):subprocess.run([sys.executable,str(R/'scripts'/a[0]),*map(str,a[1:])],check=True,env=dict(os.environ,REBORN_FAST_KEYS='1',REBORN_ROUTE_CHUNK='112',REBORN_COORD_CACHE='1'))
steps=[('victory_rail_cliff_event.py',790,29,'approach'),('rail_cart198.py',29,'Rail198-b-cart29-bottom'),('rail_lever198.py',39,0,'Rail198-C-off'),('rail_lever198.py',35,1,'Rail198-D-on'),('eventq.py',790,66,'item'),('checkpoint.py','Rail198-PP-Up'),('rail_cart198.py',29,'Rail198-b-cart29-top'),('rail_cart198.py',42,'Rail198-rocks-delivered')]
start=int(sys.argv[1])if len(sys.argv)>1 else 1
for i,a in enumerate(steps,1):
 if i<start:continue
 run(*a);print('RAIL PHASE B STEP',i,'DONE',flush=True)
n=json.loads((R/'notes/navigation-state.json').read_text());assert n['switches']['1167'] and not n['switches']['1164']
