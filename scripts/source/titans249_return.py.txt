"""Travel to Danielle at the Titans tablets using normal map controls."""
import os,sys,subprocess
from pathlib import Path
R=Path(__file__).resolve().parents[1]
os.environ.update(REBORN_FAST_KEYS='1',REBORN_COORD_CACHE='1',REBORN_ROUTE_CHUNK='84')
def run(s,*a):
 print('TITANS RETURN',s,*a,flush=True);subprocess.run([sys.executable,str(R/'scripts'/f'{s}.py'),*map(str,a)],check=True)
run('eventq',38,6,'enter')
run('fly_to',359,'--carrier','Zapdos')
run('eventq',359,53,'enter')
run('checkpoint','Postgame249-ReturnLower')
run('city_enter',360,636)
run('eventq',636,9,'enter')
run('play','wait:3')
run('checkpoint','Postgame249-DaniellePortal')
run('eventq',825,1,'talk')
run('linear_dialog',825,1,'--source-page',3,'--until-choice')
run('choose_dialog','Yes|No','Yes')
run('linear_dialog',825,1,'--source-page',3,'--after-last-choice','--past-choice')
run('checkpoint','Postgame249-SimonReady')
