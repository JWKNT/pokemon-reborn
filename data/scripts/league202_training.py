"""Bounded normal-controls paired EV training, reconciled against native saves."""
import json,os,subprocess,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1]
os.environ['REBORN_COORD_CACHE']='1'
def run(s,*a):
 print('STAGE',s,*a,flush=True)
 env=dict(os.environ)
 if s in ['q','eventq']:env.update(REBORN_FAST_KEYS='1',REBORN_ROUTE_CHUNK='112')
 subprocess.run([sys.executable,str(R/'scripts'/f'{s}.py'),*map(str,a)],check=True,env=env)
def check(label,me,ce):
 run('checkpoint',label)
 st=json.loads((R/'notes'/f'{label}-status.json').read_text())
 for species,ev in [('MIENSHAO',me),('CRYOGONAL',ce)]:
  m=next(m for m in st['party'] if m['species']==species)
  assert m['ev']==ev,(species,m['ev'],ev)
 print('SAVED PAIRED EV VERIFIED',me,ce,flush=True)
# Pilot native save confirms battle switching preserves Mienshao in party slot0.
# The battle helper verifies the named hunter at every encounter, avoiding redundant party menus.
def bulk(n,slot=1):run('train_wild_bulk','Hexan',slot,n,'--hunter','Mienshao','--targets','Noibat,Woobat','--flex-targets','--ev-ledger','--recover-slot',2)
phase=sys.argv[1]
if phase=='travel':
 run('give_held','Power Bracer','Mienshao');run('give_held','Power Lens','Hexan')
 run('party_front','Mienshao')
 run('fly_to',519,'--carrier','Tranquill')
 run('q','519,9,60,left,wait:2','530,94,13,right,wait:2','519,29,11,right,wait:2','513,15,8,right,wait:2','519,58,11,right,wait:2','633,10,8')
 check('Prep202-EV-ready',[0,79,0,0,0,108],[0,0,0,41,0,142])
elif phase=='pilot':
 bulk(1);check('Prep202-EV-pilot',[0,111,0,0,0,108],[0,0,0,73,0,142])
elif phase=='attack-special':
 bulk(5);check('Prep202-Attack-done',[0,252,0,0,0,108],[0,0,0,233,0,142])
elif phase=='mixed':
 run('give_held','Power Anklet','Mienshao');bulk(1)
 check('Prep202-Special-done',[0,252,0,0,0,140],[0,0,0,252,0,142])
elif phase=='speed':
 run('give_held','Power Anklet','Hexan');bulk(4,3)
 check('Prep202-EV-complete',[0,252,0,0,0,252],[0,0,0,252,0,252])
 run('give_held','Protective Pads','Mienshao');run('take_held','Hexan','Power Anklet')
else:raise SystemExit('Unknown phase')
