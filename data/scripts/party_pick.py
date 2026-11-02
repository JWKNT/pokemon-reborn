"""Select a named Pokemon after observing and verifying the party cursor."""
from play import *
import difflib,re
from party_cursor import selected_card,selection_path
name=sys.argv[1].lower();r=snap();t=' '.join(v['text'].lower() for v in r)
if not (any(w in t for w in ['choose a pok','chooce a pok','choose pok','on which','teach which']) or ('cancel' in t and (t.count('hp')>=5 or t.count('able')>=2))):raise SystemExit('Party selection expected')
for observation in range(3):
 candidates=[]
 for v in r:
  word=re.sub('[^a-z]','',v['text'].lower());word={'hew':'mew','monaros':'ampharos','ampharoe':'ampharos','arpharos':'ampharos','auveon':'sylveon','suveon':'sylveon','auveor':'sylveon'}.get(word,word);score=difflib.SequenceMatcher(None,name,word).ratio()
  if score>=.78 and .1<v['y']<.7:candidates.append((score,v))
 if candidates:break
 r=snap()
if not candidates:raise SystemExit('Pokemon name not found')
v=max(candidates,key=lambda a:a[0])[1];col=int(v['x']>.5);row=round((v['y']-(.15 if not col else .195))/.21)
if row not in [0,1,2]:raise SystemExit('Party row review')
print('PARTY PICK',v['text'],'slot',row*2+col,flush=True)
target=row*2+col
keys=selection_path(selected_card(STATE),target,multiselect=("confirm" in t and "entered" in t))
# Allow each visible cursor step to settle; consecutive same-key fast taps
# otherwise occasionally collapse into one input (session290 Fly recovery).
if keys:act(*[v for key in keys for v in (key,'wait:.09')],'wait:0.3');snap()
if selected_card(STATE)!=target:raise SystemExit('Party cursor mismatch; stopped before selection')
act('c:0.12','wait:1.0')
confirmed_switch=False
for _ in range(4):
 t=read();low=t.lower();print(t,flush=True)
 if '--single' in sys.argv:break
 if re.search(r'(?:do|lo|o)\s*what\s*with',low):
  m=re.search(r'(?:do|lo|o)\s*what\s*with\s+([a-z ]+)',low)
  if not m or difflib.SequenceMatcher(None,name,m.group(1).replace(' ','')).ratio()<.78:raise SystemExit('Selected Pokemon mismatch; confirmation stopped')
  if not re.search(r'sw(?:i|ui)tch\s*in',low):raise SystemExit('Switch option review')
  act('c:0.12','wait:1.5');confirmed_switch=True;continue
 if 'cancel' in low and low.count('hp')>=5:
  # A double faint offers the next replacement immediately after the first.
  if confirmed_switch:break
  act('c:0.12','wait:1.0');continue
 break
else:raise SystemExit('Party confirmation did not complete')
if '--single' not in sys.argv:
 subprocess.run([sys.executable,str(ROOT/'scripts/battle_ready.py')],check=True)
