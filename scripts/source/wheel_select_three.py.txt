"""Choose exactly three named, publicly observed party cards for Battle Wheel."""
from play import *
from party_cursor import selected_card
from collections import deque
import argparse
def selection_path(start,target):
 q=deque([(start,[])]);seen={start}
 while q:
  slot,keys=q.popleft()
  if slot==target:return keys
  up=7 if slot<2 else slot-2 if slot<6 else slot-1
  down=(slot+1)%8 if slot>=5 else slot+2
  for key,nxt in [("right",(slot+1)%8),("left",(slot-1)%8),("up",up),("down",down)]:
   if nxt not in seen:seen.add(nxt);q.append((nxt,keys+[key+":.12","wait:.12"]))
 raise RuntimeError("No multiselect route")
import difflib
def read_ordinals(expected):
 for attempt in range(4):
  t=read().lower()
  if all(w in t for w in expected):return t
  # Pixel-font OCR can merge the middle-left status into the sprite. Isolate
  # the six public status labels, without moving the current selection.
  from PIL import Image
  im=Image.open(NATIVE);w,h=im.size;canvas=Image.new('RGB',(1024,840),(30,30,30))
  for slot in range(6):
   col=slot%2;row=slot//2;x=.20 if col==0 else .64;y=(.20 if col==0 else .24)+.211*row
   crop=im.crop((int(w*x),int(h*y),int(w*(x+.29)),int(h*(y+.085))))
   canvas.paste(crop.resize((1024,140)),(0,slot*140))
  cropfile=ROOT/'work/wheel-ordinal-labels.png';canvas.save(cropfile)
  labels=json.loads(subprocess.check_output([str(ROOT/'scripts/observe'),str(cropfile)]))
  t+=' '+ ' '.join(v['text'].lower() for v in labels)
  if all(w in t for w in expected):return t
  act('wait:.25')
 raise RuntimeError(('Entry ordinals not observed',expected,t))

parser=argparse.ArgumentParser();parser.add_argument('names',nargs=3);parser.add_argument('--start',type=int,default=0,choices=[0,1,2]);args=parser.parse_args();names=args.names;assert len(set(names))==3
if args.start:
 t=read_ordinals(['first','second'][:args.start]);assert 'third' not in t
for order,name in list(enumerate(names))[args.start:]:
 rows=snap();text=' '.join(v['text'] for v in rows).lower()
 assert 'confirm' in text and ('entered' in text or 'first' in text),'Tournament selection screen required'
 hits=[]
 for v in rows:
  word=re.sub('[^a-z]','',v['text'].lower())
  score=difflib.SequenceMatcher(None,name.lower(),word).ratio()
  if score>=.78 and .1<v['y']<.7:hits.append((score,v))
 assert hits,('Named card missing',name,text)
 v=max(hits,key=lambda a:a[0])[1];col=int(v['x']>.5);row=round((v['y']-(.15 if not col else .195))/.21);assert row in [0,1,2]
 slot=row*2+col;keys=selection_path(selected_card(STATE),slot)
 if keys:act(*keys,'wait:.3');snap()
 assert selected_card(STATE)==slot
 act('c','wait:.5');t=read();print(t,flush=True)
 assert 'entry' in t.lower() and 'summary' in t.lower() and 'no entry' not in t.lower()
 assert any(difflib.SequenceMatcher(None,name.lower(),w.lower()).ratio()>=.78 for w in re.findall('[a-z]+',t,re.I)),('Wrong named menu',name,t)
 # Verified fresh three-option menu; normal clamped arrows select Entry.
 assert 'cancel' in t.lower()
 act('up:.12','wait:.12','up:.12','wait:.12','up:.12','wait:.12','c','wait:.5')
 t=read().lower();print('WHEEL ENTERED',name,t,flush=True)
 ordinal=['first','second','third'][order]
 if ordinal not in t:t=read_ordinals([ordinal])
t=read_ordinals(['first','second','third','confirm'])
# Installed Party.rb automatically selects Confirm after the third entry.
act('c','wait:1');print(read(),flush=True)
