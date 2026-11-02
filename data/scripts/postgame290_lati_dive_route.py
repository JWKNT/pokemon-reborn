"""Reviewed water and ice route. Stop safely south of the anomaly trigger."""
import os,sys,json,subprocess
from pathlib import Path
R=Path(__file__).resolve().parents[1]
os.environ.update(REBORN_FAST_KEYS='1',REBORN_COORD_CACHE='1',REBORN_ROUTE_CHUNK='84')
def run(n,*a):
 print('LATI DIVE ROUTE',n,*a,flush=True)
 subprocess.run([sys.executable,str(R/'scripts'/f'{n}.py'),*map(str,a)],check=True)
s=json.loads((R/'notes/Postgame290-BoulderOpen-status.json').read_text());assert s['map']==375
n=json.loads((R/'notes/Postgame290-BoulderOpen-navigation.json').read_text());assert n['positions']['375']['1']==[12,32]
if '--under389' not in sys.argv and '--under393' not in sys.argv:
 run('surface_walk',375,40,33);run('waterfall_step',375,40,33,'up',375,40,23)
 run('surface_walk',375,14,30);run('surface_walk',375,14,39);run('dive_transition',375,14,39,389)
if '--under393' not in sys.argv:
 run('underwater_walk',389,53,33);run('eventq',389,2,'enter')
run('underwater_walk',393,15,16);run('dive_transition',393,15,16,376)
run('surface_walk',376,35,10);run('dive_transition',376,35,10,393)
run('underwater_walk',393,54,29);run('eventq',393,3,'enter')
run('underwater_walk',402,16,59);run('eventq',402,1,'enter')
run('underwater_walk',403,14,18);run('eventq',403,5,'enter')
run('checkpoint','Postgame290-UnexploredUnderwater')
s=json.loads((R/'notes/Postgame290-UnexploredUnderwater-status.json').read_text());assert s['map']==856
run('underwater_walk',856,43,187);run('dive_transition',856,43,187,857)
run('surface_walk',857,48,129);run('checkpoint','Postgame290-PreLati')
n=json.loads((R/'notes/Postgame290-PreLati-navigation.json').read_text());assert n['variables']['622']==1
print('STOPPED SOUTH OF ANOMALY TRIGGER; NO BATTLE STARTED',flush=True)
