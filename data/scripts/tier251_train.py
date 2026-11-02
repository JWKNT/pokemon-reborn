"""Travel normally to Grand Hall and run three bounded training rounds."""
import os,sys,subprocess
from pathlib import Path
R=Path(__file__).resolve().parents[1]
os.environ.update(REBORN_FAST_KEYS='1',REBORN_COORD_CACHE='1',REBORN_ROUTE_CHUNK='84')
def run(s,*a):
 print('TRAIN',s,*a,flush=True);subprocess.run([sys.executable,str(R/'scripts'/f'{s}.py'),*map(str,a)],check=True)
run('city_enter',827,826)
run('city_enter',826,527)
run('fly_to',519,'--carrier','Zapdos')
run('eventq',519,116,'enter')
for n in range(1,4):run('jb_training_round',f'Postgame251-JB{n}')
