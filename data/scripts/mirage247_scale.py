"""Revisit the solved tower for its still-uncollected Heart Scale; UI only."""
import os,subprocess,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1]
E=dict(os.environ,REBORN_FAST_KEYS='1',REBORN_COORD_CACHE='1',REBORN_ROUTE_CHUNK='84')
def run(s,*a):
 print('SCALE',s,*a,flush=True)
 subprocess.run([sys.executable,str(R/'scripts'/f'{s}.py'),*map(str,a)],env=E,check=True)
run('eventq',666,34,'enter')
run('settle_arrival',707)
run('eventq',707,8,'enter')
run('settle_arrival',669)
run('field_repel','Super Repel')
run('eventq',669,7,'item')
run('checkpoint','Postgame247-MirageScale')
