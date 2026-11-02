"""Reviewed Tyrantrum wave and public-pixel interception of Knight Edgard12."""
from play import *
def run(slot,turns,finish=False):
 env=os.environ.copy()
 if finish:env.update(REBORN_FAST_CHEST_TRANSITION='1',REBORN_POST_BATTLE_GOAL='27,44',REBORN_FAST_KEYS='1')
 if finish and '--checkpoint-after-tyran' in sys.argv:env['REBORN_POST_BATTLE_CHECKPOINT']='Saphira-Tyran-win'+str(json.loads((ROOT/'notes/current-run-control.json').read_text())['session'])
 cmd=[sys.executable,str(ROOT/'scripts/battle_batch.py'),'Cofagrigus',str(slot),'--foes','Tyrantrum','--wild','--turns',str(turns),'--watch','--world-pause' if finish else '--status-move']
 r=subprocess.run(cmd,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
 print(r.stdout,flush=True);assert r.returncode==0
 return r.stdout
for _ in range(15):
 t=read().lower()
 if 'what will' in t and 'fight' in t:break
 act('wait:.3')
else:raise RuntimeError('No command screen')
assert 'tyrantrum' in t and 'cofagrigus' in t
assert 'was burned' in run(2,1).lower(),'Burn not confirmed'
run(1,2,True)
