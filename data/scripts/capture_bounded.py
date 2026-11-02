"""Bounded ball queue using only rendered command/actor/HP, stopping on capture."""
from play import *
import argparse,difflib
p=argparse.ArgumentParser();p.add_argument('actor');p.add_argument('species');p.add_argument('--ball',default='Ultra Ball');p.add_argument('--throws',type=int,default=8);p.add_argument('--total-hp',type=int,required=True);p.add_argument('--heal-below',type=int,required=True);p.add_argument('--heal-item',default='Ultra Potion');p.add_argument('--spore',action='store_true');p.add_argument('--false-swipe',action='store_true',help='Reviewed Mawile slot1; reapply when the public foe HP bar rises above 15 percent');p.add_argument('--rest-slot',type=int,choices=range(4));p.add_argument('--stop-below',type=int,default=0);a=p.parse_args()
if a.rest_slot is not None:assert (a.actor,a.rest_slot) in [('Walrein',3),('Zapdos',2),('Latias',2),('Cresselia',3),('Amoonguss',1),('Mew',0),('Mewtwo',1)], 'Recovery slot must match a reviewed owned build'
if a.spore:assert a.actor=='Amoonguss'
if a.false_swipe:assert a.actor=='Mawile'
assert 1<=a.throws<=12
heals=0
for i in range(a.throws):
 r=snap();t=' '.join(v['text']for v in r);low=t.lower();print('CAPTURE QUEUE',i,t,flush=True)
 if any(z in low for z in ['gotcha','was caught','nickname','pokedex','party is full','add to your']):print('CAPTURE DECISION STOP',flush=True);break
 assert 'fight' in low and re.search(r'\b(?:bag|bae)\b',low),'Command screen required'
 prompt=' '.join(v['text'].lower() for v in r if v['y']>.72 and v['x']<.55)
 # OCR sometimes joins the actor with the fixed command suffix, e.g. Darkraido?.
 if a.actor=='Mew':prompt=re.sub(r'\b(?:meu|meш)\b','mew',prompt)
 prompt=re.sub(r'\b'+re.escape(a.actor.lower())+r'do\?',a.actor.lower()+' do?',prompt)
 assert any(difflib.SequenceMatcher(None,a.actor.lower(),w.replace('mamile','mawile').replace('mauile','mawile')).ratio()>=.85 for w in prompt.split()),'Actor guard: '+prompt
 foe=' '.join(v['text'].lower().translate(str.maketrans({'р':'p','у':'y','а':'a','о':'o','с':'c','е':'e','х':'x','к':'k','і':'i','ј':'j'})) for v in r if v['y']<.37)
 normalized_foe=foe.replace('vietini','victini').replace('ho-0h','ho-oh').replace('kgurem','kyurem').replace('nyogre','kyogre').replace('mewtuo','mewtwo')
 assert a.species.lower()in normalized_foe,'Species guard: '+foe
 from public_owned_hp import read as owned_hp
 hp=[owned_hp(r,a.total_hp)]
 assert hp[0]>0,'Active Pokemon fainted'
 if hp[0]<a.stop_below:raise SystemExit('Low HP safety stop: '+str(hp[0]))
 if hp[0]<a.heal_below and a.rest_slot is not None:
  own=' '.join(v['text'].lower()for v in r if v['x']>.5 and .40<v['y']<.72)
  if re.search(r'[s5]lp',own):raise SystemExit('Low HP while asleep: manual safety review')
  assert heals<5,'Rest budget reached'
  subprocess.run([sys.executable,str(ROOT/'scripts/battle_move.py'),str(a.rest_slot),'--watch'],check=True)
  subprocess.run([sys.executable,str(ROOT/'scripts/battle_ready.py')],check=True);heals+=1
  print('REST: reassess public HP and status before next action',flush=True);continue
 if hp[0]<a.heal_below:
  assert heals<5,'Healing budget reached'
  subprocess.run([sys.executable,str(ROOT/'scripts/battle_item.py'),a.heal_item,a.actor],check=True)
  subprocess.run([sys.executable,str(ROOT/'scripts/battle_ready.py')],check=True);heals+=1
  print('HEALED: reassess HP before any next action',flush=True);continue
 if a.false_swipe:
  from PIL import Image
  im=Image.open(ROOT/'recordings/capture-preview.png').convert('RGB');assert im.size==(852,640)
  def colored(rgb):
   r,g,b=rgb
   return (g>120 and g>r*1.4 and g>b*1.4) or (r>170 and g<220 and b<100)
  filled=[x for x in range(170,330) if any(colored(im.getpixel((x,y))) for y in range(130,135))]
  assert filled and min(filled)<=173,'Public enemy HP bar needs review'
  fraction=(max(filled)-169)/160
  print('PUBLIC FALSE SWIPE GUARD',fraction,flush=True)
  if fraction>.15:
   subprocess.run([sys.executable,str(ROOT/'scripts/battle_move.py'),'1','--watch'],check=True)
   subprocess.run([sys.executable,str(ROOT/'scripts/battle_ready.py')],check=True)
   continue
 if a.spore:
  r=snap();foe=' '.join(v['text'].lower()for v in r if v['y']<.37)
  # Public HUD OCR also renders the sleep badge as SLFF/HP.
  if not re.search(r'\b[s5]l(?:p|f)',foe):
   subprocess.run([sys.executable,str(ROOT/'scripts/battle_move.py'),'0','--watch'],check=True)
   subprocess.run([sys.executable,str(ROOT/'scripts/battle_ready.py')],check=True)
   print('SPORE TURN: fresh status review before throwing',flush=True);continue
 subprocess.run([sys.executable,str(ROOT/'scripts/throw_ball.py'),a.ball],check=True)
 r=snap();low=' '.join(v['text']for v in r).lower()
 if any(z in low for z in ['gotcha','was caught','nickname','pokedex','party is full','add to your']):print('CAPTURE DECISION STOP',low,flush=True);break
 subprocess.run([sys.executable,str(ROOT/'scripts/battle_ready.py')],check=True)
else:print('THROW BUDGET REACHED',flush=True)
