"""Teach an explicitly selected machine through the normal bag and party menus."""
from play import *
import re,difflib
item,name,newmove,replacement=sys.argv[1:5]
replacement=int(replacement);assert 0<=replacement<4
# Reborn's native IDs differ from visible TMX numbers (TM94 is TMX7).
# Reject a mismatched requested move before opening any game menu.
source=pathlib.Path('/Applications/Reborn.app/Contents/Game/Scripts/Reborn/itemtext.rb').read_text()
blocks=re.findall(r'^  :(\w+) => \{(.*?)^  \},',source,re.M|re.S)
norm_machine=lambda value:re.sub('[^a-z0-9]','',value.lower())
native=next(((key,body) for key,body in blocks if key==item.upper()),None)
if native:
 visible=re.search(r':name => "([^"]+)"',native[1])
 move=re.search(r':tm => :(\w+)',native[1])
 assert visible and move and norm_machine(move[1])==norm_machine(newmove), 'Installed machine/move mismatch: '+item+' / '+newmove
 item=visible[1]
if '--bag-open' not in sys.argv:
 act('x','wait:.5','c','wait:1.5');t=read().lower()
 if 'pokedex' in t and ('seen' in t or 'search' in t):
  act('x','wait:1.2','down','down','c','wait:1.5');t=read().lower()
 if 'would you like to save' in t:
  act('x','wait:1.5','x','wait:1.5','x','wait:1.5',*(['up']*3),'c','wait:1.5');t=read().lower()
 if 'cancel' in t and t.count('hp')>=5:
  act('x','wait:1.2','down','c','wait:1.5');t=read().lower()
 if 'field notes' in t or 'pulse dex' in t:
  act('x','wait:1.2','up','c','wait:1.5');t=read().lower()
else:t=read().lower()
if not any(s in t for s in ['sort','close bag']) and not re.search(r'\bt[mh][a-z0-9]',t):raise SystemExit('Bag entry review: '+t)
for _ in range(9):
 t=read().lower()
 if sum(bool(re.match(r't[mh][a-z0-9]',z.strip())) for z in t.splitlines())>=3:break
 act('right','wait:.4')
else:raise SystemExit('Machine pocket review')
subprocess.run([sys.executable,str(ROOT/'scripts/bag_select.py'),item]+(['--single-step'] if '--single-step' in sys.argv else []),check=True)
act('c','wait:.5');t=read().lower()
if not any(z.strip(' •›>') in ['use','usei','uise','lse','llse','lise','uee','lee','p use','ulse','hllse'] for z in t.splitlines()):raise SystemExit('Machine use menu review: '+t)
act('c','wait:.6')
for _ in range(12):
 t=read().lower();print(t,flush=True)
 if 'teach which' in t or ('cancel' in t and t.count('hp')>=5):break
 move_prompt=re.search(r'teach\s+(.+?)\s+to\s+a',t)
 if 'teach' in t and (newmove.lower().replace(' ','') in t.replace(' ','') or (move_prompt and difflib.SequenceMatcher(None,newmove.lower().replace(' ',''),move_prompt[1].replace(' ','')).ratio()>=.84)) and any(z.strip(' •›>') in ['yes','no'] for z in t.splitlines()):
  subprocess.run([sys.executable,str(ROOT/'scripts/choose_dialog.py'),'Yes|No','Yes'],check=True)
  continue
 if re.search(r'\b(?:yes|no|fight|hp)\b',t):raise SystemExit('Machine prompt review')
 act('c','wait:.4')
else:raise SystemExit('Machine party prompt timeout')
subprocess.run([sys.executable,str(ROOT/'scripts/party_pick.py'),name,'--single'],check=True)
from learning import resolve,PLANS
PLANS[newmove.lower()]=replacement
for _ in range(12):
 t=read();print(t,flush=True)
 if 'trying to learn' in ' '.join(t.lower().split()):
  if not resolve(t):raise SystemExit('Learning prompt review')
  break
 normalized=' '.join(t.lower().split())
 if any(s in normalized for s in ['not compatible','already knows','not learn']):raise SystemExit('Teaching rejected: '+normalized)
 act('c','wait:.4')
else:raise SystemExit('Learning prompt timeout')
for _ in range(12):
 t=read().lower()
 if 'teach which' in t or sum(bool(re.match(r't[mh][a-z0-9]',z.strip())) for z in t.splitlines())>=3:break
 if 'yes' in t.splitlines() or 'no' in t.splitlines():raise SystemExit('Unexpected post-learning choice')
 act('c','wait:.4')
else:raise SystemExit('Teaching completion timeout')
subprocess.run([sys.executable,str(ROOT/'scripts/overworld.py')],check=True)
