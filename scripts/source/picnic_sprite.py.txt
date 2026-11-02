"""Locate grayscale apparition silhouettes in recorded public pixels."""
from pathlib import Path
import cv2,numpy as np
from PIL import Image
R=Path(__file__).resolve().parents[1]
def detect(name,dark=False,path=None):
 im=np.asarray(Image.open(path or R/'recordings/capture-preview.png').convert('L').resize((512,384),Image.Resampling.NEAREST))
 if path is None:
  from picnic_background import foreground
  a=foreground(im,dark)
 else:a=(im<90 if dark else im>175).astype(np.float32)
 sheet=np.asarray(Image.open('/Applications/Reborn.app/Contents/Game/Graphics/Characters/pkmn_'+name.lower()+'.png').convert('RGBA'));h,w=sheet.shape[:2];h//=4;w//=4
 found=[]
 for row in range(4):
  for col in range(4):
   c=sheet[row*h:(row+1)*h,col*w:(col+1)*w];mask=(c[:,:,3]>150).astype(np.float32)
   score=cv2.matchTemplate(a,mask,cv2.TM_CCOEFF_NORMED)
   # The known centered player must never become its own target.
   cy,cx=round(208-h),round(256-w/2)
   score[max(0,cy-14):cy+15,max(0,cx-14):cx+15]=0
   for _ in range(3):
    _,v,_,(x,y)=cv2.minMaxLoc(score)
    found.append((float(v),x+w/2,y+h,row,col))
    score[max(0,y-15):y+16,max(0,x-15):x+16]=0
 return sorted(found,reverse=True)
if __name__=='__main__':
 import sys,json
 print(json.dumps(detect(sys.argv[1],'--dark' in sys.argv)[:10]))
