"""Withdraw a verified selected-box Pokemon into a free party slot using normal PC menus."""
from play import *
import difflib
_play_act=act
def act(*keys):
 _play_act(*[v for k in keys for v in ((k,"wait:.15") if k.startswith(("up:","down:","left:","right:")) else (k,))])
slot=int(sys.argv[1]);name=sys.argv[2];assert 0<=slot<30
boxnumber=int(sys.argv[sys.argv.index('--box')+1]) if '--box' in sys.argv else 1
assert 1<=boxnumber<=50
norm=lambda s:re.sub('[^a-z]','',s.lower())
def verify(t):
 assert norm(name) in norm(t) or any(difflib.SequenceMatcher(None,name.lower(),w.lower()).ratio()>=.8 for w in t.split()),t
t=read()
if 'organize' in t.lower() and 'move pok' in t.lower():act('c','wait:1.5');t=read()
assert re.search(r'b(?:l)?ox\s*'+str(boxnumber)+r'\b',t,re.I),'Fresh selected box cursor0 required: '+t
act(*(['right:.12']*(slot%6)),*(['down:.12']*(slot//6)),'wait:.4');t=read();print(t,flush=True);verify(t)
act('c','wait:.5')
subprocess.run([sys.executable,str(ROOT/'scripts/choose_dialog.py'),'Move|Summary|Multi-Move|Withdraw|Item|Mark|Release|Cancel','Withdraw'],check=True)
t=read();assert 'full' not in t.lower(),t
act('x','wait:.5');subprocess.run([sys.executable,str(ROOT/'scripts/choose_dialog.py'),'Yes|No','No'],check=True)
act('x','wait:.5','x','wait:.5');subprocess.run([sys.executable,str(ROOT/'scripts/overworld.py')],check=True)
subprocess.run([sys.executable,str(ROOT/'scripts/party_open.py')],check=True);verify(read())
subprocess.run([sys.executable,str(ROOT/'scripts/overworld.py')],check=True)
print('WITHDRAW VERIFIED IN PUBLIC PARTY',name,flush=True)
