"""Travel normally to installed Focus Blast pickup area; stop for cliff review."""
import os,subprocess,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1]
os.environ.update(REBORN_FAST_KEYS='1',REBORN_COORD_CACHE='1',REBORN_ROUTE_STEP_PAUSE='.10',REBORN_ROUTE_CHUNK='56')
def run(s,*a):
 print('FOCUS TRIP',s,*a,flush=True);subprocess.run([sys.executable,str(R/'scripts'/f'{s}.py'),*map(str,a)],check=True)
run('teach_machine','TMX9','Heatran','Rock Climb',3)
run('overworld')
run('eventq',827,39,'enter')
run('eventq',826,2,'enter')
run('fly_to',564,'--carrier','Rayquaza')
run('city_enter',564,563)
run('checkpoint','Pavilion375-Apophyll')
