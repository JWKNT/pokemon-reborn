"""Buy a named mart item and count, verifying the confirmation before payment."""
from play import *
_play_act=act
def act(*keys):
 _play_act(*[v for k in keys for v in ((k,'wait:.09') if k.startswith(('up','down','left','right')) else (k,))])
from PIL import Image
import re,unicodedata,difflib
name=sys.argv[1];count=int(sys.argv[2]);price=int(sys.argv[3]);assert 1<=count<=99 and price>0
def norm(s):
 # Honey's outlined shop label was visually verified with this OCR spelling.
 if s.strip().lower()=='нoпеч':return 'honey'
 value=re.sub('[^a-z0-9]','',unicodedata.normalize('NFKD',s).encode('ascii','ignore').decode().lower()).replace('powerkeignt','powerweight')
 # Directly reviewed vitamin-counter labels, session278.
 if value == 'hplp':return 'hpup'
 if value == 'zine':return 'zinc'
 # The outlined X and A glyphs have a small, observed set of OCR variants.
 if re.fullmatch(r'[akmnx]?attack',value):return 'xattack'
 if value in {'xhecuracy','arccuracu','xaccuracy','xhccuracy','xhcuracu'}:return 'xaccuracy'
 if re.fullmatch(r'[akmnx]?sp[ah]tk',value):return 'xspatk'
 if re.fullmatch(r'[akmnx]?spdef',value):return 'xspdef'
 if re.fullmatch(r'[akmnx]?der?fend',value):return 'xdefend'
 if re.fullmatch(r'[akmnx]?speed',value):return 'xspeed'
 return value
seen=set()
for _ in range(30):
 r=snap();t=' '.join(x['text'] for x in r);im=Image.open(STATE).convert('RGB');w,h=im.size
 ys=[]
 for y in range(int(h*.10),int(h*.67)):
  pixels=[im.getpixel((x,y)) for x in range(int(w*.43),int(w*.83),3)]
  if sum(rr>170 and gg<100 and bb<110 for rr,gg,bb in pixels)>.6*len(pixels):ys.append(y/h)
 if not ys:raise SystemExit('Shop cursor review: '+t)
 center=(min(ys)+max(ys))/2;names=[x for x in r if .39<x['x']<.76 and .10<x['y']<.67 and '$' not in x['text']]
 if not names:raise SystemExit('Shop item labels missing')
 cur=min(names,key=lambda x:abs(x['y']+x['h']/2-center));print('SHOP SELECTED',cur['text'],flush=True)
 if difflib.SequenceMatcher(None,norm(cur['text']),norm(name)).ratio()>.87:break
 target=next((x for x in names if difflib.SequenceMatcher(None,norm(x['text']),norm(name)).ratio()>.87),None)
 if target:
  n=round((target['y']-cur['y'])/.071)
  if not n:raise SystemExit('Shop alignment review')
  act(*(['down:.12' if n>0 else 'up:.12']*abs(n)),'wait:0.3')
 else:
  sig=(cur['text'],tuple(x['text'] for x in names))
  if sig in seen:raise SystemExit('Item not available')
  seen.add(sig);act('down:.12','wait:0.3')
else:raise SystemExit('Shop scan limit')
act('c','wait:1');t=read();print(t,flush=True)
if 'how many' not in t.lower():raise SystemExit('Quantity prompt expected')
act(*(['right:.12']*((count-1)//10)),*(['up:.12']*((count-1)%10)),'c','wait:1');t=read();print(t,flush=True)
low=norm(t).replace('mant','want');digits=re.sub('[^0-9]','',t)
if ('want'+str(count)) not in low or str(count*price) not in digits:raise SystemExit('Purchase confirmation review')
subprocess.run([sys.executable,str(ROOT/'scripts/choose_dialog.py'),'Yes|No','Yes'],check=True)
t=read();print(t,flush=True)
if not any(x in t.lower() for x in ['here you are','thank you','thankyou']):raise SystemExit('Purchase result review')
act('c','wait:0.8');t=read();print(t,flush=True)
if 'throw in' in t.lower() and 'premier' in t.lower():
 act('c','wait:.6');print(read(),flush=True)
print('PURCHASE VERIFIED',name,count,flush=True)
