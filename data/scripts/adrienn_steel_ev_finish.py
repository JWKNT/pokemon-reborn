"""Finish ordinary EV training, restore battle items, and assert saved native results."""
from play import ROOT
import subprocess,sys,json
def r(s,*a):subprocess.run([sys.executable,str(ROOT/'scripts'/s),*map(str,a)],check=True)
r('fly_to.py',519);r('eventq.py',519,116,'enter');r('eventq.py',38,3,'talk');r('heal.py')
r('party_take_named.py','Klinklang');r('party_take_named.py','Excadrill');r('give_held.py','Wide Lens','Klinklang')
r('checkpoint.py','Adrienn-Steel-EV-complete')
s=json.loads((ROOT/'notes/Adrienn-Steel-EV-complete-status.json').read_text());p={m['species']:m for m in s['party']}
assert p['KLINKLANG']['ev']==[252,252,3,0,0,0],p['KLINKLANG']['ev']
assert p['EXCADRILL']['ev']==[247,252,0,0,0,11],p['EXCADRILL']['ev']
assert all(m['hp']==m['totalhp']for m in s['party']);assert p['KLINKLANG']['item']=='WIDELENS'and p['EXCADRILL']['item'] is None
print('STEEL EV TRAINING VERIFIED FROM NATIVE SAVE',flush=True)
