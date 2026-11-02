"""Reviewed normal-control errands after paired League training."""
import json,os,subprocess,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def run(s,*a):
 print('ERRAND',s,*a,flush=True)
 env=dict(os.environ,REBORN_COORD_CACHE='1');env.pop('REBORN_FAST_KEYS',None)
 if s in ['q','eventq','city_enter']:env.update(REBORN_FAST_KEYS='1',REBORN_ROUTE_CHUNK='84')
 subprocess.run([sys.executable,str(R/'scripts'/f'{s}.py'),*map(str,a)],check=True,env=env)
p=sys.argv[1]
if p=='circus':
 run('city_enter',633,519);run('fly_to',355)
 run('eventq',355,118,'talk');run('heal')
 run('circus_relearn_one','Mawile','Sucker Punch',12,2)
 run('eventq',355,5,'talk');run('pc_open_reviewed');run('pc_exchange_named',1,2,'Ampharos','Tranquill')
 run('teach_machine','TMX2 Fly','Altaria','Fly',2,'--single-step')
 run('checkpoint','League222-SuckerFly')
elif p=='heart':
 run('fly_to',359,'--carrier','Altaria');run('eventq',359,6,'enter');run('eventq',508,26,'enter')
 run('eventq',678,8,'item');run('checkpoint','League222-FioreHeartScale')
 run('eventq',678,1,'enter');run('eventq',508,2,'enter');run('fly_to',355,'--carrier','Altaria')
 run('circus_relearn_one','Ampharos','Power Gem',14,3);run('checkpoint','League222-PowerGem')
elif p=='cave-moves':
 run('teach_machine','TMX4','Swampert','Strength',0,'--single-step')
 run('teach_machine','TMX7','Swampert','Rock Smash',2,'--single-step')
 run('checkpoint','League222-CaveMoves')
elif p=='station':
 run('fly_to',530,'--carrier','Altaria');run('city_enter',530,591)
 run('eventq',591,6,'talk');run('choose_dialog','Yes|No','Yes');run('linear_dialog',591,6,'--active','--past-choice')
 run('checkpoint','League222-TrainTicket');run('eventq',591,19,'enter')
else:raise SystemExit('Unknown phase')
