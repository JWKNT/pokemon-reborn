"""Locate wandering Amaria from current game pixels, then approach with normal keys."""
import os
os.environ['REBORN_FAST_KEYS']='1'
from play import *
from locate import locate
from nav import route,groupby
sys.path.insert(0,'/tmp/reborn-vision-deps')
import cv2,numpy as np
from PIL import Image
m,e=map(int,sys.argv[1:3]);assert m in[680,683]
sheet=np.array(Image.open('/Applications/Reborn.app/Contents/Game/Graphics/Characters/trchar069e.png').convert('RGBA'))
model=json.loads(subprocess.check_output(['ruby',str(ROOT/'scripts/route_map.rb'),str(m),'0','0'],stderr=subprocess.DEVNULL))
cs=model['events'][str(e)]['list'];blocks=[]
choice_at=next((i for i,c in enumerate(cs)if c['code']==102),len(cs))
assert sum(c['code']==101 for c in cs[:choice_at])>=4, 'Opening too short for four neighboring confirm probes'
for command in cs:
 if command['code']==101:blocks.append(str(command['parameters'][0]))
 elif command['code']==401 and blocks:blocks[-1]+=' '+str(command['parameters'][0])
import difflib
norm=lambda z:re.sub('[^a-z]','',z.lower().replace('pokemon reborn',''))
def dialogue(t):return len(norm(t))>10 and ('amaria'in t.lower()or any(difflib.SequenceMatcher(None,norm(t),norm(b)).ratio()>.8 for b in blocks))
low_count=0
for iteration in range(45):
 rows=snap();text=' '.join(z['text']for z in rows)
 if dialogue(text):print('AMARIA DIALOGUE VERIFIED',text,flush=True);break
 assert not ('yes'in text.lower().split()and'no'in text.lower().split()), 'Choice reached; select explicitly before continuing'
 assert len(text.replace('Pokemon Reborn','').strip())<15,('Unexpected dialogue',text)
 # The coordinate frame froze the NPC while it was displayed. Match that
 # untouched screenshot; position conversion uses the verified512x384 viewport.
 im=Image.open(NATIVE);assert im.size==(2272,1816)
 canvas=im.crop((112,132,2160,1668)).resize((512,384),Image.Resampling.NEAREST)
 gray=cv2.cvtColor(np.array(canvas.convert('RGB')),cv2.COLOR_RGB2GRAY);hits=[]
 for yy in range(4):
  for xx in range(4):
   tpl=sheet[yy*42:(yy+1)*42,xx*42:(xx+1)*42]
   result=cv2.matchTemplate(gray,cv2.cvtColor(tpl[:,:,:3],cv2.COLOR_RGB2GRAY),cv2.TM_CCOEFF_NORMED,mask=tpl[:,:,3]);result[(~np.isfinite(result))|(result>1.0001)|(result< -1.0001)]=0
   _,score,_,xy=cv2.minMaxLoc(result);hits.append((score,xy,xx,yy))
 score,xy,xx,yy=max(hits)
 dx=(xy[0]+21-256)/32;dy=(xy[1]+42-208)/32
 print('LIVE AMARIA',iteration,round(score,3),'relative',round(dx,2),round(dy,2),flush=True)
 low_count=low_count+1 if score<.82 else 0
 if score<.82 and low_count>=4:raise SystemExit('Amaria sprite not visible after color-cycle review')
 if score<.82 or abs(dx)+abs(dy)<1.7:
  # A nearby swimmer can overlap Aster and obscure the template. This
  # source-reviewed opening has enough dialogue before any choice
  # here; brief turns/confirm cover the four neighboring tiles.
  act('up:.03','c:.08','left:.03','c:.08','down:.03','c:.08','right:.03','c:.08','wait:.25')
  if score<.82:
   t=read()
   if dialogue(t):print('AMARIA DIALOGUE VERIFIED',t,flush=True);break
   assert len(t.replace('Pokemon Reborn','').strip())<15,('Unexpected partial-sprite dialogue',t)
   act('wait:.8')
  continue
 direction=('right'if dx>0 else'left')if abs(dx)>abs(dy)else('down'if dy>0 else'up')
 act(direction+':.12','wait:.25')
else:raise SystemExit('Wandering NPC chase budget exhausted')
