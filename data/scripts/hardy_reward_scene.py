"""Finish only the source-reviewed Hardy victory dialogue; stop in the arena."""
from play import *
from PIL import Image
source=json.loads((ROOT/'work/Hardy137-event3-source.json').read_text())
commands=source['pages'][0]['list']
assert any(c['code']==355 and c['parameters']==['$Trainer.badges[16]=true']for c in commands)
attempt=json.loads((ROOT/'recordings/major-fights/session-137-attempts.json').read_text())[-1]
assert attempt['id']==127 and attempt['result']=='victory'
for i in range(60):
 rows=snap();t=' '.join(r['text']for r in rows);print(t,flush=True)
 assert not re.search(r'\bfight\b|out of usable|choose a pok|pp:',t,re.I)
 assert not any(r['text'].strip().lower()in ['yes','no']for r in rows),'Unexpected choice; no tap'
 bottom=' '.join(r['text']for r in rows if r['y']>.67 and len(r['text'])>2)
 im=Image.open(STATE).convert('RGB');w,h=im.size
 box=im.crop((int(w*.08),int(h*.75),int(w*.90),int(h*.87)))
 textbox=sum(min(px)>225 and max(px)-min(px)<15 for px in box.getdata())/(box.width*box.height)>.5
 if not bottom and not textbox:
  act('wait:.7');check=snap()
  assert not any(r['y']>.67 and len(r['text'])>2 for r in check),'Arena transition still active'
  print('HARDY REWARD SCENE CLOSED; NO ROUTE INPUT',flush=True);break
 assert textbox and bottom,'Unexpected scene; stopped before tap'
 act('c:.12','wait:.8')
else:raise SystemExit('Bounded Hardy reward dialogue limit')
