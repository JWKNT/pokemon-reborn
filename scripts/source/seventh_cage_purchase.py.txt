"""Buy one source-reviewed Seventh Street cage Pokemon with normal controls."""
from play import *
from PIL import Image
import argparse
p=argparse.ArgumentParser();p.add_argument('event',type=int,choices=range(16,25));p.add_argument('--resume',action='store_true');a=p.parse_args()
src=json.loads(subprocess.check_output(['ruby',str(ROOT/'scripts/event_dump.rb'),'324',str(a.event)],stderr=subprocess.DEVNULL))
cmd=src['pages'][0]['list'];source=' '.join(str(c['parameters']) for c in cmd)
assert 'pbAddPokemon' in source and 'pbDeleteItem' in source
species={16:'Vanillite',17:'Loudred',18:'Cyndaquil',19:'Lickitung',20:'Makuhita',21:'Jigglypuff',22:'Abra',23:'Roggenrola',24:'Ditto'}[a.event]
if not a.resume:subprocess.run([sys.executable,str(ROOT/'scripts/eventq.py'),'324',str(a.event),'talk'],check=True)
bought=a.resume;received=a.resume
for i in range(35):
 rows=snap();t=' '.join(v['text'] for v in rows);low=t.lower();print(t,flush=True)
 if re.search(r'\bhp\b|\bfight\b|trying to learn|choose a pok',low):raise SystemExit('Unexpected battle or selector')
 labels=[v['text'].strip().lower() for v in rows]
 if not bought and 'gonna take' in low:
  act('c','wait:.7');bought=True;continue
 if any(x in labels for x in ['yes','tes']) and any('no'==re.sub('[^a-z]','',x) for x in labels):
  if 'nickname' in low or ('party is full' in low and 'pc' in low):act('x','wait:.7');continue
  if not bought and ('gonna take' in low or 'want it' in low):act('c','wait:.7');bought=True;continue
  raise SystemExit('Unexpected choice '+t)
 if any(z in low for z in ['obtained','received','sent to','transferred to']):received=True;bought=True
 im=Image.open(STATE).convert('RGB');w,h=im.size;b=im.crop((int(w*.08),int(h*.75),int(w*.90),int(h*.87)))
 textbox=sum(min(z)>235 and max(z)-min(z)<5 for z in b.getdata())/(b.width*b.height)>.55
 if not textbox:
  if bought and received:print('PURCHASE PUBLICLY COMPLETED',species,flush=True);break
  act('wait:.7');continue
 act('c','wait:.5')
else:raise SystemExit('Purchase dialogue limit')
