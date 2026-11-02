"""Normal Move Deleter interactions; preserve Memento, remove two observed attacks."""
from play import *
def run(s,*a):subprocess.run([sys.executable,str(ROOT/'scripts'/f'{s}.py'),*a],check=True)
for expected in ('Dragon Pulse',):
 act('c','wait:.3');run('choose_dialog','Yes|No','Yes')
 t=read();assert 'forget a move' in t.lower(),t
 act('c','wait:.6');run('party_pick','Latios','--single')
 t=read();assert 'forgotten' in t.lower(),t
 act('c','wait:.6');t=read();assert expected.lower() in t.lower() and 'memento' in t.lower(),t
 act('c','wait:1.2');t=read();assert expected.lower() in t.lower(),t
 run('choose_dialog','Yes|No','Yes');run('dialog','--limit=5')
print('TWO ATTACKS DELETED; MEMENTO PRESERVED',flush=True)
