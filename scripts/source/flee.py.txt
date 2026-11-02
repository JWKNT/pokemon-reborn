"""Flee an identified wild encounter; stop if escape fails."""
from play import *
from PIL import Image
from bgm_span import append_span,wild_track
started=time.time()-3
if '--since' in sys.argv:
 since=float(sys.argv[sys.argv.index('--since')+1])
 # A completed earlier wild in this capture must not stretch a later cue
 # across intervening gameplay when the caller supplies the session start.
 for mp in (ROOT/'recordings').glob('session-???.json'):
  meta=json.loads(mp.read_text());override=ROOT/'work'/f'{mp.stem}-music-overrides.json'
  if not override.exists():continue
  for span in json.loads(override.read_text()):
   end=meta['start_epoch']+span['end']
   if 'Battle- Wild' in span.get('track','') and since<end<time.time():since=end
 screens=[json.loads(z) for z in (ROOT/'recordings/screens.jsonl').read_text().splitlines()]
 def battle_observation(z):
  text=' '.join(z['text']).lower()
  return 'cancel' not in text and (re.search(r'\bfight\b|\bwild\b',text) or 1<=len(re.findall(r'\bhp\b',text))<=2)
 observed=next((z for z in screens if z['epoch']>=since and battle_observation(z)),None)
 if observed:started=max(since,observed['epoch']-2)
tried=False
for i in range(12):
 t=read();print(t.replace('\n',' | '),flush=True);lo=t.lower()
 if any(z in lo for z in ['stored in box','transferred to','party is full']):raise SystemExit('Capture dialogue review')
 if 'fight' in lo:
  if tried:raise SystemExit('ESCAPE REVIEW')
  tried=True
  act('right:0.22','down:0.22','c','wait:2');continue
 if 'prevents escaping' in lo or any(z in re.sub('[^a-z]','',lo) for z in ['couldntescape','cantescape']):
  act('c','wait:2');print(read(),flush=True);raise SystemExit('ESCAPE REVIEW: failed run acknowledged; next command ready')
 if 'fainted' in lo:raise SystemExit('ESCAPE REVIEW')
 if 'safely' in lo:act('c','wait:1');print(read(),flush=True);break
 if 'pp:' in lo:act('x','wait:0.4');continue
 if 'hp' in lo or 'wild' in lo:act('wait:1');continue
 if len(t.splitlines())<=4:print('OVERWORLD',flush=True);break
 raise SystemExit('REVIEW')

else:raise SystemExit('Escape animation timeout')

track = wild_track()
if '--battle-track' in sys.argv:
 track = sys.argv[sys.argv.index('--battle-track') + 1]
 assert any(p.stem == track for p in pathlib.Path('/Applications/Reborn.app/Contents/Game/Audio/BGM').iterdir()), 'Unknown installed battle track'
append_span(started,time.time(),track)
