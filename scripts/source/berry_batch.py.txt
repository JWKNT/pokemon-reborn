"""Use a small verified quantity of an EV berry through the ordinary bag UI."""
from play import *
import re
from PIL import Image
item,name,count=sys.argv[1:4];count=int(count);assert 1<=count<=9
t=read().lower()
if '--bag-open' not in sys.argv:
 act('x','wait:.5','c','wait:1.2');t=read().lower()
if 'cancel' in t and t.count('hp')>=5:act('x','wait:1','down','c','wait:1.2');t=read().lower()
if 'field notes' in t or 'pulse dex' in t:act('x','wait:1','up','c','wait:1.2');t=read().lower()
if 'sort' not in t:raise SystemExit('Bag entry review')
for _ in range(9):
 if any(x['text'].strip().lower() in ['berries','berriez'] for x in snap()):break
 act('right','wait:.4')
else:raise SystemExit('Berries pocket review')
subprocess.run([sys.executable,str(ROOT/'scripts/bag_select.py'),item],check=True)
act('c','wait:.5','c','wait:1')
subprocess.run([sys.executable,str(ROOT/'scripts/party_pick.py'),name,'--single'],check=True)
if 'how many' not in read().lower():raise SystemExit('Quantity prompt review')
act(*(['up']*(count-1)),'wait:.4')
for attempt in range(4):
 t=read();print(t,flush=True)
 im=Image.open(STATE);w,h=im.size;crop=im.crop((int(w*.81),int(h*.8),int(w*.945),int(h*.925))).resize((650,500))
 q=ROOT/'work/berry-quantity.png';crop.save(q)
 qty=' '.join(v['text'] for v in json.loads(subprocess.check_output([str(ROOT/'scripts/observe'),str(q)])))
 print('QUANTITY',qty,flush=True)
 if re.search(r'[x:×]\s*0*'+str(count)+r'\b',t,re.I) or re.search(r'\b0*'+str(count)+r'\b',qty,re.I):break
 act('wait:.35')
else:raise SystemExit('Quantity verification review')
act('c','wait:1');t=read();print(t,flush=True)
if 'base' not in t.lower() or 'fell' not in t.lower():raise SystemExit('Berry effect review')
act('c','wait:.7','x','wait:1')
subprocess.run([sys.executable,str(ROOT/'scripts/overworld.py')],check=True)
