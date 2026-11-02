"""Reviewed puzzle/ordinary-trainer sequence; stops on any unmatched state."""
from play import *
from locate import locate
jobs=[(1,(9,55),'EXPERT_Male','Iroh','Simisear',1),(2,(9,44),'AceTrainerM','Karus','Flareon',2),(3,(9,32),'AceTrainerF','Nova','Arcanine',3)]
def run(script,*args):subprocess.run([sys.executable,str(ROOT/'scripts'/script),*map(str,args)],check=True)
assert 'fight' not in read().lower()
first=int(sys.argv[1]) if len(sys.argv)>1 else 1
if first==1:run('party_lead.py',3) # Swampert, from the verified post-Circus order.
for n,(x,y),cls,name,foe,eid in jobs:
 if n<first:continue
 run('q.py',f'419,{x},{y}');run('charlotte_puzzle.py',n)
 run('trainer_music.py','start',cls,name)
 act('up:.12','up:.12','up:.12','wait:1')
 t=read();print(t,flush=True)
 log=ROOT/'work'/f'charlotte-gym-{name.lower()}.log'
 with log.open('a')as out:
  subprocess.run([sys.executable,str(ROOT/'scripts/battle_batch.py'),'Swampert','1','--foes',foe,'--turns','6','--watch','--stay','--min-hp','.32','--stop-after-battle'],check=True,stdout=out,stderr=subprocess.STDOUT)
 run('trainer_music.py','finish');run('mark_event.py',419,eid,'A')
 print('GYM TRAINER COMPLETE',name,flush=True)
print('ALL CHARLOTTE GYM TRAINERS COMPLETE',flush=True)
