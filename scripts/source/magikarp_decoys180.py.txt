"""Source-reviewed normal decoy routes; each fight ends at a public review anchor."""
import json,os,subprocess,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def run(s,*a):
 print('STAGE',s,*a,flush=True)
 e=dict(os.environ,REBORN_COORD_CACHE='1');e.pop('REBORN_FAST_KEYS',None)
 if s in ['eventq','q','battle_batch']:e['REBORN_FAST_KEYS']='1'
 subprocess.run([sys.executable,str(R/'scripts'/f'{s}.py'),*map(str,a)],check=True,env=e)
def turbo(enabled):
 from play import act,read
 p=R/'notes/current-run-control.json';c=json.loads(p.read_text());t=read().lower()
 if enabled:
  assert 'fight' in t
  if not c.get('battle_turbo_enabled'):act('m:.12','wait:.5')
 else:
  assert 'fight' not in t and 'hp' not in t
  if c.get('battle_turbo_enabled'):act('m:.12','wait:.35','m:.12','wait:.35')
 c.update(battle_turbo_enabled=enabled,battle_turbo=enabled);p.write_text(json.dumps(c,indent=2))
def tail(m,e,page,label):
 run('ordinary_victory_tail',m,e,page)
 run('trainer_music','finish')
 turbo(False);run('checkpoint',label)
phase=sys.argv[1]
if phase=='claret-finish':
 run('switch_offered','Ninetales','Gigalith')
 run('battle_batch','Gigalith',3,'--foes','Ninetales','--turns',1,'--watch','--stop-after-victory')
elif phase=='claret-tail':tail(533,52,0,'Magikarp180-Claret-won')
elif phase=='carmen':
 run('eventq',533,88,'enter');run('fly_to',519,'--carrier','Tranquill')
 run('eventq',519,116,'enter');run('eventq',38,3,'talk');run('heal')
 run('eventq',38,6,'enter');run('fly_to',530,'--carrier','Tranquill')
 run('eventq',530,11,'enter');run('party_lead','Arcanine')
 run('checkpoint','Magikarp180-Carmen-ready')
 run('trainer_enter',522,145,'Casanova','Carmen','--burst-dialogue');run('battle_ready');turbo(True)
 run('battle_batch','Arcanine',1,'--foes','Persian,Klefki','--turns',5,'--watch','--min-hp','.5','--stay-team-reviewed','--openers','{"Persian":0}','--foe-slots','{"persian":1,"klefki":1}','--stop-after-victory')
elif phase=='carmen-tail':tail(522,145,0,'Magikarp180-Carmen-won')
elif phase=='aidan-tail':tail(526,10,0,'Magikarp180-Aidan-won')
elif phase=='crimson-heal':
 run('fly_to',526,'--carrier','Tranquill')
 run('eventq',526,15,'enter');run('eventq',100,4,'talk');run('heal');run('eventq',100,8,'enter')
 run('party_lead','Sylveon');run('checkpoint','Magikarp180-Crimson-healed')
 run('q','526,27,15')
 from play import act,read
 act('up:.12','c','wait:.8');t=read().lower();assert 'surf' in t and 'water' in t,t
 run('choose_dialog','Yes|No','Yes');act('c','wait:2')
 run('locate',526)
elif phase=='crimson':
 if '--surf-ready' not in sys.argv:
  run('fly_to',526,'--carrier','Tranquill');run('party_lead','Sylveon')
  run('checkpoint','Magikarp180-Crimson-travel')
 run('surface_event',526,9,'enter')
 run('surface_walk',536,37,18)
 run('checkpoint','Magikarp180-Crimson-ready')
 run('trainer_enter',536,31,'Casanova','Crimson','--burst-dialogue');run('battle_ready');turbo(True)
 run('battle_batch','Sylveon',3,'--foes','Bewear,Sylveon','--turns',6,'--watch','--min-hp','.45','--stay-team-reviewed','--stop-after-victory')
elif phase=='crimson-tail':tail(536,31,0,'Magikarp180-Crimson-won')
elif phase=='carmen1':
 run('fly_to',526,'--carrier','Tranquill')
 run('eventq',526,15,'enter');run('eventq',100,4,'talk');run('heal');run('eventq',100,8,'enter')
 run('party_lead','Swampert');run('eventq',526,56,'enter');run('checkpoint','Magikarp180-Carmen1-ready')
 run('trainer_enter',613,4,'Casanova','Carmen','--burst-dialogue');run('battle_ready');turbo(True)
 run('battle_batch','Swampert',0,'--foes','Weezing,Gengar','--turns',5,'--watch','--min-hp','.4','--stay-team-reviewed','--foe-slots','{"weezing":0,"gengar":1}','--stop-after-victory')
elif phase=='carmen1-tail':tail(613,4,0,'Magikarp180-Carmen1-won')
elif phase=='reveal':
 run('eventq',613,1,'enter');run('fly_to',530,'--carrier','Tranquill');run('eventq',530,11,'enter')
 run('eventq',522,145,'talk');run('linear_dialog',522,145,'--source-page',2,'--burst');run('mark_event',522,145,'B')
 run('eventq',522,145,'talk');run('linear_dialog',522,145,'--source-page',3,'--burst');run('checkpoint','Magikarp181-Corin-revealed')
 run('fly_to',523,'--carrier','Tranquill');run('eventq',523,112,'enter');run('eventq',133,1,'talk')
 run('linear_dialog',133,1,'--source-page',16,'--burst');run('checkpoint','Magikarp181-Goggles')
 run('eventq',133,4,'enter');run('fly_to',519,'--carrier','Tranquill')
 run('eventq',519,116,'enter');run('eventq',38,3,'talk');run('heal');run('eventq',38,6,'enter')
 run('party_lead','Arcanine');run('fly_to',693,'--carrier','Tranquill');run('checkpoint','Magikarp181-Corin-ready')
elif phase=='corin':
 if '--berry-ready' not in sys.argv:run('give_held','Cheri Berry','Arcanine','--pocket','Berries')
 run('checkpoint','Magikarp181-Corin-berry-ready')
 run('trainer_enter',693,15,'CORINROUGE','Corin-Rouge','--burst-dialogue')
 run('battle_ready');turbo(True)
 run('battle_batch','Arcanine',1,'--foes','Klefki,Cacturne','--turns',6,'--watch','--min-hp','.4','--stay','--openers','{"klefki":0}','--foe-slots','{"klefki":1,"cacturne":1}','--stop-after-victory')
elif phase=='corin-tail':tail(693,15,0,'Magikarp181-Corin-won')
else:raise SystemExit('Unknown phase')
