"""Locate the visible Tauros from screenshot pixels; no game-memory access."""
from PIL import Image
import numpy as np,subprocess,pathlib
ROOT=pathlib.Path(__file__).resolve().parents[1]
def capture():
 p=ROOT/'work/tauros-live.png';subprocess.run(['/usr/sbin/screencapture','-x','-l','260608',str(p)],check=True)
 im=Image.open(p).convert('RGB');w,h=im.size
 # Native macOS window screenshot includes shadow; game canvas boundaries verified visually.
 crop=im.crop((112,132,2160,1668)).resize((512,384),Image.Resampling.NEAREST)
 return np.array(crop)
def detect(a):
 sheet=Image.open('/Applications/Reborn.app/Contents/Game/Graphics/Characters/pkmn_tauros.png').convert('RGBA');best=None
 for row in range(4):
  for col in range(4):
   t=np.array(sheet.crop((col*58,row*56,col*58+58,row*56+56)))
   mask=(t[:,:,3]>200);yy,xx=np.where(mask & (np.indices(mask.shape)[0]<38));rgb=t[yy,xx,:3].astype(int)
   # Colored opaque samples avoid black outlines and pale highlights.
   valid=(rgb[:,0]>65)&(rgb[:,0]>rgb[:,1]*1.08)&(rgb[:,1]>30)&(rgb[:,2]<100)
   indices=np.flatnonzero(valid)
   if not len(indices):continue
   anchor=indices[len(indices)//2];color=rgb[anchor];ay,ax=yy[anchor],xx[anchor]
   cy,cx=np.where(np.max(np.abs(a.astype(int)-color),axis=2)<26);oy=cy-ay;ox=cx-ax
   ok=(ox>=0)&(oy>=0)&(ox+58<=512)&(oy+56<=384);ox=ox[ok];oy=oy[ok]
   if not len(ox):continue
   sample=np.arange(0,len(xx),max(1,len(xx)//120));sx=xx[sample];sy=yy[sample];colors=rgb[sample]
   dif=np.mean(np.minimum(np.abs(a[oy[:,None]+sy,ox[:,None]+sx].astype(int)-colors),100),axis=(1,2));i=int(np.argmin(dif))
   result=(float(dif[i]),int(ox[i])+29,int(oy[i])+56,row,col)
   if best is None or result[0]<best[0]:best=result
 return best
if __name__=='__main__':print(detect(capture()),flush=True)
