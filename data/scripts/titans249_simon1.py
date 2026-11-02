"""React only to public recorded Simon Says prompts; ordinary guarded keys."""
import os
os.environ['REBORN_FAST_KEYS']='1'
from play import *
from PIL import Image
import difflib
steps=[('simon says take one step right',['right:.12']),('simon says face downward',['down:.03']),('simon says take one step down and two steps left',['down:.12','left:.12','left:.12']),('now go up the stairs',[]),('simon says go up three paces',['up:.12']*3),('simon says touch the rock',['c:.08']),('again',[]),('simon says take one step right and two steps up',['right:.12','up:.12','up:.12']),('simon says face down again',['down:.03']),('and now face up',[])]
norm=lambda s:re.sub('[^a-z]','',s.lower().replace('danielle',''))
log=ROOT/'work'/f'249-simon1-{int(time.time())}.jsonl'
def record(d):
 with log.open('a') as f:f.write(json.dumps(dict(epoch=time.time(),**d))+'\n')
def frame():
 h=json.loads((ROOT/'recordings/capture-health.json').read_text())
 assert h.get('active') and time.time()-h['epoch']<2 and time.time()-h['preview_epoch']<1
 return Image.open(ROOT/'recordings/capture-preview.png').convert('RGB')
def box(im):
 # Ordinary white dialogue occupies the bottom of the game-only capture.
 a=im.crop((70,520,780,580));return sum(min(p)>235 for p in a.getdata())/(a.width*a.height)>.40
def textframe(im):
 p=ROOT/'work/249-simon-public.png';im.crop((0,470,852,640)).resize((1278,255)).save(p)
 return ' '.join(x['text'] for x in json.loads(subprocess.check_output([str(ROOT/'scripts/observe'),str(p)])))
if '--start-line' in sys.argv:
 t=textframe(frame());assert any(z in t.lower() for z in ['stand over there','begin','middle area']),t
 for _ in range(3):
  record({'start_line':t});act('c:.08');time.sleep(.20);t=textframe(frame())
  if not any(z in t.lower() for z in ['stand over there','begin','middle area']):break
start=time.time()
for i,(expected,keys) in enumerate(steps):
 deadline=time.time()+22;seen=None
 while time.time()<deadline:
  im=frame()
  if not box(im):time.sleep(.05);continue
  t=textframe(im)
  score=difflib.SequenceMatcher(None,norm(expected),norm(t)).ratio()
  if norm(expected) in norm(t) or score>.82:
   seen=t;im.save(ROOT/'work'/f'249-simon1-prompt-{i}.png');record({'step':i,'seen':t,'score':score});break
  if any(w in t.lower() for w in ['wrong','complicated','easier version']):raise SystemExit('Simon failure: '+t)
 else:raise SystemExit('Expected prompt timeout: '+expected)
 # The parallel event locks movement while its text window is visible.
 deadline=time.time()+8
 while box(frame()):
  if time.time()>deadline:raise SystemExit('Prompt did not close')
  time.sleep(.025)
 if keys:act(*keys)
 record({'step':i,'keys':keys,'response_complete':time.time()});print('SIMON',i,seen,'=>',keys,flush=True)
act('wait:2');print(read(),flush=True)
print('SIMON INPUT SEQUENCE COMPLETE; verify actual saved quest state',flush=True)
