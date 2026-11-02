"""Normal approach, fresh save, archive entry snapshot, and guarded Saphira intro."""
import subprocess,sys,json,os
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def run(s,*a):
 print('STAGE',s,*a,flush=True)
 env=dict(os.environ)
 if s in ['eventq','q']:env.update(REBORN_FAST_KEYS='1',REBORN_COORD_CACHE='1')
 subprocess.run([sys.executable,str(R/'scripts'/(s+'.py')),*map(str,a)],check=True,env=env)
if '--at-entry' not in sys.argv:
 run('eventq',778,15,'enter')
 run('q','780,30,12')
control=json.loads((R/'notes/current-run-control.json').read_text())
session=int(sys.argv[sys.argv.index('--session')+1]) if '--session' in sys.argv else int(control['recording_session'])
assert session==int(control['recording_session']), 'Current active capture required'
label=sys.argv[sys.argv.index('--label')+1] if '--label' in sys.argv else f'Saphira{session}-entry'
assert not (R/'notes'/f'{label}-status.json').exists(), 'Use a fresh attempt label'
run('checkpoint',label)
run('major_attempt','start',R/'work/major-131-draft.json',session,'--status',R/f'notes/{label}-status.json')
from play import read,act
cp=R/'notes/current-run-control.json';c=json.loads(cp.read_text())
t=read().lower();assert not any(z in t for z in ['fight','pp:','choose a pok'])
if c.get('battle_turbo_enabled'):
 assert not c.get('overworld_turbo_enabled')
 act('m:.12','wait:.35','m:.12','wait:.35')
 c.update(battle_turbo_enabled=False,battle_turbo=False);cp.write_text(json.dumps(c,indent=2))
run('trainer_enter',780,93,'SAPHIRA','Saphira')
run('battle_ready')
t=read().lower();assert 'fight' in t and ('bag' in t or 'bae' in t) and 'run' in t
act('m:.12','wait:.5')
c=json.loads(cp.read_text());c.update(battle_turbo_enabled=True,battle_turbo=True,active_major=131);cp.write_text(json.dumps(c,indent=2))
print('SAPHIRA COMMAND READY',flush=True)
