"""Accept reviewed Randall quest and visit Grand Hall for supply training."""
import os,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
os.environ.update(REBORN_FAST_KEYS='1',REBORN_COORD_CACHE='1',REBORN_ROUTE_STEP_PAUSE='.10',REBORN_ROUTE_CHUNK='56')
def run(name,*args):
    print('NECROZMA QUEST',name,*args,flush=True)
    subprocess.run([sys.executable,str(ROOT/'scripts'/f'{name}.py'),*map(str,args)],check=True)
run('eventq',827,51,'talk')
run('linear_dialog',827,51,'--active','--until-choice','--burst')
run('choose_dialog','Yes|No','Yes')
run('linear_dialog',827,51,'--active','--past-choice','--after-last-choice','--burst')
run('checkpoint','Necrozma362-QuestAccepted')
run('eventq',827,39,'enter')
run('eventq',826,2,'enter')
run('fly_to',519,'--carrier','Zapdos')
run('eventq',519,116,'enter')
run('checkpoint','Necrozma362-GrandHall')
