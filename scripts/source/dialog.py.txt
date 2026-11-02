from play import *
import re
from PIL import Image
def textbox():
 im=Image.open(STATE).convert("RGB");w,h=im.size
 crop=im.crop((int(w*.08),int(h*.75),int(w*.90),int(h*.87)))
 gutter=im.crop((int(w*.09),int(h*.755),int(w*.10),int(h*.875)))
 return (sum(1 for r,g,b in crop.getdata() if min(r,g,b)>235 and max(r,g,b)-min(r,g,b)<5)/(crop.width*crop.height)>.55 or
  sum(min(px)>235 and max(px)-min(px)<5 for px in gutter.getdata())/(gutter.width*gutter.height)>.9)
limit=next((int(a.split("=",1)[1]) for a in sys.argv if a.startswith("--limit=")),int(sys.argv[sys.argv.index("--limit")+1]) if "--limit" in sys.argv else 35)
assert 1<=limit<=500
seen={}
blank_streak=0
for i in range(limit):
 r=snap();t=' | '.join(a['text'] for a in r);print(t,flush=True)
 low=t.lower()
 if 'keyboard' in low or 'whatisit' in re.sub('[^a-z]','',low):
  print('TEXT ENTRY: inspect and type the quest answer',flush=True);break
 seen[low]=seen.get(low,0)+1
 blank_streak = blank_streak + 1 if re.sub('[^a-z]','',low) in ['', 'pokemonreborn'] else 0
 if blank_streak>=3 and not textbox():
  print('OVERWORLD: repeated text-free screen',flush=True);break
 if len(low)>35 and seen[low]>=3:raise SystemExit('Repeated dialogue review')
 if ('cancel' in low and low.count('able')>=2) or re.search(r'\bhp\b',low) or 'pp:' in low or (re.search(r'\bfight\b',low) and ('hp' in low or 'bag' in low)) or 'choose a pok' in low or 'trying to learn' in low:raise SystemExit('BATTLE/LEARNING REVIEW')
 if 'bag' in low and 'options' in low:act('x','wait:1');break
 choices=[a['text'].strip().lower() for a in r]
 if 'check solution' in choices or 'review instructions' in choices:raise SystemExit('PUZZLE CHOICE REVIEW')
 if sum(label in choices for label in ['dual chop','thunder punch','fire punch','ice punch'])>=3:raise SystemExit('TUTOR CHOICE REVIEW')
 if any(a in choices for a in ['sirius','doctor','go upstairs','stay downstairs']):raise SystemExit('STORY CHOICE REVIEW')
 if 'yes' in choices:
  if '--yes' in sys.argv:act('c','wait:1');continue
  raise SystemExit('CHOICE REVIEW')
 bottom=[a for a in r if a['y']>.72 and len(a['text'])>10]
 if not textbox():
  act('wait:3' if '--story-burst' in sys.argv else 'wait:1')
  rr=snap()
  if '--story-burst' in sys.argv and not textbox():
   act('wait:3');rr=snap()
  if not textbox():print('OVERWORLD',flush=True);break
  continue
 battle_intro=any(k in low for k in ['would like to battle','sent out','begin.',' vs.'])
 act('c','wait:0.3')
else:raise SystemExit('Dialogue step limit reached; inspect before continuing')
