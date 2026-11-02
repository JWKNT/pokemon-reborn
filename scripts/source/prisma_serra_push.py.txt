"""Direct Serra as a mirror with normal interaction and recorded sprite proofs."""
import os,sys,json,subprocess,time
os.environ.setdefault('REBORN_FAST_KEYS','1');os.environ.setdefault('REBORN_COORD_CACHE','1')
from play import ROOT,act
from locate import locate
from PIL import Image
import numpy as np
direction=sys.argv[1];count=int(sys.argv[2]);assert 1<=count<=12
dx,dy={'up':(0,-1),'down':(0,1),'left':(-1,0),'right':(1,0)}[direction]
v=json.loads(subprocess.check_output(['ruby',str(ROOT/'scripts/route_map.rb'),'896','0','0'],stderr=subprocess.DEVNULL));e=v['events']['72']
assert e['character']=='trchar096' and any(c['code']==209 and c['parameters'][1]['list'][0]['code']==11 for c in e['list'])
xy=(e['x'],e['y']);sheet=Image.open('/Applications/Reborn.app/Contents/Game/Graphics/Characters/trchar096.png').convert('RGBA')
def proof(player,block,face=None):
 now=time.time()
 for _ in range(40):
  h=json.loads((ROOT/'recordings/capture-health.json').read_text())
  if h.get('active') and h.get('preview_epoch',0)>=now and time.time()-h['epoch']<2:break
  time.sleep(.1)
 else:raise RuntimeError('Fresh recorded Serra frame unavailable')
 im=Image.open(ROOT/'recordings/capture-preview.png').convert('RGB').resize((2048,1536))
 assert 16<=player[0]<=29 and 58<=player[1]<=69
 left=1024+(block[0]-player[0])*128-64;top=832+(block[1]-player[1])*128-176
 scores=[]
 for row in ([{2:0,4:1,6:2,8:3}[face]] if face else range(4)):
  for col in range(4):
   t=np.array(sheet.crop((col*32,row*44,(col+1)*32,(row+1)*44)).resize((128,176),Image.Resampling.NEAREST));mask=t[:,:,3]>250
   if player[0]==block[0]:
    if player[1]<block[1]:mask[:80,:]=False
    else:mask[96:,:]=False
   for oy in [-4,0,4]:
    for ox in [-4,0,4]:
     a=np.array(im.crop((left+ox,top+oy,left+ox+128,top+oy+176)))[mask].astype(float).ravel();b=t[:,:,:3][mask].astype(float).ravel()
     scores.append(float(np.corrcoef(a,b)[0,1]))
 score=max(scores)
 with (ROOT/'work/prisma-public-pushes.jsonl').open('a') as f:f.write(json.dumps(dict(epoch=time.time(),preview_epoch=h['preview_epoch'],event=72,player=player,mirror=block,face=face,score=score))+'\n')
 assert score>.82,('Serra public-pixel review',block,score)
 print('VISIBLE SERRA VERIFIED',block,face,round(score,4),flush=True)
for i in range(count):
 before=(xy[0]-dx,xy[1]-dy)
 if i==0:
  subprocess.run([sys.executable,str(ROOT/'scripts/q.py'),f'896,{before[0]},{before[1]}'],check=True);assert locate(896)==(896,*before)
 else:act(direction+':.12','wait:.3')
 act(direction+':.12','wait:.2');proof(before,xy)
 act('c','wait:.8');after=(xy[0]+dx,xy[1]+dy);proof(before,after,{'down':2,'left':4,'right':6,'up':8}[direction])
 p=ROOT/'notes/navigation-state.json';n=json.loads(p.read_text());n['positions']['896']['72']=list(after);p.write_text(json.dumps(n));xy=after
