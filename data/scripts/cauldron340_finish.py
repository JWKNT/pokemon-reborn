"""Complete the second reviewed ridge climb and Adrienn's choice-free quest scene."""
import os,sys,subprocess
from pathlib import Path
R=Path(__file__).resolve().parents[1]
os.environ.update(REBORN_FAST_KEYS='1',REBORN_COORD_CACHE='1',REBORN_ROUTE_CHUNK='84')
def run(s,*a):
 print('CAULDRON FINISH',s,*a,flush=True);subprocess.run([sys.executable,str(R/'scripts'/f'{s}.py'),*map(str,a)],check=True)
run('q','646,22,21,up:.12,c,wait:1');run('finish_rock_climb',646,22,12)
run('eventq',646,36,'enter');run('settle_arrival',876);run('eventq',876,4,'talk');run('linear_dialog',876,4,'--active','--burst');run('checkpoint','Cauldron340-Complete')
