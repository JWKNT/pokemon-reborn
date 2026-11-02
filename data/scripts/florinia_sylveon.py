"""Bounded public-screen policy for Sylveon versus inspected Cradily only."""
from play import *
from PIL import Image
import difflib
from public_battle_field import observe
budget=int(sys.argv[1]) if len(sys.argv)>1 else 6
pending=int(sys.argv[2]) if len(sys.argv)>2 else 0
assert pending in [0,1]
journal=ROOT/'work/session162-sylveon-policy.jsonl'
for turn in range(budget):
 rows=snap();text=' '.join(x['text'] for x in rows);low=text.lower()
 if 'fight' not in low:print('INPUT BOUNDARY',text,flush=True);break
 enemy=' '.join(x['text'].lower() for x in rows if x['y']<.35)
 own=' '.join(x['text'].lower() for x in rows if .4<x['y']<.72)
 if not any(difflib.SequenceMatcher(None,'cradily',w).ratio()>.8 for w in enemy.split()) or not any(difflib.SequenceMatcher(None,'sylveon',w).ratio()>.75 for w in own.split()):print('ACTOR REVIEW',text,flush=True);break
 hp=re.search(r'(\d+)\s*/\s*(?:351|851)',own)
 if not hp or not 0<int(hp[1])<=351:
  crop=ROOT/'work/sylveon-hp-crop.png'
  Image.open(ROOT/'recordings/capture-preview.png').crop((674,400,825,445)).resize((604,180)).save(crop)
  cropped=' '.join(x['text'] for x in json.loads(subprocess.check_output([str(ROOT/'scripts/observe'),str(crop)])))
  hp=re.search(r'(\d+)\s*/\s*351',cropped)
  if not hp or not 0<int(hp[1])<=351:print('HP REVIEW',text,cropped,flush=True);break
 hp=int(hp[1]);field=observe(STATE)
 im=Image.open(STATE).convert('RGB');w,h=im.size;px=list(im.crop((int(w*.45),int(h*.09),int(w*.93),int(h*.40))).getdata())
 white=sum(min(p)>220 for p in px)/len(px);green=sum(g>r*1.4 and g>b*1.3 and g>35 for r,g,b in px)/len(px)
 if white>.23 and green>.015:field='glitch'
 if field not in ['misty','glitch']:print('FIELD REVIEW',field,white,green,flush=True);break
 if hp<90:print('LOW HP REVIEW',hp,'wish_pending',pending,flush=True);break
 slot=1 if field=='glitch' else (3 if pending or hp>=240 else 0)
 choice={'epoch':time.time(),'hp':hp,'field':field,'slot':slot,'wish_pending':pending,'evidence':text}
 print('CHOICE',choice,flush=True)
 with journal.open('a')as f:f.write(json.dumps(choice)+'\n')
 subprocess.run([sys.executable,str(ROOT/'scripts/public_turn_capture.py'),'battle_move.py',str(slot),'--watch'],check=True)
 if slot==0:pending=2
 pending=max(0,pending-1)
print('POLICY STOP; wish pending',pending,flush=True)
