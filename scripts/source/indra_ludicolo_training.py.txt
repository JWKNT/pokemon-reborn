"""Reviewed normal Circus battles: lead Power-Weight Ludicolo, paid Arcanine switch.
No save/reload, no game-state writes. Stop on any unhandled battle condition.
"""
from play import *
def run(s,*args):
 env=dict(os.environ)
 if s in ['battle_switch','trainer_plan']:env['REBORN_FAST_KEYS']='1'
 subprocess.run([sys.executable,str(ROOT/'scripts'/(s+'.py')),*map(str,args)],check=True,env=env)
rounds=int(sys.argv[1]);assert 1<=rounds<=4
for n in range(rounds):
 run('party_front','Ludicolo','Arcanine')
 run('eventq',355,126,'talk')
 run('choose_dialog','Yes|No','Yes','--source','355','126')
 run('trainer_enter',355,126,'INDRA','Indra','--active-dialogue','--past-choice')
 run('battle_switch','Arcanine')
 run('trainer_plan',ROOT/'work/indra-ludicolo-training-plan.json',ROOT/f'work/indra-ludi-{int(time.time())}.log')
 run('linear_dialog',355,126,'--active','--past-battle','--past-choice')
 run('trainer_music','finish','--world-verified')
 print('LUDICOLO HP TRAINING ROUND COMPLETE',n+1,flush=True)
