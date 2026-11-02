"""Reviewed normal-checkpoint retry through the two Druddigon waves.
Public UI controls only; stops on a missed burn or any child guard failure.
"""
from play import *
from pathlib import Path
session=json.loads((ROOT/'notes/current-run-control.json').read_text())['session']
def run(script,*args,fast_next=None):
 env=os.environ.copy();env.pop('REBORN_FAST_CHEST_TRANSITION',None);env.pop('REBORN_POST_BATTLE_MOVES',None)
 if fast_next:env.update(REBORN_FAST_CHEST_TRANSITION='1',REBORN_POST_BATTLE_MOVES=fast_next,REBORN_FAST_KEYS='1')
 if '--checkpoint-after-pair' in sys.argv and fast_next=='down,left,left,left,up':env['REBORN_POST_BATTLE_CHECKPOINT']='Saphira-Drudd-recovery'+str(session)
 r=subprocess.run([sys.executable,str(ROOT/'scripts'/script),*map(str,args)],env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
 print(r.stdout,flush=True);assert r.returncode==0,(script,r.returncode)
 return r.stdout
def switch(name):run('battle_switch.py',name)
def move(actor,slot,turns=1,fast_next=None):return run('battle_batch.py',actor,slot,'--foes','Druddigon','--wild','--turns',turns,'--watch',*(['--world-pause']if fast_next else ['--status-move']),fast_next=fast_next)
def ready():
 for _ in range(15):
  text=read().lower()
  if 'what will' in text and 'fight' in text:return
  assert 'best you can do' not in text,'Chest loss'
  act('wait:.3')
 raise RuntimeError('Battle command did not appear')
if '--battle13-open' not in sys.argv:
 assert 'continue' in read().lower(),'Start at observed Continue for native Magneton checkpoint'
 act('c:.12','wait:1.8','right:.12','wait:.12','up:.12','wait:.12','up:.12','wait:.12','left:.12','wait:.3')
 run('chest_await.py','--world-open')
ready()
switch('Arcanine');switch('Excadrill');move('Excadrill',0,3,'down')
ready()
text=move('Cofagrigus',2)
assert 'was burned' in text.lower(),'Burn not publicly verified; stop before recovery plan'
switch('Arcanine');run('battle_item.py','Lemonade','Sylveon','--single-step');switch('Sylveon')
move('Sylveon',0);move('Sylveon',1);move('Sylveon',0);switch('Cofagrigus')
switch('Sylveon');move('Sylveon',0);move('Sylveon',1);move('Sylveon',0);switch('Swampert')
move('Swampert',1,1,'down,left,left,left,up')
print('PAIR DONE; '+('Saved message pause' if '--checkpoint-after-pair' in sys.argv else 'inspect incoming Tyrantrum'),flush=True)
