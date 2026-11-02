"""Take a source-reviewed boxed member's item from a fresh Box1 cursor."""
from play import *
import re
slot=int(sys.argv[1]);name,item=sys.argv[2:4]
boxnumber=int(sys.argv[sys.argv.index('--box')+1]) if '--box' in sys.argv else 1
assert 1<=boxnumber<=50
assert 0<=slot<30
# The outlined W in the Wise Glasses receipt was directly reviewed in session292.
norm=lambda s:re.sub('[^a-z]','',s.lower()).replace('kiseglasses','wiseglasses').replace('meoustic','meowstic')
t=read()
if '--menu-open' not in sys.argv:
 assert re.search(r'b(?:l)?ox\s*'+str(boxnumber)+r'\b',t,re.I),('Fresh selected box cursor0 required',t)
 keys=['right:.12']*(slot%6)+['down:.12']*(slot//6)
 act(*[v for key in keys for v in (key,'wait:.15')],'wait:.5')
 t=read();print(t,flush=True)
assert norm(name) in norm(t) and norm(item) in norm(t),('Owned species/item mismatch',t)
if '--menu-open' not in sys.argv:
 act('c','wait:.5');t=read();print(t,flush=True)
assert all(s in t.lower() for s in ['summary','item','release','cancel']),('PC action menu review',t)
subprocess.run([sys.executable,str(ROOT/'scripts/choose_dialog.py'),'Move|Summary|Multi-Move|Withdraw|Item|Mark|Release|Cancel','Item'],check=True)
t=read();print(t,flush=True)
assert 'take' in t.lower() and norm(item) in norm(t),('Held item confirmation review',t)
subprocess.run([sys.executable,str(ROOT/'scripts/choose_dialog.py'),'Yes|No','Yes'],check=True)
t=read();print(t,flush=True)
assert any(s in t.lower() for s in ['took','received']) and norm(item) in norm(t),('Held item receipt review',t)
act('c','wait:.5','x','wait:.5')
subprocess.run([sys.executable,str(ROOT/'scripts/choose_dialog.py'),'Yes|No','No'],check=True)
act('x','wait:.5','x','wait:.5')
subprocess.run([sys.executable,str(ROOT/'scripts/overworld.py')],check=True)
