"""Locate wandering Amaria from current game pixels, then approach with normal keys."""
from play import *
from locate import locate
from nav import route,groupby
sys.path.insert(0,'/tmp/reborn-vision-deps')
import cv2,numpy as np
from PIL import Image
m,e=map(int,sys.argv[1:3]);assert m in[680,683]
sheet=np.array(Image.open('/Applications/Reborn.app/Contents/Game/Graphics/Characters/trchar069e.png').convert('RGBA'))
for iteration in range(18):
 actual=locate(m);assert actual[0]==m
 # The coordinate frame froze the NPC while it was displayed. Match that
 # untouched screenshot; position conversion uses the verified512x384 viewport.
 im=Image.open(NATIVE);assert im.size==(2272,1816)
 canvas=im.crop((112,132,2160,1668)).resize((512,384),Image.Resampling.NEAREST)
 gray=cv2.cvtColor(np.array(canvas.convert('RGB')),cv2.COLOR_RGB2GRAY);hits=[]
 for yy in range(4):
  for xx in range(4):
   tpl=sheet[yy*42:(yy+1)*42,xx*42:(xx+1)*42]
   result=cv2.matchTemplate(gray,cv2.cvtColor(tpl[:,:,:3],cv2.COLOR_RGB2GRAY),cv2.TM_CCOEFF_NORMED,mask=tpl[:,:,3]);result[~np.isfinite(result)]=0
   _,score,_,xy=cv2.minMaxLoc(result);hits.append((score,xy,xx,yy))
 score,xy,xx,yy=max(hits)
 assert score>=.82,('Amaria sprite not confidently visible',score,xy)
 npc=(round(actual[1]+(xy[0]+21-256)/32),round(actual[2]+(xy[1]+42-208)/32))
 print('VISIBLE AMARIA',iteration,'score',round(score,3),'player',actual,'NPC',npc,flush=True)
 with(ROOT/'recordings/npc-observations.jsonl').open('a')as f:f.write(json.dumps({'epoch':time.time(),'map':m,'event':e,'player':actual,'sprite_score':score,'sprite_frame':[xx,yy],'sprite_origin':xy,'estimated_tile':npc,'source':'current native screenshot; installed sprite-sheet match'})+'\n')
 v=json.loads(subprocess.check_output(['ruby',str(ROOT/'scripts/route_map.rb'),str(m),str(actual[1]),str(actual[2])],stderr=subprocess.DEVNULL))
 v['events'][str(e)]['x'],v['events'][str(e)]['y']=npc
 choices=[]
 for dx,dy,k in[(0,1,'up'),(0,-1,'down'),(1,0,'left'),(-1,0,'right')]:
  goal=(npc[0]+dx,npc[1]+dy)
  try:steps=route(v,goal);choices.append((len(steps),goal,k,steps))
  except ValueError:pass
 assert choices,'No visible NPC approach'
 n,goal,facing,steps=min(choices)
 if n:
  act(*[key+':.12'for key in steps[:4]]);continue
 act(facing+':.12','c','wait:.4');text=read();print(text,flush=True)
 if 'amaria'in text.lower():print('AMARIA DIALOGUE VERIFIED',flush=True);break
else:raise SystemExit('Wandering NPC chase budget exhausted')
