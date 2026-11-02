"""React only to public recorded Simon Says prompts; ordinary guarded keys."""
import os
os.environ['REBORN_FAST_KEYS']='1'
from play import *
from PIL import Image
import difflib
steps=[('simon says take one step down and two steps left', ['down:.12', 'left:.12', 'left:.12']), ('simon says push the grey rock right one space', ['down:.12', 'left:.12', 'left:.12', 'up:.12', 'up:.12', 'right:.12', 'right:.12']), ('simon says stand directly below the center stone', ['right:.12', 'down:.12', 'right:.12', 'right:.12', 'right:.12']), ('simon says push the brown rock up one space', ['down:.12', 'down:.12', 'right:.12', 'right:.12', 'up:.12', 'up:.12']), ('simon says touch the tallest rock', ['up:.12', 'left:.12', 'left:.12', 'left:.12', 'left:.12', 'left:.12', 'up:.12', 'left:.12', 'up:.03', 'c:.08']), ('simon says push both boulders towards the center stone', ['right:.12', 'right:.12', 'wait:.15', 'down:.12', 'right:.12', 'right:.12', 'right:.12', 'right:.12', 'right:.12', 'down:.12', 'right:.12', 'right:.12', 'up:.12', 'up:.12', 'left:.12', 'left:.12']), ('now move the grey stone up one space and right one space', []), ('move the brown rock to the opposite side of the center stone', []), ('then push the grey rock right one space and down one space', []), ('simon says stand below the center stone and touch it', ['left:.12', 'down:.12', 'left:.12', 'left:.12', 'up:.03', 'c:.08'])]
norm=lambda s:re.sub('[^a-z]','',s.lower().replace('danielle',''))
log=ROOT/'work'/f'250-rock1-{int(time.time())}.jsonl'
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
 p=ROOT/'work/250-rock-public.png';im.crop((0,470,852,640)).resize((1278,255)).save(p)
 return ' '.join(x['text'] for x in json.loads(subprocess.check_output([str(ROOT/'scripts/observe'),str(p)])))
if '--start-line' in sys.argv:
 t=textframe(frame());assert any(z in t.lower() for z in ['left of the center rock']),t
 for _ in range(3):
  record({'start_line':t});act('c:.08');time.sleep(.20);t=textframe(frame())
  if not any(z in t.lower() for z in ['left of the center rock']):break
start=time.time()
for i,(expected,keys) in enumerate(steps):
 deadline=time.time()+22;seen=None
 while time.time()<deadline:
  im=frame()
  if not box(im):time.sleep(.05);continue
  t=textframe(im)
  score=difflib.SequenceMatcher(None,norm(expected),norm(t)).ratio()
  if norm(expected) in norm(t) or score>.82:
   seen=t;im.save(ROOT/'work'/f'250-rock1-prompt-{i}.png');record({'step':i,'seen':t,'score':score});break
  if any(w in t.lower() for w in ['wrong','complicated','easier version']):raise SystemExit('Simon failure: '+t)
 else:raise SystemExit('Expected prompt timeout: '+expected)
 # The parallel event locks movement while its text window is visible.
 deadline=time.time()+8
 while box(frame()):
  if time.time()>deadline:raise SystemExit('Prompt did not close')
  time.sleep(.025)
 if keys:
  paced=[]
  for key in keys:
   paced.append(key)
   if key.endswith(':.12'):paced.append('wait:.06')
  act(*paced)
 record({'step':i,'keys':keys,'response_complete':time.time()});print('SIMON',i,seen,'=>',keys,flush=True)
act('wait:2');print(read(),flush=True)
print('SIMON INPUT SEQUENCE COMPLETE; verify actual saved quest state',flush=True)
