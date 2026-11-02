"""Exchange inspected Box1 slot with party slot via normal UI. Fresh Box cursor0."""
from play import *
import re,difflib
boxslot,partyslot=map(int,sys.argv[1:3]);incoming,outgoing=sys.argv[3:5]
assert 0<=boxslot<30 and 0<=partyslot<6

def verify(name,t):
 if re.sub('[^a-z]','',name.lower()) not in re.sub('[^a-z]','',t.lower()) and not any(difflib.SequenceMatcher(None,name.lower(),w.lower()).ratio()>=.7 for w in t.split()):raise SystemExit('PC selection review '+name+': '+t)
def boxkeys():return ['right:.05']*(boxslot%6)+['down:.05']*(boxslot//6)
t=read().lower()
if 'organize' in t and 'move pok' in t:act('c','wait:1.2');t=read().lower()
if not re.search(r'box\s*1',t):raise SystemExit('Fresh Box1 cursor0 required: '+t)
act('right:.05','wait:.4');t=read();print(t,flush=True);verify(incoming,t)
act('a','wait:.5',*(['down:.05']*(5-boxslot//6)),*(['left:.05'] if boxslot%6>=3 else []),'c','wait:.8',*(['down:.05']*(partyslot//2)),*(['right:.05'] if partyslot%2 else []),'a','wait:.8')
t=read();print(t,flush=True);verify(outgoing,t)
act('x','wait:.6',*boxkeys(),'a','wait:.7');t=read();print(t,flush=True);verify(outgoing,t)
act('x','wait:.5')
subprocess.run([sys.executable,str(ROOT/'scripts/choose_dialog.py'),'Yes|No','No'],check=True)
act('x','wait:.5','x','wait:.5')
subprocess.run([sys.executable,str(ROOT/'scripts/overworld.py')],check=True)
print('EXCHANGE COMPLETE',incoming,outgoing,flush=True)
