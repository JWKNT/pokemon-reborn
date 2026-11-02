"""Take an inspected owned Wide Lens from a named Box1 slot through normal PC UI."""
from play import *
import re
from PIL import Image
slot=int(sys.argv[1]);name=sys.argv[2];assert 0<=slot<30
t=read()
if '--menu-open' not in sys.argv:
 assert 'rattata' in t.lower() and re.search(r'box\s*1\b',t,re.I),('Fresh Box1 slot0 required',t)
 act(*[v for k in (['right:.12']*(slot%6)+['down:.12']*(slot//6)) for v in (k,'wait:.15')],'wait:.5');t=read();print(t,flush=True)
compact=re.sub('[^a-z]','',t.lower())
assert re.sub('[^a-z]','',name.lower()) in compact and 'widelens' in compact,('Owned item selection review',t)
if '--menu-open' not in sys.argv:act('c','wait:.5');t=read();print(t,flush=True)
# Source Storage.rb regular boxed-mon menu; do not proceed in quickswap mode.
assert all(n in t.lower() for n in ['summary','item','release','cancel']) and any(n in t.lower() for n in ['withdraw','withdram']),('PC action menu review',t)
subprocess.run([sys.executable,str(ROOT/'scripts/choose_dialog.py'),'Move|Summary|Multi-Move|Withdraw|Item|Mark|Release|Cancel','Item'],check=True)
t=read();print(t,flush=True)
assert 'take' in t.lower() and 'widelens' in re.sub('[^a-z]','',t.lower()),('Held item confirmation review',t)
subprocess.run([sys.executable,str(ROOT/'scripts/choose_dialog.py'),'Yes|No','Yes'],check=True)
t=read();print(t,flush=True)
assert 'took' in t.lower() and 'no item' in t.lower() and any(v in re.sub('[^a-z]','',t.lower()) for v in ['widelens','klidelens']),('Held item receipt review',t)
act('c','wait:.5','x','wait:.5')
subprocess.run([sys.executable,str(ROOT/'scripts/choose_dialog.py'),'Yes|No','No'],check=True)
act('x','wait:.5','x','wait:.5')
subprocess.run([sys.executable,str(ROOT/'scripts/overworld.py')],check=True)
