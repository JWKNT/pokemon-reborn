"""Finish only Marcello's inspected quest dialogue and leave his normal mart."""
from play import *
import difflib
source=json.loads(subprocess.check_output(['ruby',str(ROOT/'scripts/event_dump.rb'),'827','57'],stderr=subprocess.DEVNULL))
lines=[]
for c in source['pages'][2]['list']:
 if c['code']==101:lines.append(c['parameters'][0])
 elif c['code']==401:lines[-1]+=' '+c['parameters'][0]
norm=lambda s:re.sub('[^a-z]','',s.lower().replace('pokemon reborn',''))
seen=False;closed=False;empty=0
for _ in range(24):
 t=read();print(t,flush=True);low=t.lower();labels=[z.strip().lower() for z in t.splitlines()]
 if all(z in labels for z in ['buy','sell','quit']):
  subprocess.run([sys.executable,str(ROOT/'scripts/choose_dialog.py'),'Buy|Sell|Quit','Quit'],check=True);closed=True;continue
 if 'please come again' in low:
  assert closed;act('c','wait:1');continue
 if any(difflib.SequenceMatcher(None,norm(t),norm(x)).ratio()>.65 for x in lines):
  seen=True;act('c','wait:.6');continue
 if len(norm(t))<5:
  if seen and closed:break
  empty+=1;assert empty<=5,'Marcello interaction not confirmed; inspect position'
  act('left:.12','wait:.5','c','wait:.8');continue
 raise SystemExit('Marcello dialogue review: '+t)
else:raise SystemExit('Marcello dialogue bound')
assert seen and closed
subprocess.run([sys.executable,str(ROOT/'scripts/checkpoint.py'),'Twilight381-Accepted'],check=True)
j=json.loads((ROOT/'notes/Twilight381-Accepted-navigation.json').read_text());assert j['variables']['699']==1,j['variables']['699']
print('DESERT QUEST ACTIVATION VERIFIED',flush=True)
