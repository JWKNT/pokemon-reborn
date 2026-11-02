from play import *
from PIL import Image
import difflib
target=sys.argv[1].lower();walk=0;intro_reads=0
def grass_walk():
 result=subprocess.call([str(ROOT/'scripts/key_fast'),'right:0.3',*(['left:0.16','right:0.22']*6),'wait:0.5'])
 if result==0:return
 if result!=2:raise SystemExit('Movement helper failed')
 print('CAPTURE PAUSE; waiting for healthy recording before fresh UI inspection',flush=True)
 for _ in range(40):
  h=json.loads((ROOT/'recordings/capture-health.json').read_text())
  if h.get('active') and time.time()-h['epoch']<3:return
  time.sleep(.5)
 raise SystemExit('Capture did not recover; gameplay paused')
for i in range(160):
 t=read();print(i,t.replace('\n',' | '),flush=True);lo=re.sub(r'\bhron\b','aron',t.lower())
 if (ROOT/'work/stop-hunt').exists() and len(t.splitlines())<4:
  (ROOT/'work/stop-hunt').unlink();raise SystemExit('Requested overworld hunt stop')
 if 'repel' in lo or ('yes' in lo and 'no' in lo):
  if '--expire-repel' in sys.argv and 'repel' in lo:
   if 'wore off' in lo or 'uore off' in lo:
    act('c','wait:.5');lo=read().lower()
    # Last repel has no renewal choice; the observed empty world is safe.
    if re.sub('[^a-z]','',lo) in ['', 'pokemonreborn']:continue
   if 'cancel' in lo:
    labels=[z for z in ['Max Repel','Super Repel','Repel'] if any(line.strip(' •›>').lower()==z.lower() for line in lo.splitlines())]
    if labels:
     subprocess.run([sys.executable,str(ROOT/'scripts/choose_dialog.py'),'|'.join(labels+['Cancel']),'Cancel'],check=True);continue
   if 'yes' in lo.splitlines() and 'no' in lo.splitlines():
    subprocess.run([sys.executable,str(ROOT/'scripts/choose_dialog.py'),'Yes|No','No'],check=True);continue
  print('PROMPT REVIEW',flush=True);break
 if any(n in lo or any(difflib.SequenceMatcher(None,n,w.strip('.,!?')).ratio()>=.82 for w in lo.split()) for n in target.split(',')):print('TARGET FOUND',flush=True);break
 if 'hp' in lo or 'fight' in lo or any(w in lo for w in ['wild','safely','escape']):
  # HUD can appear before the species name during the public intro animation.
  # Give the normal animation two observations before choosing to flee.
  if 'fight' not in lo and not any(w in lo for w in ['safely','escape']) and intro_reads < 2:
   intro_reads+=1;act('wait:1');continue
  intro_reads=0
  if subprocess.call([sys.executable,str(ROOT/'scripts/flee.py')]):raise SystemExit('Escape review')
  if '--recenter' in sys.argv:
   index=sys.argv.index('--recenter');mid,x,y=map(int,sys.argv[index+1:index+4])
   # A battle can interrupt half of an oscillation and leave it off the grass.
   subprocess.run([sys.executable,str(ROOT/'scripts/q.py'),f'{mid},{x},{y}'],check=True)
  continue
 imworld=Image.open(STATE).convert('RGB');ww,hh=imworld.size;bb=imworld.crop((int(ww*.08),int(hh*.75),int(ww*.90),int(hh*.87)))
 if sum(min(px)>235 and max(px)-min(px)<5 for px in bb.getdata())/(bb.width*bb.height)<.55:
  if '--dense-horizontal' in sys.argv:
   # Only for a caller-reviewed short strip bounded away from transfers.
   # Direction keys cannot confirm a move; the battle helper normalizes its menu.
   act(*(['left:.42','right:.42']*3),'wait:.5');walk+=6;continue
  if '--grass-pair' in sys.argv:
   grass_walk();walk+=1;continue
  key=('right:0.9' if walk%2==0 else 'left:0.65') if '--right-wall' in sys.argv else (('up:0.62' if walk%2==0 else 'down:0.62') if '--vertical' in sys.argv else ('left:0.42' if walk%2==0 else 'right:0.42'))
  act(key,'wait:0.5');walk+=1;continue
 if len(t.lower().replace('pokemon reborn','').strip())<8:act('wait:.5');continue
 print('Review',flush=True);break
