"""Reviewed normal quest continuation after observed Kai victory."""
import json,os,subprocess,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def run(s,*a):
 print('STAGE',s,*a,flush=True)
 e=dict(os.environ,REBORN_COORD_CACHE='1');e.pop('REBORN_FAST_KEYS',None)
 if s in ['eventq','q','battle_batch']:e['REBORN_FAST_KEYS']='1'
 subprocess.run([sys.executable,str(R/'scripts'/f'{s}.py'),*map(str,a)],check=True,env=e)
def clear_turbo():
 from play import act,read
 p=R/'notes/current-run-control.json';c=json.loads(p.read_text());t=read().lower();assert 'fight' not in t
 if c.get('battle_turbo_enabled'):
  act('m:.12','wait:.35','m:.12','wait:.35');c.update(battle_turbo_enabled=False,battle_turbo=False);p.write_text(json.dumps(c,indent=2))
run('ordinary_victory_tail',524,165,3)
run('trainer_music','finish','--world-verified');run('checkpoint','Magikarp179-Jakob-won')
clear_turbo()
for m,e in [(524,30),(168,8)]:run('eventq',m,e,'enter')
run('eventq',168,18,'talk');run('choose_dialog','7th Street|Lapis Ward','7th Street');run('dialog','--limit=5')
run('checkpoint','Magikarp179-elevator')
for m,e in [(168,11),(168,15)]:run('eventq',m,e,'enter')
run('eventq',324,74,'talk');run('choose_dialog','Yes|No','Yes','--source',324,74)
run('linear_dialog',324,74,'--source-page',0,'--past-choice','--burst')
run('checkpoint','Magikarp179-stolen')
print('QUEST PHASE8 REVIEW',flush=True)
