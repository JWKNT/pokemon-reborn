"""Push a reviewed Citae Prisma mirror using normal keys and public pixel proofs."""
import os,sys,json,subprocess,time
os.environ.setdefault('REBORN_FAST_KEYS','1');os.environ.setdefault('REBORN_COORD_CACHE','1');os.environ.setdefault('REBORN_ROUTE_STEP_PAUSE','.10')
from play import ROOT,act,snap,NATIVE
from locate import locate
from sprite_match import match
from PIL import Image
import numpy as np
eid=int(sys.argv[1]);direction=sys.argv[2];count=int(sys.argv[3]);assert eid in [73,74,75,95] and 1<=count<=12
v=json.loads(subprocess.check_output(['ruby',str(ROOT/'scripts/route_map.rb'),'896','0','0'],stderr=subprocess.DEVNULL));e=v['events'][str(eid)]
assert e['character']=='mirrorpanel' and any(c['code']==209 and c['parameters'][0]==0 for c in e['list'])
xy=(e['x'],e['y']);dx,dy={'up':(0,-1),'down':(0,1),'left':(-1,0),'right':(1,0)}[direction]
sheet=Image.open('/Applications/Reborn.app/Contents/Game/Graphics/Characters/mirrorpanel.png').convert('RGBA');row=(e['direction']//2-1)*64
tile=sheet.crop((0,row,32,row+64)).resize((128,256),Image.Resampling.NEAREST)
def proof(player,block):
 # Pixel matching needs a fresh recorded frame, not OCR of the entire screen.
 # Preserve the same calibrated canvas and refuse a stale recorder preview.
 requested=time.time()
 for _ in range(40):
  health=json.loads((ROOT/'recordings/capture-health.json').read_text())
  if health.get('active') and health.get('preview_epoch',0)>=requested and time.time()-health['epoch']<2:break
  time.sleep(.1)
 else:raise RuntimeError('Fresh recorded mirror frame unavailable')
 preview=Image.open(ROOT/'recordings/capture-preview.png').convert('RGB')
 assert preview.size==(852,640)
 im=Image.open(ROOT/'work/capture-preview-frame-template.png').convert('RGB')
 assert im.size==(2272,1816)
 im.paste(preview.resize((2048,1536)),(112,134))
 # This board is far from every map edge. Installed Game_Player.center and
 # Game_Character.screen_y_ground place the tile foot at this fixed point in
 # the 2048x1536 public canvas. Unlike sprite matching this remains valid when
 # a tall mirror occludes the player. Calibrated directly against mirror74.
 assert 16<=player[0]<=29 and 58<=player[1]<=69
 foot=[1136,966]
 left=round(foot[0]+(block[0]-player[0])*128-64);top=round(foot[1]+(block[1]-player[1])*128-256)
 target=np.array(tile);mask=target[:,:,3]>250
 # Top half of tall mirror remains exposed while pushing from the south.
 if player[0]==block[0] and player[1]==block[1]-1:
  mask[:128,:]=False
  # A stored shadow is drawn over the plate's outer border when the real
  # mirror is still on its return tile. Match its unobscured interior.
  mask[:,:8]=False;mask[:,-8:]=False;mask[-8:,:]=False
 else:
  mask[128:,:]=False
 scores=[]
 for oy in range(-6,7,2):
  for ox in range(-6,7,2):
   aa=np.array(im.crop((left+ox,top+oy,left+128+ox,top+256+oy)))[mask].astype(float).ravel()
   bb=target[:,:,:3][mask].astype(float).ravel();scores.append(float(np.corrcoef(aa,bb)[0,1]))
 score=max(scores)
 with (ROOT/'work/prisma-public-pushes.jsonl').open('a') as f:f.write(json.dumps(dict(epoch=time.time(),preview_epoch=health['preview_epoch'],event=eid,player=player,mirror=block,score=score))+'\n')
 assert score>.82,('Mirror public-pixel review',block,score)
 print('VISIBLE MIRROR VERIFIED',eid,block,round(score,4),flush=True)
for i in range(count):
 before=(xy[0]-dx,xy[1]-dy)
 if i==0:
  subprocess.run([sys.executable,str(ROOT/'scripts/q.py'),f'896,{before[0]},{before[1]}'],check=True)
  assert locate(896)==(896,*before)
 else:
  act(direction+':.12','wait:.3')
 act(direction+':.12','wait:.2');proof(before,xy)
 act('c','wait:.8');after=(xy[0]+dx,xy[1]+dy);proof(before,after)
 p=ROOT/'notes/navigation-state.json';n=json.loads(p.read_text());n.setdefault('positions',{}).setdefault('896',{})[str(eid)]=list(after);p.write_text(json.dumps(n));xy=after
print('MIRROR PUSH GROUP VERIFIED',eid,xy,flush=True)
