"""Read-only match of public map pixels to installed transparent NPC sprites."""
import cv2,numpy as np,json,sys,time
from pathlib import Path
R=Path(__file__).resolve().parents[1];G=Path('/Applications/Reborn.app/Contents/Game/Graphics/Characters')
def find(frame,matrix,names):
 scale=matrix[0][0];inv=cv2.invertAffineTransform(np.array(matrix));hits=[]
 for name in names:
  src=cv2.imread(str(G/(name+'.png')),cv2.IMREAD_UNCHANGED);h,w=src.shape[:2];h//=4;w//=4
  candidates=[]
  for row in range(4):
   for col in range(4):
    cell=src[row*h:(row+1)*h,col*w:(col+1)*w]
    cell=cv2.resize(cell,(round(w*scale),round(h*scale)),interpolation=cv2.INTER_NEAREST)
    mask=(cell[:,:,3]>128).astype(np.uint8)*255
    score=cv2.matchTemplate(frame,cell[:,:,:3],cv2.TM_CCORR_NORMED,mask=mask)
    score=np.nan_to_num(score,nan=0,posinf=0,neginf=0)
    for _ in range(4):
     _,val,_,xy=cv2.minMaxLoc(score)
     if val<.88:break
     x,y=xy;foot=np.array([x+cell.shape[1]/2,y+cell.shape[0],1]);world=inv@foot
     candidates.append({'sprite':name,'score':round(val,5),'tile':[round(world[0]/32-.5,2),round(world[1]/32-1,2)],'frame':col,'direction':[2,4,6,8][row],'pixel':list(xy)})
     score[max(0,y-20):y+21,max(0,x-20):x+21]=0
  for c in sorted(candidates,key=lambda c:-c['score']):
   if not any(h['sprite']==name and np.linalg.norm(np.array(h['tile'])-c['tile'])<.8 for h in hits):hits.append(c)
 return hits
if __name__=='__main__':
 im=cv2.imread(sys.argv[1]);m=json.load(open(sys.argv[2]))['matrix'];t=time.time();hits=find(im,m,sys.argv[3:] or ['trchar148','pkmn_tyrantrum','pkmn_aerodactyl','pkmn_druddigon']);print(json.dumps({'seconds':time.time()-t,'hits':hits},indent=2))
