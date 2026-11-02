"""Advance only an already-observed victorious battle's closing dialogue.
Never select a move, replacement, choice or learning response.
"""
from play import *
from PIL import Image
music=ROOT/'work/active-trainer-music.json'
if music.exists():evidence=json.loads(music.read_text())
else:
 evidence=json.loads((ROOT/'recordings/trainer-music.jsonl').read_text().splitlines()[-1])
 assert evidence.get('victory_epoch') and time.time()-evidence['processed_epoch']<180,'Need recent completed victory evidence'
start=evidence['start_epoch'];rows=[json.loads(x)for x in (ROOT/'recordings/screens.jsonl').read_text().splitlines()]
assert any(x['epoch']>=start and re.search(r'de.?feated|for winning',' '.join(x['text']),re.I)for x in rows),'Victory must have been observed'
for _ in range(30):
 r=snap();t=' '.join(x['text']for x in r);low=t.lower();print(t,flush=True)
 if any(z in low for z in ['fight','choose a pok','trying to learn','switch in','change pok']) or any(x['text'].strip().lower() in ['yes','no']for x in r):raise SystemExit('Unexpected battle input during outro')
 im=Image.open(STATE).convert('RGB');w,h=im.size;b=im.crop((int(w*.08),int(h*.75),int(w*.90),int(h*.87)))
 box=sum(min(x)>235 and max(x)-min(x)<5 for x in b.getdata())/(b.width*b.height)>.55
 if not re.search(r'\bhp\b',low) and not box:
  act('wait:.7');check=read().lower()
  if not re.search(r'\bhp\b',check):print('BATTLE HUD CLEARED',flush=True);break
  continue
 assert not any(.08<x['y']<.37 and re.search(r'\bhp\b',x['text'],re.I)for x in r),'Opponent HUD still present'
 if box and any(x['y']>.72 and len(x['text'])>2 for x in r):act('c','wait:.4')
 else:act('wait:.5')
else:raise SystemExit('Victory outro limit')
