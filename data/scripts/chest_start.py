from play import *
from chest_safe_pause import classify
if '--active' not in sys.argv:act('up:.12','c:.12','wait:.5')
for _ in range(25):
 r=snap();t=' '.join(x['text']for x in r).lower();print(t,flush=True)
 labels=[re.sub('[^a-z]','',x['text'].lower())for x in r]
 if 'yes' in labels and 'no' in labels:
  act('down:.12','c:.12','wait:.4');continue
 if 'strength' in t or any(x['text'].strip().lower()=='begin.' for x in r):
  act('c:.12','wait:.3','x:.12','wait:.3','c:.12','wait:1.5');assert classify(snap())=='bag';print('BAG PAUSE VERIFIED',flush=True);break
 if not any(x['y']>.72 and len(x['text'])>3 for x in r):raise SystemExit('Unexpected dialogue')
 act('c:.12','wait:.35')
