"""Bounded single-actor doubles policy using observed HUDs and reviewed foes.
Stops on forced replacements, low HP, unknown HUDs and special effects.
"""
from play import *
from PIL import Image
import argparse,difflib,re
p=argparse.ArgumentParser();p.add_argument('config');p.add_argument('--turns',type=int,default=20);a=p.parse_args()
cfg=json.loads(pathlib.Path(a.config).read_text());actor=cfg['actor'];turns=0;heals=0
def run(s,*args):subprocess.run([sys.executable,str(ROOT/'scripts'/s),*map(str,args)],check=True)
def norm(t):return re.sub('[^a-z]','',t.lower().translate(str.maketrans({'р':'p','у':'y','а':'a','о':'o','с':'c','е':'e','х':'x'})))
def match(t,names):
 words=re.findall('[a-z]+',t.lower());compact=norm(t)
 return [n for n in names if norm(n) in compact or any(difflib.SequenceMatcher(None,n.lower(),w).ratio()>=.82 for w in words)]
for _ in range(a.turns):
 run('battle_ready.py');r=snap();t=' '.join(v['text'] for v in r);low=t.lower();print(t,flush=True)
 if re.search(r'de.?feated|for winning',low):print('VICTORY ANCHOR',flush=True);break
 if 'fight' not in low or 'choose a pok' in low or ('cancel' in low and low.count('hp')>=5):raise SystemExit('Replacement or command review')
 prompt=' '.join(v['text'] for v in r if v['y']>.72 and v['x']<.5)
 if not match(prompt,[actor]):raise SystemExit('Actor review: '+prompt)
 im=Image.open(STATE).convert('RGB');w,h=im.size
 fractions=[]
 for y in [.55+i*.001 for i in range(62)]:
  px=[im.getpixel((x,int(h*y))) for x in range(int(w*.740),int(w*.908))]
  fractions.append(sum((g>75 and g>rr*1.3 and g>b*1.3)or(rr>130 and b<70 and g<220)for rr,g,b in px)/len(px))
 hp=max(fractions);print('HP BAR',round(hp,3),flush=True)
 if hp<cfg.get('heal_below',0):
  if heals>=cfg.get('max_heals',2):raise SystemExit('Healing budget review')
  run('battle_item.py',cfg.get('heal_item','Hyper Potion'),actor);heals+=1;continue
 if hp<cfg.get('min_hp',.25):raise SystemExit('Low HP review')
 found=[]
 for target,lo,hi in [(1,.08,.21),(3,.21,.37)]:
  hud=' '.join(v['text'] for v in r if lo<v['y']<hi)
  names=match(hud,cfg['foes'])
  if len(names)==1:
   name=names[0];plan=cfg['foes'][name];found.append((plan.get('priority',0),target,name,plan))
  elif re.search(r'\bhp\b|l[uv].?\s*\d',hud,re.I):raise SystemExit('Unknown opponent HUD: '+hud)
 if not found:raise SystemExit('No verified opponent HUD')
 _,target,name,plan=max(found)
 if plan.get('slot') is None:raise SystemExit('Reviewed matchup change: '+name)
 print('REVIEWED ACTION',actor,name,plan['slot'],target,flush=True)
 args=[plan['slot']]+([target] if plan.get('target',True) else [])+['--watch']
 run('battle_move.py',*args);turns+=1
 now=read().lower()
 if any(x in now for x in ["doesn't affect",'does not affect','destiny bond','no pp','disabled','fell asleep','is confused','became confused','is paralyzed','became paralyzed','is frozen']):raise SystemExit('Move effect review')
else:raise SystemExit('Turn budget exhausted')
