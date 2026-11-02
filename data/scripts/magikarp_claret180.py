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
if '--repel-active' not in sys.argv:
 run('party_lead','Sylveon')
 run('field_repel','Super Repel')
run('eventq',523,42,'enter')
run('checkpoint','Magikarp180-Claret-ready')
run('trainer_enter',533,52,'Casanova','Claret')
run('battle_ready')
from play import act,read
assert 'fight' in read().lower();act('m:.12','wait:.5')
p=R/'notes/current-run-control.json';c=json.loads(p.read_text());c.update(battle_turbo_enabled=True,battle_turbo=True);p.write_text(json.dumps(c,indent=2))
run('battle_batch','Sylveon',3,'--foes','Ninetales,Zoroark','--turns',2,'--watch','--min-hp','.55','--stop-after-victory')
print('CLARET OPENING REVIEW: switch Gigalith at real Ninetales offer, Rock Slide',flush=True)
