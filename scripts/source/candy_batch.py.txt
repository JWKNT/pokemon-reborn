"""Use a verified count of Medium Exp. Candies on a named Pokemon from the open bag."""
from play import *
import re
name=sys.argv[1];count=int(sys.argv[2]);assert 1<=count<=35
if '--party-open' not in sys.argv:
 subprocess.run([sys.executable,str(ROOT/'scripts/bag_select.py'),'Exp. Candy '+(sys.argv[3] if len(sys.argv)>3 else 'M'),'--single-step'],check=True)
 act('c','wait:0.5','c','wait:1.3')
subprocess.run([sys.executable,str(ROOT/'scripts/party_pick.py'),name,'--single'],check=True)
t=read().lower()
if 'how many' not in t:raise SystemExit('Quantity prompt expected')
seq=['right']*((count-1)//10)+['up']*((count-1)%10)
act(*[v for key in seq for v in (key,'wait:.15')],'wait:0.3');t=read();print(t,flush=True)
from PIL import Image
im=Image.open(STATE);w,h=im.size
crop=im.crop((int(w*.82),int(h*.82),int(w*.94),int(h*.92))).resize((600,400))
qpath=ROOT/'work/quantity.png';crop.save(qpath)
qty=' '.join(v['text'] for v in json.loads(subprocess.check_output([str(ROOT/'scripts/observe'),str(qpath)])))
print('QUANTITY OCR',qty,flush=True)
from PIL import ImageChops
ref=ROOT/'work/quantity-seven-verified.png'
verified_seven=count==7 and ref.exists() and ImageChops.difference(crop,Image.open(ref)).getbbox() is None
ref8=ROOT/'work/quantity-eight-verified.png'
verified_eight=count==8 and ref8.exists() and ImageChops.difference(crop,Image.open(ref8)).getbbox() is None
whole_quantity=re.search(r'(?m)^\s*0*'+str(count)+r'\s*$',t) and 'how many' in t.lower()
if not (verified_seven or verified_eight or whole_quantity) and not re.search(r'[x:×]\s*0*'+str(count)+r'\b',t,re.I) and not re.search(r'0*'+str(count)+r'\b',qty,re.I):raise SystemExit('Quantity verification failed')
act('c','wait:1')
subprocess.run([sys.executable,str(ROOT/'scripts/candy_progress.py')],check=True)
t=read().lower()
if 'on which' in t or 'choose a pok' in t:act('x','wait:1.2')
elif 'sort' not in t and 'close' not in t:raise SystemExit('Candy completion review')
print(read(),flush=True)
