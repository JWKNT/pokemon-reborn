"""Normal-controls Mega Ring errands, ending before any unreviewed battle."""
import subprocess,sys,os,json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def run(n,*a):
 e=dict(os.environ,REBORN_COORD_CACHE='1',REBORN_ROUTE_CHUNK='84')
 if n!='fly_to':e['REBORN_FAST_KEYS']='1'
 else:e.pop('REBORN_FAST_KEYS',None)
 print('STAGE',n,*a,flush=True);subprocess.run([sys.executable,str(R/'scripts'/f'{n}.py'),*map(str,a)],env=e,check=True)
run('choose_dialog','Yes|No','No')
run('play','x','wait:.5','x','wait:.5');run('overworld')
run('party_open');run('overworld')
run('eventq',598,7,'talk');run('pc_open_reviewed');run('pc_withdraw_named',26,'Roggenrola')
run('checkpoint','League220-DeliveryParty')
run('eventq',598,8,'enter');run('fly_to',564);run('eventq',564,4,'enter')
run('eventq',23,16,'talk');run('linear_dialog',23,16,'--source-page',0,'--burst')
run('checkpoint','League220-FeliciaIntro')
run('eventq',23,2,'enter');run('fly_to',527);run('eventq',527,87,'enter')
run('eventq',826,8,'talk');run('linear_dialog',826,8,'--source-page',2,'--burst')
run('checkpoint','League220-ArcAutograph')
