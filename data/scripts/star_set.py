"""Change seven-star puzzle slots through visible normal menus; no hidden solution reads."""
from play import *
import json
new=json.loads(sys.argv[1]);current=int(sys.argv[2]);assert len(new)==7 and all(1<=v<=4 for v in new)
p=ROOT/'work/star-slots.json';old=json.loads(p.read_text());events=[]
def save(kind,i,text):
 events.append({'epoch':time.time(),'kind':kind,'slot':i,'public':text,'slots':list(old)});p.write_text(json.dumps(old));(ROOT/'work/star-latest-actions.json').write_text(json.dumps(events,indent=2))
def goto(i):
 global current
 if i!=current:
  n=abs(i-current);act(('right' if i>current else 'left')+':'+str(.12 if n==1 else .1*n+.02),'wait:.08')
 act('up:.06');current=i
changed=[i for i in range(7)if old[i]!=new[i]]
for i in changed:
 if not old[i]:continue
 goto(i);act('c','wait:.2');t=read();assert 'take out' in t.lower() and 'star' in t.lower(),('Removal prompt review',i,t)
 act('c','wait:.25');t=read();assert 'star' in t.lower() and ('obtained' in t.lower() or 'obrtained' in t.lower()),('Removal receipt review',i,t)
 for _ in range(3):
  act('c','wait:.25');after=read()
  if not any(v in after.lower() for v in ['star','pocket','obtained','obrtained']):break
 else:raise SystemExit('Removal dialogue did not finish')
 old[i]=0;save('removed',i,t);print('REMOVED',i,flush=True)
for i in changed:
 goto(i);act('c','wait:.2','c','wait:.2');t=read();assert 'sapphire' in t.lower() and 'emerald' in t.lower(),('Insertion menu review',i,t)
 if new[i]>1:act(*(['down:.12']*(new[i]-1)))
 act('c','wait:.25');t=read();assert 'loaded' in t.lower() and 'star' in t.lower(),('Insertion receipt review',i,t)
 act('c','wait:.2');old[i]=new[i];save('loaded',i,t);print('LOADED',i,new[i],t,flush=True)
print('SLOTS SET',old,'standing slot',current,flush=True)
