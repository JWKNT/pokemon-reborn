"""Bounded normal Circus wins with the current reviewed mixed roster.
No save/reload or game-state edits; every victory earns its normal reward.
"""
from play import *
def run(s,*args):
 env=dict(os.environ)
 if s in ['battle_switch','trainer_plan','eventq']:env['REBORN_FAST_KEYS']='1'
 if s=='eventq':env.update(REBORN_ROUTE_CHUNK='84',REBORN_COORD_CACHE='1')
 subprocess.run([sys.executable,str(ROOT/'scripts'/(s+'.py')),*map(str,args)],check=True,env=env)
rounds=1
for n in range(rounds):
 cp=ROOT/'notes/current-run-control.json';control=json.loads(cp.read_text())
 if control.get('battle_turbo_enabled',False):
  assert not control.get('overworld_turbo_enabled',False)
  t=read().lower();assert not any(z in t for z in ['fight','pp:','choose a pok']), 'World boundary required for speed reset'
  # Two normal world toggles clear remembered battle turbo while restoring
  # normal walking. This makes the next trainer's intro readable at normal speed.
  act('m:.12','wait:.35','m:.12','wait:.35')
  control.update(battle_turbo_enabled=False,battle_turbo=False);cp.write_text(json.dumps(control,indent=2))
 run('party_front','Arcanine')
 run('eventq',355,126,'talk')
 run('choose_dialog','Yes|No','Yes','--source',355,126)
 run('trainer_enter',355,126,'INDRA','Indra','--active-dialogue','--past-choice')
 turbo='--turbo' in sys.argv
 if turbo:
  run('battle_ready')
  t=read().lower();assert 'fight' in t and any(w in t.splitlines() for w in ['bag','bae']) and 'run' in t,'Turbo requires visible battle command'
  cp=ROOT/'notes/current-run-control.json';control=json.loads(cp.read_text())
  assert not control.get('overworld_turbo_enabled',False)
  if not control.get('battle_turbo_enabled',False):act('m:.12','wait:.5')
  control.update(battle_turbo_enabled=True,battle_turbo=True,battle_turbo_evidence='Normal M at reviewed Indra command; installed System.rb restores overworld speed automatically after battle');cp.write_text(json.dumps(control,indent=2))
 # System.rb keeps battle and overworld turbo separately. Do not toggle at
 # the world return: that would enable fast walking instead of disabling it.
 plan=pathlib.Path(sys.argv[sys.argv.index('--plan')+1]) if '--plan' in sys.argv else ROOT/'work/session176-indra-plan.json'
 run('trainer_plan',plan,ROOT/f'work/indra-main-{int(time.time())}.log')
 run('linear_dialog',355,126,'--active','--past-battle','--past-choice')
 run('trainer_music','finish')
 print('MAIN TRAINING VICTORY',n+1,'/',rounds,flush=True)
