"""Reviewed normal return via Dive, upper Ametrine lake and Waterfall."""
import os,subprocess,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1]
os.environ.update(REBORN_FAST_KEYS='1',REBORN_COORD_CACHE='1',REBORN_ROUTE_CHUNK='84')
def run(n,*a):
 print('RETURN',n,*a,flush=True)
 subprocess.run([sys.executable,str(R/'scripts'/f'{n}.py'),*map(str,a)],check=True)
if '--upper-lake' not in sys.argv:
 run('underwater_walk',389,14,39)
 run('dive_transition',389,14,39,375)
 run('surface_walk',375,14,30)
 run('surface_walk',375,40,12)
run('play','up:.12','c','wait:.8')
run('choose_dialog','Yes|No','Yes')
run('dialog','--limit=12')
run('checkpoint','Postgame292-AmetrineReturn')
import json
s=json.loads((R/'notes/Postgame292-AmetrineReturn-status.json').read_text())
assert s['map']==364,s
run('surface_walk',364,96,20)
run('eventq',364,15,'enter')
run('fly_to',519,'--carrier','Zapdos')
run('eventq',519,116,'enter')
run('eventq',38,3,'talk');run('heal')
run('checkpoint','Postgame292-Town')
