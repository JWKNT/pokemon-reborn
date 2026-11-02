"""Bounded normal Circus wins with the current reviewed mixed roster.
No save/reload or game-state edits; every victory earns its normal reward.
"""
from play import *
def run(s,*args):
 env=dict(os.environ)
 if s in ['battle_switch','trainer_plan']:env['REBORN_FAST_KEYS']='1'
 subprocess.run([sys.executable,str(ROOT/'scripts'/(s+'.py')),*map(str,args)],check=True,env=env)
rounds=int(sys.argv[1]);assert 1<=rounds<=4
for n in range(rounds):
 run('party_front','Arcanine')
 run('eventq',355,126,'talk')
 run('choose_dialog','Yes|No','Yes','--source',355,126)
 run('trainer_enter',355,126,'INDRA','Indra','--active-dialogue','--past-choice')
 run('trainer_plan',ROOT/'work/indra-main-training-plan.json',ROOT/f'work/indra-main-{int(time.time())}.log')
 run('linear_dialog',355,126,'--active','--past-battle','--past-choice')
 run('trainer_music','finish','--world-verified')
 print('MAIN TRAINING VICTORY',n+1,'/',rounds,flush=True)
