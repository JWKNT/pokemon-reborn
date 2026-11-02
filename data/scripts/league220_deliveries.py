"""Normal-controls Mega Ring errands, ending before any unreviewed battle."""
import subprocess,sys,os,json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def run(n,*a):
 e=dict(os.environ,REBORN_COORD_CACHE='1',REBORN_ROUTE_CHUNK='84')
 if n!='fly_to':e['REBORN_FAST_KEYS']='1'
 else:e.pop('REBORN_FAST_KEYS',None)
 print('STAGE',n,*a,flush=True);subprocess.run([sys.executable,str(R/'scripts'/f'{n}.py'),*map(str,a)],env=e,check=True)
run('eventq',532,3,'enter');run('fly_to',530);run('eventq',530,122,'item');run('fly_to',523)
run('eventq',523,3,'enter');run('quest219_return',534,4,2,'Jigglypuff');run('checkpoint','League220-JigglypuffHeld')
run('eventq',534,3,'enter');run('eventq',523,65,'enter');run('eventq',598,4,'talk');run('heal')
run('eventq',598,7,'talk');run('pc_open_reviewed');run('pc_withdraw_named',23,'Makuhita')
run('eventq',598,7,'talk');run('pc_open_reviewed');run('pc_withdraw_named',26,'Roggenrola')
run('checkpoint','League220-DeliveryParty')
