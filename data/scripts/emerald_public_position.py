"""Estimate Emerald position from recorded pixels against the static rendered map.
No process, memory or save access. Fractional values indicate mid-step frames.
"""
from pathlib import Path
import cv2,json,sys
R=Path(__file__).resolve().parents[1]
def position(image_path=None):
 im=cv2.imread(str(image_path or R/'recordings/capture-preview.png'))
 assert im is not None and im.shape[:2]==(640,852)
 im=cv2.resize(im,(512,384));mp=cv2.imread(str(R/'work/installed-map-805.png'))
 estimates=[]
 for x,y,w,h in [(20,180,180,170),(315,180,170,170),(20,35,175,130)]:
  res=cv2.matchTemplate(mp,im[y:y+h,x:x+w],cv2.TM_CCOEFF_NORMED);_,score,_,(mx,my)=cv2.minMaxLoc(res)
  estimates.append({'score':round(score,4),'x':(mx-x+256)/32-.5,'y':(my-y+192)/32-.5})
 estimates.sort(key=lambda d:d['score'],reverse=True)
 return estimates
if __name__=='__main__':print(json.dumps(position(sys.argv[1] if len(sys.argv)>1 else None)))
