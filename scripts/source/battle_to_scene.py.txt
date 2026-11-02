"""Close an observed victory only as far as the first installed story line."""
from play import *
from PIL import Image
import difflib
mid,eid=map(int,sys.argv[1:3])
v=json.loads(subprocess.check_output(['ruby',str(ROOT/'scripts/event_dump.rb'),str(mid),str(eid)],stderr=subprocess.DEVNULL))
cs=[c for p in v['pages']for c in p['list']]
blocks=[]
for c in cs:
 if c['code']==101:blocks.append(str(c['parameters'][0]))
 elif c['code']==401 and blocks:blocks[-1]+=' '+str(c['parameters'][0])
norm=lambda t:re.sub('[^a-z]','',t.lower().replace('pokemon reborn',''))
rows=[json.loads(l)for l in(ROOT/'recordings/screens.jsonl').read_text().splitlines()]
assert any(time.time()-r['epoch']<180 and re.search(r'de.?feated|for winning',' '.join(r['text']),re.I)for r in rows),'Recent observed victory required'
for _ in range(35):
 t=read();print(t,flush=True);low=t.lower();n=norm(t)
 # A defeated trainer can say "You're not too bad in a fight!". Only the
 # actual command label means that another battle input screen is present.
 if 'pp:' in low or any(z.strip().lower()in['fight','yes','no']for z in t.splitlines()):raise SystemExit('Unexpected input screen')
 hud=re.search(r'(?<![a-z])f?hp(?![a-z])',low)
 if not hud and len(n)>10 and any(difflib.SequenceMatcher(None,n,norm(b)).ratio()>.65 for b in blocks):
  print('FIRST INSTALLED STORY LINE READY',flush=True);break
 im=Image.open(STATE).convert('RGB');w,h=im.size;b=im.crop((int(w*.08),int(h*.75),int(w*.90),int(h*.87)))
 textbox=sum(min(p)>235 and max(p)-min(p)<5 for p in b.getdata())/(b.width*b.height)>.5
 if textbox and len(n)>3:act('c','wait:.4')
 else:act('wait:.6')
else:raise SystemExit('Victory tail requires review')
