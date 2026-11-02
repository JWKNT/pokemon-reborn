"""Advance inspected Grand Hall common79 reward/heal tail after public victory."""
from play import *
from PIL import Image
m=json.loads((ROOT/'work/active-trainer-music.json').read_text());assert (m['class'],m['name']) in [('TechNerd','Will'),('COOLTRAINER_Female','Carol'),('EXPERT_Male','JB'),('EXPERT_Male','Anthony'),('COOLTRAINER_Male','Fawkes'),('YOUNGSTER','Jonah'),('COOLTRAINER_Male','Jace'),('PSYCHIC_Male','Silva')]
source=json.loads((ROOT/'work/grandhall-training-source.json').read_text());assert source['id']==79 and not any(c['code'] in [102,103,104] for c in source['list'])
history=[json.loads(l)for l in (ROOT/'recordings/screens.jsonl').read_text().splitlines()[-100:]]
assert any(v['epoch']>=m['start_epoch'] and re.search(r'de.?feated|for winning',' '.join(v['text']),re.I)for v in history),'Victory evidence required'
for i in range(24):
 rows=snap();t=' '.join(v['text']for v in rows);low=t.lower();print(t,flush=True)
 assert 'fight'not in low and 'choose a pok'not in low and 'trying to learn'not in low and not any(v['text'].strip().lower()in['yes','no']for v in rows),'Unexpected reward input'
 im=Image.open(STATE).convert('RGB');w,h=im.size;patch=im.crop((int(w*.08),int(h*.75),int(w*.90),int(h*.87)))
 box=sum(min(z)>235 and max(z)-min(z)<5 for z in patch.getdata())/(patch.width*patch.height)>.55
 if not box:
  act('wait:.6');rows=snap();t=' '.join(v['text']for v in rows)
  if not any(v['y']>.72 and len(v['text'])>10 for v in rows):print('GRAND HALL REWARD WORLD',flush=True);break
  continue
 act('c:0.06','wait:.4')
else:raise SystemExit('Grand Hall reward tail limit')
