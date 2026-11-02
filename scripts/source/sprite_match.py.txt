"""Match an installed sprite against an observed screenshot crop; no game state access."""
import numpy as np
from PIL import Image
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def match(image_path,box,sprite='trchar110',zoom=1,directions=None,patterns=None,clip_top=0):
 im=Image.open(image_path).convert('RGB');im=im.crop(box)
 a=np.asarray(im.resize((round(im.width/zoom),round(im.height/zoom)),Image.Resampling.NEAREST),dtype=np.float32)
 sheet=Image.open('/Applications/Reborn.app/Contents/Game/Graphics/Characters/'+sprite+'.png').convert('RGBA')
 fw,fh=sheet.width//4,sheet.height//4
 results=[]
 for row,d in enumerate([2,4,6,8]):
  if directions and d not in directions:continue
  for col in (range(4) if patterns is None else patterns):
   t=np.asarray(sheet.crop((col*fw,row*fh,(col+1)*fw,(row+1)*fh)))
   if clip_top:t=t[clip_top:]
   th,tw=t.shape[:2]
   # Opaque interior pixels distinguish facing while ignoring the floor.
   yy,xx=np.where(t[:,:,3]>250); take=np.arange(0,len(yy),8);yy=yy[take];xx=xx[take];rgb=t[yy,xx,:3].astype(np.float32)
   if a.shape[0]<th or a.shape[1]<tw:raise ValueError('Search crop too small')
   err=np.zeros((a.shape[0]-th+1,a.shape[1]-tw+1),dtype=np.float32)
   for y,x,color in zip(yy,xx,rgb):err+=np.mean((a[y:y+err.shape[0],x:x+err.shape[1]]-color)**2,axis=2)
   err/=len(yy);y,x=np.unravel_index(err.argmin(),err.shape);results.append((float(err[y,x]),d,col,int(x),int(y)))
 return sorted(results)
if __name__=='__main__':
 import sys,json
 print(json.dumps(match(sys.argv[1],list(map(int,sys.argv[2].split(','))),zoom=float(sys.argv[3]) if len(sys.argv)>3 else 1)[:5]))
