"""Reviewed Celestinine descent through ordinary surf and transfer controls."""
import os,subprocess,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1]
os.environ.update(REBORN_FAST_KEYS='1',REBORN_COORD_CACHE='1',REBORN_ROUTE_CHUNK='84')
def run(n,*a):
 print('HEATRAN DEPTHS',n,*a,flush=True);subprocess.run([sys.executable,str(R/'scripts'/f'{n}.py'),*map(str,a)],check=True)
run('use_field_item','Super Repel')
run('surface_walk',359,21,47)
run('play','up:.12','wait:2')
run('surface_event',380,24,'enter')
run('surface_event',386,10,'enter')
run('checkpoint','Heatran294-CelestinineB2')
