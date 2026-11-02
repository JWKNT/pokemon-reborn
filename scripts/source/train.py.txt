from play import *
from PIL import Image
import re
limit=int(sys.argv[1]) if len(sys.argv)>1 else 40
move=sys.argv[2] if len(sys.argv)>2 else 'Bide'
walk=0
last_hp=1
actor=None
pending=None
repeat_ready=False
for i in range(limit):
 r=snap();txt='\n'.join(v['text'] for v in r);print(i,txt.replace('\n',' | '),flush=True)
 low=txt.lower()
 expected=next((a.split('=',1)[1].lower() for a in sys.argv if a.startswith('--foe=')),None)
 if expected and 'fight' in low and expected not in low:
  print('OPPONENT CHANGED REVIEW',flush=True);break
 if '--emile' in sys.argv:
  for v in r:
   if v['x']>.50 and .42<v['y']<.64:
    if 'kricket' in v['text'].lower():actor='K'
    if 'marsht' in v['text'].lower():actor='M'
  if 'about to' in low:
   for n in ['servine','kirlia','quilava','nidorino']:
    if n in low:pending=n
  if 'change pok' in low or 'switch your' in low:
   if not pending or not actor:
    print('SWITCH UNKNOWN');break
   desired='K' if pending in ['servine','kirlia'] else 'M'
   if desired==actor:act('x','wait:3')
   else:act('c','wait:1','right','c','wait:0.5','c','wait:3')
   actor=desired;pending=None;continue
  if actor:move='Cutter' if actor=='K' else 'Shot'
 if 'hp' in low and len(r)>3:
  imhp=Image.open(STATE).convert('RGB');ww,hh=imhp.size
  pix=[imhp.getpixel((x,int(hh*.591))) for x in range(int(ww*.761),int(ww*.929))]
  filled=sum(1 for rr,gg,bb in pix if (gg>75 and gg>rr*1.4 and gg>bb*1.4) or (rr>130 and bb<70 and gg<180))
  if filled:last_hp=filled/len(pix)
 if '--noswitch' in sys.argv and ('change pok' in low or 'switch your' in low):
  act('x','wait:2');continue
 if 'fight' in low and any(n in low for n in ['salandit','growlithe','pansear','pidge','ducklett','rufflet','oricorio','rowlet','litleo','fletch']) and any('kricket' in v['text'].lower() and v['x']>.5 for v in r):
  print('TYPE REVIEW',flush=True);sys.exit(2)
 heal_at=float(next((a.split('=',1)[1] for a in sys.argv if a.startswith('--heal-at=')),'.36'))
 if 'fight' in low and last_hp<heal_at and '--heal' in sys.argv:
  from battle_heal import heal
  heal();last_hp=1;continue
 if 'fight' in low and last_hp<.50 and '--allowlow' not in sys.argv:
  print('LOW HP',flush=True);sys.exit(2)
 if 'no pp' in low or 'not enough pp' in low:
  print('PP REVIEW',flush=True);break
 if 'disabled' in low:
  print('DISABLED REVIEW',flush=True);break
 if '--learn' in sys.argv and 'trying to' in low:
  from learning import resolve
  if resolve(txt):continue
 if any(x in low for x in ['trying to','forget','fainted','choose a pok','give a nick','evolving','switch your','change pok']):
  print('REVIEW',flush=True);break
 if 'max. hp' in low:
  act('c','wait:0.5');continue
 if 'fight' in low:
  nums=[v['text'] for v in r if v['x']>.65 and .57<v['y']<.67]
  im=Image.open(STATE).convert('RGB');w,h=im.size;ss=[]
  for yy in [0,1]:
   for xx in [0,1]:
    box=(int(w*(.52 if xx==0 else .74)),int(h*(.75 if yy==0 else .84)),int(w*(.69 if xx==0 else .91)),int(h*(.79 if yy==0 else .88)))
    ss.append(sum(1 for rr,gg,bb in im.crop(box).getdata() if bb>70 and bb>rr*1.25 and bb>gg*1.12))
  idx=max(range(4),key=lambda j:ss[j]);seq=[]
  if idx%2:seq.append('left')
  if idx//2:seq.append('up')
  if repeat_ready and '--quick' in sys.argv:
   act(*seq,'c','wait:0.5','c','wait:3');continue
  act(*seq,'c','wait:0.5');continue
 if 'pp:' in low or ('fury' in low and any(z in low for z in ['sing','bug','focus'])) or ('bug' in low and 'bide' in low):
  choices=[v for v in r if v['y']>.73 and v['x']<.72 and move.lower() in v['text'].lower()]
  if not choices and not move.startswith('slot:') and move not in ['Cutter','Bug','Gun','Tackle','Bide','Absorb','Shot','AirS','AirT','Charge','Confusion']:
   print('MOVE UNKNOWN',flush=True);break
  if not choices: choices=[{'x':0,'y':.75}]
  target=choices[0]; tx=1 if target['x']>.39 else 0;ty=1 if target['y']>.81 else 0
  if move.startswith('slot:'):tx=int(move[5:])%2;ty=int(move[5:])//2
  if move in ['Cutter','Bug','Gun','Tackle','Bide','Absorb','Shot','AirS','AirT','Charge','Confusion']:
   idx_target={'Cutter':3,'Bug':2,'Gun':2,'Tackle':0,'Bide':1,'Absorb':0,'Shot':1,'AirS':1,'AirT':2,'Charge':0,'Confusion':3}[move];tx=idx_target%2;ty=idx_target//2
  im=Image.open(STATE).convert('RGB');w,h=im.size
  scores=[]
  for yy in [0,1]:
   for xx in [0,1]:
    box=(int(w*(.062 if xx==0 else .392)),int(h*(.742 if yy==0 else .834)),int(w*(.09 if xx==0 else .42)),int(h*(.792 if yy==0 else .888)))
    score=sum(1 for rr,g,b in im.crop(box).getdata() if min(rr,g,b)>180 and max(rr,g,b)-min(rr,g,b)<75)
    scores.append(score)
  idx=max(range(4),key=lambda j:scores[j]);cx=idx%2;cy=idx//2
  seq=[]
  if cx!=tx:seq.append('right' if tx else 'left')
  if cy!=ty:seq.append('down' if ty else 'up')
  if seq:
   act(*seq,'wait:0.2');snap()
   verify=Image.open(STATE).convert('RGB');vv=[]
   for vy in [0,1]:
    for vx in [0,1]:
     box=(int(w*(.062 if vx==0 else .392)),int(h*(.742 if vy==0 else .834)),int(w*(.09 if vx==0 else .42)),int(h*(.792 if vy==0 else .888)))
     vv.append(sum(min(p)>180 and max(p)-min(p)<75 for p in verify.crop(box).getdata()))
   if max(range(4),key=lambda j:vv[j])!=ty*2+tx:
    print('MOVE CURSOR REVIEW',vv,flush=True);break
  act('c','wait:3');repeat_ready=True;continue
 bottom=' '.join(v['text'] for v in r if v['y']>.72)
 if bottom:
  act('c','wait:1');continue
 imbox=Image.open(STATE).convert('RGB');bw,bh=imbox.size
 patch=imbox.crop((int(bw*.08),int(bh*.74),int(bw*.9),int(bh*.87)))
 white=sum(1 for rr,gg,bb in patch.getdata() if min(rr,gg,bb)>210)/max(1,patch.width*patch.height)
 if white>.55 and ('hp' in low or any(n in low for n in ['kricket','swoobat','tranquill','marshtomp'])):
  act('c','wait:1');continue
 if len(r)<=3:
  if '--still' in sys.argv:
   act('wait:1.5')
   check=read().lower()
   if any(t in check for t in ['hp','fight','battle','sent out','go!']):continue
   print('OVERWORLD',flush=True);break
  if last_hp<.45:
   print('HEAL',flush=True);break
  if 'HP' in txt:
   act('wait:1');continue
  act('left:0.3' if walk%2==0 else 'right:0.3','wait:0.7');walk+=1;continue
 act('wait:1')
