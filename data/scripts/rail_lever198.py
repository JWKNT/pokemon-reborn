"""Toggle one reviewed rail lever normally, verify a fresh saved switch."""
import json,sys,subprocess,os
from pathlib import Path
R=Path(__file__).resolve().parents[1];e=int(sys.argv[1]);want=bool(int(sys.argv[2]));label=sys.argv[3];sw={33:1160,34:1162,35:1161,39:1163}[e]
n=json.loads((R/'notes/navigation-state.json').read_text());assert bool(n['switches'].get(str(sw)))!=want,'Lever already in requested state'
for args in [('eventq.py',790,e,'talk'),('checkpoint.py',label)]:subprocess.run([sys.executable,str(R/'scripts'/args[0]),*map(str,args[1:])],check=True,env=dict(os.environ,REBORN_FAST_KEYS='1',REBORN_COORD_CACHE='1',REBORN_ROUTE_CHUNK='112'))
a=json.loads((R/'notes/navigation-state.json').read_text());assert bool(a['switches'].get(str(sw)))==want
print('RAIL LEVER VERIFIED',e,sw,want,flush=True)
