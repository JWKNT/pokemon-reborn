"""Normal travel to Seacrest and accept the inspected Tapu quest."""
import os,sys,subprocess
from pathlib import Path
R=Path(__file__).resolve().parents[1]
os.environ.update(REBORN_FAST_KEYS='1',REBORN_COORD_CACHE='1',REBORN_ROUTE_CHUNK='112')
def run(n,*a):
 print('TAPU ACCEPT',n,*a,flush=True)
 subprocess.run([sys.executable,str(R/'scripts'/f'{n}.py'),*map(str,a)],check=True)
run('party_front','Zapdos')
run('fly_to',527,'--carrier','Zapdos')
run('eventq',527,87,'enter')
run('eventq',826,6,'enter')
run('eventq',827,85,'talk')
run('linear_dialog',827,85,'--source-page',8,'--until-choice','--burst')
run('choose_dialog','Yes|No','Yes')
run('linear_dialog',827,85,'--source-page',8,'--past-choice','--burst')
run('checkpoint','Tapu303-Accepted')
