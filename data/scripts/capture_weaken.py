"""Bounded catch chip from fresh public HP bars; stop above a reviewed critical-hit margin."""
import argparse,subprocess,sys,json,time,re
from pathlib import Path
from PIL import Image
from play import snap,ROOT
from public_owned_hp import read as owned_hp
p=argparse.ArgumentParser();p.add_argument('actor');p.add_argument('species');p.add_argument('slot',type=int,choices=range(4));p.add_argument('--stop-foe-hp',type=float,required=True);p.add_argument('--turns',type=int,default=6);p.add_argument('--total-hp',type=int,required=True);p.add_argument('--heal-below',type=int,required=True);p.add_argument('--recovery',type=int,choices=range(4));a=p.parse_args()
assert 0<a.stop_foe_hp<1 and 1<=a.turns<=12
for i in range(a.turns):
 rows=snap();text=' '.join(v['text'] for v in rows);low=text.lower()
 assert 'fight' in low and ('bag' in low or 'bae' in low),text
 norm=lambda s:re.sub('[^a-z]','',s.lower().replace('kgurem','kyurem').replace('mewtuo','mewtwo'))
 assert norm(a.actor) in norm(' '.join(v['text']for v in rows if v['y']>.72)),text
 assert norm(a.species) in norm(' '.join(v['text']for v in rows if v['y']<.37)),text
 im=Image.open(ROOT/'recordings/capture-preview.png').convert('RGB');assert im.size==(852,640)
 def fill(rgb):
  r,g,b=rgb
  return (g>120 and g>r*1.4 and g>b*1.4) or (r>170 and g>60 and b<80)
 filled=[x for x in range(170,330) if any(fill(im.getpixel((x,y)))for y in range(130,135))]
 assert filled and min(filled)<=173,'Enemy HP bar not found'
 fraction=(max(filled)-169)/160
 hp=owned_hp(rows,a.total_hp)
 print('PUBLIC CATCH CHIP',i,'foe_fraction',round(fraction,3),'own_hp',hp,flush=True)
 if fraction<=a.stop_foe_hp:print('SAFE CHIP STOP',flush=True);break
 slot=a.slot
 if hp<a.heal_below:
  assert a.recovery is not None,'Low HP safety stop'
  slot=a.recovery
 subprocess.run([sys.executable,str(ROOT/'scripts/battle_turn.py'),str(slot)],check=True)
else:print('CHIP TURN BUDGET REACHED',flush=True)
