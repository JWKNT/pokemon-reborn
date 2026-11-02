"""Bounded screenshot-only approach to a reviewed moving tree apparition."""
from play import *
from picnic_sprite import detect
from PIL import Image
import numpy as np
name=sys.argv[1];dark='--dark' in sys.argv
assert name.lower() in ['espeon','chingling','umbreon','cleffa','mismagius','florges','flabebe','zweilous','granbull','murkrow','houndour','kadabra','mandibuzz','chimecho','deino','vullaby','poochyena','eevee','misdreavus']
previous=None;stalled=0
for i in range(32):
 # Use a fresh frame from the existing recorder; never open another capture.
 epoch=time.time()
 for _ in range(20):
  health=json.loads((ROOT/'recordings/capture-health.json').read_text())
  if health.get('preview_epoch',0)>epoch:break
  time.sleep(.04)
 a=np.asarray(Image.open(ROOT/'recordings/capture-preview.png').convert('RGB')).astype(int)
 if np.mean(a.max(axis=2)-a.min(axis=2))>12:
  print('COLOR TRANSITION — public battle review',flush=True);print(read(),flush=True);break
 score,x,y,row,col=detect(name,dark)[0]
 print('VISIBLE',i,name,round(score,3),x,y,flush=True)
 if score<(.55 if name.lower()=='zweilous' else .43):raise SystemExit('No confident public apparition silhouette')
 pos=(round(x/8),round(y/8))
 stalled=stalled+1 if pos==previous else 0;previous=pos
 if stalled>=5:raise SystemExit('Visible target blocked by terrain; route around obstacle')
 dx=x-256;dy=y-208
 if abs(dx)<12 and abs(dy)<48:
  act(('down' if dy>0 else 'up')+':.025','c:0.08','wait:.3');print(read(),flush=True)
 elif abs(dy)<12 and abs(dx)<48:
  act(('right' if dx>0 else 'left')+':.025','c:0.08','wait:.3');print(read(),flush=True)
 else:
  direction=('right' if dx>0 else 'left') if abs(dx)>abs(dy) else ('down' if dy>0 else 'up')
  act(direction+':.08','wait:.12')
else:raise SystemExit('Bounded apparition approach ended; inspect obstacles')
