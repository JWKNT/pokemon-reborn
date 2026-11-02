"""Exchange inspected Box1 slot with party slot via normal UI. Fresh box cursor0; optional --box verifies selected box."""
from play import *
import re,difflib
_play_act=act
def act(*keys):
 # PC grid animation can swallow successive fast-driver arrows.
 _play_act(*[v for k in keys for v in ((k,'wait:.15') if k.startswith(('up:','down:','left:','right:')) else (k,))])
boxslot,partyslot=map(int,sys.argv[1:3]);incoming,outgoing=sys.argv[3:5]
assert 0<=boxslot<30 and 0<=partyslot<6
boxnumber=int(sys.argv[sys.argv.index('--box')+1]) if '--box' in sys.argv else 1
assert 1<=boxnumber<=50

def verify(name,t):
 if name=="Mew":t=re.sub(r"(?im)^hew$","Mew",t)
 t=t.replace("Meutwa","Mewtwo").replace("Mewtuo","Mewtwo")
 if re.sub('[^a-z]','',name.lower()) not in re.sub('[^a-z]','',t.lower()) and not any(difflib.SequenceMatcher(None,name.lower(),w.lower()).ratio()>=.7 for w in t.split()):raise SystemExit('PC selection review '+name+': '+t)
def boxkeys():return ['right:.12']*(boxslot%6)+['down:.12']*(boxslot//6)
t=read().lower()
if 'organize' in t and 'move pok' in t:act('c','wait:1.2');t=read().lower()
if not re.search(r'b(?:l)?ox\s*'+str(boxnumber)+r'\b',t):
 from PIL import Image
 crop=ROOT/'work/pc-box-header.png'
 Image.open(ROOT/'recordings/capture-preview.png').crop((517,48,635,90)).resize((708,252)).save(crop)
 header=' '.join(v['text'] for v in json.loads(subprocess.check_output([str(ROOT/'scripts/observe'),str(crop)])))
 if not re.search(r'b(?:l)?ox\s*'+str(boxnumber)+r'\b',header,re.I):raise SystemExit('Fresh selected box cursor0 required: '+header)

act(*boxkeys(),'wait:.4');t=read();print(t,flush=True);verify(incoming,t)
act('a','wait:.5',*(['down:.12']*(5-boxslot//6)),*(['left:.12'] if boxslot%6>=3 else []),'c','wait:.8',*(['down:.12']*(partyslot//2)),*(['right:.12'] if partyslot%2 else []),'a','wait:.8')
t=read();print(t,flush=True);verify(outgoing,t)
act('x','wait:.6',*boxkeys(),'a','wait:.7');t=read();print(t,flush=True);verify(outgoing,t)
if '--stay-open' in sys.argv:
 act(*(['up:.12']*(boxslot//6)),*(['left:.12']*(boxslot%6)),'wait:.4')
 print('EXCHANGE COMPLETE; selected box cursor reset to slot0',read(),flush=True)
 raise SystemExit(0)
act('x','wait:.5')
subprocess.run([sys.executable,str(ROOT/'scripts/choose_dialog.py'),'Yes|No','No'],check=True)
act('x','wait:.5','x','wait:.5')
subprocess.run([sys.executable,str(ROOT/'scripts/overworld.py')],check=True)
print('EXCHANGE COMPLETE',incoming,outgoing,flush=True)
