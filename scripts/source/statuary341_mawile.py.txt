"""One publicly verified Statuary encounter: heal if requested, Mega SD then Sucker Punch."""
from play import *
t=read();assert 'Statuary' in t and 'battle' in t,t
act('c','wait:1')
def run(s,*args):subprocess.run([sys.executable,str(ROOT/'scripts'/f'{s}.py'),*map(str,args)],check=True)
run('battle_ready');t=read();assert 'Garchomp' in t and '75' in t and ('Mamile' in t or 'Mawile' in t or 'Mauile' in t),t
for _ in range(int(sys.argv[1])):run('battle_item','Ultra Potion','Mawile')
run('battle_move',3,'--mega','--watch');run('battle_ready')
t=read();assert 'Garchomp' in t and '75' in t and 'FIGHT' in t and ('Mamile' in t or 'Mawile' in t or 'Mauile' in t),t
run('battle_move',2,'--watch');run('battle_ready')
t=read();assert 'defeated' in t.lower(),t
act('c','wait:.4');t=read();assert 'Gar' in t,t
act('c','wait:.2','d:1.0','wait:.2');print(read(),flush=True)
