"""Read only the visible Region Map marker from the recorded game preview."""
import json,time
from pathlib import Path
import numpy as np
from PIL import Image
R=Path(__file__).resolve().parents[1]
def marker():
 im=Image.open(R/'recordings/capture-preview.png').resize((512,384)).convert('RGB')
 a=np.array(Image.open('/Applications/Reborn.app/Contents/Game/Graphics/Pictures/rayquazaMarker.png').convert('RGBA'))
 mask=a[:,:,3]>200;s=[]
 for y in range(19):
  for x in range(15):
   u,v=121+16*x,31+16*y
   c=np.array(im.crop((u,v,u+46,v+34)))
   s.append((float(np.mean(abs(c.astype(float)[mask]-a[:,:,:3].astype(float)[mask]))),x,y))
 s.sort();assert s[0][0]<25 and s[1][0]-s[0][0]>15, s[:3]
 result=dict(epoch=time.time(),grid=list(s[0][1:]),error=s[0][0],next_error=s[1][0],source='Recorded visible Region Map marker')
 with (R/'notes/ray368-visible-marker.jsonl').open('a') as f:f.write(json.dumps(result)+'\n')
 return result
if __name__=='__main__':print(json.dumps(marker()))
