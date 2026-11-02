"""Match installed character artwork against recorded pixels; no game state access."""
from pathlib import Path
import cv2,numpy as np
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
def find(name):
 a=np.asarray(Image.open(ROOT/'recordings/capture-preview.png').convert('RGB').resize((512,384),Image.Resampling.NEAREST))
 im=Image.open('/Applications/Reborn.app/Contents/Game/Graphics/Characters/'+name+'.png').convert('RGBA');w,h=im.width//4,im.height//4
 best=None
 for row in range(4):
  for col in range(4):
   t=np.asarray(im.crop((col*w,row*h,(col+1)*w,(row+1)*h)))
   mask=t[:,:,3];r=cv2.matchTemplate(a,t[:,:,:3],cv2.TM_SQDIFF_NORMED,mask=mask)
   r=np.nan_to_num(r,nan=100,posinf=100,neginf=100);_,_,xy,_=cv2.minMaxLoc(r);score=float(r[xy[1],xy[0]])
   v=(score,xy[0]+w//2,xy[1]+h,row,col)
   if best is None or v<best:best=v
 return best
if __name__=='__main__':
 import sys
 print(find(sys.argv[1]))
