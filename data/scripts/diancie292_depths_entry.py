"""Source-reviewed normal Dive route into Aegir Depths; no boss triggers."""
import os,sys,subprocess,json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
os.environ.update(REBORN_FAST_KEYS='1',REBORN_COORD_CACHE='1',REBORN_ROUTE_CHUNK='84')
def run(n,*a):
 print('DEPTHS ENTRY',n,*a,flush=True)
 subprocess.run([sys.executable,str(R/'scripts'/f'{n}.py'),*map(str,a)],check=True)
nav=json.loads((R/'notes/navigation-state.json').read_text());assert nav['variables']['626']==1
if '--underwater' not in sys.argv:
 run('surface_walk',850,54,65)
 run('dive_transition',850,54,65,851)
run('underwater_walk',851,55,64)
run('eventq',851,15,'enter')
run('underwater_walk',851,39,106)
run('dive_transition',851,39,106,850)
run('surface_walk',850,39,110)
run('eventq',850,116,'enter')
run('checkpoint','Diancie292-Depths')
run('teach_machine','TM31','Volcanion','Brick Break',2)
run('teach_machine','TM78','Swampert','Bulldoze',1)
run('checkpoint','Diancie292-DepthsBuild')
