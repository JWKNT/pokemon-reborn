"""Normal reload and reviewed tournament exit for reserve preparation."""
import json,os,subprocess,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def run(s,*a):
 print('STAGE',s,*a,flush=True)
 e=dict(os.environ,REBORN_COORD_CACHE='1');e.pop('REBORN_FAST_KEYS',None)
 if s in ['q','eventq']:e['REBORN_FAST_KEYS']='1'
 subprocess.run([sys.executable,str(R/'scripts'/f'{s}.py'),*map(str,a)],check=True,env=e)
run('play','c:.12','wait:3')
run('checkpoint','Saphira179-preparation-departure')
from play import act,read
p=R/'notes/current-run-control.json';c=json.loads(p.read_text())
assert not c.get('overworld_turbo_enabled')
# Clear any remembered battle speed using two normal world toggles.
t=read().lower();assert not any(x in t for x in ['fight','pp:','choose a pok'])
act('m:.12','wait:.35','m:.12','wait:.35')
c.update(battle_turbo_enabled=False,battle_turbo=False,active_major=None,session=179,recording_session=179,recording_closed_session=178,recording_active=True,recording_paused=False,capture_current='179 active;178 closed for review');p.write_text(json.dumps(c,indent=2))
for mid,eid in [(780,1),(778,21),(778,2),(777,36),(777,8),(777,1),(776,51),(776,7),(776,1),(768,101),(768,112),(414,22)]:run('eventq',mid,eid,'enter')
run('eventq',772,7,'talk');run('pc_open_reviewed')
run('pc_exchange_named',12,5,'Tranquill','Excadrill')
run('eventq',772,8,'enter');run('fly_to',519,'--carrier','Tranquill')
run('checkpoint','Saphira179-GrandHall-preparation')
