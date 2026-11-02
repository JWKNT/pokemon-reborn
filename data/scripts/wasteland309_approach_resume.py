"""Normal crystal interaction, connected walking and four planned entrance pushes."""
import os,subprocess,sys,json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
os.environ.update(REBORN_FAST_KEYS='1',REBORN_COORD_CACHE='1',REBORN_ROUTE_CHUNK='112')
def run(n,*a):
 print('WASTELAND APPROACH',n,*a,flush=True);subprocess.run([sys.executable,str(R/'scripts'/f'{n}.py'),*map(str,a)],check=True)
run('eventq',273,7,'smash');run('checkpoint','Wasteland309-CrystalPassage')
run('city_enter',273,274);run('connected_walk',274,230);run('connected_walk',230,249);run('city_enter',249,275)
run('wall309_strength');run('wasteland309_push',275,2,'right',2,'Wasteland309-Room275');run('city_enter',275,276)
run('wall309_strength');run('wasteland309_push',276,1,'right',1,'Wasteland309-Room276A');run('wasteland309_push',276,2,'right',1,'Wasteland309-Room276B');run('city_enter',276,277)
run('wall309_strength');run('checkpoint','Wasteland309-WallStart')
