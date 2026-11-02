"""Buy remaining source-reviewed cages with normal UI and shard costs, then save."""
import subprocess,sys,os
from pathlib import Path
R=Path(__file__).resolve().parents[1]
env=dict(os.environ,REBORN_FAST_KEYS='1',REBORN_COORD_CACHE='1',REBORN_ROUTE_CHUNK='84')
for eid in map(int,sys.argv[1:]):
 assert 16<=eid<=24
 print('BUY CAGE',eid,flush=True)
 subprocess.run([sys.executable,str(R/'scripts/seventh_cage_purchase.py'),str(eid)],env=env,check=True)
subprocess.run([sys.executable,str(R/'scripts/checkpoint.py'),'League219-CagesPurchased'],env=env,check=True)
