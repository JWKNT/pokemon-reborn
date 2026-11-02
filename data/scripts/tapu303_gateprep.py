"""Finish reviewed gate arrival, lead terrain setter, save normally."""
import os,sys,subprocess
from pathlib import Path
R=Path(__file__).resolve().parents[1]
os.environ.update(REBORN_FAST_KEYS='1',REBORN_COORD_CACHE='1',REBORN_ROUTE_CHUNK='112')
for n,a in [('linear_dialog',[855,10,'--source-page',1,'--burst']),('party_front',['Fennekin']),('checkpoint',['Lele303-Gate'])]:
 print('GATE PREP',n,a,flush=True)
 subprocess.run([sys.executable,str(R/'scripts'/f'{n}.py'),*map(str,a)],check=True)
