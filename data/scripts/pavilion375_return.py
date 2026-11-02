"""Return the coverage-ready roster to the Pavilion before starting another attempt."""
import os,sys,subprocess
from pathlib import Path
R=Path(__file__).resolve().parents[1]
os.environ.update(REBORN_FAST_KEYS='1',REBORN_COORD_CACHE='1',REBORN_ROUTE_CHUNK='56')
def run(s,*a):
 print('PAVILION RETURN',s,*a,flush=True);subprocess.run([sys.executable,str(R/'scripts'/f'{s}.py'),*map(str,a)],check=True)
run('teach_machine','TM33','Cresselia','Reflect',2)
run('overworld')
run('fly_to',527,'--carrier','Rayquaza')
run('city_enter',527,826)
run('city_enter',826,827)
run('q','827,8,8,up:.12')
run('checkpoint','Pavilion375-ThirdPrepared')
