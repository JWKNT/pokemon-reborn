"""Bounded normal-UI interaction with wandering gift Shaymin, using rendered pixels only."""
from play import *
from PIL import Image
import cv2,numpy as np
sprite=Image.open('/Applications/Reborn.app/Contents/Game/Graphics/Characters/pkmn_shaymin.png').convert('RGBA')
templates=[]
for yy in range(4):
 for xx in range(4):
  a=sprite.crop((xx*34,yy*30,(xx+1)*34,(yy+1)*30)).resize((57,50),Image.Resampling.NEAREST)
  a=np.array(a);templates.append((cv2.cvtColor(a[:,:,:3],cv2.COLOR_RGB2BGR),a[:,:,3]))
for turn in range(90):
 t=read();low=t.lower()
 if any(z in low for z in ['shaymin:','mimi','take shaymin','wandering around','obtained shaymin','nickname']):print('GIFT DIALOGUE',t,flush=True);break
 scene=cv2.imread(str(ROOT/'recordings/capture-preview.png'));best=None
 if np.mean(np.min(scene[490:620,20:800],axis=2)>235)>.45:print('PUBLIC TEXTBOX STOP',t,flush=True);break
 for template,mask in templates:
  scores=cv2.matchTemplate(scene[:490],template,cv2.TM_SQDIFF_NORMED,mask=mask)
  scores=np.nan_to_num(scores,nan=10,posinf=10,neginf=10);_,_,_,_=cv2.minMaxLoc(scores)
  score,_,pos,_=cv2.minMaxLoc(scores)
  if best is None or score<best[0]:best=(score,pos)
 score,(x,y)=best
 print('MATCH',score,(x,y),flush=True)
 assert score<.28,('Visible Shaymin template unclear',score)
 dx=round((x+28.5-426)/53.25);dy=round((y+25-314)/53.33)
 print(turn,score,(x,y),(dx,dy),flush=True)
 if abs(dx)+abs(dy)<=1:
  k=('right' if dx>0 else 'left') if dx else ('down' if dy>0 else 'up')
  act(k+':.025','c','wait:.25')
 else:
  k=('right' if dx>0 else 'left') if abs(dx)>=abs(dy) else ('down' if dy>0 else 'up')
  act(k+':.07','wait:.18','c','wait:.2')
else:raise SystemExit('Visible chase limit; no unseen state consumed')
