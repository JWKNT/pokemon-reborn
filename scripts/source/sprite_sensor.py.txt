"""Locate visible character frames by opaque PNG pixels; reads screenshots only."""
import numpy as np
from PIL import Image, ImageCms
import io
from pathlib import Path
GAME=Path('/Applications/Reborn.app/Contents/Game/Graphics/Characters')
def detect(path,character,scale=4,head_only=False,tone=None):
 native=Image.open(path)
 rgb=native.convert('RGB')
 if native.info.get('icc_profile'):
  rgb=ImageCms.profileToProfile(rgb,ImageCms.ImageCmsProfile(io.BytesIO(native.info['icc_profile'])),ImageCms.createProfile('sRGB'),outputMode='RGB')
 im=np.array(rgb);hh,ww=im.shape[:2]
 encoded=(im[:,:,0].astype(np.uint32)<<16)|(im[:,:,1].astype(np.uint32)<<8)|im[:,:,2]
 vals,counts=np.unique(encoded,return_counts=True);hist=dict(zip(vals.tolist(),counts.tolist()))
 sheet=Image.open(GAME/(character+'.png')).convert('RGBA');fw,fh=sheet.width//4,sheet.height//4;found=[]
 for row in range(4):
  for col in range(4):
   t=np.array(sheet.crop((col*fw,row*fh,(col+1)*fw,(row+1)*fh)).resize((fw*scale,fh*scale),Image.Resampling.NEAREST));mask=t[:,:,3]>250
   if tone is not None:
    assert len(tone)==4 and tone[3]==0,'Only reviewed daytime RGB tint supported'
    t[:,:,:3]=np.clip(np.rint(t[:,:,:3].astype(float)+np.rint(np.array(tone[:3]))),0,255).astype(np.uint8)
   if head_only:mask[int(fh*scale*.32):,:]=False
   ys,xs=np.where(mask);colors=(t[ys,xs,0].astype(np.uint32)<<16)|(t[ys,xs,1].astype(np.uint32)<<8)|t[ys,xs,2]
   available=[(hist.get(int(color),0),i)for i,color in enumerate(colors)if 0<hist.get(int(color),0)<5000]
   if not available:continue
   _,pivot=min(available);py,px=ys[pivot],xs[pivot];yy,xx=np.where(encoded==colors[pivot]);lx,ly=xx-px,yy-py
   valid=(lx>=0)&(ly>=0)&(lx+t.shape[1]<=ww)&(ly+t.shape[0]<=hh);lx,ly=lx[valid],ly[valid]
   # Quick distinctive anchors avoid comparing every opaque pixel per candidate.
   idx=np.linspace(0,len(xs)-1,32,dtype=int)
   for sy,sx in zip(ys[idx],xs[idx]):
    good=np.max(np.abs(im[ly+sy,lx+sx].astype(np.int16)-t[sy,sx,:3].astype(np.int16)),axis=1)<=3
    lx,ly=lx[good],ly[good]
    if not len(lx):break
   for x,y in zip(lx,ly):
    score=float(np.mean(np.max(np.abs(im[y+ys,x+xs].astype(np.int16)-t[ys,xs,:3].astype(np.int16)),axis=1)<=3))
    if score>=.97:found.append({'foot':[int(x+fw*scale/2),int(y+fh*scale)],'score':score,'pose':[row,col]})
 out=[]
 for f in sorted(found,key=lambda z:-z['score']):
  if not any(abs(f['foot'][0]-p['foot'][0])<12 and abs(f['foot'][1]-p['foot'][1])<12 for p in out):out.append(f)
 return out
if __name__=='__main__':
 import sys,json
 print(json.dumps(detect(sys.argv[1],sys.argv[2]),indent=2))
