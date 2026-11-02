"""Continue inspected Magikarp quest through Kai using normal controls."""
import json,os,subprocess,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def run(s,*a):
 print('STAGE',s,*a,flush=True)
 e=dict(os.environ,REBORN_COORD_CACHE='1');e.pop('REBORN_FAST_KEYS',None)
 if s in ['eventq','q','battle_batch']:e['REBORN_FAST_KEYS']='1'
 subprocess.run([sys.executable,str(R/'scripts'/f'{s}.py'),*map(str,a)],check=True,env=e)
if '--at-slums' not in sys.argv:
 if '--at-obsidia-repel' not in sys.argv:
  if '--tail-complete' not in sys.argv:run('ordinary_victory_tail',62,5,0)
  run('trainer_music','finish','--world-verified');run('checkpoint','Magikarp179-goons-won')
  from play import read,act
  p=R/'notes/current-run-control.json';c=json.loads(p.read_text());t=read().lower();assert 'fight' not in t
  if c.get('battle_turbo_enabled'):
   act('m:.12','wait:.35','m:.12','wait:.35');c.update(battle_turbo_enabled=False,battle_turbo=False);p.write_text(json.dumps(c,indent=2))
  run('eventq',62,6,'enter');run('fly_to',520,'--carrier','Tranquill')
  run('field_repel','Super Repel')
 for mid,eid in [(520,241),(528,9),(85,55),(85,17)]:run('eventq',mid,eid,'enter')
 run('checkpoint','Magikarp179-Kai-ready')
for m,e in [(88,13),(95,17),(95,19),(95,3)]:run('eventq',m,e,'enter')
run('checkpoint','Magikarp179-Kai-door')
run('eventq',88,8,'talk');run('choose_dialog','No|Yes','No','--source',88,8)
run('trainer_enter',88,8,'YOUNGSTER','Kai','--active-dialogue','--past-choice','--reviewed-choice-labels','["No","Yes"]')
from play import read,act
p=R/'notes/current-run-control.json'
run('battle_ready');t=read().lower();assert 'fight' in t and 'bag' in t
act('m:.12','wait:.5');c=json.loads(p.read_text());c.update(battle_turbo_enabled=True,battle_turbo=True);p.write_text(json.dumps(c,indent=2))
run('battle_batch','Swampert',0,'--foes','Feebas,Drilbur,Swinub','--turns',5,'--watch','--stay-team-reviewed','--min-hp','.95','--stop-after-victory')
print('KAI BATTLE REVIEW',flush=True)
