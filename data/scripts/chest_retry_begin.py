from play import *
from chest_safe_pause import classify
for _ in range(20):
 r=snap();t=' '.join(x['text']for x in r);print(t,flush=True)
 if 'strength' in t.lower() or any(x['text'].strip().lower()=='begin.' for x in r):
  act('c:.12','wait:.3','x:.12','wait:.3','c:.12','wait:1.5')
  r=snap();assert classify(r)=='bag', 'Need immediate actual Bag review';print('BAG PAUSE VERIFIED',flush=True);break
 if not any(x['y']>.72 and len(x['text'])>3 for x in r):raise SystemExit('Unexpected retry dialogue')
 act('c:.12','wait:.4')
