"""Normal controls for first seven-star guess, starting at first slot's open menu."""
from play import *
import json
colors=['Ruby','Sapphire','Emerald','Amethyst'];guess=[1,1,1,2,2,3,4]
receipt=[]
for i,color in enumerate(guess):
 if i:
  act('right:.12','up:.06','c','wait:.2','c','wait:.2')
  t=read();assert 'sapphire' in t.lower() and 'emerald' in t.lower(),('Star menu review',i,t)
 if color>1:act(*(['down:.12']*(color-1)))
 act('c','wait:.25');t=read();print(i,colors[color-1],t,flush=True)
 assert 'loaded' in t.lower() and 'star' in t.lower(),('Placement review',i,t)
 receipt.append({'slot':i,'color':color,'epoch':time.time(),'public':t});(ROOT/'work/star-initial-fill.json').write_text(json.dumps(receipt,indent=2))
 act('c','wait:.2')
(ROOT/'work/star-slots.json').write_text(json.dumps(guess))
print(read(),flush=True)
