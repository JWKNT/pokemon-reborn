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
run('ordinary_victory_tail',88,8,0)
run('trainer_music','finish','--world-verified');run('checkpoint','Magikarp179-Kai-won')
clear_turbo()
for m,e in [(88,14),(95,18),(95,4),(95,15),(88,4),(85,54),(85,58)]:run('eventq',m,e,'enter')
run('fly_to',527,'--carrier','Tranquill')
run('eventq',527,142,'talk');run('linear_dialog',527,142,'--source-page',2,'--burst')
run('checkpoint','Magikarp179-Magma-clue')
run('fly_to',524,'--carrier','Tranquill');run('checkpoint','Magikarp179-Jakob-ready')
run('trainer_enter',524,165,'AQUA1','Jakob','--burst-dialogue')
run('battle_ready')
from play import read,act
assert 'fight' in read().lower();act('m:.12','wait:.5')
p=R/'notes/current-run-control.json';c=json.loads(p.read_text());c.update(battle_turbo_enabled=True,battle_turbo=True);p.write_text(json.dumps(c,indent=2))
run('battle_batch','Swampert',1,'--foes','Toxapex,Lapras,Sharpedo','--turns',5,'--watch','--stay-team-reviewed','--min-hp','.70','--stop-after-victory')
print('JAKOB BATTLE REVIEW',flush=True)
